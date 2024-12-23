import pg8000
import sys
import pytest

# Database connection details
db_config = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'Admin@123',
    'database': 'Dummy'
}

# Table name and columns to query
table_name = 'stud_info'
columns = ['fname', 'lname', 'email']


def connect_and_query():
    try:
        # Establish a connection to the PostgreSQL database
        conn = pg8000.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Prepare the SQL query to select data from the table
        query = f"SELECT {', '.join(columns)} FROM {table_name};"

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the query result
        rows = cursor.fetchall()

        # Print the results
        if rows:
            print(f"Data from {table_name} table:")
            for row in rows:
                print(f"First Name: {row[0]}, Last Name: {row[1]}, Email: {row[2]}")
        else:
            print(f"No data found in the {table_name} table.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()
        print("Connection closed.")


# The function connect_and_query() will execute automatically when the script is run.
# data = connect_and_query()
# print(data)