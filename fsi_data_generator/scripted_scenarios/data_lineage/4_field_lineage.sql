-- =============================================
-- DATA GOVERNANCE EXECUTIVE FOCUSED - FIELD LINEAGE
-- =============================================

-- Field lineage showing how fields should be transformed with temporal evolution
INSERT INTO data_quality.field_lineage (
  field_lineage_id,
  field_name,
  description,
  input_fields,
  record_lineage_id
)
VALUES
  -- Version 1.0 field mappings (basic implementation)
  ('a1c8f9e0-1d2e-4f5a-bc6d-7e8f9a0b1c2d'::uuid, 'accountNumber', 'Basic mapping of account number', 'accountNumber', '12341234-1234-1234-1234-123412341234'),
  ('b2d9f0e1-2e3f-5a6b-cd7e-8f9a0b1c2d3e'::uuid, 'currentBalance', 'Simple balance mapping', 'currentBalance', '12341234-1234-1234-1234-123412341234'),
  ('c3e0f1a2-3f4a-6b7c-de8f-9a0b1c2d3e4f'::uuid, 'availableBalance', 'Simple available balance mapping', 'availableBalance', '12341234-1234-1234-1234-123412341234'),

  ('d4f1a2b3-4a5b-7c8d-ef9a-0b1c2d3e4f5a'::uuid, 'accountNumber', 'Basic mapping of account number', 'accountNumber', '23452345-2345-2345-2345-234523452345'),
  ('1fa2b3c4-5b6c-8d9e-f0a1-b2c3d4e5f6a7'::uuid, 'accountName', 'Simple account name mapping', 'nickname', '23452345-2345-2345-2345-234523452345'),
  ('2fb3c4d5-6c7d-9e0f-a1b2-c3d4e5f6a7b8'::uuid, 'accountType', 'Simple account type mapping', 'consumerBankingProduct.productType', '23452345-2345-2345-2345-234523452345'),

  ('2fc4d5e6-7d8e-0f1a-b2c3-d4e5f6a7b8c9'::uuid, 'transactionId', 'Basic mapping of transaction ID', 'consumerBankingTransactionId', '34563456-3456-3456-3456-345634563456'),
  ('3fd5e6f7-8e9f-1a2b-c3d4-e5f6a7b8c9d0'::uuid, 'amount', 'Simple transaction amount mapping', 'amount', '34563456-3456-3456-3456-345634563456'),
  ('c9e6f7a8-9f0a-2b3c-d4e5-f6a7b8c9d0e1'::uuid, 'transactionDate', 'Simple transaction date mapping', 'transactionDate', '34563456-3456-3456-3456-345634563456'),

  -- Version 1.1 field mappings (added compliance fields)
  ('4fe7a8b9-0a1b-3c4d-e5f6-a7b8c9d0e1f2'::uuid, 'accountNumber', 'Basic mapping of account number', 'accountNumber', '45674567-4567-4567-4567-456745674567'),
  ('e1a8b9c0-1b2c-4d5e-f6a7-b8c9d0e1f2a3'::uuid, 'maskedAccountNumber', 'Added masked version for compliance', 'accountNumber', '45674567-4567-4567-4567-456745674567'),
  ('5fb9c0d1-2c3d-5e6f-a7b8-c9d0e1f2a3b4'::uuid, 'currentBalance', 'Simple balance mapping', 'currentBalance', '45674567-4567-4567-4567-456745674567'),
  ('3dc0d1e2-3d4e-6f7a-b8c9-d0e1f2a3b4c5'::uuid, 'availableBalance', 'Simple available balance mapping', 'availableBalance', '45674567-4567-4567-4567-456745674567'),
  ('6fd1e2f3-4e5f-7a8b-c9d0-e1f2a3b4c5d6'::uuid, 'status', 'New compliance status field', 'status', '45674567-4567-4567-4567-456745674567'),

  -- Version 2.0 field mappings (enhanced security and currency standardization)
  ('4ce2f3a4-5f6a-8b9c-d0e1-f2a3b4c5d6e7'::uuid, 'accountNumber', 'Secure account number formatting', 'accountNumber', '78907890-7890-7890-7890-789078907890'),
  ('7fe3a4b5-6a7b-9c0d-e1f2-a3b4c5d6e7f8'::uuid, 'maskedAccountNumber', 'Enhanced security masking', 'accountNumber', '78907890-7890-7890-7890-789078907890'),
  ('e7a4b5c6-7b8c-0d1e-f2a3-b4c5d6e7f8a9'::uuid, 'currentBalance', 'Currency standardization', 'currentBalance', '78907890-7890-7890-7890-789078907890'),
  ('5fb5c6d7-8c9d-1e2f-a3b4-c5d6e7f8a9b0'::uuid, 'availableBalance', 'Currency standardization', 'availableBalance', '78907890-7890-7890-7890-789078907890'),
  ('a9c6d7e8-9d0e-2f3a-b4c5-d6e7f8a9b0c1'::uuid, 'status', 'Compliance status field', 'status', '78907890-7890-7890-7890-789078907890'),
  ('8fd7e8f9-0e1f-3a4b-c5d6-e7f8a9b0c1d2'::uuid, 'securityLevel', 'New security classification field', 'enterpriseAccount.accountOwnership.enterpriseParty.partyStatus', '78907890-7890-7890-7890-789078907890'),

  -- Version 2.1 field mappings (performance improvements and enhanced owner data)
  ('c1e8f9a0-1f2a-4b5c-d6e7-f8a9b0c1d2e3'::uuid, 'accountNumber', 'Optimized account number formatting', 'accountNumber', 'abcdabcd-abcd-abcd-abcd-abcdabcdabcd'),
  ('9fe9a0b1-2a3b-5c6d-e7f8-a9b0c1d2e3f4'::uuid, 'maskedAccountNumber', 'Optimized masking algorithm', 'accountNumber', 'abcdabcd-abcd-abcd-abcd-abcdabcdabcd'),
  ('e3a0b1c2-3b4c-6d7e-f8a9-b0c1d2e3f4a5'::uuid, 'currentBalance', 'Optimized currency standardization', 'currentBalance', 'abcdabcd-abcd-abcd-abcd-abcdabcdabcd'),
  ('0fb1c2d3-4c5d-7e8f-a9b0-c1d2e3f4a5b6'::uuid, 'availableBalance', 'Optimized currency standardization', 'availableBalance', 'abcdabcd-abcd-abcd-abcd-abcdabcdabcd'),

  ('6ac2d3e4-5d6e-8f9a-b0c1-d2e3f4a5b6c7'::uuid, 'transactionId', 'Optimized transaction ID formatting', 'consumerBankingTransactionId', 'cdef5678-cdef-5678-abcd-cdef5678abcd'),
  ('1fc3e4f5-6e7f-9a0b-c1d2-e3f4a5b6c7d8'::uuid, 'amount', 'Optimized currency standardization', 'amount', 'cdef5678-cdef-5678-abcd-cdef5678abcd'),
  ('c7e4f5a6-7f8a-0b1c-d2e3-f4a5b6c7d8e9'::uuid, 'transactionDate', 'Enhanced date standardization', 'transactionDate', 'cdef5678-cdef-5678-abcd-cdef5678abcd'),
  ('2fe5a6b7-8a9b-1c2d-e3f4-a5b6c7d8e9f0'::uuid, 'category', 'New categorization field', 'category', 'cdef5678-cdef-5678-abcd-cdef5678abcd'),

  ('7da6b7c8-9b0c-2d3e-f4a5-b6c7d8e9f0a1'::uuid, 'ledgerBalance', 'Optimized currency standardization', 'currentBalance', 'defabc90-defa-9012-abcd-defabc90abcd'),
  ('3fa7c8d9-0c1d-3e4f-a5b6-c7d8e9f0a1b2'::uuid, 'availableBalance', 'Optimized currency standardization', 'availableBalance', 'defabc90-defa-9012-abcd-defabc90abcd'),
  ('a1c8d9e0-1d2e-4f5a-b6c7-d8e9f0a1b2c3'::uuid, 'creditLimit', 'Added standardized credit limit', 'offers.amount', 'defabc90-defa-9012-abcd-defabc90abcd'),

  ('8eb9e0f1-2e3f-5a6b-c7d8-e9f0a1b2c3d4'::uuid, 'ownerName', 'Basic name formatting', 'name', 'efabc123-efab-1234-abcd-efabc123abcd'),
  ('4fa9f1a2-3f4a-6b7c-d8e9-f0a1b2c3d4e5'::uuid, 'ownerAddress', 'Basic address formatting', 'partyEntityAddresses.enterpriseAddress', 'efabc123-efab-1234-abcd-efabc123abcd'),
  ('5fafa2b3-4a5b-7c8d-e9f0-a1b2c3d4e5f6'::uuid, 'taxIdMasked', 'Basic tax ID masking', 'ssn', 'efabc123-efab-1234-abcd-efabc123abcd'),

  -- Current version 5.0 field mappings (FDX 5.0 compliance)
  ('9fa2b3c4-5b6c-8d9e-f0a1-b2c3d4e5f6a7'::uuid, 'accountNumber', 'FDX 5.0 account number formatting', 'accountNumber', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('6fafb4d5-6c7d-9e0f-a1b2-c3d4e5f6a7b8'::uuid, 'maskedAccountNumber', 'FDX 5.0 compliant masking', 'accountNumber', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('10c4d5e6-7d8e-0f1a-b2c3-d4e5f6a7b8c9'::uuid, 'currentBalance', 'FDX 5.0 compliant balance format', 'currentBalance', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('7fafe6f7-8e9f-1a2b-c3d4-e5f6a7b8c9d0'::uuid, 'availableBalance', 'FDX 5.0 compliant available balance format', 'availableBalance', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),

  ('11e6f7a8-9f0a-2b3c-d4e5-f6a7b8c9d0e1'::uuid, 'accountNumber', 'FDX 5.0 account number formatting', 'accountNumber', 'abc45678-abc4-5678-abcd-abc45678abcd'),
  ('8fafa8b9-0a1b-3c4d-e5f6-a7b8c9d0e1f2'::uuid, 'accountName', 'FDX 5.0 account name formatting', 'nickname', 'abc45678-abc4-5678-abcd-abc45678abcd'),
  ('12a8b9c0-1b2c-4d5e-f6a7-b8c9d0e1f2a3'::uuid, 'accountType', 'FDX 5.0 standardized account type', 'consumerBankingProduct.productType', 'abc45678-abc4-5678-abcd-abc45678abcd'),

  ('9fafc0d1-2c3d-5e6f-a7b8-c9d0e1f2a3b4'::uuid, 'transactionId', 'FDX 5.0 transaction ID formatting', 'consumerBankingTransactionId', 'bc567890-bc56-7890-abcd-bc567890abcd'),
  ('13c0d1e2-3d4e-6f7a-b8c9-d0e1f2a3b4c5'::uuid, 'amount', 'FDX 5.0 transaction amount formatting', 'amount', 'bc567890-bc56-7890-abcd-bc567890abcd'),
  ('0fafd1e2-4e5f-7a8b-c9d0-e1f2a3b4c5d6'::uuid, 'transactionDate', 'FDX 5.0 transaction date formatting', 'transactionDate', 'bc567890-bc56-7890-abcd-bc567890abcd'),

  ('14e2f3a4-5f6a-8b9c-d0e1-f2a3b4c5d6e7'::uuid, 'ledgerBalance', 'FDX 5.0 current balance formatting', 'currentBalance', 'c6789012-c678-9012-abcd-c6789012abcd'),
  ('1fafe3a4-6a7b-9c0d-e1f2-a3b4c5d6e7f8'::uuid, 'availableBalance', 'FDX 5.0 available balance formatting', 'availableBalance', 'c6789012-c678-9012-abcd-c6789012abcd'),
  ('15a4b5c6-7b8c-0d1e-f2a3-b4c5d6e7f8a9'::uuid, 'creditLimit', 'FDX 5.0 credit limit formatting', 'offers.amount', 'c6789012-c678-9012-abcd-c6789012abcd'),

  ('2fafc6d7-8c9d-1e2f-a3b4-c5d6e7f8a9b0'::uuid, 'ownerName', 'FDX 5.0 owner name formatting', 'name', 'd7890123-d789-0123-abcd-d7890123abcd'),
  ('16c6d7e8-9d0e-2f3a-b4c5-d6e7f8a9b0c1'::uuid, 'ownerAddress', 'FDX 5.0 owner address formatting', 'partyEntityAddresses.enterpriseAddress', 'd7890123-d789-0123-abcd-d7890123abcd'),
  ('3fafe7e8-0e1f-3a4b-c5d6-e7f8a9b0c1d2'::uuid, 'taxIdMasked', 'FDX 5.0 tax ID masking', 'ssn', 'd7890123-d789-0123-abcd-d7890123abcd'),

  -- Additional field lineage records for detailed mapping (added for v5.0)
  ('17e8f9a0-1f2a-4b5c-d6e7-f8a9b0c1d2e3'::uuid, 'accountId', 'Maps the numeric consumer banking account ID to a string for FDX format', 'consumerBankingAccountId', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('4fafe9a0-2a3b-5c6d-e7f8-a9b0c1d2e3f4'::uuid, 'accountCategory', 'Maps product type to FDX account category based on predefined rules', 'consumerBankingProduct.productType', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('18a0b1c2-3b4c-6d7e-f8a9-b0c1d2e3f4a5'::uuid, 'nickname', 'Direct mapping of account nickname to FDX nickname', 'nickname', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('5fafb1c2-4c5d-7e8f-a9b0-c1d2e3f4a5b6'::uuid, 'status', 'Converts consumer banking status to FDX status using defined mapping rules', 'status', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('19c2d3e4-5d6e-8f9a-b0c1-d2e3f4a5b6c7'::uuid, 'currency.code', 'Maps the currency code to FDX format', 'currency.currencyCode', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('6fafd3e4-6e7f-9a0b-c1d2-e3f4a5b6c7d8'::uuid, 'openDate', 'Maps account opening date to FDX format', 'openedDate', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('20e4f5a6-7f8a-0b1c-d2e3-f4a5b6c7d8e9'::uuid, 'productName', 'Direct mapping of product name to FDX format', 'consumerBankingProduct.productName', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('7fafe5a6-8a9b-1c2d-e3f4-a5b6c7d8e9f0'::uuid, 'interestRate', 'Maps interest rate to FDX format', 'consumerBankingProduct.baseInterestRate', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('21a6b7c8-9b0c-2d3e-f4a5-b6c7d8e9f0a1'::uuid, 'interestYtd', 'Maps year-to-date interest to FDX format', 'interestYtd', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('8fafa7c8-0c1d-3e4f-a5b6-c7d8e9f0a1b2'::uuid, 'term', 'Maps account term (for CDs) to FDX format with rounding to 1 decimal place', 'term', 'fabc4567-fabc-4567-abcd-fabc4567abcd'),
  ('22c8d9e0-1d2e-4f5a-b6c7-d8e9f0a1b2c3'::uuid, 'maturityDate', 'Maps maturity date to RFC standard date string format', 'maturityDate', 'fabc4567-fabc-4567-abcd-fabc4567abcd');
