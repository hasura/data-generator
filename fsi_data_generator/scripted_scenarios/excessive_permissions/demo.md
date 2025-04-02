# Live Demo Tutorial: Identifying Security Access Risks with a Data Agent

**Goal:** To demonstrate how a data agent can analyze complex banking system access patterns to identify security risks related to excessive permissions and segregation of duties violations, providing actionable remediation recommendations.

**Target Audience:** Financial institutions, compliance officers, and information security teams.

**Demo Flow:**

## Phase 1: Setting the Stage (0:00 - 1:30)

1. **Introduction (0:00-0:15):**
   * "Welcome! Today I'll demonstrate how data agents can transform security access reviews in banking environments, making them more thorough, consistent, and efficient."
   * Briefly explain that manual reviews often miss complex relationships and patterns that automated analysis can detect.

2. **Building the Foundation (0:15-1:00):**
   * **Database Schema Overview (0:15-0:25):** "We're working with a realistic banking database schema that models departments, associates, applications, roles, and entitlements - essentially a complete identity and access management ecosystem."
   * **Relationship Mapping (0:25-0:40):** "The schema establishes critical relationships between users, roles, entitlements, and protected resources, allowing us to trace access paths and identify potential security risks."
   * **Metadata Importance (0:40-0:50):** "Each element is enriched with meaningful metadata - like department associations, job titles, and resource sensitivity - which helps our agent understand context and identify inappropriate access patterns."
   * **Generated Test Data (0:50-1:00):** "For this demonstration, we've populated the database with generated test data representing a mid-sized bank. This data includes deliberately planted security issues that mirror common real-world problems we've observed."

3. **Defining the Problem (1:00-1:30):**
   * **Security Scenarios (1:00-1:15):** "We'll focus on two critical security risk categories that plague financial institutions:
     1. Excessive permissions, where users have access beyond their legitimate business needs
     2. Toxic combinations, where users hold conflicting permissions that violate segregation of duties principles"
   * **Agent's Task (1:15-1:30):** "Our data agent will analyze access patterns across the bank, identify instances of these security risks, and provide clear, actionable remediation recommendations. The analysis process we'll demonstrate could be applied to your own access management data with minimal configuration."

## Phase 2: Executing the Analysis (1:30 - 4:15)

4. **Explaining the Analysis Approach (1:30-2:00):**
   * **General Approach (1:30-1:45):** "We provide the data agent with Python-based analysis instructions that leverage its understanding of information security principles, while keeping the SQL simple so it focuses on the higher-level patterns."
   * **Structured Process (1:45-2:00):** "The agent follows a methodical, step-by-step process for each analysis, building up context about the environment before identifying potential issues."

5. **Scenario 1: Excessive Permissions Analysis (2:00-3:00):**
   * **Step 1: Identify Sensitive Data (2:00-2:15):** "First, the agent identifies applications containing sensitive PII data based on application names and descriptions." (Show results highlighting the HR Management Portal and Teller Application)
   * **Step 2: Map Departmental Access (2:15-2:30):** "Next, it determines which departments should legitimately have access to each category of sensitive data." (Show results with HR appropriately having access to ASSOCIATE PII)
   * **Step 3: Trace User Access Paths (2:30-2:45):** "Then, it traces all access paths from users through roles to sensitive data resources." (Show mapping between users and their effective permissions)
   * **Step 4: Flag Inappropriate Access (2:45-3:00):** "Finally, it identifies users with access to sensitive data inappropriate for their department or job function." (Show results highlighting tellers with inappropriate access to HR data)

6. **Scenario 2: Toxic Combinations Analysis (3:00-4:00):**
   * **Step 1: Define Conflicting Pairs (3:00-3:15):** "First, the agent identifies permission pairs that should never be held by the same person, such as payment initiation and approval." (Show defined conflict pairs)
   * **Step 2: Map User Permissions (3:15-3:30):** "Next, it maps all active users to their complete set of effective permissions." (Show comprehensive permission mapping)
   * **Step 3: Detect Violations (3:30-3:45):** "Then, it identifies users holding conflicting permission pairs." (Show Charlie Check with both initiate and approve payment capabilities)
   * **Step 4: Recommend Remediation (3:45-4:00):** "Finally, it recommends specific remediation actions for each identified violation." (Show prioritized recommendations)

7. **Explaining Results (4:00-4:15):**
   * Highlight how the agent provides clear documentation of its findings, including the specific access paths creating the risk.
   * Show how the recommendations are actionable, targeting specific role assignments that should be modified.

## Phase 3: Highlighting the Benefits (4:15 - 5:00)

8. **Summarize the Findings (4:15-4:30):**
   * "As you've seen, the agent successfully identified two critical security issues:
     1. Tellers with inappropriate access to sensitive HR data
     2. Charlie Check with the dangerous ability to both initiate and approve payments"
   * Emphasize the efficiency of identifying these issues compared to manual reviews.

9. **Highlight Key Advantages (4:30-4:45):**
   * "This approach delivers several significant benefits:
     * Comprehensive analysis across complex permission structures that manual reviews might miss
     * Consistent application of security principles without reviewer fatigue
     * Clear documentation of findings for audit and remediation purposes
     * Rapid identification of high-risk issues allowing for prioritized remediation
     * Adaptability to your specific environment and policies"

10. **Call to Action (4:45-5:00):**
    * "Imagine applying this capability to your access management data on a regular schedule, catching security issues before they become compliance violations or security incidents. We'd be happy to discuss how this approach could be tailored to your specific security policies and controls. Any questions?"

## Key Tips for the Presenter:

* **Clarify Data Source:** Emphasize that while this demo uses test data, the same process works with production access management data.
* **Highlight Adaptability:** Stress that the analysis can be customized to accommodate different organizational structures, role designs, and security policies.
* **Security Focus:** Keep the focus on security risks and compliance implications rather than technical implementation details.
* **User-Friendly Examples:** Use specific examples (like Charlie's conflicting permissions) to make abstract security concepts concrete.
* **Business Impact:** Relate each finding to potential business impacts (fraud risk, compliance violations, audit findings).
* **Visualization:** Consider visual aids to represent complex relationships between users, roles, and permissions.
* **Keep Technical Details Optional:** Be prepared to dive deeper into technical aspects if asked, but maintain a business-focused presentation otherwise.
