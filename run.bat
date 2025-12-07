@echo off
echo Moda Arama Uygulamasi Baslatiliyor...

if not exist venv (
    echo Sanal ortam olusturuluyor...
    python -m venv venv
)

echo Sanal ortam aktif ediliyor...
call venv\Scripts\activate

echo Gereksinimler kontrol ediliyor...
pip install -r requirements.txt

echo Uygulama baslatiliyor...
echo Lutfen tarayicinizda http://127.0.0.1:5000 adresine gidin.
python run.py

pause
