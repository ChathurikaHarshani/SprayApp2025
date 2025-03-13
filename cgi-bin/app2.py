import mysql.connector

try:
    conn = mysql.connector.connect(
        host="132.148.180.201",
        user="ssUser_Admin",
        password="UNLSpraySafely1*",
        database="ssUser_Info"
    )

    cursor = conn.cursor()
    cursor.execute("DESC User_Info;")  # ✅ Get column structure
    columns = cursor.fetchall()

    print("✅ User_Info Table Structure:")
    for column in columns:
        print(column)

    cursor.close()
    conn.close()

except mysql.connector.Error as e:
    print(f"❌ Error: {e}")
