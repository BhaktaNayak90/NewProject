import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

# Get hybrid connection string from environment
hybrid_connection_string = os.getenv('HYBRID_CONNECTION_STRING')

# SQLAlchemy setup using hybrid connection string
engine = create_engine(hybrid_connection_string)

Base = declarative_base()
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)

# Define Customer model
class Customer(Base):
    __table__ = Table('Customer', metadata, autoload_with=engine)

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
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=False)
