-- =============================================
-- DATA QUALITY VALIDATION INSERTS
-- =============================================

-- Validation runs for GraphQL result data validations
INSERT INTO data_quality.validation_run
(run_timestamp, source_identifier, run_user, run_role, operation_name, variables,
validation_config_data, validation_config_verbose, validation_config_all_errors, validation_config_strict,
query, validation_schema, total_errors)
VALUES
-- Successful validation run for accounts
('2025-03-01 08:30:00', 'fdx-gateway-v2', 'api_service', 'fdx_api_role', 'getAccounts',
'{"cb_enterpriseAccountId": [12345]}',
true, true, true, true,
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
'{
  "type": "object",
  "required": ["data"],
  "properties": {
    "data": {
      "type": "object",
      "required": ["consumerBankingAccounts"],
      "properties": {
        "consumerBankingAccounts": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["consumerBankingAccountId", "enterpriseAccount"],
            "properties": {
              "enterpriseAccount": {
                "type": "object",
                "required": ["enterpriseAccountId"],
                "properties": {
                  "enterpriseAccountId": { "type": "integer", "minimum": 1 }
                }
              }
            }
          }
        }
      }
    }
  }
}',
0);

-- Store the validation_run_id from the previous insert
DO $$
DECLARE
    successful_accounts_run_id INT;
BEGIN
    SELECT currval(pg_get_serial_sequence('data_quality.validation_run', 'validation_run_id')) INTO successful_accounts_run_id;

    -- Now proceed with the rest of the inserts using the captured ID

    -- Failed validation run for accounts with missing enterprise account ID
    INSERT INTO data_quality.validation_run
    (run_timestamp, source_identifier, run_user, run_role, operation_name, variables,
    validation_config_data, validation_config_verbose, validation_config_all_errors, validation_config_strict,
    query, validation_schema, total_errors)
    VALUES
    ('2025-03-01 08:35:05', 'fdx-gateway-v2', 'api_service', 'fdx_api_role', 'getAccounts',
    '{"cb_enterpriseAccountId": [54321]}',
    true, true, true, true,
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
    '{
      "type": "object",
      "required": ["data"],
      "properties": {
        "data": {
          "type": "object",
          "required": ["consumerBankingAccounts"],
          "properties": {
            "consumerBankingAccounts": {
              "type": "array",
              "items": {
                "type": "object",
                "required": ["consumerBankingAccountId", "enterpriseAccount"],
                "properties": {
                  "enterpriseAccount": {
                    "type": "object",
                    "required": ["enterpriseAccountId"],
                    "properties": {
                      "enterpriseAccountId": { "type": "integer", "minimum": 1 }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }',
    1);

    -- Capture the failed accounts run ID
    DECLARE failed_accounts_run_id INT;
    BEGIN
        SELECT currval(pg_get_serial_sequence('data_quality.validation_run', 'validation_run_id')) INTO failed_accounts_run_id;

        -- Successful validation run for transactions
        INSERT INTO data_quality.validation_run
        (run_timestamp, source_identifier, run_user, run_role, operation_name, variables,
        validation_config_data, validation_config_verbose, validation_config_all_errors, validation_config_strict,
        query, validation_schema, total_errors)
        VALUES
        ('2025-03-03 13:15:25', 'fdx-gateway-v2', 'api_service', 'fdx_api_role', 'getTransactions',
        '{"account_id": "A45678", "startTime": "2025-02-01T00:00:00Z", "endTime": "2025-03-01T00:00:00Z"}',
        true, true, true, true,
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
        '{
          "type": "object",
          "required": ["data"],
          "properties": {
            "data": {
              "type": "object",
              "required": ["consumerBankingTransactions"],
              "properties": {
                "consumerBankingTransactions": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "required": ["amount", "creditDebitIndicator"],
                    "properties": {
                      "amount": { "type": "number" },
                      "creditDebitIndicator": { "type": "string", "enum": ["CREDIT", "DEBIT"] }
                    },
                    "allOf": [
                      {
                        "if": {
                          "properties": { "creditDebitIndicator": { "const": "CREDIT" } }
                        },
                        "then": {
                          "properties": { "amount": { "minimum": 0 } }
                        }
                      }
                    ]
                  }
                }
              }
            }
          }
        }',
        0);

        -- Capture the successful transactions run ID
        DECLARE successful_transactions_run_id INT;
        BEGIN
            SELECT currval(pg_get_serial_sequence('data_quality.validation_run', 'validation_run_id')) INTO successful_transactions_run_id;

            -- Failed validation run for transactions with invalid amount values
            INSERT INTO data_quality.validation_run
            (run_timestamp, source_identifier, run_user, run_role, operation_name, variables,
            validation_config_data, validation_config_verbose, validation_config_all_errors, validation_config_strict,
            query, validation_schema, total_errors)
            VALUES
            ('2025-03-03 13:15:30', 'fdx-gateway-v5', 'api_service', 'fdx_api_role', 'getTransactions',
            '{"account_id": "A34567", "startTime": "2025-02-01T00:00:00Z", "endTime": "2025-03-01T00:00:00Z"}',
            true, true, true, true,
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
            '{
              "type": "object",
              "required": ["data"],
              "properties": {
                "data": {
                  "type": "object",
                  "required": ["consumerBankingTransactions"],
                  "properties": {
                    "consumerBankingTransactions": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "required": ["amount", "creditDebitIndicator"],
                        "properties": {
                          "amount": { "type": "number" },
                          "creditDebitIndicator": { "type": "string", "enum": ["CREDIT", "DEBIT"] }
                        },
                        "allOf": [
                          {
                            "if": {
                              "properties": { "creditDebitIndicator": { "const": "CREDIT" } }
                            },
                            "then": {
                              "properties": { "amount": { "minimum": 0 } }
                            }
                          }
                        ]
                      }
                    }
                  }
                }
              }
            }',
            2);

            -- Capture the failed transactions run ID
            DECLARE failed_transactions_run_id INT;
            BEGIN
                SELECT currval(pg_get_serial_sequence('data_quality.validation_run', 'validation_run_id')) INTO failed_transactions_run_id;

                -- Successful validation run for account balances
                INSERT INTO data_quality.validation_run
                (run_timestamp, source_identifier, run_user, run_role, operation_name, variables,
                validation_config_data, validation_config_verbose, validation_config_all_errors, validation_config_strict,
                query, validation_schema, total_errors)
                VALUES
                ('2025-03-03 09:30:05', 'fdx-gateway-v2', 'api_service', 'fdx_api_role', 'getAccountBalances',
                '{"account_id": "A67890"}',
                true, true, true, true,
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
                '{
                  "type": "object",
                  "required": ["data"],
                  "properties": {
                    "data": {
                      "type": "object",
                      "required": ["consumerBankingBalances"],
                      "properties": {
                        "consumerBankingBalances": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "required": ["amount", "currency"],
                            "properties": {
                              "currency": {
                                "type": "object",
                                "required": ["code"],
                                "properties": {
                                  "code": { "type": "string", "enum": ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY"] }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }',
                0);

                -- Capture the successful balances run ID
                DECLARE successful_balances_run_id INT;
                BEGIN
                    SELECT currval(pg_get_serial_sequence('data_quality.validation_run', 'validation_run_id')) INTO successful_balances_run_id;

                    -- Failed validation run for account balance with missing required currency code
                    INSERT INTO data_quality.validation_run
                    (run_timestamp, source_identifier, run_user, run_role, operation_name, variables,
                    validation_config_data, validation_config_verbose, validation_config_all_errors, validation_config_strict,
                    query, validation_schema, total_errors)
                    VALUES
                    ('2025-03-03 09:30:10', 'fdx-gateway-v2', 'api_service', 'fdx_api_role', 'getAccountBalances',
                    '{"account_id": "A12345"}',
                    true, true, true, true,
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
                    '{
                      "type": "object",
                      "required": ["data"],
                      "properties": {
                        "data": {
                          "type": "object",
                          "required": ["consumerBankingBalances"],
                          "properties": {
                            "consumerBankingBalances": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "required": ["amount", "currency"],
                                "properties": {
                                  "currency": {
                                    "type": "object",
                                    "required": ["code"],
                                    "properties": {
                                      "code": { "type": "string", "enum": ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY"] }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }',
                    1);

                    -- Capture the failed balances run ID
                    DECLARE failed_balances_run_id INT;
                    BEGIN
                        SELECT currval(pg_get_serial_sequence('data_quality.validation_run', 'validation_run_id')) INTO failed_balances_run_id;

                        -- Add validation run for additional fields
                        INSERT INTO data_quality.validation_run
                        (run_timestamp, source_identifier, run_user, run_role, operation_name, variables,
                        validation_config_data, validation_config_verbose, validation_config_all_errors, validation_config_strict,
                        query, validation_schema, total_errors)
                        VALUES
                        -- Validation run for detailed account fields
                        ('2025-03-04 14:46:05', 'fdx-gateway-v2', 'api_service', 'fdx_api_role', 'getAccountDetails',
                        '{"accountId": "135790"}',
                        true, true, true, true,
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
                        '{
                          "type": "object",
                          "required": ["data"],
                          "properties": {
                            "data": {
                              "type": "object",
                              "required": ["consumerBankingAccounts"],
                              "properties": {
                                "consumerBankingAccounts": {
                                  "type": "array",
                                  "items": {
                                    "type": "object",
                                    "required": [
                                      "consumerBankingAccountId",
                                      "accountNumber",
                                      "status",
                                      "currency",
                                      "consumerBankingProduct"
                                    ],
                                    "properties": {
                                      "status": {
                                        "type": "string",
                                        "enum": ["ACTIVE", "PENDING", "INACTIVE", "SUSPENDED", "DORMANT", "FROZEN", "CLOSED", "ARCHIVED"]
                                      },
                                      "consumerBankingProduct": {
                                        "type": "object",
                                        "required": ["productType"],
                                        "properties": {
                                          "productType": {
                                            "type": "string",
                                            "enum": [
                                              "CHECKING", "SAVINGS", "MONEY_MARKET", "CERTIFICATE_OF_DEPOSIT",
                                              "IRA", "HSA", "STUDENT", "YOUTH", "SENIOR", "BUSINESS_CHECKING",
                                              "BUSINESS_SAVINGS", "PREMIUM", "FOREIGN_CURRENCY", "SPECIALIZED"
                                            ]
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }',
                        0);

                        -- Capture account details run ID
                        DECLARE account_details_run_id INT;
                        BEGIN
                            SELECT currval(pg_get_serial_sequence('data_quality.validation_run', 'validation_run_id')) INTO account_details_run_id;

                            -- Validation errors for the validation runs
                            INSERT INTO data_quality.validation_error
                            (validation_run_id, instance_path, schema_path, error_keyword, error_message,
                            failed_data, error_params, error_schema_detail, error_parent_schema_detail)
                            VALUES
                            -- Error for missing enterprise account ID in account data
                            (failed_accounts_run_id, '/data/consumerBankingAccounts/0/enterpriseAccount',
                            '/properties/data/properties/consumerBankingAccounts/items/properties/enterpriseAccount/required',
                            'required', 'must have required property "enterpriseAccountId"',
                            '{"enterpriseAccount":{}}',
                            '{"missingProperty":"enterpriseAccountId"}',
                            '{"type":"object","required":["enterpriseAccountId"],"properties":{"enterpriseAccountId":{"type":"integer","minimum":1}}}',
                            '{"type":"object","required":["consumerBankingAccountId","enterpriseAccount"],"properties":{"enterpriseAccount":{"type":"object","required":["enterpriseAccountId"],"properties":{"enterpriseAccountId":{"type":"integer","minimum":1}}}}}');

                            -- Error for negative amount with CREDIT indicator
                            INSERT INTO data_quality.validation_error
                            (validation_run_id, instance_path, schema_path, error_keyword, error_message,
                            failed_data, error_params, error_schema_detail, error_parent_schema_detail)
                            VALUES
                            (failed_transactions_run_id, '/data/consumerBankingTransactions/2/amount',
                            '/properties/data/properties/consumerBankingTransactions/items/allOf/0/then/properties/amount/minimum',
                            'minimum', 'must be >= 0',
                            '-25.50',
                            '{"limit":0}',
                            '{"minimum":0}',
                            '{"properties":{"amount":{"minimum":0}}}');

                            -- Error for another negative amount with CREDIT indicator
                            INSERT INTO data_quality.validation_error
                            (validation_run_id, instance_path, schema_path, error_keyword, error_message,
                            failed_data, error_params, error_schema_detail, error_parent_schema_detail)
                            VALUES
                            (failed_transactions_run_id, '/data/consumerBankingTransactions/5/amount',
                            '/properties/data/properties/consumerBankingTransactions/items/allOf/0/then/properties/amount/minimum',
                            'minimum', 'must be >= 0',
                            '-10.75',
                            '{"limit":0}',
                            '{"minimum":0}',
                            '{"properties":{"amount":{"minimum":0}}}');

                            -- Error for missing currency code in balance data
                            INSERT INTO data_quality.validation_error
                            (validation_run_id, instance_path, schema_path, error_keyword, error_message,
                            failed_data, error_params, error_schema_detail, error_parent_schema_detail)
                            VALUES
                            (failed_balances_run_id, '/data/consumerBankingBalances/0/currency',
                            '/properties/data/properties/consumerBankingBalances/items/properties/currency/required',
                            'required', 'must have required property "code"',
                            '{"currency":{}}',
                            '{"missingProperty":"code"}',
                            '{"type":"object","required":["code"],"properties":{"code":{"type":"string","enum":["USD","EUR","GBP","JPY","AUD","CAD","CHF","CNY"]}}}',
                            '{"type":"object","required":["amount","currency"],"properties":{"currency":{"type":"object","required":["code"],"properties":{"code":{"type":"string","enum":["USD","EUR","GBP","JPY","AUD","CAD","CHF","CNY"]}}}}}');

                        END;
                    END;
                END;
            END;
        END;
    END;
END $$;
