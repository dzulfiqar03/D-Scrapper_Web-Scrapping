from flask import Flask, render_template, request
import traceback  # Untuk menangkap log error

from scraping.penarikan_IGracias import penarikan_igracias
from scraping.penarikan_LHKPN import penarikan_lhkpn
from scraping.penarikan_minerba import penarikan_minerba
from databases.mysql import simpan_ke_mysql
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("app.html")

@app.route("/run-script", methods=["POST"])
def run_script():


    return print("Berhasil Run python")

if __name__ == "__main__":
    app.run(debug=True)
