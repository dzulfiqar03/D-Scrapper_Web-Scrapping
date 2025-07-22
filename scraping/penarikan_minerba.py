from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from selenium.webdriver.safari.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import io
import sys

def penarikan_minerba():
    output_log = io.StringIO()
    sys.stdout = output_log  # Redirect stdout
    
    try:
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            
        download_dir2 = os.path.join(os.getcwd(), "Downloads/Minerba")
        if not os.path.exists(download_dir2):
            os.makedirs(download_dir2)

        output_path = os.path.join(download_dir, "harga_acuan_minerba.xlsx")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Jalankan tanpa GUI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920,1080")
        prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)

        # === 3. Inisialisasi Driver ===
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 30)

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
