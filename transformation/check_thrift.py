from pyhive import hive

# Connect to Hive Thrift Server
conn = hive.Connection(host='spark-server', port=10000, database='default',auth='NOSASL')

cursor = conn.cursor()
cursor.execute("SELECT * FROM default_source.column_description LIMIT 10")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
