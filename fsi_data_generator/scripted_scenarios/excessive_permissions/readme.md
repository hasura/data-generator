# Security Access Control Test Scenarios

This repository contains data and prompts for analyzing two critical information security scenarios within a simulated banking environment: excessive permissions (lack of least privilege) and toxic combinations of access (Segregation of Duties violations). The data in `excessive_permissions.sql` populates a sample database with enterprises, departments, associates, applications, roles, entitlements, and their relationships.

## Included Scenarios

### 1. Excessive Permissions / Lack of Least Privilege

The `pii.prompt.txt` guides the analysis of inappropriate access to Personally Identifiable Information (PII) through a step-by-step process:

* **Scenario 1: Role-based Excessive Access**
  * Some tellers (Alice, Charlie, Diana) have been inappropriately assigned the `LEAD_TELLER` role, which grants them `read_associate_details` entitlement through the HR Management Portal application.
  * This entitlement provides access to sensitive employee data that standard tellers shouldn't have.
  * Other tellers (Bob, Evan, George) are correctly assigned only the `TELLER` role with appropriate permissions.
  * The analysis identifies associates with permissions exceeding their job function requirements.

* **Scenario 2: Cross-Application Permission Bleed**
  * The `LEAD_TELLER` role (managed by the Teller Application) incorrectly grants access to resources managed by the HR Management Portal.
  * This creates a situation where teller staff can access sensitive HR data outside their business domain.
  * The analysis helps identify inappropriate cross-application access patterns.

### 2. Toxic Combinations / Segregation of Duties (SoD) Violations

The `toxic_combinations.prompt.txt` guides the analysis of SoD violations through identifying users holding conflicting capabilities:

* **Payment Processing SoD Violation Scenario**
  * Charlie Check has been assigned both:
    * `LEAD_TELLER` role (providing operational capabilities)
    * `payment_processor` role (providing both payment initiation AND approval capabilities)
  * This combination violates the principle that the same person shouldn't be able to both initiate and approve transactions.
  * In contrast, proper segregation is demonstrated with:
    * Fiona Fine assigned only the `payment_initiator` role
    * Olivia OpsLead assigned only the `payment_approver` role
  * The analysis identifies individuals with potentially dangerous combinations of access.

## Key Elements for Analysis

The database structure captures:

* **Associates**: Employee information with departments, jobs, and status
* **Applications**: Systems with sensitivity levels and departmental ownership
* **Roles**: Access collections assigned to users with defined business purposes
* **Entitlements**: Specific capabilities granted through roles
* **Resources**: Protected data and systems requiring controlled access
* **Identities**: Digital representations of users for access control

## Analysis Approach

Both prompts guide a Python-based analysis to:
1. Define sensitive information or conflicting permission pairs
2. Map users to their effective permissions
3. Detect inappropriate access or toxic combinations
4. Recommend remediation actions

These scenarios represent common security risks that organizations must address through effective access governance controls.

## Usage

Use the provided prompts with your analysis tools to identify the security risks described above.
