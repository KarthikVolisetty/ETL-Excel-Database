**ETL: Excel to Database**

**README.md**
# ETL: Excel to Database

## Description
This ETL process reads manufacturing productivity data from an Excel file, transforms column names and values, and loads the data into a PostgreSQL database table.

## Key Features
- **Data Source**: Excel file (`Manufacturing_Line_Productivity.xlsx`).
- **Transformations**:
  - Standardized column names to lowercase with underscores.
  - Replaced specific values in the dataset (e.g., `Dee` to `karthik`).
- **Database**: PostgreSQL.

## Prerequisites
1. Install the required Python libraries:
   ```bash
   pip install pandas psycopg2 openpyxl
   ```
2. Ensure you have PostgreSQL installed and running.
3. Create a database named `Practice` in PostgreSQL (or update the script to match your database).

## Files
- `Manufacturing_Line_Productivity.xlsx`: Input file containing the data.
- `ETL_Excel_to_Database.py`: Python script to execute the ETL process.

## How to Run
1. Place `Manufacturing_Line_Productivity.xlsx` in the specified directory.
2. Update the `db_config` in the script with your database credentials.
3. Execute the script:
   ```bash
   python etl_excel_to_db.py
   ```
4. Check the `manufacturingproductivity` table in your PostgreSQL database for the loaded data.

## Output
- The script will create a table named `manufacturingproductivity` in your PostgreSQL database and load the transformed data into it.
