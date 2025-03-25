def get_product_type_by_account_id(conn, account_id):
    """
    Fetches the product_type associated with a given consumer_banking_account_id.

    :param conn: A psycopg2 database connection object.
    :param account_id: The consumer_banking_account_id to look up.
    :return: The product_type as a string.
    :raises Exception: If the product_type is not found or an error occurs.
    """
    try:
        # Create a new cursor
        with conn.cursor() as cursor:
            # SQL query to fetch the product_type
            query = """
                SELECT p.product_type
                FROM consumer_banking.accounts a
                JOIN consumer_banking.products p
                ON a.consumer_banking_product_id = p.consumer_banking_product_id
                WHERE a.consumer_banking_account_id = %s;
            """

            # Execute the query and fetch the result
            cursor.execute(query, (account_id,))
            result = cursor.fetchone()

            # Check if a result was found
            if result is None:
                raise Exception(f"No product_type found for account_id {account_id}")

            # Return the product_type
            return result.get('product_type')

    except Exception as e:
        # Reraise any exceptions that occur
        raise Exception(f"Error fetching product_type for account_id {account_id}: {str(e)}")
