-- =============================================
-- DATA QUALITY EXECUTIVE FOCUSED INSERTS
-- =============================================

-- API Calls representing different financial institutions accessing account data with version information
INSERT INTO data_quality.api_calls (id, method, path, "queryParams", "requestHeaders", "calledAt")
VALUES
  -- Early adopters of v1.1 while v1.0 still available
  ('11111111-1111-1111-1111-111111111111', 'GET', '/fdx/v4/accounts', '{"customer_id": "C12345", "include": "balances,transactions", "version": "1.1"}', '{"Authorization": "Bearer token123", "x-consumer-id": "bank_of_america", "x-api-version": "1.1"}', '2024-03-15 08:30:00'),
  ('22222222-2222-2222-2222-222222222222', 'GET', '/fdx/v4/accounts', '{"customer_id": "C67890", "include": "balances,owner", "version": "1.1"}', '{"Authorization": "Bearer token456", "x-consumer-id": "chase", "x-api-version": "1.1"}', '2024-03-25 09:15:00'),

  -- Late adopters still using v1.0 near end of lifecycle
  ('33333333-3333-3333-3333-333333333333', 'GET', '/fdx/v4/accounts', '{"account_id": "A12345", "include": "all", "version": "1.0"}', '{"Authorization": "Bearer token789", "x-consumer-id": "fidelity", "x-api-version": "1.0"}', '2024-06-20 10:30:00'),

  -- Early adopters of v2.0 while v1.1 still available
  ('44444444-4444-4444-4444-444444444444', 'GET', '/fdx/v4/accounts', '{"customer_id": "C45678", "include": "balances,transactions", "version": "2.0"}', '{"Authorization": "Bearer tokenABC", "x-consumer-id": "wellsfargo", "x-api-version": "2.0"}', '2024-06-15 08:45:00'),

  -- Late adopters still using v1.1 near end of lifecycle
  ('55555555-5555-5555-5555-555555555555', 'GET', '/fdx/v4/accounts', '{"customer_id": "C12345", "include": "balances", "version": "1.1"}', '{"Authorization": "Bearer tokenDEF", "x-consumer-id": "regional_bank_A", "x-api-version": "1.1"}', '2024-09-25 14:20:00'),

  -- Early adopters of v2.1 while v2.0 still available
  ('66666666-6666-6666-6666-666666666666', 'GET', '/fdx/v4/accounts/A12345/balances', '{"version": "2.1"}', '{"Authorization": "Bearer tokenXYZ", "x-consumer-id": "fintech_startup_A", "x-api-version": "2.1"}', '2024-09-15 09:30:00'),

  -- Late adopters still using v2.0 near end of lifecycle
  ('77777777-7777-7777-7777-777777777777', 'GET', '/fdx/v4/accounts/A67890/owner', '{"version": "2.0"}', '{"Authorization": "Bearer tokenUVW", "x-consumer-id": "neobank_B", "x-api-version": "2.0"}', '2024-12-15 10:45:00'),

  -- Early adopters of v3.0 while v2.1 still available
  ('88888888-8888-8888-8888-888888888888', 'GET', '/fdx/v4/accounts/A34567/transactions', '{"startTime": "2025-02-01T00:00:00Z", "endTime": "2025-03-01T00:00:00Z", "version": "3.0"}', '{"Authorization": "Bearer tokenRST", "x-consumer-id": "wealth_manager_C", "x-api-version": "3.0"}', '2025-01-20 13:15:00'),

  -- Late adopters still using v2.1 near end of lifecycle
  ('99999999-9999-9999-9999-999999999999', 'GET', '/fdx/v4/accounts', '{"customer_id": "C24680", "account_type": "CHECKING,SAVINGS", "include": "balances", "version": "2.1"}', '{"Authorization": "Bearer tokenJKL", "x-consumer-id": "credit_union_D", "x-api-version": "2.1"}', '2025-03-15 11:30:00'),

  -- Latest version adoption
  ('aaaa1234-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'GET', '/fdx/v4/accounts', '{"customer_id": "C13579", "account_status": "ACTIVE", "include": "all", "version": "3.0"}', '{"Authorization": "Bearer tokenMNO", "x-consumer-id": "community_bank_E", "x-api-version": "3.0"}', '2025-02-25 14:45:00'),

  -- Additional API calls to show adoption patterns
  ('bbbb0000-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'GET', '/fdx/v4/accounts', '{"customer_id": "C54321", "include": "balances,transactions,owner", "version": "3.0"}', '{"Authorization": "Bearer tokenPQR", "x-consumer-id": "fintech_wealth_advisor", "x-api-version": "3.0"}', '2025-02-01 09:00:00'),
  ('cccc0000-cccc-cccc-cccc-cccccccccccc', 'GET', '/fdx/v4/accounts', '{"customer_id": "C97531", "include": "balances,owner", "version": "2.1"}', '{"Authorization": "Bearer tokenSTU", "x-consumer-id": "digital_lending_platform", "x-api-version": "2.1"}', '2025-02-28 11:30:00'),
  ('dddd0000-dddd-dddd-dddd-dddddddddddd', 'GET', '/fdx/v4/accounts', '{"customer_id": "C86420", "include": "balances,transactions", "version": "3.0"}', '{"Authorization": "Bearer tokenVWX", "x-consumer-id": "personal_finance_app", "x-api-version": "3.0"}', '2025-03-10 10:15:00'),
  ('eeee0000-eeee-eeee-eeee-eeeeeeeeeeee', 'GET', '/fdx/v4/accounts/A54321/transactions', '{"startTime": "2025-01-01T00:00:00Z", "endTime": "2025-03-01T00:00:00Z", "type": "DEBIT,CREDIT", "version": "2.1"}', '{"Authorization": "Bearer tokenYZA", "x-consumer-id": "enterprise_accounting_system", "x-api-version": "2.1"}', '2025-03-20 13:45:00'),
  ('ffff0000-ffff-ffff-ffff-ffffffffffff', 'GET', '/fdx/v4/accounts/A97531/owner', '{"version": "3.0"}', '{"Authorization": "Bearer tokenBCD", "x-consumer-id": "credit_building_app", "x-api-version": "3.0"}', '2025-03-25 09:30:00');

-- Record transformations showing different transformation patterns
INSERT INTO data_quality.record_transformations (id, "inputType", "outputType", description, "primaryKeyNames", "primaryKeyValues", "executedAt", "apiCallId")
VALUES
  ('a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1', 'INTERNAL_ACCOUNT', 'FDX_ACCOUNT', 'Standard account data transformation to FDX format', 'account_id', 'A12345', '2025-03-01 08:30:05', '11111111-1111-1111-1111-111111111111'),
  ('b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1', 'INTERNAL_ACCOUNT', 'FDX_ACCOUNT', 'Account transformation with balance normalization to FDX format', 'account_id', 'A67890', '2025-03-01 09:15:10', '22222222-2222-2222-2222-222222222222'),
  ('c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1', 'INTERNAL_ACCOUNT', 'FDX_ACCOUNT', 'Full account transformation with enhanced owner info to FDX format', 'account_id', 'A34567', '2025-03-01 10:30:15', '33333333-3333-3333-3333-333333333333'),
  ('d1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1', 'INTERNAL_ACCOUNT', 'FDX_ACCOUNT', 'Standard account data transformation to FDX format', 'account_id', 'A45678', '2025-03-02 08:45:20', '44444444-4444-4444-4444-444444444444'),
  ('e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1', 'INTERNAL_ACCOUNT', 'FDX_ACCOUNT', 'Simple balance-only transformation to FDX format', 'account_id', 'A12345', '2025-03-02 14:20:25', '55555555-5555-5555-5555-555555555555');

-- Field transformation details showing specific field transformations
INSERT INTO data_quality.field_transformation_details (id, "transformDescription", "inputFieldName", "inputFieldValue", "outputFieldName", "outputFieldValue", "transformationId")
VALUES
  ('1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a', 'Format standardization to FDX', 'account_number', '1234567890', 'accountNumber', '1234567890', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'),
  ('2a2a2a2a-2a2a-2a2a-2a2a-2a2a2a2a2a2a', 'Data masking for FDX exposure', 'masked_account_number', 'XXXX7890', 'maskedAccountNumber', 'XXXX7890', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'),
  ('3a3a3a3a-3a3a-3a3a-3a3a-3a3a3a3a3a3a', 'Currency conversion to FDX format', 'balance_usd', '1000.00', 'currentBalance', '1000.00', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'),
  ('3b3b3b3b-3b3b-3b3b-3b3b-3b3b3b3b3b3b', 'Currency code for FDX format', 'currency_code', 'USD', 'currencyCode', 'USD', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'),

  ('4a4a4a4a-4a4a-4a4a-4a4a-4a4a4a4a4a4a', 'Format standardization to FDX', 'account_number', '9876543210', 'accountNumber', '9876543210', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('5a5a5a5a-5a5a-5a5a-5a5a-5a5a5a5a5a5a', 'Data masking for FDX exposure', 'masked_account_number', 'XXXX3210', 'maskedAccountNumber', 'XXXX3210', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('6a6a6a6a-6a6a-6a6a-6a6a-6a6a6a6a6a6a', 'Currency conversion to FDX format', 'balance_eur', '500.00', 'currentBalance', '500.00', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('6b6b6b6b-6b6b-6b6b-6b6b-6b6b6b6b6b6b', 'Currency code for FDX format', 'currency_code', 'EUR', 'currencyCode', 'EUR', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('7a7a7a7a-7a7a-7a7a-7a7a-7a7a7a7a7a7a', 'Format standardization to FDX', 'available_balance_eur', '450.00', 'availableBalance', '450.00', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),

  ('8a8a8a8a-8a8a-8a8a-8a8a-8a8a8a8a8a8a', 'PII standardization to FDX', 'customer_full_name', 'John Smith', 'ownerName', 'SMITH, JOHN', 'c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1'),
  ('9a9a9a9a-9a9a-9a9a-9a9a-9a9a9a9a9a9a', 'Address normalization to FDX', 'customer_address_structured', '{"street":"123 Main St","unit":"Apt 4","city":"Anytown","state":"CA","zip":"90210"}', 'ownerAddress', '123 MAIN ST, APT 4, ANYTOWN, CA 90210', 'c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1'),
  ('10a10a10-10a1-10a1-10a1-10a10a10a10a', 'Tax ID masking for FDX exposure', 'customer_tax_id', 'XXX-XX-6789', 'taxIdMasked', '123-45-6789', 'c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1'),

  ('11a11a11-11a1-11a1-11a1-11a11a11a11a', 'Format standardization to FDX', 'account_number', '2468135790', 'accountNumber', '2468135790', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'),
  ('12a12a12-12a1-12a1-12a1-12a12a12a12a', 'Data masking for FDX exposure', 'masked_account_number', 'XXXX5790', 'maskedAccountNumber', 'XXXX5790', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'),
  ('13a13a13-13a1-13a1-13a1-13a13a13a13a', 'Format standardization to FDX', 'balance_usd', '2500.00', 'currentBalance', '2500.00', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'),
  ('13b13b13-13b1-13b1-13b1-13b13b13b13b', 'Currency code for FDX format', 'currency_code', 'USD', 'currencyCode', 'USD', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'),

  ('14a14a14-14a1-14a1-14a1-14a14a14a14a', 'Format standardization to FDX', 'balance_usd', '1200.00', 'currentBalance', '1200.00', 'e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1'),
  ('14b14b14-14b1-14b1-14b1-14b14b14b14b', 'Currency code for FDX format', 'currency_code', 'USD', 'currencyCode', 'USD', 'e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1'),
  ('15a15a15-15a1-15a1-15a1-15a15a15a15a', 'Format standardization to FDX', 'available_balance_usd', '1150.00', 'availableBalance', '1150.00', 'e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1');


-- =============================================
-- DATA GOVERNANCE EXECUTIVE FOCUSED INSERTS
-- =============================================

-- API lineage records showing the designed data flows and their evolution over time with realistic overlapping versions
INSERT INTO data_quality.api_lineage ("apiLineageId", "serverName", "apiCall", description, "startDate", "endDate", "updatedAt")
VALUES
  -- Version 1.0 API lineage (original implementation)
  ('api_lineage_1_v1', 'fdx-gateway', 'GET /fdx/v4/accounts', 'Standard account information delivery flow', '2024-01-01 00:00:00', '2024-06-30 23:59:59', '2024-01-01 10:00:00'),
  ('api_lineage_2_v1', 'fdx-gateway', 'GET /fdx/v4/accounts/{id}', 'Individual account detail delivery flow', '2024-01-01 00:00:00', '2024-06-30 23:59:59', '2024-01-01 10:05:00'),
  ('api_lineage_3_v1', 'fdx-gateway', 'GET /fdx/v4/accounts/{id}/transactions', 'Account transaction history delivery flow', '2024-01-01 00:00:00', '2024-06-30 23:59:59', '2024-01-01 10:10:00'),

  -- Version 1.1 API lineage (added fields for compliance) - note overlapping with v1.0 for 3 months
  ('api_lineage_1_v1.1', 'fdx-gateway', 'GET /fdx/v4/accounts', 'Standard account information delivery flow with added compliance fields', '2024-03-01 00:00:00', '2024-09-30 23:59:59', '2024-03-01 09:00:00'),
  ('api_lineage_2_v1.1', 'fdx-gateway', 'GET /fdx/v4/accounts/{id}', 'Individual account detail delivery flow with added compliance fields', '2024-03-01 00:00:00', '2024-09-30 23:59:59', '2024-03-01 09:05:00'),
  ('api_lineage_3_v1.1', 'fdx-gateway', 'GET /fdx/v4/accounts/{id}/transactions', 'Account transaction history delivery flow with added compliance fields', '2024-03-01 00:00:00', '2024-09-30 23:59:59', '2024-03-01 09:10:00'),

  -- Version 2.0 API lineage (major revision with enhanced security) - note overlapping with v1.1 for 3 months
  ('api_lineage_1_v2', 'fdx-gateway-v2', 'GET /fdx/v4/accounts', 'Enhanced security account information delivery flow', '2024-06-01 00:00:00', '2024-12-31 23:59:59', '2024-06-01 08:30:00'),
  ('api_lineage_2_v2', 'fdx-gateway-v2', 'GET /fdx/v4/accounts/{id}', 'Enhanced security account detail delivery flow', '2024-06-01 00:00:00', '2024-12-31 23:59:59', '2024-06-01 08:35:00'),
  ('api_lineage_3_v2', 'fdx-gateway-v2', 'GET /fdx/v4/accounts/{id}/transactions', 'Enhanced security transaction history delivery flow', '2024-06-01 00:00:00', '2024-12-31 23:59:59', '2024-06-01 08:40:00'),
  ('api_lineage_4_v2', 'fdx-gateway-v2', 'GET /fdx/v4/accounts/{id}/balances', 'Enhanced security balance information delivery flow', '2024-06-01 00:00:00', '2024-12-31 23:59:59', '2024-06-01 08:45:00'),

  -- Version 2.1 API lineage (added owner endpoint and performance improvements) - note overlapping with v2.0 for 3 months
  ('api_lineage_1_v2.1', 'fdx-gateway-v2', 'GET /fdx/v4/accounts', 'Performance optimized account information delivery flow', '2024-09-01 00:00:00', '2025-03-31 23:59:59', '2024-09-01 11:30:00'),
  ('api_lineage_2_v2.1', 'fdx-gateway-v2', 'GET /fdx/v4/accounts/{id}', 'Performance optimized account detail delivery flow', '2024-09-01 00:00:00', '2025-03-31 23:59:59', '2024-09-01 11:35:00'),
  ('api_lineage_3_v2.1', 'fdx-gateway-v2', 'GET /fdx/v4/accounts/{id}/transactions', 'Performance optimized transaction history delivery flow', '2024-09-01 00:00:00', '2025-03-31 23:59:59', '2024-09-01 11:40:00'),
  ('api_lineage_4_v2.1', 'fdx-gateway-v2', 'GET /fdx/v4/accounts/{id}/balances', 'Performance optimized balance information delivery flow', '2024-09-01 00:00:00', '2025-03-31 23:59:59', '2024-09-01 11:45:00'),
  ('api_lineage_5_v2.1', 'fdx-gateway-v2', 'GET /fdx/v4/accounts/{id}/owner', 'New owner information delivery flow', '2024-09-01 00:00:00', '2025-03-31 23:59:59', '2024-09-01 11:50:00'),

  -- Current Version 3.0 API lineage (FDX 5.0 compliance) - note overlapping with v2.1 for 3 months
  ('api_lineage_1', 'fdx-gateway-v3', 'GET /fdx/v4/accounts', 'FDX 5.0 compliant account information delivery flow', '2025-01-01 00:00:00', NULL, '2025-01-15 10:00:00'),
  ('api_lineage_2', 'fdx-gateway-v3', 'GET /fdx/v4/accounts/{id}', 'FDX 5.0 compliant account detail delivery flow', '2025-01-01 00:00:00', NULL, '2025-01-15 10:05:00'),
  ('api_lineage_3', 'fdx-gateway-v3', 'GET /fdx/v4/accounts/{id}/transactions', 'FDX 5.0 compliant transaction history delivery flow', '2025-01-01 00:00:00', NULL, '2025-01-15 10:10:00'),
  ('api_lineage_4', 'fdx-gateway-v3', 'GET /fdx/v4/accounts/{id}/balances', 'FDX 5.0 compliant balance information delivery flow', '2025-01-01 00:00:00', NULL, '2025-01-15 10:15:00'),
  ('api_lineage_5', 'fdx-gateway-v3', 'GET /fdx/v4/accounts/{id}/owner', 'FDX 5.0 compliant owner information delivery flow', '2025-01-01 00:00:00', NULL, '2025-01-15 10:20:00');

-- Record lineage showing designated transformation paths with temporal evolution
INSERT INTO data_quality.record_lineage ("recordLineageId", "inputType", "outputType", description, "inputDescription", "outputDescription", "pkNames", "apiLineageId")
VALUES
  -- Initial version 1.0 record lineage mappings
  ('record_lineage_1_v1', 'INTERNAL_ACCOUNT_v1', 'FDX_ACCOUNT_v1', 'Initial account data mapping', 'Internal bank account data', 'FDX 4.0 formatted account representation', 'account_id', 'api_lineage_1_v1'),
  ('record_lineage_2_v1', 'INTERNAL_ACCOUNT_v1', 'FDX_ACCOUNT_v1', 'Initial account detail mapping', 'Internal account detail data', 'FDX 4.0 formatted account detail representation', 'account_id', 'api_lineage_2_v1'),
  ('record_lineage_3_v1', 'INTERNAL_TRANSACTION_v1', 'FDX_TRANSACTION_v1', 'Initial transaction data mapping', 'Internal transaction data', 'FDX 4.0 formatted transaction representation', 'transaction_id', 'api_lineage_3_v1'),

  -- Version 1.1 record lineage mappings (added compliance fields)
  ('record_lineage_1_v1.1', 'INTERNAL_ACCOUNT_v1.1', 'FDX_ACCOUNT_v1', 'Account data mapping with compliance fields', 'Internal account data with compliance fields', 'FDX 4.0 formatted account representation', 'account_id', 'api_lineage_1_v1.1'),
  ('record_lineage_2_v1.1', 'INTERNAL_ACCOUNT_v1.1', 'FDX_ACCOUNT_v1', 'Account detail mapping with compliance fields', 'Internal account detail with compliance fields', 'FDX 4.0 formatted account detail representation', 'account_id', 'api_lineage_2_v1.1'),
  ('record_lineage_3_v1.1', 'INTERNAL_TRANSACTION_v1.1', 'FDX_TRANSACTION_v1', 'Transaction data mapping with compliance fields', 'Internal transaction data with compliance fields', 'FDX 4.0 formatted transaction representation', 'transaction_id', 'api_lineage_3_v1.1'),

  -- Version 2.0 record lineage mappings (enhanced security)
  ('record_lineage_1_v2', 'INTERNAL_ACCOUNT_v2', 'FDX_ACCOUNT_v1', 'Account data mapping with enhanced security', 'Internal account data with security enhancements', 'FDX 4.0 formatted account representation', 'account_id', 'api_lineage_1_v2'),
  ('record_lineage_2_v2', 'INTERNAL_ACCOUNT_v2', 'FDX_ACCOUNT_v1', 'Account detail mapping with enhanced security', 'Internal account detail with security enhancements', 'FDX 4.0 formatted account detail representation', 'account_id', 'api_lineage_2_v2'),
  ('record_lineage_3_v2', 'INTERNAL_TRANSACTION_v2', 'FDX_TRANSACTION_v1', 'Transaction data mapping with enhanced security', 'Internal transaction data with security enhancements', 'FDX 4.0 formatted transaction representation', 'transaction_id', 'api_lineage_3_v2'),
  ('record_lineage_4_v2', 'INTERNAL_BALANCE_v2', 'FDX_BALANCE_v1', 'Balance information mapping with enhanced security', 'Internal balance data with security enhancements', 'FDX 4.0 formatted balance representation', 'account_id', 'api_lineage_4_v2'),

  -- Version 2.1 record lineage mappings (performance improvements and new owner endpoint)
  ('record_lineage_1_v2.1', 'INTERNAL_ACCOUNT_v2.1', 'FDX_ACCOUNT_v1', 'Performance-optimized account data mapping', 'Optimized internal account data', 'FDX 4.0 formatted account representation', 'account_id', 'api_lineage_1_v2.1'),
  ('record_lineage_2_v2.1', 'INTERNAL_ACCOUNT_v2.1', 'FDX_ACCOUNT_v1', 'Performance-optimized account detail mapping', 'Optimized internal account detail', 'FDX 4.0 formatted account detail representation', 'account_id', 'api_lineage_2_v2.1'),
  ('record_lineage_3_v2.1', 'INTERNAL_TRANSACTION_v2.1', 'FDX_TRANSACTION_v1', 'Performance-optimized transaction data mapping', 'Optimized internal transaction data', 'FDX 4.0 formatted transaction representation', 'transaction_id', 'api_lineage_3_v2.1'),
  ('record_lineage_4_v2.1', 'INTERNAL_BALANCE_v2.1', 'FDX_BALANCE_v1', 'Performance-optimized balance information mapping', 'Optimized internal balance data', 'FDX 4.0 formatted balance representation', 'account_id', 'api_lineage_4_v2.1'),
  ('record_lineage_5_v2.1', 'INTERNAL_CUSTOMER_v2.1', 'FDX_OWNER_v1', 'Initial owner information mapping', 'Internal customer data', 'FDX 4.0 formatted owner representation', 'customer_id', 'api_lineage_5_v2.1'),

  -- Current version 3.0 record lineage mappings (FDX 5.0 compliance)
  ('record_lineage_1', 'INTERNAL_ACCOUNT_v3', 'FDX_ACCOUNT_v2', 'FDX 5.0 compliant account data mapping', 'Enhanced internal account data', 'FDX 5.0 formatted account representation', 'account_id', 'api_lineage_1'),
  ('record_lineage_2', 'INTERNAL_ACCOUNT_v3', 'FDX_ACCOUNT_v2', 'FDX 5.0 compliant account detail mapping', 'Enhanced internal account detail', 'FDX 5.0 formatted account detail representation', 'account_id', 'api_lineage_2'),
  ('record_lineage_3', 'INTERNAL_TRANSACTION_v3', 'FDX_TRANSACTION_v2', 'FDX 5.0 compliant transaction data mapping', 'Enhanced internal transaction data', 'FDX 5.0 formatted transaction representation', 'transaction_id', 'api_lineage_3'),
  ('record_lineage_4', 'INTERNAL_BALANCE_v3', 'FDX_BALANCE_v2', 'FDX 5.0 compliant balance information mapping', 'Enhanced internal balance data', 'FDX 5.0 formatted balance representation', 'account_id', 'api_lineage_4'),
  ('record_lineage_5', 'INTERNAL_CUSTOMER_v3', 'FDX_OWNER_v2', 'FDX 5.0 compliant owner information mapping', 'Enhanced internal customer data', 'FDX 5.0 formatted owner representation', 'customer_id', 'api_lineage_5');

-- Field lineage showing how fields should be transformed with temporal evolution
INSERT INTO data_quality.field_lineage ("fieldLineageId", "fieldName", description, "inputFields", "recordLineageId")
VALUES
  -- Version 1.0 field mappings (basic implementation)
  ('field_lineage_1_v1', 'accountNumber', 'Basic mapping of account number', 'account_number', 'record_lineage_1_v1'),
  ('field_lineage_2_v1', 'currentBalance', 'Simple balance mapping', 'balance', 'record_lineage_1_v1'),
  ('field_lineage_3_v1', 'availableBalance', 'Simple available balance mapping', 'available_balance', 'record_lineage_1_v1'),

  ('field_lineage_4_v1', 'accountNumber', 'Basic mapping of account number', 'account_number', 'record_lineage_2_v1'),
  ('field_lineage_5_v1', 'accountName', 'Simple account name mapping', 'account_name', 'record_lineage_2_v1'),
  ('field_lineage_6_v1', 'accountType', 'Simple account type mapping', 'account_type', 'record_lineage_2_v1'),

  ('field_lineage_7_v1', 'transactionId', 'Basic mapping of transaction ID', 'transaction_id', 'record_lineage_3_v1'),
  ('field_lineage_8_v1', 'amount', 'Simple transaction amount mapping', 'transaction_amount', 'record_lineage_3_v1'),
  ('field_lineage_9_v1', 'transactionDate', 'Simple transaction date mapping', 'transaction_date', 'record_lineage_3_v1'),

  -- Version 1.1 field mappings (added compliance fields)
  ('field_lineage_1_v1.1', 'accountNumber', 'Basic mapping of account number', 'account_number', 'record_lineage_1_v1.1'),
  ('field_lineage_2_v1.1', 'maskedAccountNumber', 'Added masked version for compliance', 'masked_account_number', 'record_lineage_1_v1.1'),
  ('field_lineage_3_v1.1', 'currentBalance', 'Simple balance mapping', 'balance', 'record_lineage_1_v1.1'),
  ('field_lineage_4_v1.1', 'availableBalance', 'Simple available balance mapping', 'available_balance', 'record_lineage_1_v1.1'),
  ('field_lineage_5_v1.1', 'status', 'New compliance status field', 'compliance_status', 'record_lineage_1_v1.1'),

  -- Version 2.0 field mappings (enhanced security and currency standardization)
  ('field_lineage_1_v2', 'accountNumber', 'Secure account number formatting', 'account_number', 'record_lineage_1_v2'),
  ('field_lineage_2_v2', 'maskedAccountNumber', 'Enhanced security masking', 'masked_account_number', 'record_lineage_1_v2'),
  ('field_lineage_3_v2', 'currentBalance', 'Currency standardization', 'balance_usd', 'record_lineage_1_v2'),
  ('field_lineage_4_v2', 'availableBalance', 'Currency standardization', 'available_balance_usd', 'record_lineage_1_v2'),
  ('field_lineage_5_v2', 'status', 'Compliance status field', 'compliance_status', 'record_lineage_1_v2'),
  ('field_lineage_6_v2', 'securityLevel', 'New security classification field', 'security_level', 'record_lineage_1_v2'),

  -- Version 2.1 field mappings (performance improvements and enhanced owner data)
  ('field_lineage_1_v2.1', 'accountNumber', 'Optimized account number formatting', 'account_number', 'record_lineage_1_v2.1'),
  ('field_lineage_2_v2.1', 'maskedAccountNumber', 'Optimized masking algorithm', 'masked_account_number', 'record_lineage_1_v2.1'),
  ('field_lineage_3_v2.1', 'currentBalance', 'Optimized currency standardization', 'balance_usd', 'record_lineage_1_v2.1'),
  ('field_lineage_4_v2.1', 'availableBalance', 'Optimized currency standardization', 'available_balance_usd', 'record_lineage_1_v2.1'),

  ('field_lineage_7_v2.1', 'transactionId', 'Optimized transaction ID formatting', 'transaction_id', 'record_lineage_3_v2.1'),
  ('field_lineage_8_v2.1', 'amount', 'Optimized currency standardization', 'transaction_amount_usd', 'record_lineage_3_v2.1'),
  ('field_lineage_9_v2.1', 'transactionDate', 'Enhanced date standardization', 'transaction_date', 'record_lineage_3_v2.1'),
  ('field_lineage_10_v2.1', 'category', 'New categorization field', 'transaction_category', 'record_lineage_3_v2.1'),

  ('field_lineage_11_v2.1', 'ledgerBalance', 'Optimized currency standardization', 'current_balance_usd', 'record_lineage_4_v2.1'),
  ('field_lineage_12_v2.1', 'availableBalance', 'Optimized currency standardization', 'available_balance_usd', 'record_lineage_4_v2.1'),
  ('field_lineage_13_v2.1', 'creditLimit', 'Added standardized credit limit', 'credit_limit_usd', 'record_lineage_4_v2.1'),

  ('field_lineage_14_v2.1', 'ownerName', 'Basic name formatting', 'customer_name', 'record_lineage_5_v2.1'),
  ('field_lineage_15_v2.1', 'ownerAddress', 'Basic address formatting', 'customer_address', 'record_lineage_5_v2.1'),
  ('field_lineage_16_v2.1', 'taxIdMasked', 'Basic tax ID masking', 'customer_tax_id_masked', 'record_lineage_5_v2.1'),

  -- Current version 3.0 field mappings (FDX 5.0 compliance)
  ('field_lineage_1', 'accountNumber', 'FDX 5.0 account number formatting', 'account_number', 'record_lineage_1'),
  ('field_lineage_2', 'maskedAccountNumber', 'FDX 5.0 compliant masking', 'masked_account_number', 'record_lineage_1'),
  ('field_lineage_3', 'currentBalance', 'FDX 5.0 compliant balance format', 'balance_usd', 'record_lineage_1'),
  ('field_lineage_4', 'availableBalance', 'FDX 5.0 compliant available balance format', 'available_balance_usd', 'record_lineage_1'),

  ('field_lineage_5', 'accountNumber', 'FDX 5.0 account number formatting', 'account_number', 'record_lineage_2'),
  ('field_lineage_6', 'accountName', 'FDX 5.0 account name formatting', 'account_name', 'record_lineage_2'),
  ('field_lineage_7', 'accountType', 'FDX 5.0 standardized account type', 'account_type', 'record_lineage_2'),

  ('field_lineage_8', 'transactionId', 'FDX 5.0 transaction ID formatting', 'transaction_id', 'record_lineage_3'),
  ('field_lineage_9', 'amount', 'FDX 5.0 transaction amount formatting', 'transaction_amount', 'record_lineage_3'),
  ('field_lineage_10', 'transactionDate', 'FDX 5.0 transaction date formatting', 'transaction_date', 'record_lineage_3'),

  ('field_lineage_11', 'ledgerBalance', 'FDX 5.0 current balance formatting', 'current_balance', 'record_lineage_4'),
  ('field_lineage_12', 'availableBalance', 'FDX 5.0 available balance formatting', 'available_balance', 'record_lineage_4'),
  ('field_lineage_13', 'creditLimit', 'FDX 5.0 credit limit formatting', 'credit_limit', 'record_lineage_4'),

  ('field_lineage_14', 'ownerName', 'FDX 5.0 owner name formatting', 'customer_full_name', 'record_lineage_5'),
  ('field_lineage_15', 'ownerAddress', 'FDX 5.0 owner address formatting', 'customer_address', 'record_lineage_5'),
  ('field_lineage_16', 'taxIdMasked', 'FDX 5.0 tax ID masking', 'customer_tax_id', 'record_lineage_5');


-- =============================================
-- DATA ARCHITECT FOCUSED INSERTS
-- =============================================

-- Additional record transformations with varying complexity and performance
INSERT INTO data_quality.record_transformations (id, "inputType", "outputType", description, "primaryKeyNames", "primaryKeyValues", "executedAt", "apiCallId")
VALUES
  ('f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1', 'INTERNAL_BALANCE', 'FDX_BALANCE', 'Balance data transformation with currency conversion to FDX format', 'account_id', 'A12345', '2025-03-03 09:30:10', '66666666-6666-6666-6666-666666666666'),
  ('a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2', 'INTERNAL_CUSTOMER', 'FDX_OWNER', 'Customer data transformation with address normalization to FDX format', 'customer_id', 'C67890', '2025-03-03 10:45:20', '77777777-7777-7777-7777-777777777777'),
  ('a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3', 'INTERNAL_TRANSACTION', 'FDX_TRANSACTION', 'Transaction data transformation with categorization to FDX format', 'transaction_ids', 'T12345,T12346,T12347', '2025-03-03 13:15:30', '88888888-8888-8888-8888-888888888888'),
  ('a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4', 'INTERNAL_ACCOUNT', 'FDX_ACCOUNT', 'Multi-account transformation with balance aggregation to FDX format', 'account_ids', 'A24680,A24681', '2025-03-04 11:30:40', '99999999-9999-9999-9999-999999999999'),
  ('a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5', 'INTERNAL_ACCOUNT', 'FDX_ACCOUNT', 'Complete account transformation with all related data to FDX format', 'account_id', 'A13579', '2025-03-04 14:46:00', 'aaaa1234-aaaa-aaaa-aaaa-aaaaaaaaaaaa');

-- Complex field transformations for architectural analysis
INSERT INTO data_quality.field_transformation_details (id, "transformDescription", "inputFieldName", "inputFieldValue", "outputFieldName", "outputFieldValue", "transformationId")
VALUES
  -- Balance transformations
  ('20a20a20-20a1-20a1-20a1-20a20a20a20a', 'Currency conversion to FDX format', 'current_balance_usd', '1080.00', 'ledgerBalance', '1000.00', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'),
  ('20b20b20-20b1-20b1-20b1-20b20b20b20b', 'Currency code for FDX format', 'currency_code', 'EUR', 'currencyCode', 'EUR', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'),
  ('21a21a21-21a1-21a1-21a1-21a21a21a21a', 'Currency conversion to FDX format', 'available_balance_usd', '1026.00', 'availableBalance', '950.00', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'),
  ('22a22a22-22a1-22a1-22a1-22a22a22a22a', 'Date format standardization to FDX', 'balance_timestamp', '2025-03-03 09:30:00', 'balanceDate', '2025-03-03T09:30:00Z', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'),

  -- Owner transformations
  ('23a23a23-23a1-23a1-23a1-23a23a23a23a', 'Name parsing and normalization to FDX', 'customer_first_name', 'Jane', 'ownerName', 'DOE, JANE MARIE', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('24a24a24-24a1-24a1-24a1-24a24a24a24a', 'Name components for FDX format', 'customer_middle_name', 'Marie', 'middleName', 'MARIE', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('25a25a25-25a1-25a1-25a1-25a25a25a25a', 'Name components for FDX format', 'customer_last_name', 'Doe', 'lastName', 'DOE', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('26a26a26-26a1-26a1-26a1-26a26a26a26a', 'Address parsing and standardization to FDX', 'customer_address_street', '456 Broadway St', 'ownerAddress', '456 BROADWAY ST, STE 7B, NEW YORK, NY 10013', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('27a27a27-27a1-27a1-27a1-27a27a27a27a', 'Address components for FDX format', 'customer_address_unit', 'Suite 7B', 'addressLine2', 'STE 7B', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('28a28a28-28a1-28a1-28a1-28a28a28a28a', 'Address components for FDX format', 'customer_address_city', 'New York', 'city', 'NEW YORK', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('29a29a29-29a1-29a1-29a1-29a29a29a29a', 'Address components for FDX format', 'customer_address_state', 'NY', 'state', 'NY', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('30a30a30-30a1-30a1-30a1-30a30a30a30a', 'Address components for FDX format', 'customer_address_zip', '10013', 'postalCode', '10013', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),

  -- Transaction transformations
  ('31a31a31-31a1-31a1-31a1-31a31a31a31a', 'Transaction categorization for FDX format', 'transaction_category', 'GROCERY', 'description', 'WHOLEFDS NYC 10010', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('32a32a32-32a1-32a1-32a1-32a32a32a32a', 'Transaction categorization for FDX format', 'transaction_category', 'SUBSCRIPTION', 'description', 'AMAZONPRIME', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('33a33a33-33a1-33a1-33a1-33a33a33a33a', 'Transaction categorization for FDX format', 'transaction_category', 'TRANSPORTATION', 'description', 'UBER TRIP', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('34a34a34-34a1-34a1-34a1-34a34a34a34a', 'Amount sign standardization for FDX format', 'transaction_amount', '25.00', 'amount', '-25.00', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('35a35a35-35a1-35a1-35a1-35a35a35a35a', 'Transaction type determination for FDX format', 'transaction_type', 'DEBIT', 'type', 'DEBIT', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),

  -- Multi-account aggregation
  ('36a36a36-36a1-36a1-36a1-36a36a36a36a', 'Account balances aggregation to FDX format', 'total_balance', '4000.00', 'currentBalance', '1500.00', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('36b36b36-36b1-36b1-36b1-36b36b36b36b', 'Additional account balance', 'total_balance_part', '2500.00', 'relatedAccounts', '[{"accountId":"A24681","currentBalance":2500.00}]', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('37a37a37-37a1-37a1-37a1-37a37a37a37a', 'Account available balances aggregation to FDX format', 'total_available_balance', '3850.00', 'availableBalance', '1450.00', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('37b37b37-37b1-37b1-37b1-37b37b37b37b', 'Additional account available balance', 'total_available_balance_part', '2400.00', 'relatedAccountsAvailable', '[{"accountId":"A24681","availableBalance":2400.00}]', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('38a38a38-38a1-38a1-38a1-38a38a38a38a', 'Account type grouping for FDX format', 'account_group', 'DEPOSIT', 'accountType', 'CHECKING', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('38b38b38-38b1-38b1-38b1-38b38b38b38b', 'Additional account type', 'account_group_part', 'DEPOSIT', 'relatedAccountTypes', '[{"accountId":"A24681","accountType":"SAVINGS"}]', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),

  -- Complete account transformation
  ('39a39a39-39a1-39a1-39a1-39a39a39a39a', 'Account data consolidation to FDX format', 'account_summary', '{"number":"13579","type":"Investment","status":"Active"}', 'accountNumber', '13579', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('39b39b39-39b1-39b1-39b1-39b39b39b39b', 'Account type extraction', 'account_summary_type', 'Investment', 'accountType', 'INVESTMENT', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('39c39c39-39c1-39c1-39c1-39c39c39c39c', 'Account status extraction', 'account_summary_status', 'Active', 'status', 'ACTIVE', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('40a40a40-40a1-40a1-40a1-40a40a40a40a', 'Balance data consolidation to FDX format', 'balance_summary', '{"current":35000.00,"available":35000.00,"pending":0.00}', 'currentBalance', '35000.00', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('40b40b40-40b1-40b1-40b1-40b40b40b40b', 'Available balance extraction', 'balance_summary_available', '35000.00', 'availableBalance', '35000.00', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('40c40c40-40c1-40c1-40c1-40c40c40c40c', 'Pending balance extraction', 'balance_summary_pending', '0.00', 'pendingBalance', '0.00', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('41a41a41-41a1-41a1-41a1-41a41a41a41a', 'Owner data consolidation to FDX format', 'owner_summary', '{"name":"Robert J Smith","contact":{"email":"robert.smith@example.com","phone":"212-555-1234"}}', 'ownerName', 'SMITH, ROBERT J', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('41b41b41-41b1-41b1-41b1-41b41b41b41b', 'Owner email extraction', 'owner_summary_email', 'robert.smith@example.com', 'email', 'robert.smith@example.com', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('41c41c41-41c1-41c1-41c1-41c41c41c41c', 'Owner phone extraction', 'owner_summary_phone', '212-555-1234', 'phoneNumber', '212-555-1234', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5');


-- =============================================
-- CHIEF MARKETING OFFICER (CMO) FOCUSED INSERTS
-- =============================================

-- Customer usage pattern transformations
INSERT INTO data_quality.record_transformations (id, "inputType", "outputType", description, "primaryKeyNames", "primaryKeyValues", "executedAt", "apiCallId")
VALUES
  ('b6b6b6b6-b6b6-b6b6-b6b6-b6b6b6b6b6b6', 'FDX_ACCOUNT', 'WEALTH_PORTFOLIO', 'Transformation for wealth management aggregation', 'account_id', 'A54321', '2025-03-05 09:00:10', 'bbbb0000-bbbb-bbbb-bbbb-bbbbbbbbbbbb'),
  ('b7b7b7b7-b7b7-b7b7-b7b7-b7b7b7b7b7b7', 'FDX_ACCOUNT', 'LOAN_APPLICATION', 'Transformation for lending qualification', 'customer_id,account_id', 'C97531,A97531', '2025-03-05 11:30:20', 'cccc0000-cccc-cccc-cccc-cccccccccccc'),
  ('b8b8b8b8-b8b8-b8b8-b8b8-b8b8b8b8b8b8', 'FDX_ACCOUNT', 'BUDGET_TRACKER', 'Transformation for personal finance tracking', 'customer_id,account_id', 'C86420,A86420', '2025-03-06 10:15:30', 'dddd0000-dddd-dddd-dddd-dddddddddddd'),
  ('b9b9b9b9-b9b9-b9b9-b9b9-b9b9b9b9b9b9', 'FDX_TRANSACTION', 'ACCOUNTING_ENTRY', 'Transformation for enterprise accounting system', 'transaction_ids', 'T54321,T54322,T54323', '2025-03-06 13:45:40', 'eeee0000-eeee-eeee-eeee-eeeeeeeeeeee'),
  ('cdcd0000-cdcd-cdcd-cdcd-cdcdcdcdcdcd', 'FDX_OWNER', 'CREDIT_PROFILE', 'Transformation for credit assessment', 'customer_id', 'C97531', '2025-03-07 09:30:50', 'ffff0000-ffff-ffff-ffff-ffffffffffff');

-- Field transformations showing customer value-add processing
INSERT INTO data_quality.field_transformation_details (id, "transformDescription", "inputFieldName", "inputFieldValue", "outputFieldName", "outputFieldValue", "transformationId")
VALUES
  -- Wealth management transformations
  ('50a50a50-50a1-50a1-50a1-50a50a50a50a', 'Asset classification', 'accountType,investmentData', 'INVESTMENT,{...}', 'asset_class', 'EQUITY', 'b6b6b6b6-b6b6-b6b6-b6b6-b6b6b6b6b6b6'),
  ('51a51a51-51a1-51a1-51a1-51a51a51a51a', 'Risk profile calculation', 'investmentData,transactionHistory', '{...},{...}', 'risk_score', '65', 'b6b6b6b6-b6b6-b6b6-b6b6-b6b6b6b6b6b6'),
  ('52a52a52-52a1-52a1-52a1-52a52a52a52a', 'Portfolio diversification analysis', 'investmentData,balances', '{...},{...}', 'diversification_index', '0.72', 'b6b6b6b6-b6b6-b6b6-b6b6-b6b6b6b6b6b6'),

  -- Lending qualification transformations
  ('53a53a53-53a1-53a1-53a1-53a53a53a53a', 'Income estimation', 'transactionHistory,accountType', '{...},CHECKING', 'estimated_monthly_income', '5200.00', 'b7b7b7b7-b7b7-b7b7-b7b7-b7b7b7b7b7b7'),
  ('54a54a54-54a1-54a1-54a1-54a54a54a54a', 'Expense pattern analysis', 'transactionHistory', '{...}', 'expense_stability_score', '85', 'b7b7b7b7-b7b7-b7b7-b7b7-b7b7b7b7b7b7'),
  ('55a55a55-55a1-55a1-55a1-55a55a55a55a', 'Debt calculation', 'balances,accountType', '{...},CREDIT_CARD', 'current_debt_load', '12500.00', 'b7b7b7b7-b7b7-b7b7-b7b7-b7b7b7b7b7b7'),

  -- Personal finance tracking transformations
  ('56a56a56-56a1-56a1-56a1-56a56a56a56a', 'Transaction categorization', 'transactionHistory', '{...}', 'spending_categories', '{"dining":450.00,"transportation":200.00,"groceries":650.00,...}', 'b8b8b8b8-b8b8-b8b8-b8b8-b8b8b8b8b8b8'),
  ('57a57a57-57a1-57a1-57a1-57a57a57a57a', 'Budget comparison', 'transactionHistory,userBudgets', '{...},{...}', 'budget_adherence', '{"dining":0.9,"transportation":1.1,"groceries":1.0,...}', 'b8b8b8b8-b8b8-b8b8-b8b8-b8b8b8b8b8b8'),
  ('58a58a58-58a1-58a1-58a1-58a58a58a58a', 'Savings opportunity identification', 'transactionHistory,balances', '{...},{...}', 'savings_opportunities', '["Reduce dining out","Consolidate subscriptions"]', 'b8b8b8b8-b8b8-b8b8-b8b8-b8b8b8b8b8b8'),

  -- Accounting system transformations
  ('59a59a59-59a1-59a1-59a1-59a59a59a59a', 'GL account mapping', 'description,amount,type', 'OFFICE SUPPLY VENDOR,-125.45,DEBIT', 'gl_account_entry', '{"account":"5001-ExpenseOfficeSupplies","amount":125.45,"type":"debit"}', 'b9b9b9b9-b9b9-b9b9-b9b9-b9b9b9b9b9b9'),
  ('60a60a60-60a1-60a1-60a1-60a60a60a60a', 'Tax classification', 'description,amount,merchantData', 'BUSINESS TRAVEL AIRLINE,-534.90,{...}', 'tax_category', 'BUSINESS_TRAVEL_DEDUCTIBLE', 'b9b9b9b9-b9b9-b9b9-b9b9-b9b9b9b9b9b9'),
  ('61a61a61-61a1-61a1-61a1-61a61a61a61a', 'Receipt matching', 'description,amount,transactionDate', 'OFFICE SUPPLY VENDOR,-125.45,2025-02-15', 'receipt_match_id', 'REC12345', 'b9b9b9b9-b9b9-b9b9-b9b9-b9b9b9b9b9b9'),

  -- Credit assessment transformations
  ('62a62a62-62a1-62a1-62a1-62a62a62a62a', 'Payment history analysis', 'transactionHistory,dueDate,paymentDate', '{...},2025-01-15,2025-01-14', 'payment_reliability_score', '95', 'cdcd0000-cdcd-cdcd-cdcd-cdcdcdcdcdcd'),
  ('63a63a63-63a1-63a1-63a1-63a63a63a63a', 'Credit utilization calculation', 'currentBalance,creditLimit', '3500.00,10000.00', 'credit_utilization_ratio', '0.35', 'cdcd0000-cdcd-cdcd-cdcd-cdcdcdcdcdcd'),
  ('64a64a64-64a1-64a1-64a1-64a64a64a64a', 'Income stability assessment', 'transactionHistory,depositPatterns', '{...},{...}', 'income_stability_score', '88', 'cdcd0000-cdcd-cdcd-cdcd-cdcdcdcdcdcd');
