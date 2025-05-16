import psycopg2
from config import db_config, transactionTypes


def create_tables():
    enum_values = ', '.join(f"'{t}'" for t in transactionTypes)
    """ create tables in the PostgreSQL database"""
    commands = (
        # transaction type as an exact type that can be predicted
        f"""
        DO $$ BEGIN
            CREATE TYPE TRANSACTION_TYPE AS ENUM ({enum_values});
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """
        ,
        # table for authentication
        """
        CREATE TABLE IF NOT EXISTS Users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """
        ,
        # table for all users' expenses

        """
        CREATE TABLE IF NOT EXISTS Expenses (
            user_id INTEGER REFERENCES Users(user_id),
            type TRANSACTION_TYPE NOT NULL,
            optional_type VARCHAR(255),
            amount NUMERIC NOT NULL,
            date DATE        
        )
        """
    )
    conn = None
    try:
        # read the connection parameters
        params = db_config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # create table one by one
        for command in commands:
            cur.execute(command)

        # commit the changes
        conn.commit()

        # close communication with the PostgreSQL database server
        cur.close()
        print("✅ Database initialized and tables created.")
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
        

if __name__ == '__main__':
    create_tables()