import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import ClothingItem, ItemImage, ItemFeature
from app.services.ai_service import analyze_image_with_gemini

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('items', __name__, url_prefix='/item')

@bp.route('/<int:item_id>')
@login_required
def detail(item_id):
    item = ClothingItem.query.get_or_404(item_id)
    return render_template('detail.html', item=item)

@bp.route('/<int:item_id>/update', methods=['POST'])
@login_required
def update(item_id):
    item = ClothingItem.query.get_or_404(item_id)
    data = request.get_json()
    
    try:
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        
        if 'features' in data:
            for feature_data in data['features']:
                feature_id = feature_data.get('id')
                feature = ItemFeature.query.get(feature_id)
                if feature and feature.item_id == item_id:
                    feature.key = feature_data.get('key', feature.key).lower()
                    feature.value = feature_data.get('value', feature.value).lower()
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Güncelleme başarılı'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        img_front = request.files.get('image_front')
        img_back = request.files.get('image_back')
        img_side = request.files.get('image_side')
        
        # Validate files
        if img_front and not allowed_file(img_front.filename):
            return "Geçersiz dosya formatı (sadece resim dosyaları)", 400
        if img_back and not allowed_file(img_back.filename):
            return "Geçersiz dosya formatı (sadece resim dosyaları)", 400
        if img_side and not allowed_file(img_side.filename):
            return "Geçersiz dosya formatı (sadece resim dosyaları)", 400
        
        feature_input = request.form.get('features') 
        
        if name and img_front:
            new_item = ClothingItem(name=name, description=description)
            db.session.add(new_item)
            db.session.commit()
            
            def save_and_link_image(file_obj, view):
                if file_obj:
                    filename = secure_filename(f"{new_item.id}_{view}_{file_obj.filename}")
                    file_obj.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    img_record = ItemImage(item_id=new_item.id, image_filename=filename, view_type=view)
                    db.session.add(img_record)

            save_and_link_image(img_front, 'front')
            save_and_link_image(img_back, 'back')
            save_and_link_image(img_side, 'side')
            
            if feature_input:
                pairs = feature_input.split(',')
                for pair in pairs:
                    pair = pair.strip()
                    if not pair: continue
                    
                    if ':' in pair:
                        parts = pair.split(':', 1)
                        k, v = parts[0].strip().lower(), parts[1].strip().lower()
                    else:
                        k, v = 'tag', pair.lower()
                    
                    if k and v:
                        db.session.add(ItemFeature(item_id=new_item.id, key=k, value=v))
            
            db.session.commit()
            return redirect(url_for('main.index'))
            
    return render_template('upload.html')

@bp.route('/api/analyze', methods=['POST'])
@login_required
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
        
    # Save temporarily
    temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_' + secure_filename(file.filename))
    file.save(temp_path)
    
    try:
        result = analyze_image_with_gemini(temp_path)
        os.remove(temp_path) # Clean up
        return jsonify(result)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500
