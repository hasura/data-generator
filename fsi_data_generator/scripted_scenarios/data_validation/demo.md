# Live Demo Tutorial: Data Validation

**Goal:** Demonstrate how JSON Schema validation can enforce complex data quality rules across multiple domains, ensuring data integrity through Hasura DDN's universal data access layer, and how a data validation service integrated with PromptQL enables natural language analysis of data quality.

**Target Audience:** Data architects, API developers, data governance teams, compliance officers, and data quality analysts.

## Demo Flow (35 minutes)

### Phase 1: Introduction (0:00 - 8:00)

> **Pre-Demo Setup Checklist:**
> - PostgreSQL running with username "postgres" and password "password"
> - Data generator has been run (`python main.py`)
> - Data validation plugin running on port 8787 (from the Hasura Plugin Hub)
> - PromptQL integration configured and tested
> - Test the scripts once before presenting

1. **The Data Quality Challenge and Limits of Centralization (0:00-2:30):**
   * "Welcome everyone! Today I'll show you how we're solving one of the most challenging problems in enterprise data management: enforcing data quality rules across multiple domains."
   * "Let's first acknowledge a fundamental truth - large banks are inherently decentralized organizations. This isn't a flaw; it's a feature that allows specialized knowledge to flourish in different business areas."
   * "For decades, we've pursued centralization strategies for data management, but these approaches have clear limits and can never be a complete solution."
   * "In modern microservice architectures, data often spans multiple systems. Traditional validation approaches break down when we need to enforce rules that cross these boundaries."
   * "For example, how do we ensure that an application owner's department matches the application's department? Or that a property built before 1950 doesn't get a 30-year mortgage?"
   * "In large organizations like banks, you have hundreds of reporting teams dealing with data quality issues. Each team typically works with upstream systems to solve issues within their domain, but cross-domain data quality issues are handled inconsistently."

2. **Our Decentralized Solution Approach (2:30-5:00):**
   * "We need to figure out decentralized data strategy solutions that acknowledge organizational reality while still enforcing quality."
   * "We're using Hasura DDN's universal data access layer for cross-domain data retrieval, JSON Schema for validation, and a data validation service integrated within this layer."
   * "Hasura DDN allows us to query exactly the data we need across domain boundaries in a single request, regardless of the underlying systems."
   * "JSON Schema gives us a declarative way to express complex data rules that's both human-readable and machine-enforceable."
   * "Instead of each team handling data quality individually, we're centralizing validation while keeping rules distributed. The teams still own their rules, but the validation happens in a unified service."
   * "This creates a shared understanding of data quality across the organization and enables all stakeholders to have meaningful conversations about data quality."
   * "This approach is technology-agnostic and can be implemented with any backend systems through Hasura DDN's universal data access capabilities."
   * "What we're demonstrating today is a data-agnostic self-service data validation component that allows for decentralized ownership of validation rules, with centralized standards and results - a practical path towards effective decentralized data management."

3. **Data Agents and PromptQL Integration (5:00-7:00):**
   * "To implement this solution, we're using the Hasura Plugin Hub with its validation plugin, specifically designed to work with data agents through Hasura PromptQL."
   * "The most powerful aspect of this approach is that it makes data quality accessible to everyone through natural language, not just technical specialists."
   * "Everything is in plain English. This means you, your colleagues, your boss, regulators, and everyone involved can understand it without technical expertise."
   * "It's important to note that JSON Schema, while powerful, is not always immediately understandable by non-technical users. Complex rules can be difficult to grasp, creating a translation gap between business requirements and technical definitions."
   * "This is where data agents become invaluable - they can generate JSON Schema from natural language descriptions and explain existing rules in plain English, making rule creation and maintenance accessible to business teams."
   * "The rules are still distributed because teams own them, but they run inside this centralized validation service, making them available to our data agent."
   * "Data agents become your assistants in analyzing data quality, enabling you to focus on insights rather than technical queries."
   * "PromptQL and data agents enable everyone to ask questions about data quality in plain English, removing technical barriers to understanding data quality issues."

4. **Demo Overview (7:00-8:00):**
   * "Today I'll walk you through three real-world scenarios:
     1. Application management with enterprise data constraints
     2. Mortgage services with complex temporal and conditional rules
     3. Using data agents and PromptQL to evaluate rule effectiveness and quality"
   * "We'll see how our solution detects violations, provides clear feedback, and enables natural language analysis of data quality rules through data agents."
   * "All the code and prompts I'm showing are available in our demo repository, so you can run these examples yourself later."

### Phase 2: Application Management Demo (8:00 - 15:00)

5. **Scenario Setup (8:00-10:00):**
   * "First, let's look at our application management scenario. This represents a common enterprise challenge where applications are owned by specific individuals, but we need to enforce rules about those relationships."
   * "Let me show you the data query we're using through Hasura DDN." (Display and explain the query)
   * "Notice how we're retrieving data from both the App Management domain and the Enterprise domain in a single query through the universal data access layer."
   * "This is the power of Hasura DDN - it allows us to seamlessly retrieve data across domain boundaries regardless of the underlying systems."
   
6. **Validation Rules (10:00-12:00):**
   * "Now let's examine the validation schema." (Display and explain `application_schema.json`)
   * "We have three key rules:
     1. Every application must have an owner object
     2. The owner must have an ACTIVE status
     3. The owner's department must match the application's department"
   * "All three of these rules are powerful examples of cross-domain validation. They each enforce consistency between App Management and Enterprise data domains, which would traditionally require separate validation steps in different systems."
   * "This unified validation approach catches inconsistencies early, preventing downstream data quality issues."

7. **Running the Demo (12:00-15:00):**
   * "Let's run the validation and see what happens." (Execute `./application.sh`)
   * "I've deliberately included some rule violations in our test data. Let's analyze the errors."
   * Walk through each error, explaining:
     * Which rule was violated
     * How the system detected it
     * What data would need to be fixed
   * "These clear error messages make it easy to identify and fix data quality issues."
   * "What's especially powerful is that these validation results aren't just shown here - they're also written to a database, creating a persistent record of validation runs over time."
   * "This means all validation results are available to our data agents through PromptQL, allowing anyone to ask natural language questions about validation history and trends."
   * "For example, someone could ask: 'Show me the most frequent validation errors across all applications in the last month' or 'Which departments have the highest data quality scores?'"
   * "And as a side note, PromptQL actually generates Python programs behind the scenes that can be captured and reused for consistent analysis over time, but we'll focus on the validation results for now."
   * "Let me demonstrate a simple question to our data agent." (Show a natural language query about validation results)

### Phase 3: Mortgage Services Demo (15:00 - 22:00)

8. **Scenario Introduction (15:00-17:00):**
   * "Now let's look at a more complex scenario from mortgage services, which demonstrates temporal and conditional rules."
   * "In this case, we're retrieving mortgage loans with their associated applications and properties through Hasura DDN." (Display and explain the query)
   * "The relationship structure is hierarchical: Loans contain Applications, which contain Properties."
   * "Again, we're using Hasura's universal data access layer to retrieve this cross-domain data in a single request, which would traditionally require multiple API calls or database queries."

9. **Advanced Validation Rules (17:00-19:00):**
   * "Our mortgage schema introduces more sophisticated rules." (Display and explain `mortgage_schema.json`)
   * "Note these interesting constraints:
     * Each application must have exactly one property (not zero, not multiple)
     * If a loan term exceeds 20 years (240 months), the property must be built in 1950 or later
     * The loan origination date must be on or after the application submission date
     * We must have at least 5 loan records for the query to be valid"
   * "These rules combine cardinality constraints, conditional logic, and temporal validation."
   * "I should note that the 1950 property age rule is admittedly artificial - we created it specifically for this demo to show how conditional rules can work across domains. In a real bank, property age rules would likely be more nuanced, involving inspections and estimated economic life rather than a fixed date cutoff."
   * "The important takeaway is how our system can implement these types of cross-domain conditional rules, regardless of how complex the actual business logic might be."

10. **Rule Violations Demo (19:00-22:00):**
    * "Let's run this validation and see what issues we find." (Execute `./mortgage.sh`)
    * "Our test data includes several deliberate violations:"
    * Walk through each violation:
      * Property from 1940 with a 30-year loan term
      * Loan with origination date before submission date
      * Application with missing property
    * "For each issue, our validator provides specific details about what's wrong and where, making it easier to troubleshoot."
    * "Just like with our application validation, these results aren't just displayed here - they're also persisted to our database and made available through PromptQL."
    * "This enables natural language conversations about mortgage validation trends and patterns. For example, an analyst could ask: 'Which loan officers have the highest rate of validation errors?' or 'Are there specific property types that frequently trigger the age-related rule violation?'"
    * "Let me show you how we might use our data agent to analyze these validation results." (Demonstrate a natural language query about mortgage validation patterns)
    * "By enforcing these rules at the data access layer and persisting the results, we prevent downstream data issues that could affect business decisions or regulatory compliance, while also building a knowledge base of validation patterns over time."

### Phase 4: PromptQL for Rule Evaluation (22:00 - 29:00)

11. **Rule Evaluation Perspective (22:00-24:00):**
    * "Now, let's switch perspectives. So far we've looked at individual data validation results, but now we want to evaluate the rules themselves."
    * "This is a critical meta-analysis that helps us ensure our validation system is effective. We're not looking at data defects anymore; we're evaluating the quality of the rules."
    * "In a large organization with hundreds or thousands of distributed rules, understanding rule effectiveness, coverage, and dependencies becomes vital for ongoing governance."
    * "Rather than manually analyzing each rule, we can use data agents through PromptQL to analyze our rule ecosystem and recommend improvements."

12. **Data Agent with PromptQL for Rule Analysis (24:00-27:00):**
    * "Let's look at a PromptQL prompt focused on rule inventory and evaluation." (Display the natural language prompt)
    * "Now, let's submit this to our data agent through PromptQL and see what happens." (Execute the prompt)
    * "While this is processing, I want to emphasize that we're not analyzing data defects here - we're analyzing the rules themselves. We want to know if our rules are comprehensive, if they cover the right quality dimensions, and if there are any circular dependencies."
    * "This meta-analysis helps us continuously improve our rule ecosystem, ensuring that we're measuring the right things across all our domains."

13. **Analyzing Rule Effectiveness (27:00-29:00):**
    * "The system has analyzed all of our validation rules across domains and categorized them by data quality dimension."
    * "It's performed a deeper analysis looking at enforcement patterns, conditions, and quality dimensions."
    * "It's also identified rule dependencies, which is crucial for understanding cascading errors that might inundate people with irrelevant alerts."
    * "The system has evaluated the rules for circular dependencies and identified missing quality dimensions - in this case, timeliness and uniqueness are missing from most rules."
    * "Finally, it's generated a complete rule quality analysis report that can be shared with rule owners to discuss the effectiveness of the validation ecosystem."

### Phase 5: Implementation and Benefits (29:00 - 35:00)

14. **Architecture Discussion (29:00-31:00):**
    * "Let's briefly look at how this is implemented." (Show architecture diagram)
    * "The key components are:
      * Hasura DDN universal data access layer that retrieves cross-domain data
      * JSON Schema validator with support for the latest features
      * Integration point where data requests are intercepted and validated
      * Data validation service embedded in the universal data access layer
      * Hasura Plugin Hub with validation plugin for data agent integration
      * PromptQL interface for natural language interactions"
    * "This architecture is lightweight and can be added to existing systems without major changes."

15. **Key Benefits: Balancing Centralization and Decentralization (31:00-33:00):**
    * "This approach delivers several significant advantages by finding the right balance between centralization and decentralization:"
    * "**Decentralized rule ownership** - Domain teams maintain control of their business rules"
    * "**Centralized validation** - Creates a shared understanding of data quality across the organization"
    * "**Declarative rules** - Business rules expressed clearly in JSON, not buried in code"
    * "**Cross-domain validation** - Enforce consistency across system boundaries"
    * "**Early detection** - Catch issues at the data access layer before they propagate"
    * "**Self-documenting** - Schema serves as both validation and documentation"
    * "**Technology-agnostic** - Works with any stack through Hasura DDN's universal data access"
    * "**Natural language interaction** - Data agents and PromptQL make data quality accessible to everyone"
    * "**Democratized insights** - Anyone can analyze data quality without technical expertise"
    * "This is a fundamental shift from pure centralization to a practical federation model where domain expertise is respected while still maintaining central visibility and standards."

16. **Wrap Up and Next Steps: Embracing Decentralization (33:00-35:00):**
    * "We've seen how this approach creates a balanced solution that respects the inherently decentralized nature of large financial institutions while still creating unified standards."
    * "To implement this in your environment, you would:
      1. Identify your critical data quality rules
      2. Express them in JSON Schema format
      3. Integrate the validator with Hasura DDN's universal data access layer
      4. Set up the Hasura Plugin Hub with the validation plugin
      5. Configure data agents and PromptQL for natural language conversations about data quality"
    * "All the code and prompts demonstrated today are available in our demo repository, along with documentation."
    * "The key takeaway is that we're not fighting against decentralization - we're working with it. This solution acknowledges that domain teams need to own their rules while providing a centralized mechanism for validation and visibility."
    * "This represents a practical path toward decentralized data management that can succeed where purely centralized approaches have often struggled. It gives domain experts the autonomy they need while creating the visibility and cross-domain validation that the organization requires."
    * "Questions? I'm happy to dive deeper into any aspect of the implementation or discuss how this approach might work in your specific organizational context."

## Demo Tips

* **Pre-run Tests:** Before the demo, ensure all scripts work and produce the expected errors.
* **Environment Setup:**
  * Confirm PostgreSQL is running with username "postgres" and password "password"
  * Verify the data validation plugin is running on port 8787
  * Make sure you've run the data generator (`python main.py`)
  * Test the PromptQL integration
* **Visual Aids:** Highlight the specific parts of the JSON Schema being discussed.
* **Prepare for Questions:** Be ready to explain how this approach scales to more complex real-world scenarios.
* **Technical Balance:** Adjust the technical depth based on your audience's expertise.
* **Real-world Context:** Relate each validation rule to a real business consequence if it were violated.
* **Data Agent Demo:** If possible, show a live demo of the data agent processing a natural language query.

## Potential Questions and Answers

**Q: How does this approach address the traditional tension between centralized governance and decentralized operations?**  
A: Traditional approaches have often tried to force centralization onto inherently decentralized organizations, which creates resistance and workarounds. Our approach recognizes that domain knowledge should remain with the teams that understand their data best, while providing centralized standards, visibility, and enforcement. The validation service acts as a bridge - teams own their rules but publish them to a central location where they can be enforced consistently. The natural language interface further democratizes access, allowing business users to engage with data quality without technical barriers. This balances the need for local autonomy with enterprise-wide consistency.

**Q: How does this work with existing APIs and data sources?**  
A: Absolutely! Hasura DDN's universal data access layer supports various data sources and protocols including REST, SQL, and others. The whole point is that you can connect to your existing systems regardless of their interfaces.

**Q: How do we handle schema evolution over time?**  
A: There are two aspects to this question. For rule evolution, JSON Schema supports versioning, and each validation run records the exact version of the rule applied at that point in time. When a schema changes, you'll be immediately aware if a rule fails, and since you own the library of rules, you can see exactly what changed. For each data request, you specify which rule to apply, and every rule detail and response is captured for historical tracking.

If you're asking about understanding schema evolution itself, that's actually covered in another demo. We have a plugin that tracks schema evolution and allows you to combine conversations about data validation with data schema evolution. This lets you correlate schema changes to data validation issues - for example, understanding if a new field or constraint in your database schema is causing validation failures.

**Q: What about performance impact?**  
A: The entire data validation service runs asynchronously, so the performance impact is minimal. While validation does add some overhead, it doesn't block or slow down user requests since it happens in parallel with other processing. Even when considering the total system impact, the overhead is typically just milliseconds. The benefit of catching data issues early far outweighs this small cost, especially since validation doesn't create any noticeable delay for end users.

**Q: How do data agents and PromptQL work with non-technical stakeholders?**  
A: The natural language interface allows business users to ask questions about data quality without knowing the technical details. They can request analysis, identify trends, and understand the impact of data quality issues in plain English. Data agents translate these natural language requests into the technical operations needed to retrieve, validate, and analyze the data, then present results back in natural language.

**Q: How do you maintain the distributed ownership of rules while centralizing validation?**  
A: Domain teams maintain ownership of their rules in whatever way works best for their processes - typically storing them as artifacts in a code repository. What's important is that every single data request includes the complete rule definition at execution time. This means the request and the rule definition are retained for every run, creating a complete audit trail. Everyone can see rule changes because the details of each execution are preserved, regardless of how teams manage their rule repositories.

It's worth noting that JSON Schema is not always immediately understandable by non-technical users. While simple cases are fairly comprehensible, complex rules can be difficult to grasp. This approach may require translation between business requirements and technical rule definitions. We've found that data agents can help bridge this gap - they can generate JSON Schema from natural language descriptions and explain existing rules in plain English, making rule creation and maintenance more accessible to business users.

**Q: How do you handle conflicts between rules from different domains?**  
A: The system doesn't automatically handle rule conflicts, but it provides the framework for identifying dependencies and potential conflicts. Using PromptQL and data agents, you could create an automated business process that detects when rules from different domains might conflict. When potential conflicts are detected, this process could escalate them to the relevant domain owners for resolution, with the data agent facilitating the discussion. This kind of conflict resolution workflow can be customized to fit your organization's governance structure.

**Q: Can data agents suggest improvements to rules based on observed data patterns?**  
A: Yes, data agents can analyze rule effectiveness and suggest additional rules or modifications based on data patterns and quality issues. This creates a continuous improvement loop where the data quality system gets smarter over time through both human and AI collaboration. Since we can capture the Python programs generated by PromptQL as artifacts, we can also evolve these programs over time while maintaining a version history of our analysis approach. However, it's important to note that while this demo shows the framework and technical capabilities, implementing a true continuous feedback loop requires additional effort to build business processes and automation around these capabilities. These solutions are often customized to each organization's specific needs. We have professional services that can help with implementing a complete solution or training your developers to do the work themselves.

**Q: How do you ensure analysis consistency over time with PromptQL?**  
A: PromptQL generates deterministic Python programs under the hood. In a production environment, we can save these programs and rerun them against fresh data, ensuring that our analysis is consistent over time. This gives us a reliable way to measure improvements without changes in methodology affecting the results.
