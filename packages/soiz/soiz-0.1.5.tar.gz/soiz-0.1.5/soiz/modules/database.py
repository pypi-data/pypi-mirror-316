import pandas as pd
from sqlalchemy import create_engine, text
import urllib.parse


def create_sql_connection(config):
    """
    Tạo kết nối SQL Server sử dụng SQLAlchemy

    Parameters:
    config (dict): Dictionary chứa thông tin cấu hình kết nối

    Returns:
    engine: SQLAlchemy engine object
    """
    # Mã hóa password để tránh các ký tự đặc biệt
    password = urllib.parse.quote_plus(config["global"]["pass"])

    # Tạo connection string theo format của SQLAlchemy
    connection_string = f'mssql+pyodbc://{config["global"]["user"]}:{password}@{config["global"]["host"]}/{config["TrucNinh"]["db"]}?driver={urllib.parse.quote_plus(config["global"]["driver"])}'

    # Tạo engine
    engine = create_engine(connection_string)

    return engine


def get_data_from_sql(query, engine):
    """
    Đọc dữ liệu từ SQL Server vào pandas DataFrame

    Parameters:
    query (str): Câu lệnh SQL query
    engine: SQLAlchemy engine object

    Returns:
    DataFrame: Pandas DataFrame chứa kết quả query
    """
    try:
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        print(f"Lỗi khi thực hiện query: {str(e)}")
        return None


def execute_procedure(conn, proc_name, parameters=None):
    try:
        # Tạo cú pháp gọi procedure
        if parameters:
            # Nếu có tham số
            query = text(f"EXEC {proc_name} {','.join(['?'] * len(parameters))}")
            with conn.connect() as connection:
                result = connection.execute(query, parameters)
        else:
            # Nếu không có tham số
            query = text(f"EXEC {proc_name}")
            with conn.connect() as connection:
                result = connection.execute(query)

        # Lấy kết quả
        results = result.fetchall()
        return results

    except Exception as e:
        print(f"Lỗi khi thực thi procedure {proc_name}: {str(e)}")
        return None