import pymysql
import time
import os

MASTER_HOST = os.getenv('MASTER_HOST', 'mysql-master')
SLAVE_HOST = os.getenv('SLAVE_HOST', 'mysql-slave')
DATABASE = os.getenv('MYSQL_DATABASE', 'bugs')
TABLE = 'random_data'
ROOT_USER = os.getenv('MYSQL_ROOT_USER', 'root')
ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', 'root')
USER = os.getenv('MYSQL_USER', 'bugs')
PASSWORD = os.getenv('MYSQL_PASSWORD', 'bugs')
MASTER_PORT = int(os.getenv('MASTER_PORT', 3306))
SLAVE_PORT = int(os.getenv('SLAVE_PORT', 3306))

def create_table_if_not_exists(connection):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {DATABASE}.{TABLE} (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                value VARCHAR(255)
            );
        """)
    connection.commit()

def insert_random_data(connection):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO {DATABASE}.{TABLE} (value) VALUES ('test_data');")
    connection.commit()

def get_data_count(connection):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {DATABASE}.{TABLE};")
        return cursor.fetchone()[0]

def check_slave_data():
    # Connect to master
    print("Connecting to master...")
    print(f"MASTER_HOST: {MASTER_HOST}")

    print(f"ROOT_USER: {ROOT_USER}")
    print(f"ROOT_PASSWORD: {ROOT_PASSWORD}")

    print(f"USER: {USER}")
    print(f"PASSWORD: {PASSWORD}")
    print(f"DATABASE: {DATABASE}")
    print(f"MASTER_PORT: {MASTER_PORT}")

    master_conn = pymysql.connect(host=MASTER_HOST, user=ROOT_USER, password=ROOT_PASSWORD, db=DATABASE, port=MASTER_PORT)
    
    # Ensure table exists
    create_table_if_not_exists(master_conn)
    
    # Insert data into master
    print("Inserting data into master...")

    master_conn = pymysql.connect(host=MASTER_HOST, user=USER, password=PASSWORD, db=DATABASE, port=MASTER_PORT)
    insert_random_data(master_conn)
    
    master_count = get_data_count(master_conn)
    print(f"Master has {master_count} rows in {TABLE}.")

    master_conn.close()
    
    # Wait for replication and check slave
    print("Waiting for replication...")
    time.sleep(10)  # Wait for replication
    
    print("Connecting to slave...")
    slave_conn = pymysql.connect(host=SLAVE_HOST, user=USER, password=PASSWORD, db=DATABASE, port=SLAVE_PORT)

    slave_count = get_data_count(slave_conn)
    print(f"Slave has {slave_count} rows in {TABLE}.")
    
    if slave_count == master_count:
        print("Data replicated successfully.")
    else:
        print("Data replication failed.")
    
    slave_conn.close()

if __name__ == "__main__":
    check_slave_data()