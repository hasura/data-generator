-- =============================================
-- DATA QUALITY EXECUTIVE FOCUSED - RECORD TRANSFORMATIONS
-- =============================================

-- Record transformations showing different transformation patterns
INSERT INTO data_quality.record_transformations (
  record_transformation_id,
  input_type,
  output_type,
  description,
  primary_key_names,
  primary_key_values,
  created_at,
  api_call_id
)
VALUES
  ('a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'::uuid, 'CONSUMER_BANKING_ACCOUNT', 'FDX_ACCOUNT', 'Standard account data transformation to FDX format', 'consumerBankingAccountId', 'A12345', '2025-03-01 08:30:05'::timestamptz, '11111111-1111-1111-1111-111111111111'::uuid),
  ('b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'::uuid, 'CONSUMER_BANKING_ACCOUNT', 'FDX_ACCOUNT', 'Account transformation with balance normalization to FDX format', 'consumerBankingAccountId', 'A67890', '2025-03-01 09:15:10'::timestamptz, '22222222-2222-2222-2222-222222222222'::uuid),
  ('c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1'::uuid, 'CONSUMER_BANKING_ACCOUNT', 'FDX_ACCOUNT', 'Full account transformation with enhanced owner info to FDX format', 'consumerBankingAccountId', 'A34567', '2025-03-01 10:30:15'::timestamptz, '33333333-3333-3333-3333-333333333333'::uuid),
  ('d1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'::uuid, 'CONSUMER_BANKING_ACCOUNT', 'FDX_ACCOUNT', 'Standard account data transformation to FDX format', 'consumerBankingAccountId', 'A45678', '2025-03-02 08:45:20'::timestamptz, '44444444-4444-4444-4444-444444444444'::uuid),
  ('e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1'::uuid, 'CONSUMER_BANKING_ACCOUNT', 'FDX_ACCOUNT', 'Simple balance-only transformation to FDX format', 'consumerBankingAccountId', 'A12345', '2025-03-02 14:20:25'::timestamptz, '55555555-5555-5555-5555-555555555555'::uuid);

-- Additional record transformations with varying complexity and performance
INSERT INTO data_quality.record_transformations (
  record_transformation_id,
  input_type,
  output_type,
  description,
  primary_key_names,
  primary_key_values,
  created_at,
  api_call_id
)
VALUES
  ('f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'::uuid, 'CONSUMER_BANKING_BALANCE', 'FDX_BALANCE', 'Balance data transformation with currency conversion to FDX format', 'consumerBankingBalanceId', 'A12345', '2025-03-03 09:30:10'::timestamptz, '66666666-6666-6666-6666-666666666666'::uuid),
  ('a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'::uuid, 'ENTERPRISE_PARTY', 'FDX_OWNER', 'Party data transformation to FDX format', 'enterprisePartyId', 'C67890', '2025-03-03 10:45:20'::timestamptz, '77777777-7777-7777-7777-777777777777'::uuid),
  ('a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'::uuid, 'CONSUMER_BANKING_TRANSACTION', 'FDX_TRANSACTION', 'Transaction data transformation with categorization to FDX format', 'consumerBankingTransactionId', 'T12345,T12346,T12347', '2025-03-03 13:15:30'::timestamptz, '88888888-8888-8888-8888-888888888888'::uuid),
  ('a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'::uuid, 'CONSUMER_BANKING_ACCOUNT', 'FDX_ACCOUNT', 'Multi-account transformation with balance aggregation to FDX format', 'consumerBankingAccountId', 'A24680,A24681', '2025-03-04 11:30:40'::timestamptz, '99999999-9999-9999-9999-999999999999'::uuid),
  ('a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'::uuid, 'CONSUMER_BANKING_ACCOUNT', 'FDX_ACCOUNT', 'Complete account transformation with all related data to FDX format', 'consumerBankingAccountId', 'A13579', '2025-03-04 14:46:00'::timestamptz, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'::uuid);

-- CMO focused transformations
INSERT INTO data_quality.record_transformations (
  record_transformation_id,
  input_type,
  output_type,
  description,
  primary_key_names,
  primary_key_values,
  created_at,
  api_call_id
)
VALUES
  ('b6b6b6b6-b6b6-b6b6-b6b6-b6b6b6b6b6b6'::uuid, 'FDX_ACCOUNT', 'WEALTH_PORTFOLIO', 'Transformation for wealth management aggregation', 'consumerBankingAccountId', 'A54321', '2025-03-05 09:00:10'::timestamptz, 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'::uuid),
  ('b7b7b7b7-b7b7-b7b7-b7b7-b7b7b7b7b7b7'::uuid, 'FDX_ACCOUNT', 'LOAN_APPLICATION', 'Transformation for lending qualification', 'consumerBankingAccountId,enterprisePartyId', 'A97531,C97531', '2025-03-05 11:30:20'::timestamptz, 'cccccccc-cccc-cccc-cccc-cccccccccccc'::uuid),
  ('b8b8b8b8-b8b8-b8b8-b8b8-b8b8b8b8b8b8'::uuid, 'FDX_ACCOUNT', 'BUDGET_TRACKER', 'Transformation for personal finance tracking', 'consumerBankingAccountId,enterprisePartyId', 'A86420,C86420', '2025-03-06 10:15:30'::timestamptz, 'dddddddd-dddd-dddd-dddd-dddddddddddd'::uuid),
  ('b9b9b9b9-b9b9-b9b9-b9b9-b9b9b9b9b9b9'::uuid, 'FDX_TRANSACTION', 'ACCOUNTING_ENTRY', 'Transformation for enterprise accounting system', 'consumerBankingTransactionId', 'T54321,T54322,T54323', '2025-03-06 13:45:40'::timestamptz, 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee'::uuid),
  ('cdcd0000-cdcd-cdcd-cdcd-cdcdcdcdcdcd'::uuid, 'FDX_OWNER', 'CREDIT_PROFILE', 'Transformation for credit assessment', 'enterprisePartyId', 'C97531', '2025-03-07 09:30:50'::timestamptz, 'ffffffff-ffff-ffff-ffff-ffffffffffff'::uuid);
