import sqlite3
from customer.account import BankAccount
from customer.customers import Customer  # katalogas.failas klase


def open_connection():
    connection = sqlite3.connect("customer.db")
    cursor = connection.cursor()
    return connection, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


def query_database(query, params=None):
    try:
        connection, cursor = open_connection()
        if params:
            cursor.execute(query, params)
            connection.commit()
        else:
            for row in cursor.execute(query):
                print(row)

    except sqlite3.DataError as error:
        print(error)
    finally:
        connection.close()


def create_customers_table():
    try:
        connection, cursor = open_connection()
        query = """CREATE TABLE IF NOT EXISTS customers (
                        customers_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customers_name TEXT UNIQUE,
                        account_id INTEGER,
                        FOREIGN KEY (account_id) REFERENCES account(account_id))"""

        cursor.execute(query)
        connection.commit()


    except sqlite3.DatabaseError as error:
        print(error)

    finally:
        close_connection(connection, cursor)


create_customers_table()


def create_account_table():
    try:
        connection, cursor = open_connection()
        query = """CREATE TABLE IF NOT EXISTS account (
                        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_number INTEGER,
                        customers_id INTEGER,
                        FOREIGN KEY (customers_id) REFERENCES customers(customers_id))
                    """

        cursor.execute(query)
        connection.commit()

    except sqlite3.DatabaseError as error:
        print(error)

    finally:
        close_connection(connection, cursor)


create_account_table()


def create_customers(customer):
    query = """INSERT INTO customers VALUES (? ,?, ?)"""
    params = (customer.customer_id, customer.customer_name, customer.bank_account_id)
    query_database(query, params)


def create_account(bankAccount):
    query = """INSERT INTO account VALUES (? ,?, ?)"""
    params = (bankAccount.bank_account_id, bankAccount.bank_account_number, bankAccount.customer_id)
    query_database(query, params)


def create_records(customer, bankAccount):
    create_customers(customer)
    create_account(bankAccount)
    customer.customer_id = (cursor.execute("""SELECT customer_id
                                            FROM customer
                                            WHERE customer_name DESC
                                            LIMIT 1
                                            """))


create_records()


def get_account():
    query = """SELECT * FROM account"""
    query_database(query)


def get_customers():
    query = """SELECT * FROM customers"""
    query_database(query)


customer1 = Customer(None, "Pavadinimastrecias", None)
create_customers(customer1)

account1 = BankAccount(None, "10987456321", None)
create_account(account1)

get_account()
get_customers()
