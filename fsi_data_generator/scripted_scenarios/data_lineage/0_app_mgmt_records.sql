-- =============================================
-- FDX GATEWAY APPLICATION RECORDS WITH VERIFICATION
-- =============================================

-- Begin a transaction for the entire operation
BEGIN;

-- Step 1: Check prerequisites
DO $$
DECLARE
    active_associates INTEGER;
    it_departments INTEGER;
    schema_check_app_mgmt BOOLEAN;
    schema_check_enterprise BOOLEAN;
BEGIN
    -- Check if required schemas exist
    SELECT EXISTS (
        SELECT 1 FROM information_schema.schemata WHERE schema_name = 'app_mgmt'
    ) INTO schema_check_app_mgmt;

    SELECT EXISTS (
        SELECT 1 FROM information_schema.schemata WHERE schema_name = 'enterprise'
    ) INTO schema_check_enterprise;

    IF NOT schema_check_app_mgmt THEN
        RAISE EXCEPTION 'Schema app_mgmt does not exist';
    END IF;

    IF NOT schema_check_enterprise THEN
        RAISE EXCEPTION 'Schema enterprise does not exist';
    END IF;

    -- Check if required tables exist in each schema
    PERFORM 1 FROM information_schema.tables
    WHERE table_schema = 'app_mgmt' AND table_name = 'architectures';
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Table app_mgmt.architectures does not exist';
    END IF;

    PERFORM 1 FROM information_schema.tables
    WHERE table_schema = 'app_mgmt' AND table_name = 'sdlc_processes';
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Table app_mgmt.sdlc_processes does not exist';
    END IF;

    PERFORM 1 FROM information_schema.tables
    WHERE table_schema = 'app_mgmt' AND table_name = 'teams';
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Table app_mgmt.teams does not exist';
    END IF;

    PERFORM 1 FROM information_schema.tables
    WHERE table_schema = 'app_mgmt' AND table_name = 'applications';
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Table app_mgmt.applications does not exist';
    END IF;

    PERFORM 1 FROM information_schema.tables
    WHERE table_schema = 'enterprise' AND table_name = 'associates';
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Table enterprise.associates does not exist';
    END IF;

    PERFORM 1 FROM information_schema.tables
    WHERE table_schema = 'enterprise' AND table_name = 'departments';
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Table enterprise.departments does not exist';
    END IF;

    -- Check if there are active associates
    SELECT COUNT(*) INTO active_associates
    FROM enterprise.associates
    WHERE status = 'ACTIVE';

    IF active_associates = 0 THEN
        RAISE EXCEPTION 'No active associates found in enterprise.associates';
    END IF;

    -- Check if there's an IT department
    SELECT COUNT(*) INTO it_departments
    FROM enterprise.departments
    WHERE operating_unit = 'IT';

    IF it_departments = 0 THEN
        RAISE EXCEPTION 'No IT department found in enterprise.departments';
    END IF;

    -- Log start of operation
    RAISE NOTICE 'Starting FDX Gateway application setup at %', NOW();
END $$;

-- Step 2: Check for existing records to avoid duplicates
DO $$
DECLARE
    existing_architecture INTEGER;
    existing_sdlc INTEGER;
    existing_team INTEGER;
    existing_application INTEGER;
BEGIN
    -- Check if architecture record already exists
    SELECT COUNT(*) INTO existing_architecture
    FROM app_mgmt.architectures
    WHERE app_mgmt_architecture_id = '11111111-d111-4111-bd11-111111111111'::uuid;

    IF existing_architecture > 0 THEN
        RAISE EXCEPTION 'Architecture record with ID 11111111-d111-4111-bd11-111111111111 already exists';
    END IF;

    -- Check if SDLC process record already exists
    SELECT COUNT(*) INTO existing_sdlc
    FROM app_mgmt.sdlc_processes
    WHERE app_mgmt_sdlc_process_id = '22222222-d222-4222-bd22-222222222222'::uuid;

    IF existing_sdlc > 0 THEN
        RAISE EXCEPTION 'SDLC process record with ID 22222222-d222-4222-bd22-222222222222 already exists';
    END IF;

    -- Check if team record already exists
    SELECT COUNT(*) INTO existing_team
    FROM app_mgmt.teams
    WHERE app_mgmt_team_id = '33333333-d333-4333-bd33-333333333333'::uuid;

    IF existing_team > 0 THEN
        RAISE EXCEPTION 'Team record with ID 33333333-d333-4333-bd33-333333333333 already exists';
    END IF;

    -- Check if application record already exists
    SELECT COUNT(*) INTO existing_application
    FROM app_mgmt.applications
    WHERE app_mgmt_application_id = '44444444-d444-4444-bd44-444444444444'::uuid
    OR application_name = 'FDX API Gateway';

    IF existing_application > 0 THEN
        RAISE EXCEPTION 'Application record with ID 44444444-d444-4444-bd44-444444444444 or name "FDX API Gateway" already exists';
    END IF;
END $$;

-- Step 3: Create architecture record
WITH associate_id AS (
  SELECT enterprise_associate_id
  FROM enterprise.associates
  WHERE status = 'ACTIVE'
  LIMIT 1
)
INSERT INTO app_mgmt.architectures (
  app_mgmt_architecture_id,
  architecture_name,
  description,
  approval_date,
  approved_by_id,
  documentation_url,
  status,
  created_by_user_id,
  modified_by_user_id
)
SELECT
  '11111111-d111-4111-bd11-111111111111'::uuid,
  'FDX API Gateway Architecture',
  'Standardized architecture for Financial Data Exchange (FDX) API gateways across all versions',
  '2024-01-15 00:00:00'::timestamptz,
  enterprise_associate_id,
  'https://wiki.internal/architecture/fdx-gateway',
  'approved',
  enterprise_associate_id,
  enterprise_associate_id
FROM associate_id;

-- Verify architecture was created
DO $$
DECLARE
    architecture_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO architecture_count
    FROM app_mgmt.architectures
    WHERE app_mgmt_architecture_id = '11111111-d111-4111-bd11-111111111111'::uuid;

    IF architecture_count = 0 THEN
        RAISE EXCEPTION 'Failed to create architecture record';
    ELSE
        RAISE NOTICE 'Successfully created architecture record';
    END IF;
END $$;

-- Step 4: Create SDLC process record
WITH associate_id AS (
  SELECT enterprise_associate_id
  FROM enterprise.associates
  WHERE status = 'ACTIVE'
  LIMIT 1
)
INSERT INTO app_mgmt.sdlc_processes (
  app_mgmt_sdlc_process_id,
  process_name,
  description,
  process_owner,
  version,
  documentation_url
)
SELECT
  '22222222-d222-4222-bd22-222222222222'::uuid,
  'FDX API Development Process',
  'Standardized development process for Financial Data Exchange (FDX) API implementations',
  enterprise_associate_id,
  '2.1',
  'https://wiki.internal/sdlc/fdx-api'
FROM associate_id;

-- Verify SDLC process was created
DO $$
DECLARE
    process_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO process_count
    FROM app_mgmt.sdlc_processes
    WHERE app_mgmt_sdlc_process_id = '22222222-d222-4222-bd22-222222222222'::uuid;

    IF process_count = 0 THEN
        RAISE EXCEPTION 'Failed to create SDLC process record';
    ELSE
        RAISE NOTICE 'Successfully created SDLC process record';
    END IF;
END $$;

-- Step 5: Create team for FDX Gateway
WITH associate_id AS (
  SELECT enterprise_associate_id
  FROM enterprise.associates
  WHERE status = 'ACTIVE'
  LIMIT 1
)
INSERT INTO app_mgmt.teams (
  app_mgmt_team_id,
  team_name,
  description,
  team_lead_id
)
SELECT
  '33333333-d333-4333-bd33-333333333333'::uuid,
  'FDX API Gateway Team',
  'Team responsible for developing and maintaining the FDX API Gateway',
  enterprise_associate_id
FROM associate_id;

-- Verify team was created
DO $$
DECLARE
    team_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO team_count
    FROM app_mgmt.teams
    WHERE app_mgmt_team_id = '33333333-d333-4333-bd33-333333333333'::uuid;

    IF team_count = 0 THEN
        RAISE EXCEPTION 'Failed to create team record';
    ELSE
        RAISE NOTICE 'Successfully created team record';
    END IF;
END $$;

-- Step 6: Create FDX Gateway application
WITH associate_id AS (
  SELECT enterprise_associate_id
  FROM enterprise.associates
  WHERE status = 'ACTIVE'
  LIMIT 1
),
department_id AS (
  SELECT enterprise_department_id
  FROM enterprise.departments
  WHERE operating_unit = 'IT'
  LIMIT 1
)
INSERT INTO app_mgmt.applications (
  app_mgmt_application_id,
  enterprise_department_id,
  application_name,
  description,
  application_type,
  vendor,
  version,
  deployment_environment,
  operated_by_team_id,
  maintained_by_team_id,
  created_by_team_id,
  application_owner_id,
  lifecycle_status,
  date_deployed,
  architecture_id,
  sdlc_process_id,
  source_code_repository,
  documentation_url
)
SELECT
  '44444444-d444-4444-bd44-444444444444'::uuid,
  d.enterprise_department_id,
  'FDX API Gateway',
  'Gateway for Financial Data Exchange (FDX) API calls that provides standardized access to banking data',
  'API',
  'Internal',
  '5.0',
  'CLOUD_HYBRID',
  '33333333-d333-4333-bd33-333333333333'::uuid,
  '33333333-d333-4333-bd33-333333333333'::uuid,
  '33333333-d333-4333-bd33-333333333333'::uuid,
  a.enterprise_associate_id,
  'PRODUCTION',
  '2025-01-01 00:00:00'::timestamptz,
  '11111111-d111-4111-bd11-111111111111'::uuid,
  '22222222-d222-4222-bd22-222222222222'::uuid,
  'https://git.internal/fdx-gateway',
  'https://wiki.internal/applications/fdx-gateway'
FROM associate_id a, department_id d;

-- Verify application was created
DO $$
DECLARE
    application_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO application_count
    FROM app_mgmt.applications
    WHERE app_mgmt_application_id = '44444444-d444-4444-bd44-444444444444'::uuid;

    IF application_count = 0 THEN
        RAISE EXCEPTION 'Failed to create application record';
    ELSE
        RAISE NOTICE 'Successfully created application record';
    END IF;
END $$;

-- Final verification
DO $$
DECLARE
    record_counts RECORD;
BEGIN
    SELECT
        (SELECT COUNT(*) FROM app_mgmt.architectures WHERE app_mgmt_architecture_id = '11111111-d111-4111-bd11-111111111111'::uuid) as architecture_count,
        (SELECT COUNT(*) FROM app_mgmt.sdlc_processes WHERE app_mgmt_sdlc_process_id = '22222222-d222-4222-bd22-222222222222'::uuid) as sdlc_count,
        (SELECT COUNT(*) FROM app_mgmt.teams WHERE app_mgmt_team_id = '33333333-d333-4333-bd33-333333333333'::uuid) as team_count,
        (SELECT COUNT(*) FROM app_mgmt.applications WHERE app_mgmt_application_id = '44444444-d444-4444-bd44-444444444444'::uuid) as application_count
    INTO record_counts;

    IF record_counts.architecture_count <> 1 OR
       record_counts.sdlc_count <> 1 OR
       record_counts.team_count <> 1 OR
       record_counts.application_count <> 1 THEN
        RAISE EXCEPTION 'Final verification failed: architecture=%, sdlc=%, team=%, application=%',
            record_counts.architecture_count,
            record_counts.sdlc_count,
            record_counts.team_count,
            record_counts.application_count;
    END IF;

    RAISE NOTICE 'All records successfully created';
END $$;

-- If all verifications pass, commit the transaction
COMMIT;

-- If you need a reference to the created application, you can run this after script execution:
-- SELECT app_mgmt_application_id FROM app_mgmt.applications WHERE application_name = 'FDX API Gateway';
