import mysql.connector

def create_connection(host, user, password, dbname):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=dbname
    )
    return connection

def insert_form_data(first_name, last_name, company, role, email, birth_date, city, state, terms, news, message_creator, db_credentials):
    connection = create_connection(db_credentials["MYSQL_HOST"], db_credentials["MYSQL_USER"], db_credentials["MYSQL_PASSWORD"], db_credentials["MYSQL_DBNAME"])
    cursor = connection.cursor()

    query = """
    INSERT INTO your_table_name (first_name, last_name, company, role, email, birth_date, city, state, terms, news, message_creator)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (first_name, last_name, company, role, email, birth_date, city, state, terms, news, message_creator))
    connection.commit()

    cursor.close()
    connection.close()