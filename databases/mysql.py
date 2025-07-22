import mysql.connector

def simpan_ke_mysql(nama_lengkap, company):
    try:
        conn = mysql.connector.connect(
            host="dscrapper.mysql.pythonanywhere-services.com",        # Ganti sesuai server MySQL kamu
            user="dscrapper",             # Ganti sesuai user MySQL kamu
            password="",   # Ganti dengan password usermu
            database="dscrapper$default"  # Nama database
        )
        cursor = conn.cursor()
        sql = "INSERT INTO db_dscrapper(nama_lengkap, company) VALUES (%s, %s)"
        val = (nama_lengkap, company)
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Gagal simpan ke MySQL:", e)
