-- =============================================
-- DATA QUALITY EXECUTIVE FOCUSED - API CALLS
-- =============================================

-- API Calls with updated column names
INSERT INTO data_quality.api_calls (
  api_call_id,
  method,
  path,
  query_params,
  request_headers,
  server_name,
  major_version,
  minor_version,
  related_institution,
  created_at
)
VALUES
  -- Early adopters of v1.1 while v1.0 still available
  ('11111111-1111-1111-1111-111111111111'::uuid, 'GET', '/fdx/v1_1/accounts', '{"customerId": "C12345", "include": "balances,transactions"}', '{"Authorization": "Bearer token123", "x-institution-id": "bank_of_america", "x-hasura-user-id": "12345"}', 'fdx-gateway', 1, 1, 'bank_of_america', '2024-03-15 08:30:00'::timestamptz),
  ('22222222-2222-2222-2222-222222222222'::uuid, 'GET', '/fdx/v1_1/accounts', '{"customerId": "C67890", "include": "balances,owner"}', '{"Authorization": "Bearer token456", "x-institution-id": "chase", "x-hasura-user-id": "67890"}', 'fdx-gateway', 1, 1, 'chase', '2024-03-25 09:15:00'::timestamptz),

  -- Late adopters still using v1.0 near end of lifecycle
  ('33333333-3333-3333-3333-333333333333'::uuid, 'GET', '/fdx/v1/accounts', '{"accountId": "A12345", "include": "all"}', '{"Authorization": "Bearer token789", "x-institution-id": "fidelity", "x-hasura-user-id": "10001"}', 'fdx-gateway', 1, 0, 'fidelity', '2024-06-20 10:30:00'::timestamptz),

  -- Early adopters of v2.0 while v1.1 still available
  ('44444444-4444-4444-4444-444444444444'::uuid, 'GET', '/fdx/v2/accounts', '{"customerId": "C45678", "include": "balances,transactions"}', '{"Authorization": "Bearer tokenABC", "x-institution-id": "wellsfargo", "x-hasura-user-id": "45678"}', 'fdx-gateway', 2, 0, 'wellsfargo', '2024-06-15 08:45:00'::timestamptz),

  -- Late adopters still using v1.1 near end of lifecycle
  ('55555555-5555-5555-5555-555555555555'::uuid, 'GET', '/fdx/v1_1/accounts', '{"customerId": "C12345", "include": "balances"}', '{"Authorization": "Bearer tokenDEF", "x-institution-id": "regional_bank_A", "x-hasura-user-id": "12345"}', 'fdx-gateway', 1, 1, 'regional_bank_A', '2024-09-25 14:20:00'::timestamptz),

  -- Early adopters of v2.1 while v2.0 still available
  ('66666666-6666-6666-6666-666666666666'::uuid, 'GET', '/fdx/v2_1/accounts/A12345/balances', '{}', '{"Authorization": "Bearer tokenXYZ", "x-institution-id": "fintech_startup_A", "x-hasura-user-id": "12345"}', 'fdx-gateway', 2, 1, 'fintech_startup_A', '2024-09-15 09:30:00'::timestamptz),

  -- Late adopters still using v2.0 near end of lifecycle
  ('77777777-7777-7777-7777-777777777777'::uuid, 'GET', '/fdx/v2/accounts/A67890/owner', '{}', '{"Authorization": "Bearer tokenUVW", "x-institution-id": "neobank_B", "x-hasura-user-id": "67890"}', 'fdx-gateway', 2, 0, 'neobank_B', '2024-12-15 10:45:00'::timestamptz),

  -- Early adopters of v3.0 while v2.1 still available - UPDATED TIMESTAMP
  ('88888888-8888-8888-8888-888888888888'::uuid, 'GET', '/fdx/v3/accounts/A34567/transactions', '{"startTime": "2025-02-01T00:00:00Z", "endTime": "2025-03-01T00:00:00Z"}', '{"Authorization": "Bearer tokenRST", "x-institution-id": "wealth_manager_C", "x-hasura-user-id": "34567"}', 'fdx-gateway', 3, 0, 'wealth_manager_C', '2025-03-03 13:15:26'::timestamptz),

  -- Late adopters still using v2.1 near end of lifecycle - UPDATED TIMESTAMP
  ('99999999-9999-9999-9999-999999999999'::uuid, 'GET', '/fdx/2_1/accounts', '{"customerId": "C24680", "accountType": "CHECKING,SAVINGS", "include": "balances"}', '{"Authorization": "Bearer tokenJKL", "x-institution-id": "credit_union_D", "x-hasura-user-id": "24680"}', 'fdx-gateway', 2, 1, 'credit_union_D', '2025-03-01 08:30:01'::timestamptz),

  -- Latest version adoption - UPDATED TIMESTAMP
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'::uuid, 'GET', '/fdx/v5/accounts', '{"customerId": "C13579", "accountStatus": "ACTIVE", "include": "all"}', '{"Authorization": "Bearer tokenMNO", "x-institution-id": "community_bank_E", "x-api-version": "3.0", "x-hasura-user-id": "13579"}', 'fdx-gateway', 5, 0, 'community_bank_E', '2025-03-01 08:35:06'::timestamptz),

  -- Additional API calls to show adoption patterns - UPDATED TIMESTAMPS
  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'::uuid, 'GET', '/fdx/v5/accounts', '{"customerId": "C54321", "include": "balances,transactions,owner"}', '{"Authorization": "Bearer tokenPQR", "x-institution-id": "fintech_wealth_advisor", "x-hasura-user-id": "54321"}', 'fdx-gateway', 5, 0, 'fintech_wealth_advisor', '2025-03-03 09:30:11'::timestamptz),
  ('cccccccc-cccc-cccc-cccc-cccccccccccc'::uuid, 'GET', '/fdx/v5/accounts', '{"customerId": "C97531", "include": "balances,owner"}', '{"Authorization": "Bearer tokenSTU", "x-institution-id": "digital_lending_platform", "x-hasura-user-id": "97531"}', 'fdx-gateway', 5, 0, 'digital_lending_platform', '2025-03-04 14:46:06'::timestamptz),
  ('dddddddd-dddd-dddd-dddd-dddddddddddd'::uuid, 'GET', '/fdx/v5/accounts', '{"customerId": "C86420", "include": "balances,transactions"}', '{"Authorization": "Bearer tokenVWX", "x-institution-id": "personal_finance_app", "x-hasura-user-id": "86420"}', 'fdx-gateway', 5, 0, 'personal_finance_app', '2025-03-10 10:15:00'::timestamptz),
  ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee'::uuid, 'GET', '/fdx/v5/accounts/A54321/transactions', '{"startTime": "2025-01-01T00:00:00Z", "endTime": "2025-03-01T00:00:00Z", "type": "DEBIT,CREDIT"}', '{"Authorization": "Bearer tokenYZA", "x-institution-id": "enterprise_accounting_system", "x-hasura-user-id": "54321"}', 'fdx-gateway', 5, 0, 'enterprise_accounting_system', '2025-03-03 13:15:31'::timestamptz),
  ('ffffffff-ffff-ffff-ffff-ffffffffffff'::uuid, 'GET', '/fdx/v5/accounts/A97531/owner', '{}', '{"Authorization": "Bearer tokenBCD", "x-institution-id": "credit_building_app", "x-hasura-user-id": "97531"}', 'fdx-gateway', 5, 0, 'credit_building_app', '2025-03-03 09:30:06'::timestamptz);
