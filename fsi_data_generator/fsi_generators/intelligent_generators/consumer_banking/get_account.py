def get_account(conn, id_):
    # Fetch the consumer banking account to get its opened date
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT * FROM consumer_banking.accounts WHERE consumer_banking_account_id = %s""", (id_,))
        consumer_account = cursor.fetchone()

        if not consumer_account:
            raise ValueError(f"No consumer banking account found with ID {id_}")

        return consumer_account

    except Exception as e:
        raise e
    finally:
        cursor.close()
