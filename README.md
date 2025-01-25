# Proyek-Analisis-Data
Submission proyek akhir Dicoding

# Setup terminal
mkdir proyek-analisis-datas
cd proyek-analisis-data
pipenv install
pipenv shell
pip install -r requirements.txt

- note: requirements.txt tidak dapat diinstal kalau diluar folder 'dashboard' jadi saya taruh requirements.txt didalam dashboard dan diluar untuk mengikuti template saja

# Jalankan streamlit
streamlit run dashboard.py
