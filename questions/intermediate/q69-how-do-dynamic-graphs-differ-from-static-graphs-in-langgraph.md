## Question 69: How do dynamic graphs differ from static graphs in LangGraph?

**Difficulty:** medium | **Tags:** dynamic, static

**Dynamic vs. Static Graphs in LangGraph**

**Key Concepts**

- **Static Graphs**: In LangGraph, a static graph is defined at design time. The structure—nodes (steps) and edges (transitions)—is fixed and does not change during execution. The flow of data and control is predetermined, and the developer explicitly specifies how the workflow proceeds from one node to another.

- **Dynamic Graphs**: A dynamic graph, on the other hand, adapts its structure at runtime. The next node or action is determined based on the current state, context, or results of previous steps. This allows for more flexible, agentic, and adaptive workflows, where the path through the graph can change depending on the data or decisions made during execution.

---

**Detailed Explanation**

- **Static Graphs**
  - The workflow is explicitly defined by the developer.
  - All possible transitions and paths are known ahead of time.
  - Example: A sequence of steps for data processing where each step always follows the previous one, regardless of the data.
  - **Best for**: Predictable, repeatable processes where the logic does not need to adapt to changing input or context.

- **Dynamic Graphs**
  - The workflow can change at runtime based on the current state or outputs.
  - The next node is chosen dynamically, often using logic or even an LLM (Language Model) to decide what to do next.
  - Example: An agent that decides which tool to use or which branch to follow based on the user's query or intermediate results.
  - **Best for**: Agentic workflows, complex decision-making, or when the process must adapt to new information.

---

**Code Example**

*Static Graph Example:*
```python
from langgraph import StateGraph

graph = StateGraph()
graph.add_node("step1", step1_function)
graph.add_node("step2", step2_function)
graph.add_edge("step1", "step2")
graph.set_entry_point("step1")
```
*This graph always runs step1, then step2.*

*Dynamic Graph Example:*
```python
def dynamic_router(state):
    if state["needs_review"]:
        return "human_review"
    else:
        return "send_reply"

graph.add_node("router", dynamic_router)
graph.add_edge("router", "human_review")
graph.add_edge("router", "send_reply")
```
*Here, the next step is chosen at runtime based on the state.*

---

**Best Practices**
- Use static graphs for simple, linear, or well-defined workflows.
- Use dynamic graphs when you need flexibility, such as in agentic systems or when integrating with LLMs for decision-making.
- Clearly document the logic for dynamic routing to ensure maintainability.

**Common Pitfalls**
- Overcomplicating simple workflows with unnecessary dynamic routing.
- Not handling all possible states or transitions in dynamic graphs, leading to runtime errors.

---

**Real-World Example**
- **Static**: A data ETL pipeline where data always flows through the same cleaning, transformation, and loading steps.
- **Dynamic**: A customer support agent that decides whether to escalate a ticket, send an automated reply, or ask for more information based on the content and urgency of the incoming message.

---

**References**
- [Dynamic Planning vs Static Workflows: What Truly Defines an AI Agent (Medium)](https://tao-hpu.medium.com/dynamic-planning-vs-static-workflows-what-truly-defines-an-ai-agent-b13ca5a2d110)
- [LangGraph 101: Let's Build A Deep Research Agent (Towards Data Science)](https://towardsdatascience.com/langgraph-101-lets-build-a-deep-research-agent/)
- [Thinking in LangGraph (LangChain Docs)](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)

---

