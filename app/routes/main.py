import os
from flask import Blueprint, render_template, request, send_from_directory, current_app, redirect, url_for, flash
from flask_login import login_required
from app.utils.search import smart_search
# Veritabanı modellerini içeri aktarıyoruz
from app import db
from app.models import ClothingItem

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    results = []
    search_message = ""
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            results, search_message = smart_search(query)
    return render_template('index.html', results=results, search_message=search_message)

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# --- YENİ EKLENEN: TÜM MODELLER SAYFASI ---
@bp.route('/tum-modeller')
@login_required
def tum_modeller():
    # En yeni eklenen en üstte görünsün
    tum_urunler = ClothingItem.query.order_by(ClothingItem.id.desc()).all()
    return render_template('tum_modeller.html', products=tum_urunler)

# --- YENİ EKLENEN: SİLME FONKSİYONU ---
@bp.route('/urun-sil/<int:id>', methods=['POST'])
@login_required
def urun_sil(id):
    item = ClothingItem.query.get_or_404(id)
    
    # 1. Önce resimleri klasörden silmeyi dene
    try:
        for img in item.images:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], img.image_filename)
            if os.path.exists(file_path):
                os.remove(file_path)
    except Exception as e:
        print(f"Dosya silme hatası (Önemsiz): {e}")

    # 2. Veritabanından kaydı sil
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Kayıt başarıyla silindi.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Veritabanı hatası oluştu.', 'danger')
        print(e)

    return redirect(url_for('main.tum_modeller'))