# Fiduciary Abuse Test Scenarios

These test scenarios simulate potential fiduciary abuse by guardians managing the financial accounts of individuals. They focus on suspicious transaction patterns that could indicate misappropriation of funds.

## Test Scenarios for Fiduciary Abuse Detection

**Scenario 1: Direct Transfer to Guardian**

* **Setup:**
    * Creates accounts for both a consumer (John Doe) and their guardian (Jane Smith).
    * Establishes a guardian relationship between John Doe and Jane Smith.
    * Funds are present in John Doe's account.
* **Test:**
    * A series of transactions are initiated, showing direct transfers of funds from John Doe's account to Jane Smith's account.
    * These transactions vary in amount and time, simulating a pattern of funds being moved.
    * The transactions are direct transfers from the consumer to the guardian.
* **Objective:**
    * To detect instances where a guardian directly receives funds from the consumer's account without a clear, legitimate purpose.

**Scenario 2: Guardian Disburses Similar Amount After Receiving Funds**

* **Setup:**
    * Creates accounts for a consumer (Alice Johnson) and their guardian (Bob Williams).
    * Establishes a guardian relationship between Alice Johnson and Bob Williams.
    * Funds are present in Alice Johnson's account.
* **Test:**
    * Funds are transferred from Alice Johnson's account to Bob Williams' account.
    * Shortly after, Bob Williams disburses a similar amount, often through different transaction types (e.g., online purchases, ATM withdrawals, casino withdrawals).
    * Large transfers are made from the consumer to the guardian, and then the guardian quickly disperses the funds.
* **Objective:**
    * To identify situations where a guardian receives funds and quickly uses them for personal expenses or in ways that suggest misappropriation.
    * To detect rapid disbursement after fund receipt.

**Scenario 3: Multiple Guardians and Transactions**

* **Setup:**
    * Creates accounts for a consumer (Charlie Brown) and multiple guardians (Lucy Van Pelt and Linus Van Pelt).
    * Establishes guardian relationships between Charlie Brown and both Lucy and Linus.
    * Funds are present in Charlie Browns account.
* **Test:**
    * Transactions are initiated, showing transfers of funds from Charlie Brown's account to both Lucy and Linus.
    * Lucy and Linus then make subsequent transactions from their own accounts, showing how the funds are used.
    * The transactions show funds moving to multiple guardians, and then those guardians spending the funds.
* **Objective:**
    * To detect abuse in scenarios involving multiple guardians, where funds might be moved between guardians or used in ways that are difficult to track.
    * To detect abuse when multiple guardians are involved.

## Key Elements for Detection:

* **Direct transfers:** Funds moving directly from the consumer's account to the guardian's account.
* **Rapid disbursement:** Funds being spent quickly after being received by the guardian.
* **Transaction patterns:** Unusual transaction types or amounts that deviate from typical spending habits.
* **Multiple guardians:** Scenarios involving more than one guardian, potentially masking misappropriation.
* **Timestamps:** The time between transactions is important, to show quick movements of funds.
* **Transaction descriptions:** The descriptions of the transactions can show red flags, like casino withdrawls.

These summarized scenarios provide a clear framework for documenting and executing tests designed to detect potential fiduciary abuse.
