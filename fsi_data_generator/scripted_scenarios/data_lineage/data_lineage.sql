-- =============================================
-- DATA QUALITY EXECUTIVE FOCUSED INSERTS
-- =============================================

-- API Calls representing different financial institutions accessing account data
INSERT INTO data_quality.api_calls (id, method, path, "queryParams", "requestHeaders", "calledAt")
VALUES
  ('11111111-1111-1111-1111-111111111111', 'GET', '/fdx/v4/accounts', '{"customer_id": "C12345", "include": "balances,transactions"}', '{"Authorization": "Bearer token123", "x-institution-id": "bank_of_america"}', '2025-03-01 08:30:00'),
  ('22222222-2222-2222-2222-222222222222', 'GET', '/fdx/v4/accounts', '{"customer_id": "C67890", "include": "balances,owner"}', '{"Authorization": "Bearer token456", "x-institution-id": "chase"}', '2025-03-01 09:15:00'),
  ('33333333-3333-3333-3333-333333333333', 'GET', '/fdx/v4/accounts', '{"account_id": "A12345", "include": "all"}', '{"Authorization": "Bearer token789", "x-institution-id": "fidelity"}', '2025-03-01 10:30:00'),
  ('44444444-4444-4444-4444-444444444444', 'GET', '/fdx/v4/accounts', '{"customer_id": "C45678", "include": "balances,transactions"}', '{"Authorization": "Bearer tokenABC", "x-institution-id": "wellsfargo"}', '2025-03-02 08:45:00'),
  ('55555555-5555-5555-5555-555555555555', 'GET', '/fdx/v4/accounts', '{"customer_id": "C12345", "include": "balances"}', '{"Authorization": "Bearer tokenDEF", "x-institution-id": "bank_of_america"}', '2025-03-02 14:20:00');

-- Record transformations showing different transformation patterns
INSERT INTO data_quality.record_transformations (id, "inputType", "outputType", description, "primaryKeyNames", "primaryKeyValues", "executedAt", "apiCallId")
VALUES
  ('a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1', 'FDX_ACCOUNT', 'INTERNAL_ACCOUNT', 'Standard account data transformation', 'account_id', 'A12345', '2025-03-01 08:30:05', '11111111-1111-1111-1111-111111111111'),
  ('b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1', 'FDX_ACCOUNT', 'INTERNAL_ACCOUNT', 'Account transformation with balance normalization', 'account_id', 'A67890', '2025-03-01 09:15:10', '22222222-2222-2222-2222-222222222222'),
  ('c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1', 'FDX_ACCOUNT', 'INTERNAL_ACCOUNT', 'Full account transformation with enhanced owner info', 'account_id', 'A34567', '2025-03-01 10:30:15', '33333333-3333-3333-3333-333333333333'),
  ('d1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1', 'FDX_ACCOUNT', 'INTERNAL_ACCOUNT', 'Standard account data transformation', 'account_id', 'A45678', '2025-03-02 08:45:20', '44444444-4444-4444-4444-444444444444'),
  ('e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1', 'FDX_ACCOUNT', 'INTERNAL_ACCOUNT', 'Simple balance-only transformation', 'account_id', 'A12345', '2025-03-02 14:20:25', '55555555-5555-5555-5555-555555555555');

-- Field transformation details showing specific field transformations
INSERT INTO data_quality.field_transformation_details (id, "transformDescription", "inputFieldName", "inputFieldValue", "outputFieldName", "outputFieldValue", "transformationId")
VALUES
  ('1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a', 'Format standardization', 'accountNumber', '1234567890', 'account_number', '1234567890', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'),
  ('2a2a2a2a-2a2a-2a2a-2a2a-2a2a2a2a2a2a', 'Data masking', 'accountNumber', '1234567890', 'masked_account_number', 'XXXX7890', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'),
  ('3a3a3a3a-3a3a-3a3a-3a3a-3a3a3a3a3a3a', 'Currency conversion', 'currentBalance', '1000.00 USD', 'balance_usd', '1000.00', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'),

  ('4a4a4a4a-4a4a-4a4a-4a4a-4a4a4a4a4a4a', 'Format standardization', 'accountNumber', '9876543210', 'account_number', '9876543210', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('5a5a5a5a-5a5a-5a5a-5a5a-5a5a5a5a5a5a', 'Data masking', 'accountNumber', '9876543210', 'masked_account_number', 'XXXX3210', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('6a6a6a6a-6a6a-6a6a-6a6a-6a6a6a6a6a6a', 'Currency conversion', 'currentBalance', '500.00 EUR', 'balance_usd', '540.00', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('7a7a7a7a-7a7a-7a7a-7a7a-7a7a7a7a7a7a', 'Format standardization', 'availableBalance', '450.00 EUR', 'available_balance_usd', '486.00', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),

  ('8a8a8a8a-8a8a-8a8a-8a8a-8a8a8a8a8a8a', 'PII standardization', 'ownerName', 'SMITH, JOHN', 'owner_full_name', 'John Smith', 'c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1'),
  ('9a9a9a9a-9a9a-9a9a-9a9a-9a9a9a9a9a9a', 'Address normalization', 'ownerAddress', '123 MAIN ST, APT 4, ANYTOWN, CA 90210', 'owner_address_structured', '{"street":"123 Main St","unit":"Apt 4","city":"Anytown","state":"CA","zip":"90210"}', 'c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1'),
  ('10a10a10-10a1-10a1-10a1-10a10a10a10a', 'Tax ID masking', 'taxId', '123-45-6789', 'masked_tax_id', 'XXX-XX-6789', 'c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1'),

  ('11a11a11-11a1-11a1-11a1-11a11a11a11a', 'Format standardization', 'accountNumber', '2468135790', 'account_number', '2468135790', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'),
  ('12a12a12-12a1-12a1-12a1-12a12a12a12a', 'Data masking', 'accountNumber', '2468135790', 'masked_account_number', 'XXXX5790', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'),
  ('13a13a13-13a1-13a1-13a1-13a13a13a13a', 'Format standardization', 'currentBalance', '2500.00', 'balance_usd', '2500.00', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'),

  ('14a14a14-14a1-14a1-14a1-14a14a14a14a', 'Format standardization', 'currentBalance', '1200.00', 'balance_usd', '1200.00', 'e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1'),
  ('15a15a15-15a1-15a1-15a1-15a15a15a15a', 'Format standardization', 'availableBalance', '1150.00', 'available_balance_usd', '1150.00', 'e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1');


-- =============================================
-- DATA GOVERNANCE EXECUTIVE FOCUSED INSERTS
-- =============================================

-- API lineage records showing the designed data flows
INSERT INTO data_quality.api_lineage ("apiLineageId", "serverName", "apiCall", description, "startDate", "endDate", "updatedAt")
VALUES
  ('api_lineage_1', 'fdx-gateway', 'GET /fdx/v4/accounts', 'Standard account information retrieval flow', '2024-01-01 00:00:00', NULL, '2025-01-15 10:00:00'),
  ('api_lineage_2', 'fdx-gateway', 'GET /fdx/v4/accounts/{id}', 'Individual account detail retrieval flow', '2024-01-01 00:00:00', NULL, '2025-01-15 10:05:00'),
  ('api_lineage_3', 'fdx-gateway', 'GET /fdx/v4/accounts/{id}/transactions', 'Account transaction history retrieval flow', '2024-01-01 00:00:00', NULL, '2025-01-15 10:10:00'),
  ('api_lineage_4', 'fdx-gateway', 'GET /fdx/v4/accounts/{id}/balances', 'Account balance information retrieval flow', '2024-01-01 00:00:00', NULL, '2025-01-15 10:15:00'),
  ('api_lineage_5', 'fdx-gateway', 'GET /fdx/v4/accounts/{id}/owner', 'Account owner information retrieval flow', '2024-01-01 00:00:00', NULL, '2025-01-15 10:20:00');

-- Record lineage showing designated transformation paths
INSERT INTO data_quality.record_lineage ("recordLineageId", "inputType", "outputType", description, "inputDescription", "outputDescription", "pkNames", "apiLineageId")
VALUES
  ('record_lineage_1', 'FDX_ACCOUNT', 'INTERNAL_ACCOUNT', 'Standard account data mapping', 'Raw FDX account data', 'Normalized internal account representation', 'account_id', 'api_lineage_1'),
  ('record_lineage_2', 'FDX_ACCOUNT', 'INTERNAL_ACCOUNT', 'Individual account detail mapping', 'Raw FDX account detail', 'Detailed internal account representation', 'account_id', 'api_lineage_2'),
  ('record_lineage_3', 'FDX_TRANSACTION', 'INTERNAL_TRANSACTION', 'Transaction data mapping', 'Raw FDX transaction data', 'Normalized internal transaction representation', 'transaction_id', 'api_lineage_3'),
  ('record_lineage_4', 'FDX_BALANCE', 'INTERNAL_BALANCE', 'Balance information mapping', 'Raw FDX balance data', 'Normalized internal balance representation', 'account_id', 'api_lineage_4'),
  ('record_lineage_5', 'FDX_OWNER', 'INTERNAL_CUSTOMER', 'Owner information mapping to customer record', 'Raw FDX owner data', 'Internal customer representation', 'customer_id', 'api_lineage_5');

-- Field lineage showing how fields should be transformed
INSERT INTO data_quality.field_lineage ("fieldLineageId", "fieldName", description, "inputFields", "recordLineageId")
VALUES
  ('field_lineage_1', 'account_number', 'Direct mapping of account number', 'accountNumber', 'record_lineage_1'),
  ('field_lineage_2', 'masked_account_number', 'Masked version of account number', 'accountNumber', 'record_lineage_1'),
  ('field_lineage_3', 'balance_usd', 'Standardized USD balance', 'currentBalance,currencyCode', 'record_lineage_1'),
  ('field_lineage_4', 'available_balance_usd', 'Standardized USD available balance', 'availableBalance,currencyCode', 'record_lineage_1'),

  ('field_lineage_5', 'account_number', 'Direct mapping of account number', 'accountNumber', 'record_lineage_2'),
  ('field_lineage_6', 'account_name', 'Account name or nickname', 'accountNickname,accountName', 'record_lineage_2'),
  ('field_lineage_7', 'account_type', 'Standardized account type', 'accountType,accountSubType', 'record_lineage_2'),

  ('field_lineage_8', 'transaction_id', 'Direct mapping of transaction ID', 'transactionId', 'record_lineage_3'),
  ('field_lineage_9', 'transaction_amount', 'Standardized transaction amount', 'amount,currencyCode', 'record_lineage_3'),
  ('field_lineage_10', 'transaction_date', 'Standardized transaction date', 'postingDate,transactionDate', 'record_lineage_3'),

  ('field_lineage_11', 'current_balance', 'Standardized current balance', 'currentBalance,currencyCode', 'record_lineage_4'),
  ('field_lineage_12', 'available_balance', 'Standardized available balance', 'availableBalance,currencyCode', 'record_lineage_4'),
  ('field_lineage_13', 'credit_limit', 'Credit limit if applicable', 'creditLine,creditLimit', 'record_lineage_4'),

  ('field_lineage_14', 'customer_full_name', 'Normalized customer name', 'ownerName,firstName,lastName,middleName', 'record_lineage_5'),
  ('field_lineage_15', 'customer_address', 'Structured customer address', 'ownerAddress,addressLines,city,state,postalCode,country', 'record_lineage_5'),
  ('field_lineage_16', 'customer_tax_id', 'Masked tax identifier', 'taxId,taxIdMasked', 'record_lineage_5');


-- =============================================
-- DATA ARCHITECT FOCUSED INSERTS
-- =============================================

-- Additional API calls with different patterns and usage
INSERT INTO data_quality.api_calls (id, method, path, "queryParams", "requestHeaders", "calledAt")
VALUES
  ('66666666-6666-6666-6666-666666666666', 'GET', '/fdx/v4/accounts/A12345/balances', NULL, '{"Authorization": "Bearer tokenXYZ", "x-institution-id": "fintech_startup_A"}', '2025-03-03 09:30:00'),
  ('77777777-7777-7777-7777-777777777777', 'GET', '/fdx/v4/accounts/A67890/owner', NULL, '{"Authorization": "Bearer tokenUVW", "x-institution-id": "neobank_B"}', '2025-03-03 10:45:00'),
  ('88888888-8888-8888-8888-888888888888', 'GET', '/fdx/v4/accounts/A34567/transactions', '{"startTime": "2025-02-01T00:00:00Z", "endTime": "2025-03-01T00:00:00Z"}', '{"Authorization": "Bearer tokenRST", "x-institution-id": "wealth_manager_C"}', '2025-03-03 13:15:00'),
  ('99999999-9999-9999-9999-999999999999', 'GET', '/fdx/v4/accounts', '{"customer_id": "C24680", "account_type": "CHECKING,SAVINGS", "include": "balances"}', '{"Authorization": "Bearer tokenJKL", "x-institution-id": "credit_union_D"}', '2025-03-04 11:30:00'),
  ('aaaa1234-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'GET', '/fdx/v4/accounts', '{"customer_id": "C13579", "account_status": "ACTIVE", "include": "all"}', '{"Authorization": "Bearer tokenMNO", "x-institution-id": "community_bank_E"}', '2025-03-04 14:45:00');

-- Additional record transformations with varying complexity and performance
INSERT INTO data_quality.record_transformations (id, "inputType", "outputType", description, "primaryKeyNames", "primaryKeyValues", "executedAt", "apiCallId")
VALUES
  ('f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1', 'FDX_BALANCE', 'INTERNAL_BALANCE', 'Balance data transformation with currency conversion', 'account_id', 'A12345', '2025-03-03 09:30:10', '66666666-6666-6666-6666-666666666666'),
  ('a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2', 'FDX_OWNER', 'INTERNAL_CUSTOMER', 'Customer data transformation with address normalization', 'customer_id', 'C67890', '2025-03-03 10:45:20', '77777777-7777-7777-7777-777777777777'),
  ('a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3', 'FDX_TRANSACTION', 'INTERNAL_TRANSACTION', 'Transaction data transformation with categorization', 'transaction_ids', 'T12345,T12346,T12347', '2025-03-03 13:15:30', '88888888-8888-8888-8888-888888888888'),
  ('a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4', 'FDX_ACCOUNT', 'INTERNAL_ACCOUNT', 'Multi-account transformation with balance aggregation', 'account_ids', 'A24680,A24681', '2025-03-04 11:30:40', '99999999-9999-9999-9999-999999999999'),
  ('a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5', 'FDX_ACCOUNT', 'INTERNAL_ACCOUNT', 'Complete account transformation with all related data', 'account_id', 'A13579', '2025-03-04 14:46:00', 'aaaa1234-aaaa-aaaa-aaaa-aaaaaaaaaaaa');

-- Complex field transformations for architectural analysis
INSERT INTO data_quality.field_transformation_details (id, "transformDescription", "inputFieldName", "inputFieldValue", "outputFieldName", "outputFieldValue", "transformationId")
VALUES
  -- Balance transformations
  ('20a20a20-20a1-20a1-20a1-20a20a20a20a', 'Currency conversion with rate lookup', 'ledgerBalance', '1000.00 EUR', 'ledger_balance_usd', '1080.00', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'),
  ('21a21a21-21a1-21a1-21a1-21a21a21a21a', 'Currency conversion with rate lookup', 'availableBalance', '950.00 EUR', 'available_balance_usd', '1026.00', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'),
  ('22a22a22-22a1-22a1-22a1-22a22a22a22a', 'Date format standardization', 'balanceDate', '2025-03-03T09:30:00Z', 'balance_timestamp', '2025-03-03 09:30:00', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'),

  -- Owner transformations
  ('23a23a23-23a1-23a1-23a1-23a23a23a23a', 'Name parsing and normalization', 'ownerName', 'DOE, JANE MARIE', 'customer_first_name', 'Jane', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('24a24a24-24a1-24a1-24a1-24a24a24a24a', 'Name parsing and normalization', 'ownerName', 'DOE, JANE MARIE', 'customer_middle_name', 'Marie', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('25a25a25-25a1-25a1-25a1-25a25a25a25a', 'Name parsing and normalization', 'ownerName', 'DOE, JANE MARIE', 'customer_last_name', 'Doe', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('26a26a26-26a1-26a1-26a1-26a26a26a26a', 'Address parsing and standardization', 'ownerAddress', '456 BROADWAY ST, STE 7B, NEW YORK, NY 10013', 'customer_address_street', '456 Broadway St', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('27a27a27-27a1-27a1-27a1-27a27a27a27a', 'Address parsing and standardization', 'ownerAddress', '456 BROADWAY ST, STE 7B, NEW YORK, NY 10013', 'customer_address_unit', 'Suite 7B', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('28a28a28-28a1-28a1-28a1-28a28a28a28a', 'Address parsing and standardization', 'ownerAddress', '456 BROADWAY ST, STE 7B, NEW YORK, NY 10013', 'customer_address_city', 'New York', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('29a29a29-29a1-29a1-29a1-29a29a29a29a', 'Address parsing and standardization', 'ownerAddress', '456 BROADWAY ST, STE 7B, NEW YORK, NY 10013', 'customer_address_state', 'NY', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('30a30a30-30a1-30a1-30a1-30a30a30a30a', 'Address parsing and standardization', 'ownerAddress', '456 BROADWAY ST, STE 7B, NEW YORK, NY 10013', 'customer_address_zip', '10013', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),

  -- Transaction transformations
  ('31a31a31-31a1-31a1-31a1-31a31a31a31a', 'Transaction categorization', 'description', 'WHOLEFDS NYC 10010', 'transaction_category', 'GROCERY', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('32a32a32-32a1-32a1-32a1-32a32a32a32a', 'Transaction categorization', 'description', 'AMAZONPRIME', 'transaction_category', 'SUBSCRIPTION', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('33a33a33-33a1-33a1-33a1-33a33a33a33a', 'Transaction categorization', 'description', 'UBER TRIP', 'transaction_category', 'TRANSPORTATION', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('34a34a34-34a1-34a1-34a1-34a34a34a34a', 'Amount sign standardization', 'amount', '-25.00', 'transaction_amount', '25.00', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('35a35a35-35a1-35a1-35a1-35a35a35a35a', 'Transaction type determination', 'amount', '-25.00', 'transaction_type', 'DEBIT', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),

  -- Multi-account aggregation
  ('36a36a36-36a1-36a1-36a1-36a36a36a36a', 'Account balances aggregation', 'currentBalance', '[1500.00, 2500.00]', 'total_balance', '4000.00', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('37a37a37-37a1-37a1-37a1-37a37a37a37a', 'Account available balances aggregation', 'availableBalance', '[1450.00, 2400.00]', 'total_available_balance', '3850.00', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('38a38a38-38a1-38a1-38a1-38a38a38a38a', 'Account type grouping', 'accountType', '["CHECKING", "SAVINGS"]', 'account_group', 'DEPOSIT', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),

  -- Complete account transformation
  ('39a39a39-39a1-39a1-39a1-39a39a39a39a', 'Account data consolidation', 'accountNumber,accountType,status', '13579,INVESTMENT,ACTIVE', 'account_summary', '{"number":"13579","type":"Investment","status":"Active"}', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('40a40a40-40a1-40a1-40a1-40a40a40a40a', 'Balance data consolidation', 'currentBalance,availableBalance,pendingBalance', '35000.00,35000.00,0.00', 'balance_summary', '{"current":35000.00,"available":35000.00,"pending":0.00}', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('41a41a41-41a1-41a1-41a1-41a41a41a41a', 'Owner data consolidation', 'ownerName,ownerAddress,ownerEmail,ownerPhone', 'SMITH, ROBERT J,789 PARK AVE...,robert.smith@example.com,212-555-1234', 'owner_summary', '{"name":"Robert J Smith","contact":{"email":"robert.smith@example.com","phone":"212-555-1234"}}', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5');


-- =============================================
-- CHIEF MARKETING OFFICER (CMO) FOCUSED INSERTS
-- =============================================

-- API calls with various institution types and patterns
INSERT INTO data_quality.api_calls (id, method, path, "queryParams", "requestHeaders", "calledAt")
VALUES
  ('bbbb0000-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'GET', '/fdx/v4/accounts', '{"customer_id": "C54321", "include": "balances,transactions,owner"}', '{"Authorization": "Bearer tokenPQR", "x-institution-id": "fintech_wealth_advisor"}', '2025-03-05 09:00:00'),
  ('cccc0000-cccc-cccc-cccc-cccccccccccc', 'GET', '/fdx/v4/accounts', '{"customer_id": "C97531", "include": "balances,owner"}', '{"Authorization": "Bearer tokenSTU", "x-institution-id": "digital_lending_platform"}', '2025-03-05 11:30:00'),
  ('dddd0000-dddd-dddd-dddd-dddddddddddd', 'GET', '/fdx/v4/accounts', '{"customer_id": "C86420", "include": "balances,transactions"}', '{"Authorization": "Bearer tokenVWX", "x-institution-id": "personal_finance_app"}', '2025-03-06 10:15:00'),
  ('eeee0000-eeee-eeee-eeee-eeeeeeeeeeee', 'GET', '/fdx/v4/accounts/A54321/transactions', '{"startTime": "2025-01-01T00:00:00Z", "endTime": "2025-03-01T00:00:00Z", "type": "DEBIT,CREDIT"}', '{"Authorization": "Bearer tokenYZA", "x-institution-id": "enterprise_accounting_system"}', '2025-03-06 13:45:00'),
  ('ffff0000-ffff-ffff-ffff-ffffffffffff', 'GET', '/fdx/v4/accounts/A97531/owner', NULL, '{"Authorization": "Bearer tokenBCD", "x-institution-id": "credit_building_app"}', '2025-03-07 09:30:00');

-- Record transformations showing customer usage patterns
INSERT INTO data_quality.record_transformations (id, "inputType", "outputType", description, "primaryKeyNames", "primaryKeyValues", "executedAt", "apiCallId")
VALUES
  ('a6a6a6a6-a6a6-a6a6-a6a6-a6a6a6a6a6a6', 'FDX_ACCOUNT', 'WEALTH_PORTFOLIO', 'Transformation for wealth management aggregation', 'account_id', 'A54321', '2025-03-05 09:00:10', 'bbbb0000-bbbb-bbbb-bbbb-bbbbbbbbbbbb'),
  ('a7a7a7a7-a7a7-a7a7-a7a7-a7a7a7a7a7a7', 'FDX_ACCOUNT', 'LOAN_APPLICATION', 'Transformation for lending qualification', 'customer_id,account_id', 'C97531,A97531', '2025-03-05 11:30:20', 'cccc0000-cccc-cccc-cccc-cccccccccccc'),
  ('a8a8a8a8-a8a8-a8a8-a8a8-a8a8a8a8a8a8', 'FDX_ACCOUNT', 'BUDGET_TRACKER', 'Transformation for personal finance tracking', 'customer_id,account_id', 'C86420,A86420', '2025-03-06 10:15:30', 'dddd0000-dddd-dddd-dddd-dddddddddddd'),
  ('a9a9a9a9-a9a9-a9a9-a9a9-a9a9a9a9a9a9', 'FDX_TRANSACTION', 'ACCOUNTING_ENTRY', 'Transformation for enterprise accounting system', 'transaction_ids', 'T54321,T54322,T54323', '2025-03-06 13:45:40', 'eeee0000-eeee-eeee-eeee-eeeeeeeeeeee'),
  ('aaaa0000-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'FDX_OWNER', 'CREDIT_PROFILE', 'Transformation for credit assessment', 'customer_id', 'C97531', '2025-03-07 09:30:50', 'ffff0000-ffff-ffff-ffff-ffffffffffff');

-- Field transformations showing customer value-add processing
INSERT INTO data_quality.field_transformation_details (id, "transformDescription", "inputFieldName", "inputFieldValue", "outputFieldName", "outputFieldValue", "transformationId")
VALUES
  -- Wealth management transformations
  ('50a50a50-50a1-50a1-50a1-50a50a50a50a', 'Asset classification', 'accountType,investmentData', 'INVESTMENT,{...}', 'asset_class', 'EQUITY', 'a6a6a6a6-a6a6-a6a6-a6a6-a6a6a6a6a6a6'),
  ('51a51a51-51a1-51a1-51a1-51a51a51a51a', 'Risk profile calculation', 'investmentData,transactionHistory', '{...},{...}', 'risk_score', '65', 'a6a6a6a6-a6a6-a6a6-a6a6-a6a6a6a6a6a6'),
  ('52a52a52-52a1-52a1-52a1-52a52a52a52a', 'Portfolio diversification analysis', 'investmentData,balances', '{...},{...}', 'diversification_index', '0.72', 'a6a6a6a6-a6a6-a6a6-a6a6-a6a6a6a6a6a6'),

  -- Lending qualification transformations
  ('53a53a53-53a1-53a1-53a1-53a53a53a53a', 'Income estimation', 'transactionHistory,accountType', '{...},CHECKING', 'estimated_monthly_income', '5200.00', 'a7a7a7a7-a7a7-a7a7-a7a7-a7a7a7a7a7a7'),
  ('54a54a54-54a1-54a1-54a1-54a54a54a54a', 'Expense pattern analysis', 'transactionHistory', '{...}', 'expense_stability_score', '85', 'a7a7a7a7-a7a7-a7a7-a7a7-a7a7a7a7a7a7'),
  ('55a55a55-55a1-55a1-55a1-55a55a55a55a', 'Debt calculation', 'balances,accountType', '{...},CREDIT_CARD', 'current_debt_load', '12500.00', 'a7a7a7a7-a7a7-a7a7-a7a7-a7a7a7a7a7a7'),

  -- Personal finance tracking transformations
  ('56a56a56-56a1-56a1-56a1-56a56a56a56a', 'Transaction categorization', 'transactionHistory', '{...}', 'spending_categories', '{"dining":450.00,"transportation":200.00,"groceries":650.00,...}', 'a8a8a8a8-a8a8-a8a8-a8a8-a8a8a8a8a8a8'),
  ('57a57a57-57a1-57a1-57a1-57a57a57a57a', 'Budget comparison', 'transactionHistory,userBudgets', '{...},{...}', 'budget_adherence', '{"dining":0.9,"transportation":1.1,"groceries":1.0,...}', 'a8a8a8a8-a8a8-a8a8-a8a8-a8a8a8a8a8a8'),
  ('58a58a58-58a1-58a1-58a1-58a58a58a58a', 'Savings opportunity identification', 'transactionHistory,balances', '{...},{...}', 'savings_opportunities', '["Reduce dining out","Consolidate subscriptions"]', 'a8a8a8a8-a8a8-a8a8-a8a8-a8a8a8a8a8a8'),

  -- Accounting system transformations
  ('59a59a59-59a1-59a1-59a1-59a59a59a59a', 'GL account mapping', 'description,amount,type', 'OFFICE SUPPLY VENDOR,-125.45,DEBIT', 'gl_account_entry', '{"account":"5001-ExpenseOfficeSupplies","amount":125.45,"type":"debit"}', 'a9a9a9a9-a9a9-a9a9-a9a9-a9a9a9a9a9a9'),
  ('60a60a60-60a1-60a1-60a1-60a60a60a60a', 'Tax classification', 'description,amount,merchantData', 'BUSINESS TRAVEL AIRLINE,-534.90,{...}', 'tax_category', 'BUSINESS_TRAVEL_DEDUCTIBLE', 'a9a9a9a9-a9a9-a9a9-a9a9-a9a9a9a9a9a9'),
  ('61a61a61-61a1-61a1-61a1-61a61a61a61a', 'Receipt matching', 'description,amount,transactionDate', 'OFFICE SUPPLY VENDOR,-125.45,2025-02-15', 'receipt_match_id', 'REC12345', 'a9a9a9a9-a9a9-a9a9-a9a9-a9a9a9a9a9a9'),

  -- Credit assessment transformations
  ('62a62a62-62a1-62a1-62a1-62a62a62a62a', 'Payment history analysis', 'transactionHistory,dueDate,paymentDate', '{...},2025-01-15,2025-01-14', 'payment_reliability_score', '95', 'aaaa0000-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
  ('63a63a63-63a1-63a1-63a1-63a63a63a63a', 'Credit utilization calculation', 'currentBalance,creditLimit', '3500.00,10000.00', 'credit_utilization_ratio', '0.35', 'aaaa0000-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
  ('64a64a64-64a1-64a1-64a1-64a64a64a64a', 'Income stability assessment', 'transactionHistory,depositPatterns', '{...},{...}', 'income_stability_score', '88', 'aaaa0000-aaaa-aaaa-aaaa-aaaaaaaaaaaa');
