-- =============================================
-- DATA GOVERNANCE EXECUTIVE FOCUSED - API LINEAGE
-- =============================================

-- API lineage records showing the designed data flows and their evolution over time with realistic overlapping versions
INSERT INTO data_quality.api_lineage (
  api_lineage_id,
  app_mgmt_application_id,
  server_name,
  major_version,
  minor_version,
  api_call,
  query,
  description,
  start_date,
  end_date,
  updated_at
)
WITH app_id AS (
  SELECT app_mgmt_application_id
  FROM app_mgmt.applications
  WHERE application_name = 'FDX API Gateway'
)
SELECT
  '11111111-1111-1111-aaaa-111111111111',
  app_mgmt_application_id,
  'fdx-gateway',
  1,
  0,
  'GET /fdx/v1/accounts',
  'query FDX_Core_Accounts($cb_enterpriseAccountId: [ConsumerBanking_Int4!]!) {
  consumerBankingAccounts(
    where: {status: {_in: [ACTIVE]}, enterpriseAccountId: {_in: $cb_enterpriseAccountId}}
    order_by: {accountNumber: Asc}
  ) {
    consumerBankingProduct {
      productName
      productType
      baseInterestRate
    }
    consumerBankingAccountId
    accountNumber
    nickname
    displayName
    openingDayBalance
    currentBalance
    availableBalance
    interestYtd
    annualPercentageYield
    maturityDate
    term
    status
    currency {
      code
    }
    enterpriseAccount {
      enterpriseAccountId
    }
  }
}',
  'Standard account information delivery flow',
  '2024-01-01 00:00:00'::timestamptz,
  '2024-06-30 23:59:59'::timestamptz,
  '2024-01-01 10:00:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  '22222222-2222-2222-aaaa-222222222222',
  app_mgmt_application_id,
  'fdx-gateway',
  1,
  0,
  'GET /fdx/v1/accounts/{accountId}',
  'query FDX_Core_Account_Details($accountId: String!) {
  consumerBankingAccounts(
    where: {accountNumber: {_eq: $accountId}}
    limit: 1
  ) {
    consumerBankingProduct {
      productName
      productType
      baseInterestRate
    }
    consumerBankingAccountId
    accountNumber
    nickname
    displayName
    openingDayBalance
    currentBalance
    availableBalance
    interestYtd
    annualPercentageYield
    maturityDate
    term
    status
    openedDate
    currency {
      code
    }
    enterpriseAccount {
      enterpriseAccountId
    }
  }
}',
  'Individual account detail delivery flow',
  '2024-01-01 00:00:00'::timestamptz,
  '2024-06-30 23:59:59'::timestamptz,
  '2024-01-01 10:05:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  '33333333-3333-3333-aaaa-333333333333',
  app_mgmt_application_id,
  'fdx-gateway',
  1,
  0,
  'GET /fdx/v1/accounts/{accountId}/transactions',
  'query FDX_Core_Transactions($account_id: String!, $startTime: String!, $endTime: String!) {
  consumerBankingTransactions(
    where: {
      consumerBankingAccount: {accountNumber: {_eq: $account_id}},
      transactionDate: {_gte: $startTime, _lte: $endTime}
    }
    order_by: {transactionDate: Desc}
  ) {
    consumerBankingTransactionId
    transactionReference
    amount
    currency {
      code
    }
    creditDebitIndicator
    status
    transactionDate
    valueDate
    description
    category
    transactionType
  }
}',
  'Account transaction history delivery flow',
  '2024-01-01 00:00:00'::timestamptz,
  '2024-06-30 23:59:59'::timestamptz,
  '2024-01-01 10:10:00'::timestamptz
FROM app_id
UNION ALL
-- Version 1.1 API lineage (added fields for compliance) - note overlapping with v1.0 for 3 months
SELECT
  '44444444-4444-4444-aaaa-444444444444',
  app_mgmt_application_id,
  'fdx-gateway',
  1,
  1,
  'GET /fdx/v1_1/accounts',
  'query FDX_Core_Accounts($cb_enterpriseAccountId: [ConsumerBanking_Int4!]!) {
  consumerBankingAccounts(
    where: {status: {_in: [ACTIVE]}, enterpriseAccountId: {_in: $cb_enterpriseAccountId}}
    order_by: {accountNumber: Asc}
  ) {
    consumerBankingProduct {
      productName
      productType
      baseInterestRate
    }
    consumerBankingAccountId
    accountNumber
    nickname
    displayName
    openingDayBalance
    currentBalance
    availableBalance
    interestYtd
    annualPercentageYield
    maturityDate
    term
    status
    currency {
      code
    }
    enterpriseAccount {
      enterpriseAccountId
    }
  }
}',
  'Standard account information delivery flow with added compliance fields',
  '2024-03-01 00:00:00'::timestamptz,
  '2024-09-30 23:59:59'::timestamptz,
  '2024-03-01 09:00:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  '55555555-5555-5555-aaaa-555555555555',
  app_mgmt_application_id,
  'fdx-gateway',
  1,
  1,
  'GET /fdx/v1_1/accounts/{accountId}',
  'query FDX_Core_Account_Details($accountId: String!) {
  consumerBankingAccounts(
    where: {accountNumber: {_eq: $accountId}}
    limit: 1
  ) {
    consumerBankingProduct {
      productName
      productType
      baseInterestRate
    }
    consumerBankingAccountId
    accountNumber
    nickname
    displayName
    openingDayBalance
    currentBalance
    availableBalance
    interestYtd
    annualPercentageYield
    maturityDate
    term
    status
    openedDate
    currency {
      code
    }
    enterpriseAccount {
      enterpriseAccountId
    }
  }
}',
  'Individual account detail delivery flow with added compliance fields',
  '2024-03-01 00:00:00'::timestamptz,
  '2024-09-30 23:59:59'::timestamptz,
  '2024-03-01 09:05:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  '66666666-6666-6666-aaaa-666666666666',
  app_mgmt_application_id,
  'fdx-gateway',
  1,
  1,
  'GET /fdx/v1_1/accounts/{accountId}/transactions',
  'query FDX_Core_Transactions($account_id: String!, $startTime: String!, $endTime: String!) {
  consumerBankingTransactions(
    where: {
      consumerBankingAccount: {accountNumber: {_eq: $account_id}},
      transactionDate: {_gte: $startTime, _lte: $endTime}
    }
    order_by: {transactionDate: Desc}
  ) {
    consumerBankingTransactionId
    transactionReference
    amount
    currency {
      code
    }
    creditDebitIndicator
    status
    transactionDate
    valueDate
    description
    category
    transactionType
  }
}',
  'Account transaction history delivery flow with added compliance fields',
  '2024-03-01 00:00:00'::timestamptz,
  '2024-09-30 23:59:59'::timestamptz,
  '2024-03-01 09:10:00'::timestamptz
FROM app_id
UNION ALL
-- Version 2.0 API lineage (major revision with enhanced security) - note overlapping with v1.1 for 3 months
SELECT
  '77777777-7777-7777-aaaa-777777777777',
  app_mgmt_application_id,
  'fdx-gateway',
  2,
  0,
  'GET /fdx/v2/accounts',
  'query FDX_Core_Accounts($cb_enterpriseAccountId: [ConsumerBanking_Int4!]!) {
  consumerBankingAccounts(
    where: {status: {_in: [ACTIVE]}, enterpriseAccountId: {_in: $cb_enterpriseAccountId}}
    order_by: {accountNumber: Asc}
  ) {
    consumerBankingProduct {
      productName
      productType
      baseInterestRate
    }
    consumerBankingAccountId
    accountNumber
    nickname
    displayName
    openingDayBalance
    currentBalance
    availableBalance
    interestYtd
    annualPercentageYield
    maturityDate
    term
    status
    currency {
      code
    }
    enterpriseAccount {
      enterpriseAccountId
    }
  }
}',
  'Enhanced security account information delivery flow',
  '2024-06-01 00:00:00'::timestamptz,
  '2024-12-31 23:59:59'::timestamptz,
  '2024-06-01 08:30:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  '88888888-8888-8888-aaaa-888888888888',
  app_mgmt_application_id,
  'fdx-gateway',
  2,
  0,
  'GET /fdx/v2/accounts/{accountId}',
  'query FDX_Core_Account_Details($accountId: String!) {
  consumerBankingAccounts(
    where: {accountNumber: {_eq: $accountId}}
    limit: 1
  ) {
    consumerBankingProduct {
      productName
      productType
      baseInterestRate
    }
    consumerBankingAccountId
    accountNumber
    nickname
    displayName
    openingDayBalance
    currentBalance
    availableBalance
    interestYtd
    annualPercentageYield
    maturityDate
    term
    status
    openedDate
    currency {
      code
    }
    enterpriseAccount {
      enterpriseAccountId
    }
  }
}',
  'Enhanced security account detail delivery flow',
  '2024-06-01 00:00:00'::timestamptz,
  '2024-12-31 23:59:59'::timestamptz,
  '2024-06-01 08:35:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  '99999999-9999-9999-aaaa-999999999999',
  app_mgmt_application_id,
  'fdx-gateway',
  2,
  0,
  'GET /fdx/v2/accounts/{accountId}/transactions',
  'query FDX_Core_Transactions($account_id: String!, $startTime: String!, $endTime: String!) {
  consumerBankingTransactions(
    where: {
      consumerBankingAccount: {accountNumber: {_eq: $account_id}},
      transactionDate: {_gte: $startTime, _lte: $endTime}
    }
    order_by: {transactionDate: Desc}
  ) {
    consumerBankingTransactionId
    transactionReference
    amount
    currency {
      code
    }
    creditDebitIndicator
    status
    transactionDate
    valueDate
    description
    category
    transactionType
  }
}',
  'Enhanced security transaction history delivery flow',
  '2024-06-01 00:00:00'::timestamptz,
  '2024-12-31 23:59:59'::timestamptz,
  '2024-06-01 08:40:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  app_mgmt_application_id,
  'fdx-gateway',
  2,
  0,
  'GET /fdx/v2/accounts/{accountId}/balances',
  'query FDX_Core_AccountBalances($account_id: String!) {
  consumerBankingBalances(
    where: {consumerBankingAccount: {accountNumber: {_eq: $account_id}}}
    order_by: {dateTime: Desc}
    limit: 1
  ) {
    consumerBankingBalanceId
    creditDebitIndicator
    type
    dateTime
    amount
    currency {
      code
    }
    subType
  }
}',
  'Enhanced security balance information delivery flow',
  '2024-06-01 00:00:00'::timestamptz,
  '2024-12-31 23:59:59'::timestamptz,
  '2024-06-01 08:45:00'::timestamptz
FROM app_id
UNION ALL
-- Version 2.1 API lineage (added owner endpoint and performance improvements) - note overlapping with v2.0 for 3 months
SELECT
  'bbbbbbbb-bbbb-bbbb-aaaa-bbbbbbbbbbbb',
  app_mgmt_application_id,
  'fdx-gateway',
  2,
  1,
  'GET /fdx/v2_1/accounts',
  'query FDX_Core_Accounts($cb_enterpriseAccountId: [ConsumerBanking_Int4!]!) {
  consumerBankingAccounts(
    where: {status: {_in: [ACTIVE]}, enterpriseAccountId: {_in: $cb_enterpriseAccountId}}
    order_by: {accountNumber: Asc}
  ) {
    consumerBankingProduct {
      productName
      productType
      baseInterestRate
    }
    consumerBankingAccountId
    accountNumber
    nickname
    displayName
    openingDayBalance
    currentBalance
    availableBalance
    interestYtd
    annualPercentageYield
    maturityDate
    term
    status
    currency {
      code
    }
    enterpriseAccount {
      enterpriseAccountId
    }
  }
}',
  'Performance optimized account information delivery flow',
  '2024-09-01 00:00:00'::timestamptz,
  '2025-03-31 23:59:59'::timestamptz,
  '2024-09-01 11:30:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  'cccccccc-cccc-cccc-aaaa-cccccccccccc',
  app_mgmt_application_id,
  'fdx-gateway',
  2,
  1,
  'GET /fdx/v2_1/accounts/{accountId}',
  'query FDX_Core_Account_Details($accountId: String!) {
  consumerBankingAccounts(
    where: {accountNumber: {_eq: $accountId}}
    limit: 1
  ) {
    consumerBankingProduct {
      productName
      productType
      baseInterestRate
    }
    consumerBankingAccountId
    accountNumber
    nickname
    displayName
    openingDayBalance
    currentBalance
    availableBalance
    interestYtd
    annualPercentageYield
    maturityDate
    term
    status
    openedDate
    currency {
      code
    }
    enterpriseAccount {
      enterpriseAccountId
    }
  }
}',
  'Performance optimized account detail delivery flow',
  '2024-09-01 00:00:00'::timestamptz,
  '2025-03-31 23:59:59'::timestamptz,
  '2024-09-01 11:35:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  'dddddddd-dddd-dddd-aaaa-dddddddddddd',
  app_mgmt_application_id,
  'fdx-gateway',
  2,
  1,
  'GET /fdx/v2_1/accounts/{accountId}/transactions',
  'query FDX_Core_Transactions($account_id: String!, $startTime: String!, $endTime: String!) {
  consumerBankingTransactions(
    where: {
      consumerBankingAccount: {accountNumber: {_eq: $account_id}},
      transactionDate: {_gte: $startTime, _lte: $endTime}
    }
    order_by: {transactionDate: Desc}
  ) {
    consumerBankingTransactionId
    transactionReference
    amount
    currency {
      code
    }
    creditDebitIndicator
    status
    transactionDate
    valueDate
    description
    category
    transactionType
  }
}',
  'Performance optimized transaction history delivery flow',
  '2024-09-01 00:00:00'::timestamptz,
  '2025-03-31 23:59:59'::timestamptz,
  '2024-09-01 11:40:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  'eeeeeeee-eeee-eeee-aaaa-eeeeeeeeeeee',
  app_mgmt_application_id,
  'fdx-gateway',
  2,
  1,
  'GET /fdx/v2_1/accounts/{accountId}/balances',
  'query FDX_Core_AccountBalances($account_id: String!) {
  consumerBankingBalances(
    where: {consumerBankingAccount: {accountNumber: {_eq: $account_id}}}
    order_by: {dateTime: Desc}
    limit: 1
  ) {
    consumerBankingBalanceId
    creditDebitIndicator
    type
    dateTime
    amount
    currency {
      code
    }
    subType
  }
}',
  'Performance optimized balance information delivery flow',
  '2024-09-01 00:00:00'::timestamptz,
  '2025-03-31 23:59:59'::timestamptz,
  '2024-09-01 11:45:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  'ffffffff-ffff-ffff-aaaa-ffffffffffff',
  app_mgmt_application_id,
  'fdx-gateway',
  2,
  1,
  'GET /fdx/v2_1/accounts/{accountId}/owner',
  'query FDX_Core_Account_Owner($accountId: String!) {
  consumerBankingAccountOwners(
    where: {consumerBankingAccount: {accountNumber: {_eq: $accountId}}}
  ) {
    ownershipType
    primaryOwner
    customerDetail {
      firstName
      lastName
      middleName
      address {
        line1
        line2
        city
        state
        postalCode
        country
      }
      contactDetails {
        email
        phone
      }
      taxIdentification {
        taxIdType
        taxId
      }
    }
  }
}',
  'New owner information delivery flow',
  '2024-09-01 00:00:00'::timestamptz,
  '2025-03-31 23:59:59'::timestamptz,
  '2024-09-01 11:50:00'::timestamptz
FROM app_id
UNION ALL
-- Current Version 5.0 API lineage (FDX 5.0 compliance) - note overlapping with v2.1 for 3 months
SELECT
  '11111111-2222-3333-aaaa-123456789abc',
  app_mgmt_application_id,
  'fdx-gateway',
  5,
  0,
  'GET /fdx/v5/accounts',
  'query FDX_Core_Accounts($cb_enterpriseAccountId: [ConsumerBanking_Int4!]!) {
  consumerBankingAccounts(
    where: {status: {_in: [ACTIVE]}, enterpriseAccountId: {_in: $cb_enterpriseAccountId}}
    order_by: {accountNumber: Asc}
  ) {
    consumerBankingProduct {
      productName
      productType
      baseInterestRate
    }
    consumerBankingAccountId
    accountNumber
    nickname
    displayName
    openingDayBalance
    currentBalance
    availableBalance
    interestYtd
    annualPercentageYield
    maturityDate
    term
    status
    currency {
      code
    }
    enterpriseAccount {
      enterpriseAccountId
    }
  }
}',
  'FDX 5.0 compliant account information delivery flow',
  '2025-01-01 00:00:00'::timestamptz,
  NULL,
  '2025-01-15 10:00:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  '22222222-3333-4444-aaaa-234567890abc',
  app_mgmt_application_id,
  'fdx-gateway',
  5,
  0,
  'GET /fdx/v5/accounts/{accountId}',
  'query FDX_Core_Account_Details($accountId: String!) {
  consumerBankingAccounts(
    where: {accountNumber: {_eq: $accountId}}
    limit: 1
  ) {
    consumerBankingProduct {
      productName
      productType
      baseInterestRate
    }
    consumerBankingAccountId
    accountNumber
    nickname
    displayName
    openingDayBalance
    currentBalance
    availableBalance
    interestYtd
    annualPercentageYield
    maturityDate
    term
    status
    openedDate
    currency {
      code
    }
    enterpriseAccount {
      enterpriseAccountId
    }
  }
}',
  'FDX 5.0 compliant account detail delivery flow',
  '2025-01-01 00:00:00'::timestamptz,
  NULL,
  '2025-01-15 10:05:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  '33333333-4444-5555-aaaa-345678901abc',
  app_mgmt_application_id,
  'fdx-gateway',
  5,
  0,
  'GET /fdx/v5/accounts/{accountId}/transactions',
  'query FDX_Core_Transactions($account_id: String!, $startTime: String!, $endTime: String!) {
  consumerBankingTransactions(
    where: {
      consumerBankingAccount: {accountNumber: {_eq: $account_id}},
      transactionDate: {_gte: $startTime, _lte: $endTime}
    }
    order_by: {transactionDate: Desc}
  ) {
    consumerBankingTransactionId
    transactionReference
    amount
    currency {
      code
    }
    creditDebitIndicator
    status
    transactionDate
    valueDate
    description
    category
    transactionType
  }
}',
  'FDX 5.0 compliant transaction history delivery flow',
  '2025-01-01 00:00:00'::timestamptz,
  NULL,
  '2025-01-15 10:10:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  '44444444-5555-6666-aaaa-456789012abc',
  app_mgmt_application_id,
  'fdx-gateway',
  5,
  0,
  'GET /fdx/v5/accounts/{accountId}/balances',
  'query FDX_Core_AccountBalances($account_id: String!) {
  consumerBankingBalances(
    where: {consumerBankingAccount: {accountNumber: {_eq: $account_id}}}
    order_by: {dateTime: Desc}
    limit: 1
  ) {
    consumerBankingBalanceId
    creditDebitIndicator
    type
    dateTime
    amount
    currency {
      code
    }
    subType
  }
}',
  'FDX 5.0 compliant balance information delivery flow',
  '2025-01-01 00:00:00'::timestamptz,
  NULL,
  '2025-01-15 10:15:00'::timestamptz
FROM app_id
UNION ALL
SELECT
  '55555555-6666-7777-aaaa-567890123abc',
  app_mgmt_application_id,
  'fdx-gateway',
  5,
  0,
  'GET /fdx/v5/accounts/{accountId}/owner',
  'query FDX_Core_Account_Owner($accountId: String!) {
  consumerBankingAccountOwners(
    where: {consumerBankingAccount: {accountNumber: {_eq: $accountId}}}
  ) {
    ownershipType
    primaryOwner
    customerDetail {
      firstName
      lastName
      middleName
      address {
        line1
        line2
        city
        state
        postalCode
        country
      }
      contactDetails {
        email
        phone
      }
      taxIdentification {
        taxIdType
        taxId
      }
    }
  }
}',
  'FDX 5.0 compliant owner information delivery flow',
  '2025-01-01 00:00:00'::timestamptz,
  NULL,
  '2025-01-15 10:20:00'::timestamptz
FROM app_id;
