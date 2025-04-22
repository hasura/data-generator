-- =============================================
-- DATA GOVERNANCE EXECUTIVE FOCUSED - RECORD LINEAGE
-- =============================================

-- Record lineage showing designated transformation paths with temporal evolution
INSERT INTO data_quality.record_lineage (
  record_lineage_id,
  input_type,
  output_type,
  description,
  input_description,
  output_description,
  pk_names,
  api_lineage_id
)
VALUES
  -- Initial version 1.0 record lineage mappings
  ('12341234-1234-1234-1234-123412341234'::uuid, 'CONSUMER_BANKING_ACCOUNT_v1', 'FDX_ACCOUNT_v1', 'Initial account data mapping', 'Internal bank account data', 'FDX 4.0 formatted account representation', 'consumerBankingAccountId', '11111111-1111-1111-aaaa-111111111111'),
  ('23452345-2345-2345-2345-234523452345'::uuid, 'CONSUMER_BANKING_ACCOUNT_v1', 'FDX_ACCOUNT_v1', 'Initial account detail mapping', 'Internal account detail data', 'FDX 4.0 formatted account detail representation', 'consumerBankingAccountId', '22222222-2222-2222-aaaa-222222222222'),
  ('34563456-3456-3456-3456-345634563456'::uuid, 'CONSUMER_BANKING_TRANSACTION_v1', 'FDX_TRANSACTION_v1', 'Initial transaction data mapping', 'Internal transaction data', 'FDX 4.0 formatted transaction representation', 'consumerBankingTransactionId', '33333333-3333-3333-aaaa-333333333333'),

  -- Version 1.1 record lineage mappings (added compliance fields)
  ('45674567-4567-4567-4567-456745674567'::uuid, 'CONSUMER_BANKING_ACCOUNT_v1.1', 'FDX_ACCOUNT_v1', 'Account data mapping with compliance fields', 'Internal account data with compliance fields', 'FDX 4.0 formatted account representation', 'consumerBankingAccountId', '44444444-4444-4444-aaaa-444444444444'),
  ('56785678-5678-5678-5678-567856785678'::uuid, 'CONSUMER_BANKING_ACCOUNT_v1.1', 'FDX_ACCOUNT_v1', 'Account detail mapping with compliance fields', 'Internal account detail with compliance fields', 'FDX 4.0 formatted account detail representation', 'consumerBankingAccountId', '55555555-5555-5555-aaaa-555555555555'),
  ('67896789-6789-6789-6789-678967896789'::uuid, 'CONSUMER_BANKING_TRANSACTION_v1.1', 'FDX_TRANSACTION_v1', 'Transaction data mapping with compliance fields', 'Internal transaction data with compliance fields', 'FDX 4.0 formatted transaction representation', 'consumerBankingTransactionId', '66666666-6666-6666-aaaa-666666666666'),

  -- Version 2.0 record lineage mappings (enhanced security)
  ('78907890-7890-7890-7890-789078907890'::uuid, 'CONSUMER_BANKING_ACCOUNT_v2', 'FDX_ACCOUNT_v1', 'Account data mapping with enhanced security', 'Internal account data with security enhancements', 'FDX 4.0 formatted account representation', 'consumerBankingAccountId', '77777777-7777-7777-aaaa-777777777777'),
  ('89018901-8901-8901-8901-890189018901'::uuid, 'CONSUMER_BANKING_ACCOUNT_v2', 'FDX_ACCOUNT_v1', 'Account detail mapping with enhanced security', 'Internal account detail with security enhancements', 'FDX 4.0 formatted account detail representation', 'consumerBankingAccountId', '88888888-8888-8888-aaaa-888888888888'),
  ('90129012-9012-9012-9012-901290129012'::uuid, 'CONSUMER_BANKING_TRANSACTION_v2', 'FDX_TRANSACTION_v1', 'Transaction data mapping with enhanced security', 'Internal transaction data with security enhancements', 'FDX 4.0 formatted transaction representation', 'consumerBankingTransactionId', '99999999-9999-9999-aaaa-999999999999'),
  ('01230123-0123-0123-0123-012301230123'::uuid, 'CONSUMER_BANKING_BALANCE_v2', 'FDX_BALANCE_v1', 'Balance information mapping with enhanced security', 'Internal balance data with security enhancements', 'FDX 4.0 formatted balance representation', 'consumerBankingBalanceId', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),

  -- Version 2.1 record lineage mappings (performance improvements and new owner endpoint)
  ('abcdabcd-abcd-abcd-abcd-abcdabcdabcd'::uuid, 'CONSUMER_BANKING_ACCOUNT_v2.1', 'FDX_ACCOUNT_v1', 'Performance-optimized account data mapping', 'Optimized internal account data', 'FDX 4.0 formatted account representation', 'consumerBankingAccountId', 'bbbbbbbb-bbbb-bbbb-aaaa-bbbbbbbbbbbb'),
  ('bcdef123-bcde-4321-abcd-bcdef123abcd'::uuid, 'CONSUMER_BANKING_ACCOUNT_v2.1', 'FDX_ACCOUNT_v1', 'Performance-optimized account detail mapping', 'Optimized internal account detail', 'FDX 4.0 formatted account detail representation', 'consumerBankingAccountId', 'cccccccc-cccc-cccc-aaaa-cccccccccccc'),
  ('cdef5678-cdef-5678-abcd-cdef5678abcd'::uuid, 'CONSUMER_BANKING_TRANSACTION_v2.1', 'FDX_TRANSACTION_v1', 'Performance-optimized transaction data mapping', 'Optimized internal transaction data', 'FDX 4.0 formatted transaction representation', 'consumerBankingTransactionId', 'dddddddd-dddd-dddd-aaaa-dddddddddddd'),
  ('defabc90-defa-9012-abcd-defabc90abcd'::uuid, 'CONSUMER_BANKING_BALANCE_v2.1', 'FDX_BALANCE_v1', 'Performance-optimized balance information mapping', 'Optimized internal balance data', 'FDX 4.0 formatted balance representation', 'consumerBankingBalanceId', 'eeeeeeee-eeee-eeee-aaaa-eeeeeeeeeeee'),
  ('efabc123-efab-1234-abcd-efabc123abcd'::uuid, 'ENTERPRISE_PARTY_v2.1', 'FDX_OWNER_v1', 'Initial owner information mapping', 'Enterprise party data', 'FDX 4.0 formatted owner representation', 'enterprisePartyId', 'ffffffff-ffff-ffff-aaaa-ffffffffffff'),

  -- Current version 5.0 record lineage mappings (FDX 5.0 compliance)
  ('fabc4567-fabc-4567-abcd-fabc4567abcd'::uuid, 'CONSUMER_BANKING_ACCOUNT_v3', 'FDX_ACCOUNT_v2', 'FDX 5.0 compliant account data mapping', 'Enhanced internal account data', 'FDX 5.0 formatted account representation', 'consumerBankingAccountId', '11111111-2222-3333-aaaa-123456789abc'),
  ('abc45678-abc4-5678-abcd-abc45678abcd'::uuid, 'CONSUMER_BANKING_ACCOUNT_v3', 'FDX_ACCOUNT_v2', 'FDX 5.0 compliant account detail mapping', 'Enhanced internal account detail', 'FDX 5.0 formatted account detail representation', 'consumerBankingAccountId', '22222222-3333-4444-aaaa-234567890abc'),
  ('bc567890-bc56-7890-abcd-bc567890abcd'::uuid, 'CONSUMER_BANKING_TRANSACTION_v3', 'FDX_TRANSACTION_v2', 'FDX 5.0 compliant transaction data mapping', 'Enhanced internal transaction data', 'FDX 5.0 formatted transaction representation', 'consumerBankingTransactionId', '33333333-4444-5555-aaaa-345678901abc'),
  ('c6789012-c678-9012-abcd-c6789012abcd'::uuid, 'CONSUMER_BANKING_BALANCE_v3', 'FDX_BALANCE_v2', 'FDX 5.0 compliant balance information mapping', 'Enhanced internal balance data', 'FDX 5.0 formatted balance representation', 'consumerBankingBalanceId', '44444444-5555-6666-aaaa-456789012abc'),
  ('d7890123-d789-0123-abcd-d7890123abcd'::uuid, 'ENTERPRISE_PARTY_v3', 'FDX_OWNER_v2', 'FDX 5.0 compliant owner information mapping', 'Enhanced enterprise party data', 'FDX 5.0 formatted owner representation', 'enterprisePartyId', '55555555-6666-7777-aaaa-567890123abc');
