from pyhive import hive

# Connect to Hive Thrift Server
conn = hive.Connection(host='spark-server', port=10000, auth='NOSASL')

cursor = conn.cursor()
cursor.execute("SHOW DATABASES")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()