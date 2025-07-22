from flask import Flask, render_template, request
import traceback  # Untuk menangkap log error

from scraping.penarikan_IGracias import penarikan_igracias
from scraping.penarikan_LHKPN import penarikan_lhkpn
from scraping.penarikan_minerba import penarikan_minerba
from databases.mysql import simpan_ke_mysql
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-script", methods=["POST"])
def run_script():
    errors = []
    hasil_log = "Anda Belum Memilih Scraping"
    pilihan = request.form.get('pilihan')
    nama_depan = request.form.get('first-name', '').strip()
    nama_belakang = request.form.get('last-name', '').strip()
    company = request.form.get('company', '').strip()
    nama_lengkap = f"{nama_depan} {nama_belakang}"

    if not nama_depan:
            errors.append("⚠️ First Name tidak boleh kosong!")
    if not nama_belakang:
        errors.append("⚠️ Last Name tidak boleh kosong!")

    if errors:
        hasil_log = "\n".join(errors)
        return render_template("index.html", hasil=hasil_log)

    else:
        try:
            if pilihan == "Igracias":
                hasil_log = penarikan_igracias()
            elif pilihan == "LHKPN":
                hasil_log = penarikan_lhkpn()
            elif pilihan == "Minerba":
                hasil_log = penarikan_minerba()
            else:
                hasil_log = "Pilihan scraping tidak valid!"
        except Exception as e:
            # Tangkap dan tampilkan traceback error ke HTML (untuk debugging)
            hasil_log = f"Terjadi kesalahan saat menjalankan script:\n{traceback.format_exc()}"

        # Simpan hasil ke MySQL
        simpan_ke_mysql(nama_lengkap, company)

        return render_template("index.html", hasil=hasil_log, nama_lengkap=nama_lengkap)

if __name__ == "__main__":
    app.run(debug=True)
