from pyhive import hive

# Connect to Hive Thrift Server
conn = hive.Connection(host='spark-server', port=10000, database='default',auth='NOSASL')

# Run a query (similar to what dbt does)
cursor = conn.cursor()
cursor.execute("SELECT * FROM default_source.column_description LIMIT 10")

# Print results
for row in cursor.fetchall():
    print(row)

# Close connection
cursor.close()
conn.close()
