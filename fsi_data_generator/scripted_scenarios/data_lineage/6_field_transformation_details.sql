-- =============================================
-- DATA QUALITY EXECUTIVE FOCUSED - FIELD TRANSFORMATION DETAILS
-- =============================================

-- Field transformation details showing specific field transformations
INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  ('a1c8f9e0-1d2e-4f5a-bc6d-7e8f9a0b1c2d'::uuid, 'Format standardization to FDX', 'accountNumber', '1234567890', 'accountNumber', '1234567890', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'),
  ('b2d9f0e1-2e3f-5a6b-cd7e-8f9a0b1c2d3e'::uuid, 'Data masking for FDX exposure', 'accountNumber', '1234567890', 'maskedAccountNumber', 'XXXX7890', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'),
  ('c3e0f1a2-3f4a-6b7c-de8f-9a0b1c2d3e4f'::uuid, 'Currency conversion to FDX format', 'currentBalance', '1000.00', 'currentBalance', '1000.00', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'),
  ('d4f1a2b3-4a5b-7c8d-ef9a-0b1c2d3e4f5a'::uuid, 'Currency code for FDX format', 'currency.code', 'USD', 'currencyCode', 'USD', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1');

-- Add more field transformation details in chunks to prevent issues
INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  ('e5a2b3c4-5b6c-8d9e-f0a1-b2c3d4e5f6a7'::uuid, 'Format standardization to FDX', 'accountNumber', '9876543210', 'accountNumber', '9876543210', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('f6b3c4d5-6c7d-9e0f-a1b2-c3d4e5f6a789'::uuid, 'Data masking for FDX exposure', 'accountNumber', '9876543210', 'maskedAccountNumber', 'XXXX3210', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('a7c4d5e6-7d8e-0f1a-b2c3-d4e5f6a7b8c9'::uuid, 'Currency conversion to FDX format', 'currentBalance', '500.00', 'currentBalance', '500.00', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('b8d5e6f7-8e9f-1a2b-c3d4-e5f6a7b8c912'::uuid, 'Currency code for FDX format', 'currency.code', 'EUR', 'currencyCode', 'EUR', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1'),
  ('c9e6f7a8-9f0a-2b3c-d4e5-f6a7b8c9d0e1'::uuid, 'Format standardization to FDX', 'availableBalance', '450.00', 'availableBalance', '450.00', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1');

INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  ('d0f7a8b9-0a1b-3c4d-e5f6-a7b8c9d0e123'::uuid, 'PII standardization to FDX', 'enterpriseAccount.accountOwnership.enterpriseParty.name', 'John Smith', 'ownerName', 'SMITH, JOHN', 'c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1'),
  ('e1a8b9c0-1b2c-4d5e-f6a7-b8c9d0e1f2a3'::uuid, 'Address normalization to FDX', 'enterpriseAccount.accountOwnership.enterpriseParty.partyEntityAddresses.enterpriseAddress', '{"streetName":"123 Main St","unitNumber":"Apt 4","townName":"Anytown","countrySubDivision":"CA","postCode":"90210"}', 'ownerAddress', '123 MAIN ST, APT 4, ANYTOWN, CA 90210', 'c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1'),
  ('f2b9c0d1-2c3d-5e6f-a7b8-c9d0e1f2a345'::uuid, 'Tax ID masking for FDX exposure', 'enterpriseAccount.accountOwnership.enterpriseParty.ssn', '123-45-6789', 'taxIdMasked', 'XXX-XX-6789', 'c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1');

INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  ('a3c0d1e2-3d4e-6f7a-b8c9-d0e1f2a3b4c5'::uuid, 'Format standardization to FDX', 'accountNumber', '2468135790', 'accountNumber', '2468135790', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'),
  ('b4d1e2f3-4e5f-7a8b-c9d0-e1f2a3b4c567'::uuid, 'Data masking for FDX exposure', 'accountNumber', '2468135790', 'maskedAccountNumber', 'XXXX5790', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'),
  ('c5e2f3a4-5f6a-8b9c-d0e1-f2a3b4c5d6e7'::uuid, 'Format standardization to FDX', 'currentBalance', '2500.00', 'currentBalance', '2500.00', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1'),
  ('d6f3a4b5-6a7b-9c0d-e1f2-a3b4c5d6e789'::uuid, 'Currency code for FDX format', 'currency.code', 'USD', 'currencyCode', 'USD', 'd1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1');

INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  ('e7a4b5c6-7b8c-0d1e-f2a3-b4c5d6e7f890'::uuid, 'Format standardization to FDX', 'currentBalance', '1200.00', 'currentBalance', '1200.00', 'e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1'),
  ('f8b5c6d7-8c9d-1e2f-a3b4-c5d6e7f8a901'::uuid, 'Currency code for FDX format', 'currency.code', 'USD', 'currencyCode', 'USD', 'e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1'),
  ('a9c6d7e8-9d0e-2f3a-b4c5-d6e7f8a9b0c1'::uuid, 'Format standardization to FDX', 'availableBalance', '1150.00', 'availableBalance', '1150.00', 'e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1');

-- Balance transformations
INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  ('b0d7e8f9-0e1f-3a4b-c5d6-e7f8a9b0c123'::uuid, 'Currency conversion to FDX format', 'currentBalance', '1000.00', 'ledgerBalance', '1000.00', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'),
  ('c1e8f9a0-1f2a-4b5c-d6e7-f8a9b0c1d2e3'::uuid, 'Currency code for FDX format', 'currency.code', 'EUR', 'currencyCode', 'EUR', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'),
  ('d2f9a0b1-2a3b-5c6d-e7f8-a9b0c1d2e345'::uuid, 'Currency conversion to FDX format', 'availableBalance', '950.00', 'availableBalance', '950.00', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1'),
  ('e3a0b1c2-3b4c-6d7e-f8a9-b0c1d2e3f456'::uuid, 'Date format standardization to FDX', 'dateTime', '2025-03-03 09:30:00', 'balanceDate', '2025-03-03T09:30:00Z', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1');

-- Owner transformations from enterprise party
INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  ('f4b1c2d3-4c5d-7e8f-a9b0-c1d2e3f4a567'::uuid, 'Name parsing and normalization to FDX', 'name', 'Jane Doe', 'ownerName', 'DOE, JANE MARIE', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('a5c2d3e4-5d6e-8f9a-b0c1-d2e3f4a5b678'::uuid, 'Name components for FDX format', 'customerDemographics.customerLifetimeValue', '50000.00', 'middleName', 'MARIE', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('b6d3e4f5-6e7f-9a0b-c1d2-e3f4a5b6c789'::uuid, 'Name components for FDX format', 'name', 'Jane Doe', 'lastName', 'DOE', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('c7e4f5a6-7f8a-0b1c-d2e3-f4a5b6c7d890'::uuid, 'Address parsing and standardization to FDX', 'partyEntityAddresses.enterpriseAddress.streetName', '456 Broadway St', 'ownerAddress', '456 BROADWAY ST, STE 7B, NEW YORK, NY 10013', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('d8f5a6b7-8a9b-1c2d-e3f4-a5b6c7d8e901'::uuid, 'Address components for FDX format', 'partyEntityAddresses.enterpriseAddress.unitNumber', 'Suite 7B', 'addressLine2', 'STE 7B', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('e9a6b7c8-9b0c-2d3e-f4a5-b6c7d8e9f0a1'::uuid, 'Address components for FDX format', 'partyEntityAddresses.enterpriseAddress.townName', 'New York', 'city', 'NEW YORK', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('f0b7c8d9-0c1d-3e4f-a5b6-c7d8e9f0a123'::uuid, 'Address components for FDX format', 'partyEntityAddresses.enterpriseAddress.countrySubDivision', 'NY', 'state', 'NY', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2'),
  ('a1c8d9e0-1d2e-4f5a-b6c7-d8e9f0a1b234'::uuid, 'Address components for FDX format', 'partyEntityAddresses.enterpriseAddress.postCode', '10013', 'postalCode', '10013', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2');

-- Transaction transformations
INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  ('b2d9e0f1-2e3f-5a6b-c7d8-e9f0a1b2c345'::uuid, 'Transaction categorization for FDX format', 'transactionBankTransactionCodes.code', 'RETAIL__GROCERY', 'description', 'WHOLEFDS NYC 10010', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('c3e0f1a2-3f4a-6b7c-d8e9-f0a1b2c3d456'::uuid, 'Transaction categorization for FDX format', 'transactionBankTransactionCodes.code', 'SERVICES__UTILITIES', 'description', 'AMAZONPRIME', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('d4f1a2b3-4a5b-7c8d-e9f0-a1b2c3d4e567'::uuid, 'Transaction categorization for FDX format', 'transactionBankTransactionCodes.code', 'SERVICES__TRAVEL', 'description', 'UBER TRIP', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('e5a2b3c4-5b6c-8d9e-f0a1-b2c3d4e5f678'::uuid, 'Amount sign standardization for FDX format', 'amount', '25.00', 'amount', '-25.00', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3'),
  ('f6b3c4d5-6c7d-9e0f-a1b2-c3d4e5f6a890'::uuid, 'Transaction type determination for FDX format', 'transactionType', 'DEBIT', 'type', 'DEBIT', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3');

-- Multi-account aggregation
INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  ('a7c4d5e6-7d8e-0f1a-b2c3-d4e5f6a7b901'::uuid, 'Account balances aggregation to FDX format', 'currentBalance', '1500.00', 'currentBalance', '1500.00', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('b8d5e6f7-8e9f-1a2b-c3d4-e5f6a7b8c023'::uuid, 'Additional account balance', 'enterpriseAccount.accountOwnership.enterprisePartyId', '24681', 'relatedAccounts', '[{"accountId":"A24681","currentBalance":2500.00}]', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('c9e6f7a8-9f0a-2b3c-d4e5-f6a7b8c9d134'::uuid, 'Account available balances aggregation to FDX format', 'availableBalance', '1450.00', 'availableBalance', '1450.00', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('d0f7a8b9-0a1b-3c4d-e5f6-a7b8c9d0e245'::uuid, 'Additional account available balance', 'enterpriseAccount.accountOwnership.enterprisePartyId', '24681', 'relatedAccountsAvailable', '[{"accountId":"A24681","availableBalance":2400.00}]', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('e1a8b9c0-1b2c-4d5e-f6a7-b8c9d0e1f356'::uuid, 'Account type grouping for FDX format', 'consumerBankingProduct.productType', 'CHECKING', 'accountType', 'CHECKING', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4'),
  ('f2b9c0d1-2c3d-5e6f-a7b8-c9d0e1f2a467'::uuid, 'Additional account type', 'enterpriseAccount.accountOwnership.enterprisePartyId', '24681', 'relatedAccountTypes', '[{"accountId":"A24681","accountType":"SAVINGS"}]', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4');

-- Complete account transformation
INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  ('a3c0d1e2-3d4e-6f7a-b8c9-d0e1f2a3b567'::uuid, 'Account data consolidation to FDX format', 'accountNumber', '13579', 'accountNumber', '13579', 'a5a5a5a5-a5a5a5a5-a5a5-a5a5a5a5a5a5'),
  ('b4d1e2f3-4e5f-7a8b-c9d0-e1f2a3b4c678'::uuid, 'Account type extraction', 'consumerBankingProduct.productType', 'MONEY_MARKET', 'accountType', 'INVESTMENT', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('c5e2f3a4-5f6a-8b9c-d0e1-f2a3b4c5d789'::uuid, 'Account status extraction', 'status', 'ACTIVE', 'status', 'ACTIVE', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('d6f3a4b5-6a7b-9c0d-e1f2-a3b4c5d6e890'::uuid, 'Balance data consolidation to FDX format', 'currentBalance', '35000.00', 'currentBalance', '35000.00', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('e7a4b5c6-7b8c-0d1e-f2a3-b4c5d6e7f901'::uuid, 'Available balance extraction', 'availableBalance', '35000.00', 'availableBalance', '35000.00', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('f8b5c6d7-8c9d-1e2f-a3b4-c5d6e7f8a012'::uuid, 'Pending balance extraction', 'balances.amount', '0.00', 'pendingBalance', '0.00', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('a9c6d7e8-9d0e-2f3a-b4c5-d6e7f8a9b123'::uuid, 'Owner data consolidation to FDX format', 'enterpriseAccount.accountOwnership.enterpriseParty.name', 'Robert J Smith', 'ownerName', 'SMITH, ROBERT J', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('b0d7e8f9-0e1f-3a4b-c5d6-e7f8a9b0c234'::uuid, 'Owner email extraction', 'enterpriseAccount.accountOwnership.enterpriseParty.emailAddress', 'robert.smith@example.com', 'email', 'robert.smith@example.com', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('c1e8f9a0-1f2a-4b5c-d6e7-f8a9b0c1d345'::uuid, 'Owner phone extraction', 'enterpriseAccount.accountOwnership.enterpriseParty.phone', '212-555-1234', 'phoneNumber', '212-555-1234', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5');

-- Additional field transformations for the latest version
INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  -- accountId transformation
  ('d2f9a0b1-2a3b-5c6d-e7f8-a9b0c1d2e456'::uuid, 'Convert numeric ID to string', 'consumerBankingAccountId', '135790', 'accountId', '135790', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),

  -- accountCategory transformation
  ('e3a0b1c2-3b4c-6d7e-f8a9-b0c1d2e3f567'::uuid, 'Map product type to FDX account category', 'consumerBankingProduct.productType', 'CHECKING', 'accountCategory', 'DEPOSIT_ACCOUNT', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('f4b1c2d3-4c5d-7e8f-a9b0-c1d2e3f4a678'::uuid, 'Map product type to FDX account category', 'consumerBankingProduct.productType', 'MONEY_MARKET', 'accountCategory', 'INVESTMENT_ACCOUNT', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('a5c2d3e4-5d6e-8f9a-b0c1-d2e3f4a5b789'::uuid, 'Map product type to FDX account category', 'consumerBankingProduct.productType', 'HSA', 'accountCategory', 'INSURANCE_ACCOUNT', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('b6d3e4f5-6e7f-9a0b-c1d2-e3f4a5b6c890'::uuid, 'Map product type to FDX account category', 'consumerBankingProduct.productType', 'BUSINESS_CHECKING', 'accountCategory', 'COMMERCIAL_ACCOUNT', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5');

-- Final set of transformations
INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  -- nickname transformation
  ('c7e4f5a6-7f8a-0b1c-d2e3-f4a5b6c7d912'::uuid, 'Direct mapping of nickname field', 'nickname', 'My Savings', 'nickname', 'My Savings', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),

  -- status transformation
  ('d8f5a6b7-8a9b-1c2d-e3f4-a5b6c7d8e123'::uuid, 'Convert OB status to FDX status', 'status', 'ACTIVE', 'status', 'OPEN', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('e9a6b7c8-9b0c-2d3e-f4a5-b6c7d8e9f234'::uuid, 'Convert OB status to FDX status', 'status', 'PENDING', 'status', 'PENDINGOPEN', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('f0b7c8d9-0c1d-3e4f-a5b6-c7d8e9f0a345'::uuid, 'Convert OB status to FDX status', 'status', 'INACTIVE', 'status', 'RESTRICTED', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),
  ('a1c8d9e0-1d2e-4f5a-b6c7-d8e9f0a1b456'::uuid, 'Convert OB status to FDX status', 'status', 'CLOSED', 'status', 'CLOSED', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5');

-- More transformations
INSERT INTO data_quality.field_transformation_details (
  field_transformation_detail_id,
  transform_description,
  input_field_name,
  input_field_value,
  output_field_name,
  output_field_value,
  record_transformation_id
)
VALUES
  -- currencyCode transformation
  ('b2d9e0f1-2e3f-5a6b-c7d8-e9f0a1b2c567'::uuid, 'Map currency code to FDX format', 'currency.code', 'USD', 'currency.currencyCode', 'USD', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),

  -- openDate transformation
  ('c3e0f1a2-3f4a-6b7c-d8e9-f0a1b2c3d678'::uuid, 'Format open date to FDX standard', 'openedDate', '2024-01-15T08:30:00Z', 'openDate', '2024-01-15', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),

  -- productName transformation
  ('d4f1a2b3-4a5b-7c8d-e9f0-a1b2c3d4e789'::uuid, 'Direct mapping of product name', 'consumerBankingProduct.productName', 'Premium Checking', 'productName', 'Premium Checking', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),

  -- interestRate transformation
  ('e5a2b3c4-5b6c-8d9e-f0a1-b2c3d4e5f890'::uuid, 'Map base interest rate to FDX format', 'consumerBankingProduct.baseInterestRate', '0.0125', 'interestRate', '0.0125', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),

  -- interestYtd transformation
  ('f6b3c4d5-6c7d-9e0f-a1b2-c3d4e5f6a901'::uuid, 'Map year-to-date interest to FDX format', 'interestYtd', '125.75', 'interestYtd', '125.75', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),

  -- term transformation (for CDs)
  ('a7c4d5e6-7d8e-0f1a-b2c3-d4e5f6a7b012'::uuid, 'Map account term with rounding to 1 decimal place', 'term', '12.0', 'term', '12.0', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5'),

  -- maturityDate transformation (for CDs)
  ('b8d5e6f7-8e9f-1a2b-c3d4-e5f6a7b8c123'::uuid, 'Convert maturity date to FDX format', 'maturityDate', '2025-01-15T00:00:00Z', 'maturityDate', '2025-01-15', 'a5a5a5a5-a5a5-a5a5-a5a5-a5a5a5a5a5a5');
