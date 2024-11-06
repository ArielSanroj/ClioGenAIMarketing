import os
import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.environ['PGDATABASE'],
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'],
            host=os.environ['PGHOST'],
            port=os.environ['PGPORT']
        )
        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS campaigns (
                    id SERIAL PRIMARY KEY,
                    business_name TEXT,
                    campaign_type TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS audience_analysis (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER,
                    demographics JSON,
                    insights TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()

    def save_campaign(self, business_name, campaign_type, content):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO campaigns (business_name, campaign_type, content) VALUES (%s, %s, %s) RETURNING id",
                (business_name, campaign_type, content)
            )
            self.conn.commit()
            return cur.fetchone()[0]

    def get_campaigns(self, business_name):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM campaigns WHERE business_name = %s ORDER BY created_at DESC",
                (business_name,)
            )
            return cur.fetchall()

db = Database()
