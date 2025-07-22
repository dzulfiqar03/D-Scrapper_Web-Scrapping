
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import os
import io
import sys
def penarikan_igracias():
    output_log = io.StringIO()
    sys.stdout = output_log  # Redirect stdout
    # === 1. Setup Direktori Download ===
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

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

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)

    # === 4. Buka Halaman iGracias ===
    driver.get("https://igracias.telkomuniversity.ac.id")
    time.sleep(2)
    
    try:
        # === 5. Hover ke tombol Login ===
        hover_login = "button[class^='dropbtn']"
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, hover_login)))
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        print("✅ Hover pada menu login")

        # === 6. Klik tombol Login ===
        clickLogin = "a[id^='login_button_general']"
        driver.find_element(By.CSS_SELECTOR, clickLogin).click()
        print("✅ Klik tombol login berhasil")
        time.sleep(3)

        # === 8. Isi Form Login ===
        username = input("Masukkan Username Anda: ")
        password = input("Masukkan Password Anda: ")

        username_input = "input[name='textUsername']"
        password_input = "input[name='textPassword']"

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, username_input))).send_keys(username)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, password_input))).send_keys(password)

        print("✅ Form login berhasil diisi")


        # === 9. Submit Form ===
        # Tambahkan tombol submit login jika ada
        submit_button = "input[type='submit']"
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button))).click()

        clickNilai = "a[appcur_lang^='Nilai']"
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, clickNilai))).click()
        print("✅ Klik tombol login berhasil")

        clickNilai2 = "a[class^='showThirdLevelMenu']"
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, clickNilai2))).click()
        print("✅ Klik tombol login berhasil")

        clickNilai3 = "a[href^='/score/?pageid=11']"
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, clickNilai3))).click()
        print("✅ Klik tombol login berhasil")



        # === 10. Scroll (jika diperlukan) ===
        for _ in range(10):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(0.3)
            print("✅ Scroll selesai")

        html = driver.page_source

        # Parsing pakai BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')

        # Temukan tabel
        table = soup.find('table', attrs = {'class': 'crud_table dataTable'})
        rows = table.find_all('tr')
        # Ekstrak data ke array
        data = []
        for i in range(0,3):
            for row in rows:
                cols = row.find_all(['td', 'th', 'span'])
                cols = [col.get_text(strip=True) for col in cols]
                data.append(cols)
                time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,"a[id^='tDisplay_next']").click()
            time.sleep(3)  

        # === 11. Akhiri Script (jangan langsung quit kalau masih mau ambil data) ===
        time.sleep(5)  # Tunggu proses login selesai jika lanjut scraping

        print(data)
        # Buat DataFrame
        df_nilai = pd.DataFrame(data)


        clickEkivalensi = "a[title^='View Equivalency']"
        driver.find_element(By.CSS_SELECTOR, clickEkivalensi).click()
        print("✅ Klik tombol login berhasil")

        data2 = []

        for i in range(0, 4):  # loop tab ke-2, 3, 4 (index 2-4)
            tab_index = i + 1

            # Klik tab dengan index tertentu
            tab_selector = f"a[href='#ui-tabs-{tab_index}']"
            driver.find_element(By.CSS_SELECTOR, tab_selector).click()
            time.sleep(2)

            # Perbarui soup setelah klik tab
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Temukan tab div tertentu, lalu cari tabel di dalamnya
            tab_div = soup.find("div", id=f"ui-tabs-{tab_index}")
            if not tab_div:
                print(f"❌ Tab div dengan id ui-tabs-{tab_index} tidak ditemukan.")
                continue

            table = tab_div.find("table", attrs={'class': 'crud_table', 'align': 'center'})
            if not table:
                print(f"❌ Tabel tidak ditemukan di tab ui-tabs-{tab_index}")
                continue

            # Temukan semua baris <tr> dalam tabel
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all(['td', 'th'])
                cols = [col.get_text(strip=True) for col in cols]
                data2.append(cols)

            print(f"✅ Data berhasil diambil dari tab ui-tabs-{tab_index}")
            time.sleep(1)
            # === 11. Akhiri Script (jangan langsung quit kalau masih mau ambil data) ===
            time.sleep(5)  # Tunggu proses login selesai jika lanjut scraping

        print(data2)

        clicklogout = "a[class^='logout_link']"
        driver.find_element(By.CSS_SELECTOR, clicklogout).click()
        print("✅ logout berhasil")

        # Buat DataFrame
        df_ekivalensi = pd.DataFrame(data2)

        driver.get("https://situ-kem.telkomuniversity.ac.id/tak/auth/login")

        # === 8. Isi Form Login ===
        usernameSITU = input("Masukkan Username Anda: ")
        passwordSITU = input("Masukkan Password Anda: ")

        usernameSITU_input = "input[name='username']"
        passwordSITU_input = "input[name='password']"

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, usernameSITU_input))).send_keys(usernameSITU)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, passwordSITU_input))).send_keys(passwordSITU)

        # === 9. Submit Form ===
        # Tambahkan tombol submit login jika ada
        driver.find_element(By.CSS_SELECTOR,"button[type^='submit']").click()

        print("✅ Form login berhasil diisi")

        time.sleep(5)

        driver.find_element(By.CSS_SELECTOR,"a[href^='/tak/dashboard']").click()
        time.sleep(3)
        # === 10. Scroll (jika diperlukan) ===
        for _ in range(10):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(0.3)
            print("✅ Scroll selesai")


        html2 = driver.page_source

        # Parsing pakai BeautifulSoup
        soup2 = BeautifulSoup(html2, 'lxml')

        # Temukan tabel
        table3 = soup2.find('table', attrs = {'class': 'table table-bordered table-hover dataTable no-footer'})
        rows3 = table3.find_all('tr')
        # Ekstrak data ke array
        data3 = []
        for i in range(0,3):
            for row in rows3:
                cols = row.find_all(['td', 'th', 'span', 'option'])
                cols = [col.get_text(strip=True) for col in cols]
                data3.append(cols)
                time.sleep(2)
            driver.find_element(By.CSS_SELECTOR,"a[class^='paginate_button next']").click()
            time.sleep(3)  

        # === 11. Akhiri Script (jangan langsung quit kalau masih mau ambil data) ===
        time.sleep(5)  # Tunggu proses login selesai jika lanjut scraping

        print(data3)
        # Buat DataFrame
        df_tak = pd.DataFrame(data3)

        print(f"✔️ Data TAK berhasil disimpan")

        # Dapatkan path ke folder Downloads
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        output_path = os.path.join(downloads_path, "IGracias.xlsx")


        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df_nilai.to_excel(writer, sheet_name='Nilai', index=False)
            df_ekivalensi.to_excel(writer, sheet_name='Ekivalensi', index=False)
            df_tak.to_excel(writer, sheet_name='TAK', index=False)

        print(f"✔️ File berhasil disimpan ke: {output_path}")
        driver.quit()
        
        log_hasil = output_log.getvalue()  # Ambil semua print log
        return log_hasil  # Kembalikan log untuk ditampilkan di HTML
    
    finally:
        sys.stdout = sys.__stdout__
