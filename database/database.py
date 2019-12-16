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


def create_customers(customer):
    query = """INSERT INTO customers VALUES (? ,?, ?)"""
    params = (customer.customer_id, customer.customer_name, customer.bank_account_id)
    query_database(query, params)


def create_account(bankAccount, customer_id):
    query = """INSERT INTO account VALUES (? ,?, ?)"""
    params = (bankAccount.bank_account_id, bankAccount.bank_account_number, customer_id)
    query_database(query, params)


def update_customers(bank_account_id, customer_id):
    query = """UPDATE customers SET account_id = ? WHERE customers_id = ?"""
    params = (bank_account_id, customer_id)
    query_database(query, params)


def create_records(customer, bankAccount):

    create_customers(customer)

    connection, cursor = open_connection()
    customer_id_for_account_table = cursor.execute("""SELECT customers_id
                                            FROM customers
                                            WHERE customers_name = ?                                            
                                            """, (customer.customer_name,)).fetchone()
    close_connection(connection, cursor)
    print(customer_id_for_account_table)
    customer.customer_id = customer_id_for_account_table[0]

    create_account(bankAccount, customer.customer_id)
    connection, cursor = open_connection()
    account_id_for_customer_table = cursor.execute("""SELECT account_id
                                            FROM account
                                            ORDER BY account_id DESC                                            
                                            """).fetchone()
    close_connection(connection, cursor)
    bankAccount.account_id = account_id_for_customer_table[0]
    print(account_id_for_customer_table[0])
    update_customers(bankAccount.account_id, customer.customer_id)

def get_account():
    query = """SELECT * FROM account"""
    query_database(query)


def get_customers():
    query = """SELECT * FROM customers, account"""
    query_database(query)


create_customers_table()
create_account_table()

customer1 = Customer(None, "jgj123", None)
account1 = BankAccount(None, "1546445", None)
create_records(customer1, account1)
#get_account()
get_customers()
