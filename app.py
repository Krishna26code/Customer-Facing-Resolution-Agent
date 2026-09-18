import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="AIONOS Airline Resolution Agent",
    page_icon="✈️",
    layout="wide",
)

# -----------------------------
# Source data from the assignment
# -----------------------------
CUSTOMERS = {
    "Priya Nair": {
        "tier": "Gold",
        "pnr": "SK4821X",
        "email": "priya.nair@example.com",
        "phone": "+91-98xxxxxxx1",
        "history": "6 flights in last 12 months; 1 prior complaint (delayed baggage, resolved with voucher)",
    },
    "Arvind Kulkarni": {
        "tier": "Silver",
        "pnr": "TR1190B",
        "email": "arvind.kulkarni@example.com",
        "phone": "+91-98xxxxxxx2",
        "history": "3 flights, no prior complaints",
    },
    "Meher Kaur": {
        "tier": "Platinum",
        "pnr": "WL7742",
        "email": "meher.kaur@example.com",
        "phone": "+91-98xxxxxxx3",
        "history": "10 flights, 1 prior complaint (overbooking, resolved with a tier-status upgrade)",
    },
}

BOOKINGS = {
    "SK4821X": {
        "customer": "Priya Nair",
        "flight": "SK-204",
        "route": "Delhi → Goa",
        "date": "Wed 23 Sep 2026",
        "departure": "18:40",
        "status": "Cancelled (operational reason)",
        "cause": "airline",
    },
    "SK4821X_RETURN": {
        "customer": "Priya Nair",
        "flight": "Return",
        "route": "Goa → Delhi",
        "date": "Fri 25 Sep 2026",
        "departure": "16:20",
        "status": "Unaffected",
        "cause": "none",
    },
    "TR1190B": {
        "customer": "Arvind Kulkarni",
        "flight": "SK-118",
        "route": "Mumbai → Bengaluru",
        "date": "Wed 23 Sep 2026",
        "departure": "07:10",
        "status": "Delayed 4h (new departure 11:10)",
        "delay_hours": 4,
        "cause": "airline",
    },
    "WL7742": {
        "customer": "Meher Kaur",
        "flight": "SK-305",
        "route": "Delhi → Hyderabad",
        "date": "Wed 23 Sep 2026",
        "departure": "14:00",
        "status": "Delayed 6h (new departure 20:00)",
        "delay_hours": 6,
        "cause": "airline",
    },
}

POLICIES = {
    "Cancellation Rebooking Rule": "If a flight is cancelled by the airline, the customer is entitled to free rebooking on the next available flight within 24 hours, or a customer's choice.",
    "Delay Compensation Rule": "Delay under 3 hours: ₹500 meal voucher. Delay 3 hours or more: meal voucher + lounge access. Delay more than 5 hours: meal voucher + hotel accommodation, covering only the delayed hours (not a full night's stay).",
    "Refund Processing Rule": "Refunds for airline-caused cancellations are processed in full within 7 business days. Refunds are issued to the original payment method only.",
    "Fare Difference Rule": "If a customer voluntarily chooses to rebook on a higher-fare flight (not airline-caused), they must pay the fare difference. Agents cannot waive fare differences above ₹1,500.",
    "Loyalty Tier Rule": "Gold and Platinum tier customers get priority rebooking (first access to next-available seats) but no additional compensation beyond the standard policy.",
}

PROHIBITED = [
    "Approving any compensation beyond stated policy amounts.",
    "Waiving a fare difference above ₹1,500.",
    "Making exceptions for non-airline-caused disruptions (e.g. customer missed the flight).",
    "Handling threats of legal action or formal complaints — escalate immediately.",
    "Processing refunds to a different payment method than the original.",
]

SCENARIOS = {
    "Scenario 1 — Priya Nair": {
        "customer": "Priya Nair",
        "prompt": "Flight SK-204 (Delhi → Goa) is cancelled. Customer says she is “furious” and wants a full cash refund plus a free upgrade to business class on her return flight.",
    },
    "Scenario 2 — Arvind Kulkarni": {
        "customer": "Arvind Kulkarni",
        "prompt": "Flight SK-118 (Mumbai → Bengaluru) is delayed 4 hours. Customer is frustrated about missing a connecting meeting and asks for hotel accommodation.",
    },
    "Scenario 3 — Meher Kaur": {
        "customer": "Meher Kaur",
        "prompt": "Flight SK-305 (Delhi → Hyderabad) is delayed 6 hours. Customer asks for a full night's hotel stay rather than coverage for the delayed hours, and separately asks to be moved to a different, higher-fare flight instead of waiting — the fare difference is ₹2,000.",
    },
}

# -----------------------------
# Agent logic
# -----------------------------
def customer_context(name):
    c = CUSTOMERS[name]
    pnr = c["pnr"]
    booking = BOOKINGS[pnr]
    return c, booking

def policy_for_delay(hours):
    if hours > 5:
        return (
            "Meal voucher + lounge access + hotel accommodation covering only "
            "the delayed hours (not a full night's stay)."
        )
    if hours >= 3:
        return "Meal voucher + lounge access."
    return "₹500 meal voucher."

def classify_intent(text):
    t = text.lower()
    intents = []
    if any(x in t for x in ["refund", "money back", "cash back"]):
        intents.append("refund")
    if any(x in t for x in ["rebook", "rebooking", "another flight", "next flight", "move me"]):
        intents.append("rebooking")
    if any(x in t for x in ["hotel", "accommodation", "room"]):
        intents.append("hotel")
    if any(x in t for x in ["voucher", "meal", "food"]):
        intents.append("meal voucher")
    if any(x in t for x in ["lounge"]):
        intents.append("lounge")
    if any(x in t for x in ["complaint", "legal", "lawyer", "court", "sue"]):
        intents.append("formal complaint / legal threat")
    if any(x in t for x in ["compensation", "compensate", "pay me"]):
        intents.append("compensation")
    if not intents:
        intents.append("general status / resolution")
    return intents

def generate_response(name, user_text):
    c, b = customer_context(name)
    t = user_text.lower()
    intents = classify_intent(user_text)
    escalations = []
    actions = []
    sources = []

    # Immediate escalation for legal/formal complaint
    if "formal complaint / legal threat" in intents:
        escalations.append("Formal complaint or legal-action language requires immediate human escalation.")
        sources.append("Prohibited Actions for the Agent")

    # Cancellation
    if b["status"].lower().startswith("cancelled"):
        sources += ["Cancellation Rebooking Rule", "Refund Processing Rule", "Loyalty Tier Rule"]

        if "rebooking" in intents or any(x in t for x in ["upgrade", "business"]):
            actions.append("Offer free rebooking on the next available flight within 24 hours or the customer's choice.")
            if c["tier"] in ["Gold", "Platinum"]:
                actions.append(f"Apply {c['tier']} priority rebooking (first access to next-available seats).")
            if "business" in t or "upgrade" in t:
                escalations.append(
                    "A free business-class upgrade is not stated as an entitlement in the supplied policy; "
                    "do not promise it."
                )

        if "refund" in intents:
            actions.append("Initiate the full airline-cancellation refund request.")
            actions.append("Refund timeline: within 7 business days.")
            actions.append("Refund destination: original payment method only.")

        if "compensation" in intents:
            escalations.append("Do not approve compensation beyond the stated policy amounts.")

        if not actions and not escalations:
            actions.append("Confirm the cancellation and offer the permitted rebooking/refund paths.")

    # Delay
    elif "delay_hours" in b:
        hours = b["delay_hours"]
        sources += ["Delay Compensation Rule", "Fare Difference Rule", "Loyalty Tier Rule"]

        if "hotel" in intents:
            if hours > 5:
                actions.append(
                    "Arrange hotel accommodation covering the delayed hours only; a full night's stay is not covered."
                )
            else:
                escalations.append("Hotel accommodation is not provided by the stated policy for a delay of 5 hours or less.")

        if "rebooking" in intents or "higher-fare" in t or "fare difference" in t or "₹2,000" in t or "2000" in t:
            actions.append("A voluntary higher-fare rebooking is subject to the fare difference.")
            if "₹2,000" in t or "2000" in t:
                escalations.append("The requested ₹2,000 fare difference cannot be waived because the policy limits agent waivers to ₹1,500.")
            else:
                actions.append("If the customer chooses the higher-fare option, collect the applicable fare difference.")

        actions.append(policy_for_delay(hours))

        if "compensation" in intents:
            actions.append(f"Standard delay entitlement for {hours} hours: {policy_for_delay(hours)}")

    # Generic
    if not actions and not escalations:
        actions.append(f"Current booking status: {b['status']}.")

    if escalations:
        headline = "⚠️ Human review required"
    else:
        headline = "✅ Request can be handled under the supplied policy"

    response = [headline, ""]
    if actions:
        response.append("**Proposed action**")
        response.extend([f"- {a}" for a in actions])
    if escalations:
        response.append("")
        response.append("**Escalation / guardrail**")
        response.extend([f"- {e}" for e in escalations])
    response.append("")
    response.append("**Relevant source(s)**")
    response.extend([f"- {s}: {POLICIES.get(s, 'Agent safety/permission rule from assignment data.')}" for s in dict.fromkeys(sources)])

    return "\n".join(response), intents, actions, escalations, sources

def scenario_response(scenario_name):
    s = SCENARIOS[scenario_name]
    return generate_response(s["customer"], s["prompt"])

# -----------------------------
# UI
# -----------------------------
st.title("✈️ AIONOS — Customer-Facing Resolution Agent")
st.caption("Assignment 3: Airline Disruption | Source-grounded prototype")

with st.sidebar:
    st.header("Agent controls")
    customer = st.selectbox("Customer", list(CUSTOMERS.keys()))
    st.divider()
    st.subheader("Demo scenarios")
    selected_scenario = st.selectbox("Load scenario", ["— Select —"] + list(SCENARIOS.keys()))

    if st.button("Reset conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.audit = []
        st.rerun()

    st.divider()
    st.subheader("Safety rules")
    st.success("The agent only uses the supplied customer, booking and policy data.")
    st.warning("Unclear, prohibited or high-risk requests are escalated instead of invented around.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "audit" not in st.session_state:
    st.session_state.audit = []

# Scenario demo
if selected_scenario != "— Select —":
    s = SCENARIOS[selected_scenario]
    st.info(f"**Scenario input:** {s['prompt']}")
    if st.button("Run scenario", type="primary"):
        answer, intents, actions, escalations, sources = scenario_response(selected_scenario)
        st.session_state.messages.append({"role": "user", "content": s["prompt"]})
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.audit.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "customer": s["customer"],
            "intent": ", ".join(intents),
            "action": " | ".join(actions) if actions else "Escalated",
            "escalation": " | ".join(escalations) if escalations else "No",
            "sources": ", ".join(sources),
        })

# Customer summary
c, b = customer_context(customer)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Customer", customer)
col2.metric("Tier", c["tier"])
col3.metric("PNR", c["pnr"])
col4.metric("Flight status", b["status"].split("(")[0].strip())

with st.expander("Customer & booking data", expanded=False):
    st.write({
        "Email": c["email"],
        "Phone": c["phone"],
        "Travel history": c["history"],
        "Flight": b["flight"],
        "Route": b["route"],
        "Date": b["date"],
        "Scheduled departure": b["departure"],
        "Status": b["status"],
    })

# Chat history
st.subheader("Conversation")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about the disruption, refund, rebooking, hotel, compensation, etc.")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    answer, intents, actions, escalations, sources = generate_response(customer, prompt)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.audit.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "customer": customer,
        "intent": ", ".join(intents),
        "action": " | ".join(actions) if actions else "Escalated",
        "escalation": " | ".join(escalations) if escalations else "No",
        "sources": ", ".join(sources),
    })
    st.rerun()

# Bottom tabs
tab1, tab2, tab3 = st.tabs(["📚 Policy source", "🧾 Audit trail", "🛡️ Guardrails"])

with tab1:
    st.markdown("### Supplied service rules")
    for title, text in POLICIES.items():
        st.markdown(f"**{title}**")
        st.write(text)

with tab2:
    if st.session_state.audit:
        st.dataframe(st.session_state.audit, use_container_width=True, hide_index=True)
    else:
        st.info("No actions recorded yet. Run a scenario or ask the agent a question.")

with tab3:
    st.markdown("### Prohibited actions")
    for item in PROHIBITED:
        st.markdown(f"- 🚫 {item}")
    st.markdown("### Agent behaviour")
    st.markdown(
        "- Understand intent → check supplied data → apply policy → take permitted action → "
        "escalate when authority is missing → record the decision and sources."
    )

st.divider()
st.caption("Prototype note: This demo intentionally does not invent seat availability, prices, customer facts, policies, or actions that are not present in the assignment data.")
