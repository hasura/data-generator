BEGIN; -- Start the transaction

-- Example 1: Direct Transfer to GUARDIAN (Expanded)

-- Enterprise Account for John Doe
INSERT INTO enterprise.accounts (opening_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '1 year', 'Active', NOW(), 'Personal', 'John Doe Main Account');

-- Get the generated enterprise_account_id
SELECT currval('enterprise.accounts_enterprise_account_id_seq') INTO john_doe_enterprise_account_id;

-- Enterprise Account for Jane Smith
INSERT INTO enterprise.accounts (opening_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '6 months', 'Active', NOW(), 'Personal', 'Jane Smith Main Account');

-- Get the generated enterprise_account_id
SELECT currval('enterprise.accounts_enterprise_account_id_seq') INTO jane_smith_enterprise_account_id;

-- Enterprise Party (Consumer - John Doe)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('Individual', 'John Doe', 'john.doe@example.com', '555-123-4567');

-- Get the generated enterprise_party_id
SELECT currval('enterprise.parties_enterprise_party_id_seq') INTO john_doe_id;

-- Enterprise Party (GUARDIAN - Jane Smith)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('Individual', 'Jane Smith', 'jane.smith@example.com', '555-987-6543');

-- Get the generated enterprise_party_id
SELECT currval('enterprise.parties_enterprise_party_id_seq') INTO jane_smith_id;

-- Party Relationships
INSERT INTO enterprise.party_relationships (enterprise_party_id, related_party_id, relationship_type)
VALUES (john_doe_id, jane_smith_id, 'GUARDIAN');

-- Get the consumer_banking_product_id for 'CHECKING'
SELECT consumer_banking_product_id INTO checking_product_id
FROM consumer_banking.products
WHERE product_type = 'CHECKING'
LIMIT 1; -- Assuming there's only one 'CHECKING' product

-- Consumer Banking Account (John Doe)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id)
VALUES (john_doe_enterprise_account_id, checking_product_id);

-- Get account ID
SELECT currval('consumer_banking.accounts_consumer_banking_account_id_seq') INTO john_doe_account_id;

-- Consumer Banking Account (Jane Smith)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id)
VALUES (jane_smith_enterprise_account_id, checking_product_id);

-- Get account ID
SELECT currval('consumer_banking.accounts_consumer_banking_account_id_seq') INTO jane_smith_account_id;

-- Transactions (Varied amounts and times)
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (john_doe_account_id, 'DEBIT', 'Booked', '2023-03-01T10:00:00Z', '2023-03-01T10:00:00Z', 'Online Transfer', 1000.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (jane_smith_account_id, 'CREDIT', 'Booked', '2023-03-01T10:15:00Z', '2023-03-01T10:15:00Z', 'Online Transfer', 1000.00, 'USD');

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (john_doe_account_id, 'DEBIT', 'Booked', '2023-03-15T12:00:00Z', '2023-03-15T12:00:00Z', 'ATM Withdrawal', 250.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (jane_smith_account_id, 'CREDIT', 'Booked', '2023-03-15T14:00:00Z', '2023-03-15T14:00:00Z', 'Deposit', 250.00, 'USD');

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (john_doe_account_id, 'DEBIT', 'Booked', '2023-04-01T09:00:00Z', '2023-04-01T09:00:00Z', 'Check #123', 5000.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (jane_smith_account_id, 'CREDIT', 'Booked', '2023-04-05T10:00:00Z', '2023-04-05T10:00:00Z', 'Deposit', 4900.00, 'USD');


-- Example 2: GUARDIAN Disburses Similar Amount After Receiving Funds (Expanded)

-- Enterprise Account for Alice Johnson
INSERT INTO enterprise.accounts (opening_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '8 months', 'Active', NOW(), 'Personal', 'Alice Johnson Main Account');

-- Get the generated enterprise_account_id
SELECT currval('enterprise.accounts_enterprise_account_id_seq') INTO alice_johnson_enterprise_account_id;

-- Enterprise Account for Bob Williams
INSERT INTO enterprise.accounts (opening_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '3 months', 'Active', NOW(), 'Personal', 'Bob Williams Main Account');

-- Get the generated enterprise_account_id
SELECT currval('enterprise.accounts_enterprise_account_id_seq') INTO bob_williams_enterprise_account_id;

-- Enterprise Party (Consumer)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('Individual', 'Alice Johnson', 'alice.johnson@example.com', '555-555-5555');

-- Get IDs
SELECT currval('enterprise.parties_enterprise_party_id_seq') INTO alice_johnson_id;

-- Enterprise Party (GUARDIAN)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('Individual', 'Bob Williams', 'bob.williams@example.com', '555-111-2222');

-- Get IDs
SELECT currval('enterprise.parties_enterprise_party_id_seq') INTO bob_williams_id;

-- Party Relationships
INSERT INTO enterprise.party_relationships (enterprise_party_id, related_party_id, relationship_type)
VALUES (alice_johnson_id, bob_williams_id, 'GUARDIAN');

-- Consumer Banking Account (Alice Johnson)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id)
VALUES (alice_johnson_enterprise_account_id, checking_product_id);

-- Get account ID
SELECT currval('consumer_banking.accounts_consumer_banking_account_id_seq') INTO alice_johnson_account_id;

-- Consumer Banking Account (Bob Williams)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id)
VALUES (bob_williams_enterprise_account_id, checking_product_id);

-- Get account ID
SELECT currval('consumer_banking.accounts_consumer_banking_account_id_seq') INTO bob_williams_account_id;

-- Transactions (Varied amounts, times, and transaction types)
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (alice_johnson_account_id, 'DEBIT', 'Booked', '2023-03-05T14:30:00Z', '2023-03-05T14:30:00Z', 'ATM Withdrawal', 500.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (bob_williams_account_id, 'CREDIT', 'Booked', '2023-03-05T14:45:00Z', '2023-03-05T14:45:00Z', 'Deposit', 500.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (bob_williams_account_id, 'DEBIT', 'Booked', '2023-03-06T09:00:00Z', '2023-03-06T09:00:00Z', 'Online Purchase', 480.00, 'USD');

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (alice_johnson_account_id, 'DEBIT', 'Booked', '2023-03-20T10:00:00Z', '2023-03-20T10:00:00Z', 'Transfer to External Account', 10000.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (bob_williams_account_id, 'CREDIT', 'Booked', '2023-03-20T10:30:00Z', '2023-03-20T10:30:00Z', 'Incoming Wire', 9850.00, 'USD');

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (alice_johnson_account_id, 'DEBIT', 'Booked', '2023-04-10T16:00:00Z', '2023-04-10T16:00:00Z', 'Bill Payment - Utility Company', 300.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (bob_williams_account_id, 'DEBIT', 'Booked', '2023-04-11T08:00:00Z', '2023-04-11T08:00:00Z', 'Withdrawal - Casino ATM', 280.00, 'USD');


-- Example 3: Multiple GUARDIANs and Transactions

-- Enterprise Account for Charlie Brown
INSERT INTO enterprise.accounts (opening_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '10 months', 'Active', NOW(), 'Personal', 'Charlie Brown Main Account');

-- Get the generated enterprise_account_id
SELECT currval('enterprise.accounts_enterprise_account_id_seq') INTO charlie_brown_enterprise_account_id;

-- Enterprise Account for Lucy Van Pelt
INSERT INTO enterprise.accounts (opening_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '7 months', 'Active', NOW(), 'Personal', 'Lucy Van Pelt Main Account');

-- Get the generated enterprise_account_id
SELECT currval('enterprise.accounts_enterprise_account_id_seq') INTO lucy_van_pelt_enterprise_account_id;

-- Enterprise Account for Linus Van Pelt
INSERT INTO enterprise.accounts (opening_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '5 months', 'Active', NOW(), 'Personal', 'Linus Van Pelt Main Account');

-- Get the generated enterprise_account_id
SELECT currval('enterprise.accounts_enterprise_account_id_seq') INTO linus_van_pelt_enterprise_account_id;

-- Enterprise Party (Consumer)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('Individual', 'Charlie Brown', 'charlie.brown@example.com', '555-333-4444');

-- Get IDs
SELECT currval('enterprise.parties_enterprise_party_id_seq') INTO charlie_brown_id;

-- Enterprise Party (GUARDIAN 1)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('Individual', 'Lucy Van Pelt', 'lucy.vanpelt@example.com', '555-222-1111');

-- Get IDs
SELECT currval('enterprise.parties_enterprise_party_id_seq') INTO lucy_van_pelt_id;

-- Enterprise Party (GUARDIAN 2)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('Individual', 'Linus Van Pelt', 'linus.vanpelt@example.com', '555-777-8888');

-- Get IDs
SELECT currval('enterprise.parties_enterprise_party_id_seq') INTO linus_van_pelt_id;

-- Party Relationships
INSERT INTO enterprise.party_relationships (enterprise_party_id, related_party_id, relationship_type)
VALUES (charlie_brown_id, lucy_van_pelt_id, 'GUARDIAN');
INSERT INTO enterprise.party_relationships (enterprise_party_id, related_party_id, relationship_type)
VALUES (charlie_brown_id, linus_van_pelt_id, 'GUARDIAN');

-- Consumer Banking Account (Charlie Brown)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id)
VALUES (charlie_brown_enterprise_account_id, checking_product_id);

-- Get account ID
SELECT currval('consumer_banking.accounts_consumer_banking_account_id_seq') INTO charlie_brown_account_id;

-- Consumer Banking Account (Lucy Van Pelt)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id)
VALUES (lucy_van_pelt_enterprise_account_id, checking_product_id);

-- Get account ID
SELECT currval('consumer_banking.accounts_consumer_banking_account_id_seq') INTO lucy_van_pelt_account_id;

-- Consumer Banking Account (Linus Van Pelt)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id)
VALUES (linus_van_pelt_enterprise_account_id, checking_product_id);

-- Get account ID
SELECT currval('consumer_banking.accounts_consumer_banking_account_id_seq') INTO linus_van_pelt_account_id;

-- Transactions (Varied GUARDIANs, amounts, and times)
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (charlie_brown_account_id, 'DEBIT', 'Booked', '2023-02-10T11:00:00Z', '2023-02-10T11:00:00Z', 'Online Transfer to Lucy', 500.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (lucy_van_pelt_account_id, 'CREDIT', 'Booked', '2023-02-10T11:15:00Z', '2023-02-10T11:15:00Z', 'Online Transfer', 500.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (lucy_van_pelt_account_id, 'DEBIT', 'Booked', '2023-02-11T10:00:00Z', '2023-02-11T10:00:00Z', 'Purchase - Department Store', 450.00, 'USD');

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (charlie_brown_account_id, 'DEBIT', 'Booked', '2023-03-05T15:30:00Z', '2023-03-05T15:30:00Z', 'Check #456 to Linus', 1000.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (linus_van_pelt_account_id, 'CREDIT', 'Booked', '2023-03-08T09:00:00Z', '2023-03-08T09:00:00Z', 'Deposit - Check', 1000.00, 'USD');
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, Credit_Debit_indicator, status, booking_date_time, value_date_time, transaction_information, amount, currency)
VALUES (linus_van_pelt_account_id, 'DEBIT', 'Booked', '2023-03-10T14:00:00Z', '2023-03-10T14:00:00Z', 'Online Transfer - Personal Account', 900.00, 'USD');

COMMIT; -- Complete the transaction
