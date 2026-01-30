import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="retail_user",
        password="StrongPassword@123",
        database="retail"
    )

def fetch_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM orders WHERE order_id = %s",
        (order_id,)
    )

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result
