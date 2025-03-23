-- Note: Tables, schemas, and sequences are already guaranteed to exist
-- This script fixes constraints based on the DBML schema

BEGIN;
-- Start the transaction

-- Example 1: Direct Transfer to GUARDIAN (Expanded)

-- Enterprise Account for John Doe
INSERT INTO enterprise.accounts (opened_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '1 year', 'ACTIVE', NOW(), 'Personal', 'John Doe Main Account');

-- Enterprise Account for Jane Smith
INSERT INTO enterprise.accounts (opened_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '6 months', 'ACTIVE', NOW(), 'Personal', 'Jane Smith Main Account');

-- Enterprise Party (Consumer - John Doe)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('INDIVIDUAL', 'John Doe', 'john.doe@example.com', '555-123-4567');

-- Enterprise Party (GUARDIAN - Jane Smith)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('INDIVIDUAL', 'Jane Smith', 'jane.smith@example.com', '555-987-6543');

-- Account Ownership - Link John Doe to his account
INSERT INTO enterprise.account_ownership (enterprise_account_id, enterprise_party_id)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'John Doe Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'John Doe'
          AND email_address = 'john.doe@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1);

-- Account Ownership - Link Jane Smith to her account
INSERT INTO enterprise.account_ownership (enterprise_account_id, enterprise_party_id)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Jane Smith Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Jane Smith'
          AND email_address = 'jane.smith@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1);

-- Party Relationships
INSERT INTO enterprise.party_relationships (enterprise_party_id, related_party_id, relationship_type)
SELECT (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'John Doe'
          AND email_address = 'john.doe@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Jane Smith'
          AND email_address = 'jane.smith@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1),
       'GUARDIAN';

-- Consumer Banking Account (John Doe)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id, opened_date, status,
                                       status_update_date_time)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'John Doe Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT consumer_banking_product_id FROM consumer_banking.products WHERE product_type = 'CHECKING' LIMIT 1),
       NOW() - INTERVAL '1 year',
       'ACTIVE',
       NOW();

-- Consumer Banking Account (Jane Smith)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id, opened_date, status,
                                       status_update_date_time)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Jane Smith Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT consumer_banking_product_id FROM consumer_banking.products WHERE product_type = 'CHECKING' LIMIT 1),
       NOW() - INTERVAL '6 months',
       'ACTIVE',
       NOW();

-- Transactions (Varied amounts and times)
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'John Doe Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-03-01T10:00:00Z',
       '2023-03-01T10:00:00Z',
       'Online Transfer',
       1000.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Jane Smith Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'CR',
       'booked',
       '2023-03-01T10:15:00Z',
       '2023-03-01T10:15:00Z',
       'Online Transfer',
       1000.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'John Doe Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-03-15T12:00:00Z',
       '2023-03-15T12:00:00Z',
       'ATM Withdrawal',
       250.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Jane Smith Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'CR',
       'booked',
       '2023-03-15T14:00:00Z',
       '2023-03-15T14:00:00Z',
       'Deposit',
       250.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'John Doe Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-04-01T09:00:00Z',
       '2023-04-01T09:00:00Z',
       'Check #123',
       5000.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Jane Smith Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'CR',
       'booked',
       '2023-04-05T10:00:00Z',
       '2023-04-05T10:00:00Z',
       'Deposit',
       4900.00,
       'USD';


-- Example 2: GUARDIAN Disburses Similar Amount After Receiving Funds (Expanded)

-- Enterprise Account for Alice Johnson
INSERT INTO enterprise.accounts (opened_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '8 months', 'ACTIVE', NOW(), 'Personal', 'Alice Johnson Main Account');

-- Enterprise Account for Bob Williams
INSERT INTO enterprise.accounts (opened_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '3 months', 'ACTIVE', NOW(), 'Personal', 'Bob Williams Main Account');

-- Enterprise Party (Consumer)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('INDIVIDUAL', 'Alice Johnson', 'alice.johnson@example.com', '555-555-5555');

-- Enterprise Party (GUARDIAN)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('INDIVIDUAL', 'Bob Williams', 'bob.williams@example.com', '555-111-2222');

-- Account Ownership - Link Alice Johnson to her account
INSERT INTO enterprise.account_ownership (enterprise_account_id, enterprise_party_id)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Alice Johnson Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Alice Johnson'
          AND email_address = 'alice.johnson@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1);

-- Account Ownership - Link Bob Williams to his account
INSERT INTO enterprise.account_ownership (enterprise_account_id, enterprise_party_id)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Bob Williams Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Bob Williams'
          AND email_address = 'bob.williams@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1);

-- Party Relationships
INSERT INTO enterprise.party_relationships (enterprise_party_id, related_party_id, relationship_type)
SELECT (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Alice Johnson'
          AND email_address = 'alice.johnson@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Bob Williams'
          AND email_address = 'bob.williams@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1),
       'GUARDIAN';

-- Consumer Banking Account (Alice Johnson)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id, opened_date, status,
                                       status_update_date_time)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Alice Johnson Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT consumer_banking_product_id FROM consumer_banking.products WHERE product_type = 'CHECKING' LIMIT 1),
       NOW() - INTERVAL '8 months',
       'ACTIVE',
       NOW();

-- Consumer Banking Account (Bob Williams)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id, opened_date, status,
                                       status_update_date_time)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Bob Williams Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT consumer_banking_product_id FROM consumer_banking.products WHERE product_type = 'CHECKING' LIMIT 1),
       NOW() - INTERVAL '3 months',
       'ACTIVE',
       NOW();

-- Transactions (Varied amounts, times, and transaction types)
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Alice Johnson Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-03-05T14:30:00Z',
       '2023-03-05T14:30:00Z',
       'ATM Withdrawal',
       500.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Bob Williams Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'CR',
       'booked',
       '2023-03-05T14:45:00Z',
       '2023-03-05T14:45:00Z',
       'Deposit',
       500.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Bob Williams Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-03-06T09:00:00Z',
       '2023-03-06T09:00:00Z',
       'Online Purchase',
       480.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Alice Johnson Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-03-20T10:00:00Z',
       '2023-03-20T10:00:00Z',
       'Transfer to External Account',
       10000.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Bob Williams Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'CR',
       'booked',
       '2023-03-20T10:30:00Z',
       '2023-03-20T10:30:00Z',
       'Incoming Wire',
       9850.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Alice Johnson Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-04-10T16:00:00Z',
       '2023-04-10T16:00:00Z',
       'Bill Payment - Utility Company',
       300.00,
       'USD';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Bob Williams Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-04-11T08:00:00Z',
       '2023-04-11T08:00:00Z',
       'Withdrawal - Casino ATM',
       280.00,
       'USD';


-- Example 3: Multiple GUARDIANs and Transactions

-- Enterprise Account for Charlie Brown
INSERT INTO enterprise.accounts (opened_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '10 months', 'ACTIVE', NOW(), 'Personal', 'Charlie Brown Main Account');

-- Enterprise Account for Lucy Van Pelt
INSERT INTO enterprise.accounts (opened_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '7 months', 'ACTIVE', NOW(), 'Personal', 'Lucy Van Pelt Main Account');

-- Enterprise Account for Linus Van Pelt
INSERT INTO enterprise.accounts (opened_date, status, status_update_date_time, account_category, description)
VALUES (NOW() - INTERVAL '5 months', 'ACTIVE', NOW(), 'Personal', 'Linus Van Pelt Main Account');

-- Enterprise Party (Consumer)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('INDIVIDUAL', 'Charlie Brown', 'charlie.brown@example.com', '555-333-4444');

-- Enterprise Party (GUARDIAN 1)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('INDIVIDUAL', 'Lucy Van Pelt', 'lucy.vanpelt@example.com', '555-222-1111');

-- Enterprise Party (GUARDIAN 2)
INSERT INTO enterprise.parties (party_type, name, email_address, phone)
VALUES ('INDIVIDUAL', 'Linus Van Pelt', 'linus.vanpelt@example.com', '555-777-8888');

-- Account Ownership - Link Charlie Brown to his account
INSERT INTO enterprise.account_ownership (enterprise_account_id, enterprise_party_id)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Charlie Brown Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Charlie Brown'
          AND email_address = 'charlie.brown@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1);

-- Account Ownership - Link Lucy Van Pelt to her account
INSERT INTO enterprise.account_ownership (enterprise_account_id, enterprise_party_id)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Lucy Van Pelt Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Lucy Van Pelt'
          AND email_address = 'lucy.vanpelt@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1);

-- Account Ownership - Link Linus Van Pelt to his account
INSERT INTO enterprise.account_ownership (enterprise_account_id, enterprise_party_id)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Linus Van Pelt Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Linus Van Pelt'
          AND email_address = 'linus.vanpelt@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1);

-- Party Relationships
INSERT INTO enterprise.party_relationships (enterprise_party_id, related_party_id, relationship_type)
SELECT (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Charlie Brown'
          AND email_address = 'charlie.brown@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Lucy Van Pelt'
          AND email_address = 'lucy.vanpelt@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1),
       'GUARDIAN';

INSERT INTO enterprise.party_relationships (enterprise_party_id, related_party_id, relationship_type)
SELECT (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Charlie Brown'
          AND email_address = 'charlie.brown@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1),
       (SELECT enterprise_party_id
        FROM enterprise.parties
        WHERE name = 'Linus Van Pelt'
          AND email_address = 'linus.vanpelt@example.com'
        ORDER BY enterprise_party_id DESC
        LIMIT 1),
       'GUARDIAN';

-- Consumer Banking Account (Charlie Brown)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id, opened_date, status,
                                       status_update_date_time)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Charlie Brown Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT consumer_banking_product_id FROM consumer_banking.products WHERE product_type = 'CHECKING' LIMIT 1),
       NOW() - INTERVAL '10 months',
       'ACTIVE',
       NOW();

-- Consumer Banking Account (Lucy Van Pelt)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id, opened_date, status,
                                       status_update_date_time)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Lucy Van Pelt Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT consumer_banking_product_id FROM consumer_banking.products WHERE product_type = 'CHECKING' LIMIT 1),
       NOW() - INTERVAL '7 months',
       'ACTIVE',
       NOW();

-- Consumer Banking Account (Linus Van Pelt)
INSERT INTO consumer_banking.accounts (enterprise_account_id, consumer_banking_product_id, opened_date, status,
                                       status_update_date_time)
SELECT (SELECT enterprise_account_id
        FROM enterprise.accounts
        WHERE description = 'Linus Van Pelt Main Account'
        ORDER BY enterprise_account_id DESC
        LIMIT 1),
       (SELECT consumer_banking_product_id FROM consumer_banking.products WHERE product_type = 'CHECKING' LIMIT 1),
       NOW() - INTERVAL '5 months',
       'ACTIVE',
       NOW();

-- Transactions (Varied GUARDIANs, amounts, and times)
INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency, category,
                                           transaction_type)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Charlie Brown Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-02-10T11:00:00Z',
       '2023-02-10T11:00:00Z',
       'Online Transfer to Lucy',
       500.00,
       'USD',
       'Cash',
       'Other';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency, category,
                                           transaction_type)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Lucy Van Pelt Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'CR',
       'booked',
       '2023-02-10T11:15:00Z',
       '2023-02-10T11:15:00Z',
       'Online Transfer',
       500.00,
       'USD',
       'Cash',
       'Other';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency, category,
                                           transaction_type)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Lucy Van Pelt Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-02-11T10:00:00Z',
       '2023-02-11T10:00:00Z',
       'Purchase - Department Store',
       450.00,
       'USD',
       'Cash',
       'Other';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency, category,
                                           transaction_type)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Charlie Brown Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-03-05T15:30:00Z',
       '2023-03-05T15:30:00Z',
       'Check #456 to Linus',
       1000.00,
       'USD',
       'Cash',
       'Other';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency, category,
                                           transaction_type)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Linus Van Pelt Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'CR',
       'booked',
       '2023-03-08T09:00:00Z',
       '2023-03-08T09:00:00Z',
       'Deposit - Check',
       1000.00,
       'USD',
       'Cash',
       'Other';

INSERT INTO consumer_banking.transactions (consumer_banking_account_id, credit_debit_indicator, status,
                                           transaction_date, value_date, description, amount, currency, category,
                                           transaction_type)
SELECT (SELECT consumer_banking_account_id
        FROM consumer_banking.accounts
                 JOIN enterprise.accounts
                      ON consumer_banking.accounts.enterprise_account_id = enterprise.accounts.enterprise_account_id
        WHERE enterprise.accounts.description = 'Linus Van Pelt Main Account'
        ORDER BY consumer_banking_account_id DESC
        LIMIT 1),
       'DR',
       'booked',
       '2023-03-10T14:00:00Z',
       '2023-03-10T14:00:00Z',
       'Online Transfer - Personal Account',
       900.00,
       'USD',
       'Cash',
       'Other';

COMMIT; -- Complete the transaction
