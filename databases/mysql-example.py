import mysql.connector

def yourfunctiontobecalled(your_parameter):
    try:
        conn = mysql.connector.connect(
            host="localhost",        # Ganti sesuai server MySQL kamu
            user="YOUR_USERNAME_HERE",             # Ganti sesuai user MySQL kamu
            password="YOUR_PASSWORD_HERE",   # Ganti dengan password usermu
            database="YOUR_DATABASE_NAME"  # Nama database
        )
        cursor = conn.cursor()
        sql = "INSERT INTO YOUR_TABLE_NAME (your_parameter) VALUES (%s, %s)"
        val = (your_parameter)
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Gagal simpan ke MySQL:", e)
