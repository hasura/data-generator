-- PostgreSQL script to insert applications and their owners with validation issues

-- First, create some departments if they don't exist
WITH inserted_departments AS (
    INSERT INTO enterprise.departments
        (department_name, operating_unit)
    VALUES
        ('Core Banking Technology', 'CONSUMER_BANKING'),
        ('Enterprise Data Management', 'IT'),
        ('Financial Technology Solutions', 'CONSUMER_LENDING')
    ON CONFLICT (department_name) DO UPDATE
        SET operating_unit = EXCLUDED.operating_unit
    RETURNING enterprise_department_id, department_name
),

-- Insert associates (employees and one contractor) to be application owners
inserted_associates AS (
    INSERT INTO enterprise.associates
        (first_name, last_name, email, phone_number, hire_date, status, job_title,
         officer_title, enterprise_department_id, relationship_type)
    VALUES
        ('Michael', 'Reynolds', 'michael.reynolds@example.com', '555-0101', '2015-06-15', 'ACTIVE', 'Technology Director',
         'SVP', (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Core Banking Technology'), 'EMPLOYEE'),
        ('Sarah', 'Johnson', 'sarah.johnson@example.com', '555-0102', '2018-03-22', 'ACTIVE', 'Data Governance Lead',
         'VP', (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Enterprise Data Management'), 'EMPLOYEE'),
        ('David', 'Chen', 'david.chen@example.com', '555-0103', '2016-09-30', 'ACTIVE', 'Financial Systems Manager',
         'VP', (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Financial Technology Solutions'), 'EMPLOYEE'),
        ('Emily', 'Washington', 'emily.washington@example.com', '555-0104', '2019-11-05', 'ACTIVE', 'Digital Banking Lead',
         'SVP', (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Core Banking Technology'), 'EMPLOYEE'),
        ('Robert', 'Garcia', 'robert.garcia@example.com', '555-0105', '2017-07-18', 'INACTIVE', 'Data Architecture Manager',
         'VP', (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Enterprise Data Management'), 'EMPLOYEE'),
        ('Jennifer', 'Lee', 'jennifer.lee@example.com', '555-0106', '2020-01-10', 'ACTIVE', 'Payment Systems Director',
         'SVP', (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Financial Technology Solutions'), 'EMPLOYEE'),
        ('Thomas', 'Brown', 'thomas.brown@example.com', '555-0107', '2018-05-14', 'INACTIVE', 'Fraud Detection Manager',
         'VP', (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Financial Technology Solutions'), 'EMPLOYEE'),
        ('Amanda', 'Miller', 'amanda.miller@example.com', '555-0108', '2021-04-12', 'ACTIVE', 'Cloud Platform Engineer',
         'Manager', (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Core Banking Technology'), 'EMPLOYEE'),
        ('James', 'Wilson', 'james.wilson@example.com', '555-0109', '2019-08-03', 'ACTIVE', 'Enterprise API Architect',
         'VP', (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Enterprise Data Management'), 'CONTRACTOR'),
        ('Lisa', 'Taylor', 'lisa.taylor@example.com', '555-0110', '2017-02-28', 'ACTIVE', 'Compliance Systems Director',
         'SVP', (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Financial Technology Solutions'), 'EMPLOYEE')
    RETURNING enterprise_associate_id, first_name, last_name, status, enterprise_department_id
)

-- Now insert applications with various issues
INSERT INTO app_mgmt.applications
    (app_mgmt_application_id, enterprise_department_id, application_name, description,
     application_type, lifecycle_status, application_owner_id)
VALUES
    -- Application 1: Valid application with active owner
    (gen_random_uuid(), -- <<< FIXED: Use standard function
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Core Banking Technology'),
     'Customer Account Management System',
     'Core system for managing customer accounts, balances, and transactions',
     'WEB',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'Michael' AND last_name = 'Reynolds')),

    -- Application 2: Valid application with active owner
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Enterprise Data Management'),
     'Enterprise Data Warehouse',
     'Centralized data warehouse for business intelligence and reporting',
     'DATABASE',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'Sarah' AND last_name = 'Johnson')),

    -- Application 3: Valid application with active owner
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Financial Technology Solutions'),
     'Payment Processing System',
     'System for processing electronic payments, transfers, and ACH transactions',
     'API',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'Jennifer' AND last_name = 'Lee')),

    -- Application 4: Valid application with active owner
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Core Banking Technology'),
     'Mobile Banking Platform',
     'Mobile application for customers to manage their accounts and transactions',
     'MOBILE',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'Emily' AND last_name = 'Washington')),

    -- Application 5: ISSUE - Inactive owner
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Enterprise Data Management'),
     'Data Governance Portal',
     'Platform for managing data governance policies and procedures',
     'WEB',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'Robert' AND last_name = 'Garcia')),

    -- Application 6: Valid application with active owner (contractor)
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Enterprise Data Management'),
     'API Gateway',
     'Centralized gateway for managing and securing API traffic',
     'API',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'James' AND last_name = 'Wilson')),

    -- Application 7: Valid application with active owner
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Financial Technology Solutions'),
     'Fraud Detection System',
     'AI-based system for detecting and preventing fraudulent transactions',
     'BATCH',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'Lisa' AND last_name = 'Taylor')),

    -- Application 8: ISSUE - Inactive owner
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Financial Technology Solutions'),
     'Risk Management Dashboard',
     'Dashboard for monitoring and managing financial risks',
     'WEB',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'Thomas' AND last_name = 'Brown')),

    -- Application 9: Valid application with active owner
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Core Banking Technology'),
     'Cloud Infrastructure Management',
     'System for managing and monitoring cloud infrastructure resources',
     'SAAS',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'Amanda' AND last_name = 'Miller')),

    -- Application 10: Valid application with active owner
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Financial Technology Solutions'),
     'Compliance Reporting System',
     'System for generating and submitting regulatory compliance reports',
     'BATCH',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'David' AND last_name = 'Chen')),

    -- Application 11: ISSUE - Department doesn't match owner's department
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Core Banking Technology'),
     'Customer Data Analytics Platform',
     'Platform for analyzing customer behavior and transaction patterns',
     'DATABASE',
     'PRODUCTION',
     (SELECT enterprise_associate_id FROM inserted_associates WHERE first_name = 'Sarah' AND last_name = 'Johnson')), -- Sarah is in Enterprise Data Management

    -- Application 12: ISSUE - No owner (NULL owner_id)
    (gen_random_uuid(),
     (SELECT enterprise_department_id FROM inserted_departments WHERE department_name = 'Enterprise Data Management'),
     'Document Management System',
     'System for storing and managing digital documents and records',
     'WEB',
     'PRODUCTION',
     NULL);
