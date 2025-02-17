import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

# SQLAlchemy setup
server = os.getenv('DB_SERVER', 'LINKOLJUL23-134')
database = os.getenv('DB_NAME', 'CustomerDB')
username = os.getenv('DB_USER', 'APISERVICE1')
password = os.getenv('DB_PASSWORD', 'Pursuit@123')
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")

Base = declarative_base()
metadata = MetaData()

# Define Customer model
class Customer(Base):
    __table__ = Table('CustomerDetails', metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)

# API endpoint to fetch customer by ID
@app.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    session = Session()
    try:
        customer = session.query(Customer).filter_by(id=id).first()
        if customer:
            return jsonify({'id': customer.id, 'name': customer.customer_name, 'address': customer.customer_address})
        else:
            return jsonify({'error': 'Customer not found'}), 404
    except Exception as e:
        # Log the exception or handle it as per your application's requirements
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False for production deployment
