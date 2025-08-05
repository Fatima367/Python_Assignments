### Assignment

# Console-Based Support Agent System using OpenAI Agents SDK

### 🧠 Objective:
**Build a multi-agent system in the console using the OpenAI Agents SDK. The system must:**

* Handle different types of user queries (billing, technical, general)
* Use agent-to-agent handoffs
* Implement tools with dynamic is_enabled logic
* Pass context between agents
* Include guardrails for output validation (optional challenge)


### 🛠️ Required Concepts (must use):
|**Concept**	|	**Requirement** |
|---------------|-------------------|
|🧠 Agents     | At least 3 agents (triage + specialized) |
|🔧 Tools		| Each specialized agent must have at least 1 tool |
|⚙️ is_enabled()  |	At least 1 tool must be conditionally enabled using context |
|🔁 Handoffs		| Triage agent must decide which agent to hand off to |
|📦 Context		| Use context to carry user info (e.g., is_premium, issue_type) |
|🎛 CLI Interface		| Console-based input/output (no GUI required) |



#### 📦 Suggested Agent Architecture:

### 💡 Features to Implement:
* Dynamic tool gating:
* refund() only enabled if is_premium_user == True
* restart_service() only if issue_type == "technical"
* Handoffs:
    Triage agent routes based on context (e.g., user says "I want a refund" → handoff to Billing)
* Context injection:
    Use a Pydantic model to store context (e.g., name, is_premium_user, issue_type)
* Output:
    Print tool outputs and handoff transitions in the console

### 🧪 Bonus (Optional):
Add an OutputGuardrail to make sure output never contains any apology statements ("sorry", etc)
Use stream_events() to show tool execution steps


-------------------------------------

[complete details](https://docs.google.com/document/d/1gZwuQuW5HTjNEVTfaGX56brdR5I0oj11/edit?usp=sharing&ouid=103459919058078389355&rtpof=true&sd=true).


- Submission form: [https://forms.gle/1uwdntcc2CsjRRWe7](https://forms.gle/1uwdntcc2CsjRRWe7)