-- Complete INSERT Statements Only - Explicit UUIDs, Dept Context, Ownership, Contrast & SOD Violation (More Columns Populated)
-- Assumes all required schemas, tables (incl. departments.operating_unit, applications.enterprise_department_id FK), and ENUM types exist.
-- Fills in additional relevant columns like hire_date, manager_id, app_type, lifecycle_status, identity timestamps.
-- NOTE: Still may contain NULLs for columns requiring extensive external setup (e.g., addresses, buildings, specific FKs).

-- Current time for context: Tuesday, April 1, 2025 at 7:06:50 PM EDT (Charlotte, NC)

BEGIN; -- Start transaction

WITH ins_depts AS (
    -- Insert Departments, including CORRECT Operating Unit Enum Values, and return IDs/Names
    INSERT INTO enterprise.departments (department_name, location, operating_unit) VALUES
    ('Human Resources', 'HQ Bldg A', 'HR'::enterprise.operating_unit),
    ('Retail Branch Operations', 'Multiple Branches', 'CONSUMER_BANKING'::enterprise.operating_unit),
    ('IT Security', 'Tech Center B', 'IT'::enterprise.operating_unit)
    -- ON CONFLICT (department_name) DO NOTHING
    RETURNING enterprise_department_id, department_name

), ins_associates AS (
    -- 1. Insert ALL Associates first, add hire_date, manager_id, return generated IDs and email
    -- We need Olivia's ID first to assign her as manager, so insert managers first conceptually.
    -- However, CTEs evaluate independently. We'll use subqueries with email lookups.
    INSERT INTO enterprise.associates (first_name, last_name, email, job_title, status, relationship_type, salary, enterprise_department_id, hire_date, manager_id)
    -- Managers/Owners first (no manager assumed for them in this scope)
    SELECT 'Hannah', 'HRHead', 'hannah.hrhead@bank.com', 'HR Manager', 'ACTIVE'::enterprise.associate_status, 'EMPLOYEE'::enterprise.relationship_status, 95000.00, dept.enterprise_department_id, '2018-03-15'::date, NULL::integer FROM ins_depts dept WHERE dept.department_name = 'Human Resources' UNION ALL
    SELECT 'Olivia', 'OpsLead', 'olivia.opslead@bank.com', 'Retail Ops Manager', 'ACTIVE'::enterprise.associate_status, 'EMPLOYEE'::enterprise.relationship_status, 98000.00, dept.enterprise_department_id, '2019-06-20'::date, NULL::integer FROM ins_depts dept WHERE dept.department_name = 'Retail Branch Operations' UNION ALL
    SELECT 'Ian', 'ITAdmin', 'ian.itadmin@bank.com', 'IT Security Admin', 'ACTIVE'::enterprise.associate_status, 'EMPLOYEE'::enterprise.relationship_status, 90000.00, dept.enterprise_department_id, '2020-01-10'::date, NULL::integer FROM ins_depts dept WHERE dept.department_name = 'IT Security' UNION ALL
    -- Tellers (managed by Olivia OpsLead)
    SELECT 'Alice', 'Example', 'alice.example@bank.com', 'Teller', 'ACTIVE'::enterprise.associate_status, 'EMPLOYEE'::enterprise.relationship_status, 55000.00, dept.enterprise_department_id, '2021-05-01'::date, (SELECT sub.enterprise_associate_id FROM enterprise.associates sub WHERE sub.email = 'olivia.opslead@bank.com') FROM ins_depts dept WHERE dept.department_name = 'Retail Branch Operations' UNION ALL
    SELECT 'Bob', 'Secure', 'bob.secure@bank.com', 'Teller', 'ACTIVE'::enterprise.associate_status, 'EMPLOYEE'::enterprise.relationship_status, 54000.00, dept.enterprise_department_id, '2021-07-15'::date, (SELECT sub.enterprise_associate_id FROM enterprise.associates sub WHERE sub.email = 'olivia.opslead@bank.com') FROM ins_depts dept WHERE dept.department_name = 'Retail Branch Operations' UNION ALL
    SELECT 'Charlie', 'Check', 'charlie.check@bank.com', 'Teller', 'ACTIVE'::enterprise.associate_status, 'EMPLOYEE'::enterprise.relationship_status, 56000.00, dept.enterprise_department_id, '2022-01-20'::date, (SELECT sub.enterprise_associate_id FROM enterprise.associates sub WHERE sub.email = 'olivia.opslead@bank.com') FROM ins_depts dept WHERE dept.department_name = 'Retail Branch Operations' UNION ALL
    SELECT 'Diana', 'Data', 'diana.data@bank.com', 'Teller', 'ACTIVE'::enterprise.associate_status, 'EMPLOYEE'::enterprise.relationship_status, 54500.00, dept.enterprise_department_id, '2022-04-11'::date, (SELECT sub.enterprise_associate_id FROM enterprise.associates sub WHERE sub.email = 'olivia.opslead@bank.com') FROM ins_depts dept WHERE dept.department_name = 'Retail Branch Operations' UNION ALL
    SELECT 'Evan', 'Ensure', 'evan.ensure@bank.com', 'Teller', 'ACTIVE'::enterprise.associate_status, 'EMPLOYEE'::enterprise.relationship_status, 55500.00, dept.enterprise_department_id, '2022-08-01'::date, (SELECT sub.enterprise_associate_id FROM enterprise.associates sub WHERE sub.email = 'olivia.opslead@bank.com') FROM ins_depts dept WHERE dept.department_name = 'Retail Branch Operations' UNION ALL
    SELECT 'Fiona', 'Fine', 'fiona.fine@bank.com', 'Teller', 'ACTIVE'::enterprise.associate_status, 'EMPLOYEE'::enterprise.relationship_status, 53000.00, dept.enterprise_department_id, '2023-02-10'::date, (SELECT sub.enterprise_associate_id FROM enterprise.associates sub WHERE sub.email = 'olivia.opslead@bank.com') FROM ins_depts dept WHERE dept.department_name = 'Retail Branch Operations' UNION ALL
    SELECT 'George', 'Guard', 'george.guard@bank.com', 'Teller', 'ACTIVE'::enterprise.associate_status, 'EMPLOYEE'::enterprise.relationship_status, 53500.00, dept.enterprise_department_id, '2023-05-22'::date, (SELECT sub.enterprise_associate_id FROM enterprise.associates sub WHERE sub.email = 'olivia.opslead@bank.com') FROM ins_depts dept WHERE dept.department_name = 'Retail Branch Operations'
    -- ON CONFLICT (email) DO NOTHING
    RETURNING enterprise_associate_id, email, first_name, last_name, enterprise_department_id

), ins_apps AS (
    -- Insert Applications, add app_type, lifecycle_status, date_deployed
    INSERT INTO app_mgmt.applications (app_mgmt_application_id, application_name, description, enterprise_department_id, application_owner_id, created_by_user_id, application_type, lifecycle_status, date_deployed)
    SELECT
        'a1111111-a111-a111-a111-a11111111111'::UUID,
        'HR Management Portal',
        'Manages sensitive employee PII, salary, benefits. Owning Department: Human Resources. Data Sensitivity: High.',
        dept.enterprise_department_id,
        (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'hannah.hrhead@bank.com') as application_owner_id,
        (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com') as created_by_user_id,
        'WEB'::app_mgmt.application_types, -- Added
        'PRODUCTION'::app_mgmt.application_lifecycle_status, -- Added
        '2020-01-15 09:00:00+00'::TIMESTAMPTZ -- Added
    FROM ins_depts dept WHERE dept.department_name = 'Human Resources'
    UNION ALL
    SELECT
        'a2222222-a222-a222-a222-a22222222222'::UUID,
        'Teller Application',
        'Core system for processing customer financial transactions. Owning Department: Retail Branch Operations. Data Sensitivity: Medium.',
        dept.enterprise_department_id,
        (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'olivia.opslead@bank.com') as application_owner_id,
        (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com') as created_by_user_id,
        'DESKTOP'::app_mgmt.application_types, -- Added
        'PRODUCTION'::app_mgmt.application_lifecycle_status, -- Added
        '2019-11-01 09:00:00+00'::TIMESTAMPTZ -- Added
    FROM ins_depts dept WHERE dept.department_name = 'Retail Branch Operations'
    -- ON CONFLICT (app_mgmt_application_id) DO NOTHING
    RETURNING app_mgmt_application_id, application_name, enterprise_department_id

), ins_identities AS (
    -- 2. Insert Identities, add modified, synced, is_fallback_approver
    INSERT INTO security.identities (security_identity_id, name, display_name, owner_id, service_account, environment, created, status, inactive, modified, synced, is_fallback_approver)
    SELECT
        CASE
            WHEN a.email = 'alice.example@bank.com' THEN 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'::UUID
            WHEN a.email = 'bob.secure@bank.com' THEN 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'::UUID
            WHEN a.email = 'charlie.check@bank.com' THEN '11111111-1111-1111-1111-111111111111'::UUID
            WHEN a.email = 'diana.data@bank.com' THEN '22222222-2222-2222-2222-222222222222'::UUID
            WHEN a.email = 'evan.ensure@bank.com' THEN '33333333-3333-3333-3333-333333333333'::UUID
            WHEN a.email = 'fiona.fine@bank.com' THEN '44444444-4444-4444-4444-444444444444'::UUID
            WHEN a.email = 'george.guard@bank.com' THEN '55555555-5555-5555-5555-555555555555'::UUID
            WHEN a.email = 'hannah.hrhead@bank.com' THEN '8fbad65a-aaa1-4123-8abc-111111111111'::UUID
            WHEN a.email = 'olivia.opslead@bank.com' THEN '9fbad65a-bbb2-4123-8abc-222222222222'::UUID
            WHEN a.email = 'ian.itadmin@bank.com' THEN 'afbad65a-ccc3-4123-8abc-333333333333'::UUID
        END as security_identity_id,
        LOWER(SUBSTRING(a.first_name, 1, 1) || a.last_name) as name,
        a.first_name || ' ' || a.last_name as display_name,
        a.enterprise_associate_id as owner_id,
        false as service_account,
        'production'::security.environment,
        CURRENT_TIMESTAMP,
        'ACTIVE' as status, -- This is VARCHAR, case doesn't strictly matter
        false as inactive,
        CURRENT_TIMESTAMP as modified, -- Added
        CURRENT_TIMESTAMP as synced, -- Added
        false as is_fallback_approver -- Added
    FROM ins_associates a
    -- ON CONFLICT (name) DO NOTHING
    RETURNING security_identity_id, name

), ins_resource AS (
    -- 3. Insert Resource Definitions
    INSERT INTO security.resource_definitions (security_resource_id, resource_name, resource_type, resource_identifier, application_id, description, created_at, created_by_id)
    SELECT
        'cccccccc-cccc-cccc-cccc-cccccccccccc'::UUID,
        'Enterprise Associates Data' as resource_name,
        'DATA'::security.resource_type,
        '/data/enterprise/associates' as resource_identifier,
        apps.app_mgmt_application_id,
        'Table containing sensitive employee records including PII and salary.' as description,
        CURRENT_TIMESTAMP,
        (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com') as created_by_id
    FROM ins_apps apps WHERE apps.application_name = 'HR Management Portal'
    UNION ALL
    SELECT
        'c1c1c1c1-cccc-cccc-cccc-cccccccccccc'::UUID,
        'Scheduled Payments Data' as resource_name,
        'DATA'::security.resource_type,
        '/data/consumer_banking/scheduled_payments' as resource_identifier,
        apps.app_mgmt_application_id,
        'Table used to stage and process outgoing scheduled payments and wire transfers.' as description,
        CURRENT_TIMESTAMP,
        (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com') as created_by_id
    FROM ins_apps apps WHERE apps.application_name = 'Teller Application'
    -- ON CONFLICT (security_resource_id) DO NOTHING
    RETURNING security_resource_id, resource_identifier, application_id

), ins_entitlement AS (
    -- 4. Insert Entitlements
    INSERT INTO security.enhanced_entitlements (security_entitlement_id, entitlement_name, display_name, description, managing_application_id, status, created_at, created_by_id)
     SELECT
        'dddddddd-dddd-dddd-dddd-dddddddddddd'::UUID,
        'read_associate_details' as entitlement_name,
        'Read Associate Details' as display_name,
        'Grants view access into the sensitive enterprise associate data store.' as description,
        apps.app_mgmt_application_id,
        'ACTIVE'::security.entitlement_status,
        CURRENT_TIMESTAMP,
        (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com') as created_by_id
    FROM ins_apps apps WHERE apps.application_name = 'HR Management Portal'
    UNION ALL
     SELECT
        'd1d1d1d1-dddd-dddd-dddd-dddddddddddd'::UUID,
        'initiate_payment' as entitlement_name,
        'Initiate Payment' as display_name,
        'Allows user to create new entries in the scheduled payments system for later approval.' as description,
        apps.app_mgmt_application_id,
        'ACTIVE'::security.entitlement_status,
        CURRENT_TIMESTAMP,
        (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com') as created_by_id
    FROM ins_apps apps WHERE apps.application_name = 'Teller Application'
    UNION ALL
     SELECT
        'd2d2d2d2-dddd-dddd-dddd-dddddddddddd'::UUID,
        'approve_payment' as entitlement_name,
        'Approve Payment' as display_name,
        'Allows user to provide final approval and release of scheduled payments initiated by others.' as description,
        apps.app_mgmt_application_id,
        'ACTIVE'::security.entitlement_status,
        CURRENT_TIMESTAMP,
        (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com') as created_by_id
    FROM ins_apps apps WHERE apps.application_name = 'Teller Application'
    -- ON CONFLICT (security_entitlement_id) DO NOTHING
    RETURNING security_entitlement_id, entitlement_name

), ins_ent_res AS (
    -- 5. Insert Entitlement-Resource Links
    INSERT INTO security.entitlement_resources (security_entitlement_resource_id, security_entitlement_id, security_resource_id, permission_type, created_at, created_by_id)
    SELECT '77777777-7777-7777-7777-777777777777'::UUID, ent.security_entitlement_id, res.security_resource_id, 'READ'::security.permission_type, CURRENT_TIMESTAMP, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_entitlement ent JOIN ins_resource res ON ent.entitlement_name = 'read_associate_details' AND res.resource_identifier = 'enterprise.associates'
    UNION ALL
    SELECT '71717171-7777-7777-7777-777777777777'::UUID, ent.security_entitlement_id, res.security_resource_id, 'WRITE'::security.permission_type, CURRENT_TIMESTAMP, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_entitlement ent JOIN ins_resource res ON ent.entitlement_name = 'initiate_payment' AND res.resource_identifier = 'consumer_banking.scheduled_payments'
    UNION ALL
    SELECT '72727272-7777-7777-7777-777777777777'::UUID, ent.security_entitlement_id, res.security_resource_id, 'ADMIN'::security.permission_type, CURRENT_TIMESTAMP, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_entitlement ent JOIN ins_resource res ON ent.entitlement_name = 'approve_payment' AND res.resource_identifier = 'consumer_banking.scheduled_payments'
    -- ON CONFLICT (security_entitlement_resource_id) DO NOTHING

), ins_roles AS (
    -- 6. Insert Roles
    INSERT INTO security.roles (security_role_id, role_name, display_name, description, managing_application_id, owner_id, status, created_at, created_by_id)
    SELECT
        'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee'::UUID, 'LEAD_TELLER', 'Lead Teller',
        'Senior Teller responsible for standard duties, transaction overrides, balancing support, and accessing associate schedules/contacts when needed. Includes read access to basic associate details for operational purposes.',
        apps.app_mgmt_application_id, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'olivia.opslead@bank.com'),
        'ACTIVE'::security.role_status, CURRENT_TIMESTAMP, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_apps apps WHERE apps.application_name = 'Teller Application'
    UNION ALL
    SELECT
        'ffffffff-ffff-ffff-ffff-ffffffffffff'::UUID, 'TELLER', 'Teller',
        'Standard Teller role for processing customer transactions (deposits, withdrawals, check cashing) within defined limits. Access restricted to necessary customer account information.',
        apps.app_mgmt_application_id, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'olivia.opslead@bank.com'),
        'ACTIVE'::security.role_status, CURRENT_TIMESTAMP, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_apps apps WHERE apps.application_name = 'Teller Application'
    UNION ALL
    SELECT
        '1a2b3c4d-1111-4ace-1111-111111111111'::UUID, 'HR_MANAGER_ROLE', 'HR Manager',
        'Manages HR functions including recruitment, employee relations, benefits, payroll oversight, and performance. Requires access to sensitive employee records and PII.',
        apps.app_mgmt_application_id, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'hannah.hrhead@bank.com'),
        'ACTIVE'::security.role_status, CURRENT_TIMESTAMP, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_apps apps WHERE apps.application_name = 'HR Management Portal'
    UNION ALL
    SELECT
        'faceb001-1111-1111-1111-111111111111'::UUID, 'payment_initiator', 'Payment Initiator',
        'Responsible for preparing and submitting payment instructions (e.g., ACH, wires) based on authorized requests for subsequent review and approval.',
        apps.app_mgmt_application_id, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'olivia.opslead@bank.com'),
        'ACTIVE'::security.role_status, CURRENT_TIMESTAMP, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_apps apps WHERE apps.application_name = 'Teller Application'
    UNION ALL
    SELECT
        'faceb002-2222-2222-2222-222222222222'::UUID, 'payment_approver', 'Payment Approver',
        'Authorized to review and approve outgoing payments initiated by others, within established limits. Verifies accuracy and authorization before release.',
        apps.app_mgmt_application_id, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'olivia.opslead@bank.com'),
        'ACTIVE'::security.role_status, CURRENT_TIMESTAMP, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_apps apps WHERE apps.application_name = 'Teller Application'
    UNION ALL
    SELECT
        'faceb003-3333-3333-3333-333333333333'::UUID, 'payment_processor', 'Payment Processor',
        'Handles end-to-end processing of specific internal or low-risk payment types, including setup, verification, and release under defined procedures.',
        apps.app_mgmt_application_id, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'olivia.opslead@bank.com'),
        'ACTIVE'::security.role_status, CURRENT_TIMESTAMP, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_apps apps WHERE apps.application_name = 'Teller Application'
    -- ON CONFLICT (security_role_id) DO NOTHING
    RETURNING security_role_id, role_name

), ins_role_ent AS (
    -- 7. Insert Role-Entitlement Links
    INSERT INTO security.role_entitlements (security_role_entitlement_id, security_role_id, security_entitlement_id, created_at, started_at, active, created_by_id)
    SELECT '88888888-8888-8888-8888-888888888888'::UUID, r.security_role_id, ent.security_entitlement_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, true, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_roles r, ins_entitlement ent WHERE r.role_name = 'LEAD_TELLER' AND ent.entitlement_name = 'read_associate_details'
    UNION ALL
    SELECT '8a8a8a8a-8888-8888-8888-888888888888'::UUID, r.security_role_id, ent.security_entitlement_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, true, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_roles r, ins_entitlement ent WHERE r.role_name = 'HR_MANAGER_ROLE' AND ent.entitlement_name = 'read_associate_details'
    UNION ALL
    SELECT '8b8b8b8b-1111-1111-1111-111111111111'::UUID, r.security_role_id, ent.security_entitlement_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, true, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_roles r, ins_entitlement ent WHERE r.role_name = 'payment_initiator' AND ent.entitlement_name = 'initiate_payment'
    UNION ALL
    SELECT '8c8c8c8c-2222-2222-2222-222222222222'::UUID, r.security_role_id, ent.security_entitlement_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, true, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_roles r, ins_entitlement ent WHERE r.role_name = 'payment_approver' AND ent.entitlement_name = 'approve_payment'
    UNION ALL
    SELECT '8d8d8d8d-3333-3333-3333-333333333333'::UUID, r.security_role_id, ent.security_entitlement_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, true, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_roles r, ins_entitlement ent WHERE r.role_name = 'payment_processor' AND ent.entitlement_name = 'initiate_payment' -- Still linked
    UNION ALL
    SELECT '8e8e8e8e-3333-3333-3333-333333333333'::UUID, r.security_role_id, ent.security_entitlement_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, true, (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
    FROM ins_roles r, ins_entitlement ent WHERE r.role_name = 'payment_processor' AND ent.entitlement_name = 'approve_payment' -- Still linked
    -- ON CONFLICT (security_role_entitlement_id) DO NOTHING

)
-- 8. Final Insert: Assign roles to identities
INSERT INTO security.identity_roles (security_identity_role_id, security_identity_id, security_role_id, start_date, active, assigned_by_id)
-- Assign Tellers to LEAD_TELLER (Excessive) or TELLER (Corrected)
SELECT
    CASE i.name
      WHEN 'aexample' THEN '9a11ce00-aaaa-aaaa-aaaa-aaaaaaaaaaaa'::UUID
      WHEN 'ccheck' THEN '9c3e11e0-cccc-cccc-cccc-cccccccccccc'::UUID -- Charlie gets LEAD_TELLER here... AND payment_processor below
      WHEN 'ddata' THEN '9d4a4a00-dddd-dddd-dddd-dddddddddddd'::UUID
      WHEN 'bsecure' THEN '9b0b0000-bbbb-bbbb-bbbb-bbbbbbbbbbbb'::UUID
      WHEN 'eensure' THEN '9e501a10-eeee-eeee-eeee-eeeeeeeeeeee'::UUID
      WHEN 'gguard' THEN '96a6d000-0000-0000-0000-000000000000'::UUID
    END,
    i.security_identity_id,
    r.security_role_id,
    CURRENT_TIMESTAMP,
    true,
    (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
FROM ins_identities i
JOIN ins_roles r ON (
    (i.name IN ('aexample', 'ccheck', 'ddata') AND r.role_name = 'LEAD_TELLER') OR
    (i.name IN ('bsecure', 'eensure', 'gguard') AND r.role_name = 'TELLER') -- Use new role name 'TELLER'
) WHERE i.name != 'ffine' -- Exclude Fiona (Payment Initiator)

UNION ALL

-- Assign HR Manager to HR Role (Valid Access)
SELECT
    '91a11a11-aaaa-aaaa-aaaa-aaaaaaaaaaaa'::UUID, i.security_identity_id, r.security_role_id, CURRENT_TIMESTAMP, true,
    (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
FROM ins_identities i, ins_roles r WHERE i.name = 'hhrhead' AND r.role_name = 'HR_MANAGER_ROLE'

UNION ALL

-- Assign Charlie Check the payment_processor role (SoD Violation)
SELECT
    '9f0d0000-cccc-cccc-cccc-cccccccccccc'::UUID, i.security_identity_id, r.security_role_id, CURRENT_TIMESTAMP, true,
    (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
FROM ins_identities i, ins_roles r WHERE i.name = 'ccheck' AND r.role_name = 'payment_processor' -- Use new role name

UNION ALL

-- Assign Fiona Fine the INITIATOR role (Contrast)
SELECT
    '9f104e00-ffff-ffff-ffff-ffffffffffff'::UUID, i.security_identity_id, r.security_role_id, CURRENT_TIMESTAMP, true,
    (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
FROM ins_identities i, ins_roles r WHERE i.name = 'ffine' AND r.role_name = 'payment_initiator' -- Use new role name

UNION ALL

-- Assign Olivia OpsLead the APPROVER role (Contrast)
SELECT
    '901141a0-0000-0000-0000-000000000000'::UUID, i.security_identity_id, r.security_role_id, CURRENT_TIMESTAMP, true,
    (SELECT ia.enterprise_associate_id FROM ins_associates ia WHERE ia.email = 'ian.itadmin@bank.com')
FROM ins_identities i, ins_roles r WHERE i.name = 'oopslead' AND r.role_name = 'payment_approver'; -- Use new role name
-- No ON CONFLICT

COMMIT; -- Commit transaction
