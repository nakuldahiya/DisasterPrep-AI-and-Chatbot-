def generate_prompt(user_input, disaster, intent):

    if disaster is None:
        return """
You are a disaster assistant.

If the query is not related to disasters, respond:
"I can only help with disaster-related queries."
"""

    if intent == "plan":
        return f"""
You are an expert Disaster Management Planner.

Create a detailed plan for {disaster}.

Structure:
1. Before the disaster
2. During the disaster
3. After the disaster

Make it practical, clear, and actionable.

User request:
{user_input}
"""

    return f"""
You are a disaster safety expert.

Provide step-by-step safety guidance for {disaster}.

Keep it:
- Clear
- Practical
- Focused on safety

User question:
{user_input}
"""