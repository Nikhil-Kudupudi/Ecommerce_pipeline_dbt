import os 
import yaml 
import snowflake.connector
import sys 

def load_snowflake_config():
    config_file_path = os.path.join(os.path.dirname(__file__), '../config/snowflake-config.yaml')
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['snowflake']

def main():
    print("✅ Running Snowflake delayed orders check...")
    print("✅ Python path:", sys.executable)
    print("✅ Snowflake connector version:", snowflake.connector.__version__)
    config = load_snowflake_config()
    try:
        conn = snowflake.connector.connect(
            user=config['user'],
            private_key_file=config['private_key_path'],
            account=config['account'],
            warehouse=config['warehouse'],
            database=config['database'],
            role=config['role'],
            schema=config['schema'],
            login_timeout=20,
            client_session_keep_alive=False,
            ocsp_fail_open=True
        )
        print("✅ Successfully connected to Snowflake.")

        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) 
            FROM ECOMMERCE_DB.ANALYTICS.ORDER_STATUS 
            WHERE FINAL_STATUS = 'DELAYED'
        """)
        result = cur.fetchone()
        print("✅ Delayed orders found:", result)
        cur.close()
        conn.close()
        if result[0] > 0:
            raise Exception(f"{result[0]} delayed orders found.")
    except Exception as e:
        print("❌ Error connecting to Snowflake:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()