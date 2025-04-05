-- PostgreSQL script to insert mortgage loan data

-- Insert application data and retrieve the generated IDs
WITH inserted_applications AS (
    INSERT INTO mortgage_services.applications
        (application_type, status, submission_date_time, creation_date_time,
         requested_loan_amount, requested_loan_term_months, estimated_property_value, estimated_credit_score,
         referral_source, loan_purpose, mortgage_services_loan_product_id, last_updated_date_time)
    VALUES
        ('PURCHASE', 'APPROVED', '2024-03-15 10:00:00', '2024-03-10 09:22:35',
         425000.00, 360, 490000.00, 768, 'Real Estate Agent', 'PRIMARY_RESIDENCE', (SELECT mortgage_services_loan_product_id FROM mortgage_services.loan_products ORDER BY RANDOM() LIMIT 1), CURRENT_TIMESTAMP),
        ('PURCHASE', 'IN_REVIEW', '2024-03-16 11:30:00', '2024-03-12 16:45:18',
         325000.00, 360, 375000.00, 742, 'Website', 'PRIMARY_RESIDENCE', (SELECT mortgage_services_loan_product_id FROM mortgage_services.loan_products ORDER BY RANDOM() LIMIT 1), CURRENT_TIMESTAMP),
        ('CONSTRUCTION', 'APPROVED', '2024-03-17 09:15:00', '2024-03-11 14:10:22',
         550000.00, 360, 650000.00, 802, 'Repeat Customer', 'SECOND_HOME', (SELECT mortgage_services_loan_product_id FROM mortgage_services.loan_products ORDER BY RANDOM() LIMIT 1), CURRENT_TIMESTAMP),
        ('PURCHASE', 'DENIED', '2024-03-18 14:20:00', '2024-03-13 11:35:47',
         475000.00, 300, 525000.00, 675, 'Real Estate Agent', 'INVESTMENT_PROPERTY', (SELECT mortgage_services_loan_product_id FROM mortgage_services.loan_products ORDER BY RANDOM() LIMIT 1), CURRENT_TIMESTAMP),
        ('HOME_IMPROVEMENT', 'APPROVED', '2024-03-19 16:45:00', '2024-03-14 10:20:12',
         175000.00, 240, 425000.00, 785, 'Branch Referral', 'OTHER', (SELECT mortgage_services_loan_product_id FROM mortgage_services.loan_products ORDER BY RANDOM() LIMIT 1), CURRENT_TIMESTAMP),
        ('PURCHASE', 'IN_REVIEW', '2024-03-20 13:10:00', '2024-03-15 15:40:33',
         390000.00, 180, 450000.00, 755, 'Online Advertisement', 'SECOND_HOME', (SELECT mortgage_services_loan_product_id FROM mortgage_services.loan_products ORDER BY RANDOM() LIMIT 1), CURRENT_TIMESTAMP),
        ('CONSTRUCTION', 'APPROVED', '2024-03-21 10:30:00', '2024-03-16 08:55:14',
         425000.00, 360, 475000.00, 790, 'Builder Referral', 'PRIMARY_RESIDENCE', (SELECT mortgage_services_loan_product_id FROM mortgage_services.loan_products ORDER BY RANDOM() LIMIT 1), CURRENT_TIMESTAMP),
        ('PURCHASE', 'APPROVED', '2024-03-22 11:00:00', '2024-03-17 13:25:09',
         285000.00, 240, 320000.00, 715, 'Mortgage Broker', 'INVESTMENT_PROPERTY', (SELECT mortgage_services_loan_product_id FROM mortgage_services.loan_products ORDER BY RANDOM() LIMIT 1), CURRENT_TIMESTAMP),
        ('VA', 'IN_REVIEW', '2024-03-23 15:20:00', '2024-03-18 09:15:27',
         450000.00, 360, 475000.00, 745, 'VA Benefits Program', 'PRIMARY_RESIDENCE', (SELECT mortgage_services_loan_product_id FROM mortgage_services.loan_products ORDER BY RANDOM() LIMIT 1), CURRENT_TIMESTAMP)
    RETURNING mortgage_services_application_id
),
-- Insert property data using the application IDs
inserted_properties AS (
    INSERT INTO mortgage_services.properties
        (mortgage_services_application_id, property_type, occupancy_type, year_built, square_feet,
         bedrooms, bathrooms, address, lot_size, hoa_dues, is_new_construction)
    SELECT
        mortgage_services_application_id,
        CASE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 'SINGLE_FAMILY'::mortgage_services.property_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 'CONDO'::mortgage_services.property_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 'SINGLE_FAMILY'::mortgage_services.property_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 'MULTI_FAMILY'::mortgage_services.property_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 'SINGLE_FAMILY'::mortgage_services.property_type
            -- Skipping APP-006 to violate the minItems rule for properties (each application must have at least one property)
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 'SINGLE_FAMILY'::mortgage_services.property_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 'CONDO'::mortgage_services.property_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 'SINGLE_FAMILY'::mortgage_services.property_type
        END,
        CASE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 'PRIMARY_RESIDENCE'::mortgage_services.occupancy_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 'PRIMARY_RESIDENCE'::mortgage_services.occupancy_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 'PRIMARY_RESIDENCE'::mortgage_services.occupancy_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 'INVESTMENT'::mortgage_services.occupancy_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 'PRIMARY_RESIDENCE'::mortgage_services.occupancy_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 'PRIMARY_RESIDENCE'::mortgage_services.occupancy_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 'INVESTMENT'::mortgage_services.occupancy_type
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 'PRIMARY_RESIDENCE'::mortgage_services.occupancy_type
        END,
        CASE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 1995
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 2005
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 2023
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 1975
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 1985
            -- VIOLATION #1: Property built in 1940 (violates the rule requiring yearBuilt >= 1950 for loans > 240 months)
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 1940
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 2015
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 2000
        END,
        CASE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 2354
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 1285
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 2650
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 3455
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 1842
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 1725
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 1150
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 2280
        END,
        CASE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 4
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 2
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 4
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 6
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 3
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 3
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 2
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 4
        END,
        CASE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 2.5
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 2.0
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 3.5
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 4.0
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 2.5
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 1.5
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 1.0
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 2.5
        END,
        CASE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN '123 Heritage Lane, Oakville, CA 94582'
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN '456 Waterfront Way, Unit 802, Marina Heights, FL 33139'
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN '789 Creekside Terrace, Riverdale, TX 77043'
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN '101 Investors Circle, Apartment 1-4, Profitsville, NY 10021'
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN '202 Sycamore Drive, Greenwood, CO 80111'
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN '404 Victorian Avenue, Heritage District, MA 02210'
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN '505 Rental Property Lane, Unit 303, Money Maker, AZ 85251'
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN '606 Veterans Boulevard, Stars and Stripes, VA 23464'
        END,
        CASE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 0.25
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN NULL
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 0.75
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 0.5
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 0.3
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 0.2
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN NULL
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 0.35
        END,
        CASE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN NULL
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 450.00
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN NULL
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN NULL
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 325.00
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN NULL
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 275.00
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN NULL
        END,
        CASE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN FALSE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN FALSE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN TRUE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN FALSE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN FALSE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN FALSE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN FALSE
            WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN FALSE
        END
    FROM
        inserted_applications
    WHERE
        mortgage_services_application_id != (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 5 LIMIT 1) -- Skip APP-006 to violate minItems rule
    RETURNING mortgage_services_application_id
)
-- Insert loans using the application IDs
INSERT INTO mortgage_services.loans
    (mortgage_services_application_id, loan_amount, interest_rate, loan_term_months, origination_date,
     maturity_date, down_payment, closing_costs, monthly_payment, enterprise_account_id)
SELECT
    mortgage_services_application_id,
    CASE
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 362500
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 278450
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 455000
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 427300
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 152750
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 5 LIMIT 1) THEN 328900
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 372600
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 228750
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 418500
    END,
    CASE
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 5.125
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 5.250
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 5.375
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 5.625
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 6.000
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 5 LIMIT 1) THEN 5.500
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 5.250
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 5.750
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 4.875
    END,
    CASE
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 360
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 360
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 360
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 300
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 240
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 5 LIMIT 1) THEN 180
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 360 -- VIOLATION #1 with yearBuilt 1940
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 240
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 360
    END,
    CASE
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN '2024-03-20'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN '2024-03-25'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN '2024-03-30'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN '2024-04-05'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN '2024-04-10'::date
        -- VIOLATION #2: originationDate is before submissionDateTime (2024-03-20)
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 5 LIMIT 1) THEN '2024-02-15'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN '2024-03-25'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN '2024-04-25'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN '2024-04-30'::date
    END,
    CASE
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN '2054-03-20'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN '2054-03-25'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN '2054-03-30'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN '2049-04-05'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN '2044-04-10'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 5 LIMIT 1) THEN '2039-04-15'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN '2054-03-25'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN '2044-04-25'::date
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN '2054-04-30'::date
    END,
    CASE
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 72500.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 46550.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 95000.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 97700.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 22250.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 5 LIMIT 1) THEN 61100.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 52400.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 31250.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 31500.00
    END,
    CASE
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 15235.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 12450.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 18900.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 16800.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 8765.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 5 LIMIT 1) THEN 14320.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 15650.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 11200.00
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 17500.00
    END,
    CASE
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN 1971.56
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN 1537.22
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN 2547.38
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN 2463.18
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN 1090.57
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 5 LIMIT 1) THEN 2471.34
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN 2058.47
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN 1382.29
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN 2213.65
    END,
    CASE
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 0 LIMIT 1) THEN (SELECT enterprise_account_id FROM enterprise.accounts ORDER BY RANDOM() LIMIT 1)
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 1 LIMIT 1) THEN (SELECT enterprise_account_id FROM enterprise.accounts ORDER BY RANDOM() LIMIT 1)
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 2 LIMIT 1) THEN (SELECT enterprise_account_id FROM enterprise.accounts ORDER BY RANDOM() LIMIT 1)
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 3 LIMIT 1) THEN (SELECT enterprise_account_id FROM enterprise.accounts ORDER BY RANDOM() LIMIT 1)
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 4 LIMIT 1) THEN (SELECT enterprise_account_id FROM enterprise.accounts ORDER BY RANDOM() LIMIT 1)
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 5 LIMIT 1) THEN (SELECT enterprise_account_id FROM enterprise.accounts ORDER BY RANDOM() LIMIT 1)
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 6 LIMIT 1) THEN (SELECT enterprise_account_id FROM enterprise.accounts ORDER BY RANDOM() LIMIT 1)
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 7 LIMIT 1) THEN (SELECT enterprise_account_id FROM enterprise.accounts ORDER BY RANDOM() LIMIT 1)
        WHEN mortgage_services_application_id = (SELECT mortgage_services_application_id FROM inserted_applications OFFSET 8 LIMIT 1) THEN (SELECT enterprise_account_id FROM enterprise.accounts ORDER BY RANDOM() LIMIT 1)
    END
FROM inserted_applications;
