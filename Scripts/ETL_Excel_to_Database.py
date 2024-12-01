# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 20:09:10 2024

@author: karth
"""


import pandas as pd
import psycopg2

# ------------------------------------- Stage 1: Extract Data --------------------------------------------- #
# In this stage, we extract data from an Excel file.

# Load the Excel file containing manufacturing productivity data into a pandas DataFrame.
data = pd.read_excel("C:\\MyStuff\\DataEngineering\\Projects\\ETL_Excel_to_Database\\Input\\Manufacturing_Line_Productivity.xlsx")

# Print confirmation that the data has been loaded.
print("Data successfully extracted from Excel file.")
# Uncomment this line if you want to preview the loaded data.
# print(data)


# ------------------------------------- Stage 2: Transform Data ------------------------------------------- #
# In this stage, we transform the data to make it consistent and database-ready.

# Normalize column names by converting them to lowercase and replacing spaces with underscores.
data.columns = [col.lower().replace(' ', '_') for col in data.columns]

# Replace occurrences of the value 'Dee' with 'karthik' in the DataFrame.
data.replace('Dee', 'karthik', inplace=True)

# Display confirmation and the transformed column names.
print("Data transformation complete. Transformed column names:")
print(data.columns)

# Display the data types of each column for debugging and understanding the schema.
print("\nData Types:\n", data.dtypes)


# ------------------------------------- Stage 3: Load Data ------------------------------------------------ #
# In this stage, we load the transformed data into a PostgreSQL database.

# Define database connection parameters.
db_config = {
    'host': 'localhost',
    'database': 'Practice',
    'user': 'postgres',
    'password': 'Karthik@1261'
}

try:
    # Establish a connection to the PostgreSQL database.
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    print("\nDatabase connection established successfully.")

    # Declare the name of the database table.
    table_name = 'manufacturingproductivity'

    # Generate SQL column definitions dynamically based on the DataFrame's columns and their data types.
    columns = []
    for column_name, dtype in zip(data.columns, data.dtypes):
        if dtype == 'int64':  # Integer data type
            pg_type = 'INTEGER'
        elif column_name == 'date':  # Handle 'date' column specifically
            pg_type = 'DATE'
        elif column_name in ['start_time', 'end_time']:  # Handle time columns specifically
            pg_type = 'TIME'
        else:  # Default to text for other data types
            pg_type = 'TEXT'
        columns.append(f"{column_name} {pg_type}")

    # Create the SQL query for creating the table if it does not exist.
    create_table = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"

    # Execute the query to create the table.
    cur.execute(create_table)
    conn.commit()
    print(f"\nTable '{table_name}' created successfully in the database.")

    # Insert each row of the DataFrame into the database table.
    print(f"\nStarting data load into table '{table_name}'...")
    for index, row in data.iterrows():
        # Prepare column names and values placeholders for the SQL INSERT statement.
        columns = ', '.join(row.index)
        values = ', '.join(['%s'] * len(row))

        # Create the SQL INSERT query.
        insert_table = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"

        # Execute the query with the row values.
        cur.execute(insert_table, tuple(row.values))

    # Commit the transaction to save changes to the database.
    conn.commit()
    print("\nData loaded successfully into the database.")

except psycopg2.Error as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure the database connection is closed.
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("\nDatabase connection closed.")

