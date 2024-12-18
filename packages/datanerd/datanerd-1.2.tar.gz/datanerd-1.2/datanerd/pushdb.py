import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

def pushdb(data: pd.DataFrame, tablename: str, server: str, database: str, schema: str) -> None:
    """
    Push a pandas DataFrame to a SQL Server database table.

    This function takes a pandas DataFrame and pushes it to a specified table in a SQL Server database.
    It uses SQLAlchemy and pyodbc to establish a connection and transfer the data.

    Args:
        data (pd.DataFrame): The pandas DataFrame containing the data to be pushed to the database.
        tablename (str): The name of the table in the database where the data will be inserted.
        server (str): The name or IP address of the SQL Server.
        database (str): The name of the database on the SQL Server.
        schema (str): The schema name in the database where the table is located.

    Returns:
        None

    Raises:
        SQLAlchemyError: If there's an error in creating the engine or executing the SQL.
        ValueError: If the DataFrame is empty or if any of the string parameters are empty.

    Example:
        >>> df = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
        >>> pushdb(df, 'my_table', 'my_server', 'my_database', 'dbo')
    """
    # Input validation
    if data.empty:
        raise ValueError("The input DataFrame is empty.")
    if not all([tablename, server, database, schema]):
        raise ValueError("All string parameters (tablename, server, database, schema) must be non-empty.")

    connection_string = 'DRIVER={{ODBC Driver 17 for SQL Server}};' \
                        'SERVER={server};' \
                        'DATABASE={database};' \
                        'Trusted_Connection=yes'.format(server=server, database=database)

    connection_url = sa.engine.URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

    engine = sa.create_engine(connection_url, fast_executemany=True)

    # Start a session to manage transactions
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        data.to_sql(tablename, engine, schema=schema, if_exists="fail", index=False)
    except sa.exc.SQLAlchemyError as e:
        raise sa.exc.SQLAlchemyError(f"Error pushing data to the database: {str(e)}")
    finally:
        session.close()
        engine.dispose()