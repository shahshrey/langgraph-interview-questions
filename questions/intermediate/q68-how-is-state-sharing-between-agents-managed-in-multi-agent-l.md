## Question 68: How is state-sharing between agents managed in multi-agent LangGraph systems?

**Difficulty:** medium | **Tags:** multi-agent, state sharing

**How State-Sharing Between Agents is Managed in Multi-Agent LangGraph Systems**

---

### Key Concepts

- **Centralized Shared State:**  
  In LangGraph, all agents (nodes) in a graph operate on a single, centralized state object. This state acts as a collaborative workspace, holding the current context, data, and results of the workflow. Each agent receives the current state as input, performs its logic, and returns a **partial state update** (a dict of just the keys it changed) — not a mutated full state.

- **State as a Data Structure:**  
  The shared state is defined by a schema — a `TypedDict`, Pydantic model, or dataclass. This state can include messages, intermediate results, agent-specific data, and global context.

- **State Updates and Merging (Reducers):**  
  When multiple agents update the state, LangGraph uses **reducers** declared on state keys (e.g., `Annotated[list, operator.add]` or `Annotated[list, add_messages]`) to combine changes. This ensures that updates from different agents are accumulated/merged rather than overwriting each other's contributions.

- **Subgraphs and Shared Keys:**  
  Each agent can itself be a **subgraph** (a compiled graph added as a node in the parent). If the subgraph's state schema shares keys with the parent (e.g., `messages`), state flows between them automatically on those overlapping keys; non-shared keys stay private to the subgraph. If the schemas differ entirely, you wrap the subgraph in a node function that transforms state in and out.

- **Handoffs with `Command`:**  
  Agents can both update shared state and route control by returning `Command(update={...}, goto="other_agent")` from a node. An agent running inside a subgraph can hand off to a sibling agent in the parent graph with `Command(goto="other_agent", graph=Command.PARENT)`. Prebuilt libraries such as `langgraph-supervisor` and `langgraph-swarm` package these handoff patterns.

---

### Code Example

A simplified example of state sharing in LangGraph:

```python
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

# Define the shared state structure with reducers for merged keys
class SharedState(TypedDict):
    messages: Annotated[list, operator.add]  # updates are appended, not overwritten
    results: dict

# Define agent nodes — each returns a partial update (or a Command)
def agent_a(state: SharedState) -> Command:
    # ... agent A logic ...
    return Command(
        update={"messages": ["Agent A processed"], "results": {"A": "Result from A"}},
        goto="agent_b",  # hand off to agent B, sharing the updated state
    )

def agent_b(state: SharedState):
    # Agent B can read everything agent A contributed via `state`
    return {"messages": ["Agent B processed"]}

# Build the graph
builder = StateGraph(SharedState)
builder.add_node("agent_a", agent_a)
builder.add_node("agent_b", agent_b)
builder.add_edge(START, "agent_a")
builder.add_edge("agent_b", END)
graph = builder.compile()

result = graph.invoke({"messages": [], "results": {}})
```

In this example, both agents read from and contribute updates to the same shared state; the `messages` reducer appends each agent's contribution, and `Command` performs the agent-to-agent handoff. (In a subgraph-based design, an inner agent would use `Command(goto="agent_b", graph=Command.PARENT)` to hand off at the parent level.)

---

### Best Practices

- **Design Clear State Schemas:**  
  Define explicit, typed schemas for your shared state to avoid confusion and ensure data integrity.

- **Minimize State Conflicts:**  
  Structure your workflow so that agents update different parts of the state, or declare reducers on keys that multiple agents write to (required when parallel branches update the same key).

- **Use Subgraphs for Agent-Private State:**  
  Give each agent its own subgraph state schema and share only the keys (e.g., `messages`) that genuinely need to be visible to other agents; or use prebuilt `langgraph-supervisor`/`langgraph-swarm` architectures.

- **Use State for Coordination:**  
  Agents can use the shared state to coordinate actions, pass messages, and track progress, enabling complex multi-agent workflows.

---

### Common Pitfalls

- **State Overwrites:**  
  If agents are not careful, they may overwrite each other’s updates. Always merge changes thoughtfully.

- **Scalability Bottlenecks:**  
  The centralized state can become a bottleneck if many agents try to update it simultaneously. Consider workflow design and state partitioning for large-scale systems.

---

### Real-World Example

- **Research Workflow:**  
  In a research assistant scenario, one agent gathers data, another analyzes it, and a third generates a report. All agents contribute their findings to the shared state, ensuring seamless collaboration and traceability.

---

### References

- [LangGraph Multi-Agent Overview (LangChain Docs)](https://docs.langchain.com/oss/python/langgraph/multi-agent)
- [LangGraph Subgraphs (LangChain Docs)](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)
- [AWS Blog: Build Multi-Agent Systems with LangGraph](https://aws.amazon.com/blogs/machine-learning/build-multi-agent-systems-with-langgraph-and-amazon-bedrock/)

---

**Summary:**  
LangGraph manages state-sharing in multi-agent systems through a centralized, typed state object that all agents read from and contribute partial updates to, with reducers merging concurrent writes. Subgraphs share state with the parent through overlapping keys, and `Command`-based handoffs (including `graph=Command.PARENT`) let agents update shared state while routing control. This approach enables flexible, collaborative, and traceable workflows, but requires careful design to avoid conflicts and bottlenecks.

---

