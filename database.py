from contextlib import contextmanager
import queries


# context manager for making the cursor with whatever connection is passed
@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.CREATE_CPA)
        cursor.execute(queries.CREATE_CLIENTS)
        cursor.execute(queries.CREATE_TAX_ASSISTANT)
        cursor.execute(queries.CREATE_TAX_RETURN)


def insert_cpa(connection, first_name, last_name, email, license_num, license_expire):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.INSERT_CPA_RETURN_ID, (first_name, last_name, email, license_num, license_expire))
        return cursor.fetchone()[0]


def insert_client(connection, first_name, last_name, address, city, state, income, provided_materials, CPA_id):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.INSERT_CLIENT_RETURN_ID, (first_name, last_name, address, city, state, income, provided_materials, CPA_id))
        return cursor.fetchone()[0]


def insert_assistant(connection, first_name, last_name):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.INSERT_TAX_ASSISTANT, (first_name, last_name))
        return cursor.fetchone()[0]


def insert_tax_return(connection, timestamp, file_status, cpa_check, client_id, assistant_id, cpa_id):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.INSERT_TAX_RETURN, (timestamp, file_status, cpa_check, client_id, assistant_id, cpa_id))


def get_client(connection, client_id):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.SELECT_CLIENT, (client_id, ))
        return cursor.fetchone()


def get_cpa(connection, cpa_id):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.SELECT_CPA, (cpa_id, ))
        return cursor.fetchone()


def get_assistant(connection, assistant_id):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.SELECT_ASSISTANT, (assistant_id, ))
        return cursor.fetchone()


def get_client_return(connection, client_id):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.SELECT_CLIENT_RETURN, (client_id, ))
        return cursor.fetchone()


def get_all_returns(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.SELECT_ALL_TAX_RETURNS)
        return cursor.fetchall()


def get_random_cpa(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.SELECT_RANDOM_CPA)
        return cursor.fetchone()[0]


def update_client_materials(connection, status, client_id):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.UPDATE_MATERIALS_STATUS, (status, client_id))


def update_tax_return_assistant(connection, timestamp, file_status, cpa_check, assistant_id, return_id):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.UPDATE_RETURN_STATUS_ASSISTANT, (timestamp, file_status, cpa_check, assistant_id, return_id))


def update_tax_return_cpa(connection, timestamp, file_status, cpa_check, cpa_id, return_id):
    with get_cursor(connection) as cursor:
        cursor.execute(queries.UPDATE_RETURN_STATUS_CPA, (timestamp, file_status, cpa_check, cpa_id, return_id))