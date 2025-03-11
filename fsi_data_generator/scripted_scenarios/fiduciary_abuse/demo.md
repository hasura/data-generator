# Live Demo Tutorial: Detecting Fiduciary Misconduct with a Data Agent

**Goal:** To demonstrate how a data agent can analyze complex financial data to identify and address fiduciary misconduct, showcasing its speed, accuracy, and efficiency.

**Target Audience:** Potential clients in the financial services industry.

**Demo Flow:**

## Phase 1: Setting the Stage (0:00 - 1:32)

1.  **Introduction (0:00-0:11):**
    * Start with enthusiasm: "Hi, I'm excited to show you how data agents can revolutionize financial services by providing repeatable, accurate, and testable data analysis."
    * Briefly introduce the concept of data agents and their potential in financial compliance.
2.  **Building the Foundation (0:11-1:01):**
    * **Data Model Creation (0:11-0:19):** Explain the necessity of a realistic data model. "First, we establish a data model that mirrors a typical operational environment within financial services. This ensures the analysis reflects real-world scenarios."
    * **Hasura Super Graph (0:19-0:42):** "We then use this model to generate a Hasura super graph, establishing relationships between data elements to simulate information flows and identify potential compliance issues. This is built upon the structure of a typical financial enterprise’s data."
    * **Metadata Importance (0:42-0:51):** Emphasize the role of high-quality metadata. "Crucially, we enrich the super graph with detailed metadata for every element, ensuring clarity and accuracy. This metadata is essential for the data agent to understand and interpret the data correctly."
    * **Generated Fake Data (0:51-1:01):** "To populate the model for this demonstration, we use generated, fake data. This allows us to showcase the agent's capabilities without relying on sensitive information. **If you were to implement this within your organization, you would use anonymized production data from your own systems to ensure realism and relevance.**"
3.  **Defining the Problem (1:01-1:32):**
    * **Fiduciary Misconduct Scenario (1:01-1:12):** Introduce the sample problem: "We'll demonstrate how the data agent detects fiduciary misconduct. We've inserted specific, controlled records simulating this issue into the data."
    * **Agent's Task (1:12-1:32):** "The goal is for the data agent to sift through the generated data, find the signal we inserted, mirroring the operational scale you would encounter, to identify the misconduct and provide actionable insights. **This process could be replicated with your own anonymized production data for internal analysis.**"

## Phase 2: Executing the Analysis (1:32 - 4:00)

4.  **Explaining the Analysis (1:32-2:22):**
    * **General Explanation (1:32-1:54):** "We provide the data agent with two types of instructions. First, a general explanation: it's an expert in financial services data analysis and a Python programmer, with general guidance on the analysis."
    * **Specific Prompt (1:54-2:11):** "Then, we give a specific, step-by-step prompt on how to identify the issue. Each step is simple, with instructions to store and reuse information."
    * **Addressing LLM Limitations (2:11-2:22):** "This structured approach helps the agent overcome limitations of large language models by ensuring information retention and flow, especially when dealing with the complexity of real-world data."
5.  **Live Demonstration with PromptQL (2:22-4:00):**
    * **PromptQL Interaction (2:22-2:30):** "Now, let's see it in action with PromptQL, our data agent. I'll paste the four-step prompt."
    * **Step 1: Identifying Fiduciary Relationships (2:30-2:45):** "First, the agent identifies fiduciary relationships within the system, based on the relationships defined in the generated data." (Show the results, e.g., "Guardian is a fiduciary.")
    * **Step 2: Finding Relevant Accounts (3:00-3:10):** "Next, it finds fiduciaries and principals who bank at the same institution, using the generated account data." (Show the results.)
    * **Step 3: Detecting Suspicious Transactions (3:10-3:40):** "Then, it looks for suspicious transactions, like withdrawals from the principal's account to the fiduciary's, including potentially obfuscated transfers, within the context of the generated transaction records." (Show the results, highlighting variations like timing or amount discrepancies.)
    * **Step 4: Determining Next Steps (3:40-4:00):** "Finally, the agent determines the appropriate next steps, such as regulatory reporting, based on typical bank policy, applied to the generated data scenarios." (Show the final report, including risk levels and recommended actions.)

## Phase 3: Highlighting the Benefits (4:00 - 4:35)

6.  **Summarize the Results (4:00-4:16):**
    * Emphasize the clarity and efficiency of the results. "As you can see, the agent provides a clear breakdown of each issue, including risk levels and recommended actions"
7.  **Highlight Key Advantages (4:16-4:27):**
    * Focus on the speed and efficiency. "We achieved this result using metadata and semantic analysis on data at scale, significantly reducing the time and effort compared to traditional methods. **You could achieve similar results using your own anonymized production data in your own environment.**"
    * Emphasize the reduction of data movement, reduced cost, faster time-time-market, the increased relevance of potential internal results, and the ability to use this as a platform to extend into all types of compliance issues.
8.  **Call to Action (4:27-4:35):**
    * "I hope you found this demonstration insightful, particularly how it delivers realistic and actionable insights. **Imagine the potential of replicating this process within your own organization. Any questions?**

## Key Tips for the Sales Engineer:

* **Clarify Generated Data:** Clearly state that the demo uses generated, fake data.
* **Emphasize Client Data Use:** Emphasize that clients would use *their own* anonymized production data for internal implementation.
* **Data Security:** Reassure clients about data security and anonymization principles when they implement in their environment.
* **Tailoring:** Adapt the demo to the client's industry and compliance needs.
* **Clarity:** Explain complex concepts in simple, easy-to-understand language.
* **Enthusiasm:** Let your passion for the technology shine through.
* **Keep it concise:** Respect the audiences time.
