from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from selenium.webdriver.safari.options import Options
import io
import sys

def penarikan_minerba():
    output_log = io.StringIO()
    sys.stdout = output_log  # Redirect stdout
    
    try:
        # Jalankan Safari
        driver = webdriver.Safari()

        # Buka halaman harga acuan
        driver.get('https://www.minerba.esdm.go.id/harga_acuan')

        # Tunggu load
        time.sleep(5)

        # Ambil isi halaman
        html = driver.page_source

        # Tutup browser
        driver.quit()

        # Parsing pakai BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')

        # Temukan tabel
        table = soup.find('table')
        rows = table.find_all('tr')

        # Ekstrak data ke array
        data = []
        for row in rows:
            cols = row.find_all(['td', 'th'])
            cols = [col.get_text(strip=True) for col in cols]
            data.append(cols)

        # Buat DataFrame
        df = pd.DataFrame(data)

        # Dapatkan path ke folder Downloads
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        output_path = os.path.join(downloads_path, "harga_acuan_minerba.xlsx")

        # Simpan ke file Excel
        df.to_excel(output_path, index=False, header=False)

        print(f"✔️ File berhasil disimpan ke: {output_path}")
        
        log_hasil = output_log.getvalue()  # Ambil semua print log
        return log_hasil  # Kembalikan log untuk ditampilkan di HTML
    
    finally:
        sys.stdout = sys.__stdout__
