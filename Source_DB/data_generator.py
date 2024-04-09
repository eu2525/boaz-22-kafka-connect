# data_generator.py
import time
from argparse import ArgumentParser

import pandas as pd
import psycopg2


def create_table(db_connect):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Boaz (
        id SERIAL PRIMARY KEY,
        First_Name text,
        Last_Name text,
        GENDER text ,
        Generation int
    );
    """
    print(create_table_query)
    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()


def insert_data(db_connect):
    df = pd.read_csv('./boaz.csv')
    for index, data in df.iterrows():
        # SQL 쿼리 생성
        insert_row_query = f"""
        INSERT INTO Boaz
            (First_Name, Last_Name, Gender, Generation)
            VALUES (
                '{data['First_Name']}',
                '{data['Last_Name']}',
                '{data['Gender']}',
                {data['Generation']}
            );
        """
        # 데이터베이스에 쿼리 실행
        with db_connect.cursor() as cur:
            cur.execute(insert_row_query)
            db_connect.commit()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--db-host", dest="db_host", type=str, default="localhost")
    args = parser.parse_args()

    db_connect = psycopg2.connect(
        user="myuser",
        password="mypassword",
        host=args.db_host,
        port=5433,
        database="mydatabase",
    )
    create_table(db_connect)
    insert_data(db_connect)
