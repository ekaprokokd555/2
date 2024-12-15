import random
import string
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Fungsi untuk menghasilkan string acak (username dan password)
def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# Fungsi untuk membuat akun Outlook secara otomatis
def create_outlook_account(driver):
    driver.get("https://signup.live.com/")

    # Tunggu beberapa detik agar halaman dimuat (gunakan WebDriverWait untuk menunggu elemen)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "loginfmt")))

    # Membuat username acak
    username = generate_random_string(10) + "@outlook.com"
    password = generate_random_string(12)

    # Isi formulir pendaftaran
    email_field = driver.find_element(By.NAME, "loginfmt")
    email_field.send_keys(username)
    email_field.send_keys(Keys.RETURN)

    # Tunggu halaman berikutnya muncul
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idSIButton9")))

    # Klik tombol Next untuk password
    next_button = driver.find_element(By.ID, "idSIButton9")
    next_button.click()

    # Tunggu beberapa detik agar elemen muncul
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "passwd")))

    # Isi password
    password_field = driver.find_element(By.NAME, "passwd")
    password_field.send_keys(password)

    # Klik tombol Sign in
    sign_in_button = driver.find_element(By.ID, "idSIButton9")
    sign_in_button.click()

    # Tunggu beberapa detik agar proses selesai
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idSIButton9")))

    # Klik Yes untuk menyimpan info login (jika ada)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    except:
        pass  # Jika tombol tidak ada, lanjutkan

    # Setelah akun dibuat, simpan informasi akun
    return username, password

# Fungsi utama untuk membuat beberapa akun
def create_bulk_accounts(num_accounts=5):
    # Menyiapkan WebDriver untuk Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Jalankan di background (tanpa UI)
    
    # Menyiapkan WebDriver dengan ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Membuka file untuk menyimpan hasil
    with open("outlook_accounts.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Password"])  # Menulis header file CSV

        # Buat beberapa akun
        for _ in range(num_accounts):
            username, password = create_outlook_account(driver)
            print(f"Account created: {username}, {password}")

            # Simpan akun yang berhasil dibuat ke file CSV
            writer.writerow([username, password])

            # Beri jeda antar akun untuk menghindari masalah deteksi otomatisasi
            time.sleep(5)

    # Tutup browser setelah selesai
    driver.quit()

if __name__ == "__main__":
    create_bulk_accounts(num_accounts=5)  # Ganti angka 5 dengan jumlah akun yang diinginkan
