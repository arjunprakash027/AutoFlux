from pyhive import hive
import sys

# Define Thrift Server connection parameters
host = "spark-server"  # Change this to your Spark Thrift Server hostname or IP
port = 10000  # Default Thrift Server port
database = "default"  # Change this to your database name


# Establish connection to Spark Thrift Server
conn = hive.Connection(
    host=host,
    port=port,
    database=database,
    auth="NOSASL"  # Use 'NOSASL' if authentication is disabled
)

# Create a cursor to execute SQL queries
cursor = conn.cursor()

# Run a simple query to check connection
cursor.execute("SHOW DATABASES")
databases = cursor.fetchall()

print("Connected successfully! Available databases:")
for db in databases:
    print(db[0])

# Close connection
cursor.close()
conn.close()
