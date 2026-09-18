# ✈️ AIONOS — Customer-Facing Resolution Agent

A Streamlit prototype for **Assignment 3: Customer-Facing Resolution Agent** from the AIONOS Agentic AI Factory assignment.

The prototype models an airline disruption support agent that understands customer intent, checks supplied booking/customer data, applies the supplied service policies, recommends the permitted next action, escalates requests outside agent authority, and maintains an audit trail.

---

## 📌 Assignment Objective

Build an agent for a realistic customer journey such as airline disruption, banking support, telecom complaint, or hotel guest service.

For the airline-disruption version, the agent should:

- Understand the customer's intent
- Ask only necessary questions
- Use supplied data and policies
- Recommend or execute the correct next action
- Handle an angry or confused customer
- Escalate when authority is missing
- Preserve a clear conversation and action record

This project focuses on the airline disruption use case.

---

## 🚀 Features

### Customer & Booking Context
The app includes three sample customers:

- **Priya Nair** — Gold
- **Arvind Kulkarni** — Silver
- **Meher Kaur** — Platinum

For each customer, the agent can use:

- Customer tier
- PNR
- Email and phone
- Travel history
- Flight number
- Route
- Date
- Scheduled departure
- Current disruption status

### Intent Detection

The agent recognizes requests related to:

- Refunds
- Rebooking
- Hotel accommodation
- Meal vouchers
- Lounge access
- Compensation
- Formal complaints / legal threats
- General status and resolution questions

### Policy-Grounded Resolution

The prototype uses the supplied assignment policies for:

- Cancellation rebooking
- Delay compensation
- Refund processing
- Fare differences
- Loyalty-tier priority rebooking

### Escalation & Guardrails

The agent does not invent permissions or exceptions.

Examples:

- A business-class upgrade is not automatically promised.
- Fare differences above ₹1,500 cannot be waived by the agent.
- Legal threats / formal complaints are escalated.
- Compensation outside the stated policy is not approved.
- Refunds are not redirected to a different payment method.

### Audit Trail

Each interaction records:

- Time
- Customer
- Detected intent
- Proposed action
- Escalation status
- Relevant source/policy

---

## 🗂️ Project Structure

```text
Customer-Facing-Resolution-Agent/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 💻 Requirements

Recommended environment:

- Python **3.10–3.13**
- Streamlit

### Important for this project

On some Windows systems, `python` may point to an old Python 2 installation.

For example:

```text
python --version
Python 2.7.13

py --version
Python 3.13.9
```

In that situation, use the Python launcher:

```powershell
py -3.13
```

instead of:

```powershell
python
```

---

## ⚙️ Installation

Open Command Prompt or PowerShell inside the project directory.

### 1. Confirm Python

```powershell
py --version
```

You should see Python 3.10+.

### 2. Upgrade pip

```powershell
py -3.13 -m pip install --upgrade pip
```

### 3. Install dependencies

```powershell
py -3.13 -m pip install -r requirements.txt
```

### 4. Run the Streamlit app

```powershell
py -3.13 -m streamlit run app.py
```

Streamlit will provide a local URL, normally similar to:

```text
http://localhost:8501
```

Open that URL in your browser.

---

## 🎬 Demo Flow

The sidebar contains three ready-made scenarios.

### Scenario 1 — Priya Nair

Flight **SK-204 (Delhi → Goa)** is cancelled.

The customer is furious and requests:

- Full cash refund
- Free business-class upgrade on the return flight

The agent should:

1. Identify the cancellation.
2. Recognize the refund request.
3. Apply the cancellation refund rule.
4. Recognize that a business-class upgrade is not stated as an entitlement.
5. Avoid promising an unsupported upgrade.

---

### Scenario 2 — Arvind Kulkarni

Flight **SK-118 (Mumbai → Bengaluru)** is delayed by 4 hours.

The customer is frustrated because of a missed meeting and asks for hotel accommodation.

The agent should:

1. Identify a 4-hour airline-caused delay.
2. Apply the delay compensation rule.
3. Provide meal voucher + lounge access.
4. Recognize that hotel accommodation is not provided for a delay of 5 hours or less.

---

### Scenario 3 — Meher Kaur

Flight **SK-305 (Delhi → Hyderabad)** is delayed by 6 hours.

The customer asks for:

- A full night's hotel stay
- A different higher-fare flight
- Waiver of a ₹2,000 fare difference

The agent should:

1. Apply the >5-hour delay policy.
2. Provide hotel accommodation only for the delayed hours.
3. Apply the higher-fare rebooking rule.
4. Refuse to waive the ₹2,000 fare difference because the agent waiver limit is ₹1,500.
5. Escalate requests outside the agent's authority.

---

## 🧠 Agent Decision Flow

```text
Customer Message
       │
       ▼
Understand Intent
       │
       ▼
Check Customer + Booking Data
       │
       ▼
Find Relevant Supplied Policy
       │
       ▼
Is Requested Action Permitted?
       │
   ┌───┴────┐
   │        │
  YES       NO / UNCLEAR
   │        │
   ▼        ▼
Propose    Escalate
Action     to Human
   │        │
   └───┬────┘
       ▼
Record Decision + Source
       │
       ▼
Respond to Customer
```

---

## 📚 Source & Assumptions

The prototype is intentionally based on the supplied assignment data.

It does **not** invent:

- Seat availability
- Flight prices
- Additional compensation
- Customer information
- Airline policies
- Agent permissions
- External booking results

The application is a prototype and does not connect to a live airline reservation system.

---

## 🛡️ Guardrails

The agent follows these prohibited-action rules:

- Do not approve compensation beyond stated policy amounts.
- Do not waive a fare difference above ₹1,500.
- Do not make exceptions for non-airline-caused disruptions.
- Escalate threats of legal action or formal complaints.
- Do not process refunds to a different payment method.

When a request is outside the supplied authority, the application shows a human-review / escalation message rather than making up an answer.

---

## 🧾 Audit Trail

The **Audit trail** tab provides a structured record of agent interactions.

Example fields:

| Field | Description |
|---|---|
| Time | Time of interaction |
| Customer | Customer involved |
| Intent | Detected customer intent |
| Action | Proposed action |
| Escalation | Whether human review is required |
| Sources | Policies used for the decision |

---

## 🖥️ Main UI Sections

### Sidebar
- Customer selector
- Demo scenario selector
- Run scenario
- Reset conversation
- Safety rules

### Customer Summary
Displays:

- Customer
- Tier
- PNR
- Flight status

### Conversation
Chat interface for interacting with the agent.

### Policy Source
Displays the supplied policies used by the resolution logic.

### Audit Trail
Displays the structured interaction history.

### Guardrails
Displays prohibited actions and the agent's decision behaviour.

---

## 🔧 Technology

- **Python**
- **Streamlit**
- Rule/policy-based resolution logic
- In-memory sample customer and booking data

No external API key is required to run the current prototype.

---

## 📦 Deployment

The app can be deployed on a Streamlit-compatible hosting environment after uploading:

```text
app.py
requirements.txt
README.md
```

For local demonstration:

```powershell
py -3.13 -m streamlit run app.py
```

---

## 🎯 Demo Talking Points

For a 15-minute assignment demo, explain:

1. **Problem** — airline disruption creates frustrated customers and requires policy-aware decisions.
2. **Input** — customer message + supplied booking/customer data.
3. **Intent detection** — identifies refund, rebooking, hotel, compensation, etc.
4. **Policy grounding** — maps the intent to the supplied service rule.
5. **Decision** — determines whether the agent can handle the request.
6. **Escalation** — routes prohibited or unclear requests to human review.
7. **Auditability** — records intent, action, escalation and source.
8. **Safety** — the agent does not invent policies, permissions or customer facts.
9. **Demo scenarios** — show all three supplied cases.
10. **Future scope** — connect the same flow to live airline booking, CRM, ticketing and policy systems.

---

## ⚠️ Prototype Disclaimer

This is an assignment prototype. It does not execute real bookings, refunds, hotel reservations, or payments.

All customer and booking information included in the application is sample data for demonstration.

---

## 👤 Project

**AIONOS — Agentic AI Factory**

**Use Case:** Customer-Facing Resolution Agent  
**Domain:** Airline Disruption Support  
**Framework:** Streamlit
