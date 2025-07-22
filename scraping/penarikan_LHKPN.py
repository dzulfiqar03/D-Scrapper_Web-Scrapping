import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import io
import sys

def penarikan_lhkpn():
    output_log = io.StringIO()
    sys.stdout = output_log  # Redirect stdout
    try:
    # === 1. Setup Direktori Download ===
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            
        download_dir2 = os.path.join(os.getcwd(), "Downloads/LHKPN")
        if not os.path.exists(download_dir2):
            os.makedirs(download_dir2)

        output_path = os.path.join(download_dir, "LHKPN.xlsx")

        # === 2. Setup Chrome Options ===
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Jalankan tanpa GUI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)

        # === 4. Buka Halaman Tableau ===
        driver.get("https://elhkpn.kpk.go.id/portal/user/petakepatuhan")

        # === 5. Masuk ke iframe Tableau ===
        wait = WebDriverWait(driver, 30)
        iframes = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframes[0])
        print("✅ Masuk iframe Tableau")
        time.sleep(5)

        selector_main = "div[widgetid^='tableauTabbedNavigation_tab_1']"
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_main))).click()
        print("✅ Klik selector_main")

        # === 6. Scroll Awal untuk Trigger Elemen ===
        for _ in range(10):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(0.3)
        print("✅ Scroll awal selesai")

        # === 7. Fungsi Scroll Dinamis ke Elemen ===
        def scroll_until_element_found(selector, max_scrolls=20, delay=1):
            for i in range(max_scrolls):
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                    print(f"✅ Elemen ditemukan pada scroll ke-{i+1}")
                    return element
                except:
                    driver.execute_script("window.scrollBy(0, 300);")
                    time.sleep(delay)
            raise Exception(f"❌ Gagal menemukan elemen: {selector}")

        # === 8. Klik Proses Unduh ===
        selector_download = "button[data-tb-test-id^='viz-viewer-toolbar-button-download']"
        scroll_until_element_found(selector_download)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_download))).click()
        print("✅ Klik Download")

        selector_crosstab = "div[data-tb-test-id^='download-flyout-download-crosstab-MenuItem']"
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_crosstab))).click()
        print("✅ Klik Crosstab")

        selector_table = "div[title^='Tabel Ikhtisar Penyampaian instansi UK']"
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_table))).click()
        print("✅ Klik Tabel")

        selector_export = "button[data-tb-test-id^='export-crosstab-export-Button']"
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_export))).click()
        print("✅ Klik Export")

        # === 9. Tunggu Hingga File Selesai Terunduh ===
        def is_excel_file_downloaded():
            files = [f for f in os.listdir(download_dir) if f.endswith(".xlsx")]
            cr_files = [f for f in os.listdir(download_dir) if f.endswith(".crdownload")]
            return files and not cr_files

        for _ in range(30):
            if is_excel_file_downloaded():
                break
            time.sleep(1)

        # === 10. Rename File Hasil Unduhan ===
        def get_latest_matching_file(base_name: str, ext=".xlsx"):
            # Bersihkan nama seperti (1), (2)
            def clean(filename):
                return re.sub(r"\s*\(\d+\)", "", filename)
            
            target_clean = clean(base_name)
            matches = [
                os.path.join(download_dir, f) for f in os.listdir(download_dir)
                if f.endswith(ext) and clean(f) == target_clean
            ]
            if not matches:
                return None
            return max(matches, key=os.path.getmtime)

        base_download_name = "Tabel Ikhtisar Penyampaian instansi UK.xlsx"
        latest_file = get_latest_matching_file(base_download_name)

        if latest_file and os.path.exists(latest_file):
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(latest_file, output_path)
            print("✅ File berhasil diunduh & di-rename ke:", output_path)
        else:
            print("❌ Gagal menemukan file untuk di-rename")

        # === 11. Tutup Browser ===
        driver.quit()

        log_hasil = output_log.getvalue()  # Ambil semua print log
        return log_hasil  # Kembalikan log untuk ditampilkan di HTML

    finally:
        sys.stdout = sys.__stdout__