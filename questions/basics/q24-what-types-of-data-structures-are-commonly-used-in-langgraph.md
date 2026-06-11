## Question 24: What types of data structures are commonly used in LangGraph nodes and edges?

**Difficulty:** easy | **Tags:** data structures

**LangGraph** is a framework for building graph-based AI workflows, where the main components are nodes (which perform actions) and edges (which define transitions between nodes). The data structures used in nodes and edges are designed to support flexible, modular, and stateful workflows.

---

### Key Data Structures in LangGraph Nodes and Edges

#### 1. **State (Dictionary/Schema)**
- **Nodes** in LangGraph operate on a shared state, which is defined by a schema — most commonly a `TypedDict`, but a Pydantic model or dataclass also works.
- This state holds all the information that needs to be passed between nodes, such as user input, intermediate results, or context.
- The schema ensures that the data structure is consistent and interpretable across all nodes and edges.
- Example:
  ```python
  import operator
  from typing import Annotated
  from typing_extensions import TypedDict

  class State(TypedDict):
      messages: Annotated[list, operator.add]  # reducer: appends instead of overwriting
      user_id: int
      context: dict
  ```

#### 2. **Nodes (Functions or Callables)**
- Each node is usually a function or callable object that takes the current state as input and returns a **partial update** dict, which LangGraph merges into the state (using any reducers defined on the schema).
- Nodes are registered on the graph builder by name with `add_node`.
- Example:
  ```python
  def greet_node(state: State) -> dict:
      return {"messages": ["How can I help you?"]}
  ```

#### 3. **Edges (Transitions)**
- **Edges** define the possible transitions between nodes. Static edges are declared with `add_edge`, while conditional (dynamic) routing uses `add_conditional_edges` with a routing function that inspects the current state and returns the name of the next node.
- Example:
  ```python
  from langgraph.graph import StateGraph, START, END

  builder = StateGraph(State)
  builder.add_node("greet_node", greet_node)
  builder.add_node("process_input", process_input)
  builder.add_edge(START, "greet_node")
  builder.add_edge("greet_node", "process_input")
  builder.add_conditional_edges(
      "process_input",
      lambda state: END if state["context"].get("done") else "greet_node",
      ["greet_node", END],
  )
  graph = builder.compile()
  ```

---

### Best Practices
- **Use a well-defined state schema** (e.g., Pydantic models or dataclasses) to ensure type safety and clarity.
- **Keep node functions pure** (no side effects) for easier testing and debugging.
- **Design edges to be flexible**, allowing for both static and dynamic transitions.

### Common Pitfalls
- Inconsistent state structure can lead to errors when nodes expect different data formats.
- Overly complex edge logic can make the workflow hard to follow and debug.

---

### Real-World Example
In a chatbot built with LangGraph:
- The state might include a list of messages, user profile data, and conversation context.
- Nodes could be functions like `greet_user`, `process_question`, and `end_conversation`.
- Edges would define how the conversation flows based on user input and state (e.g., if the user says "bye", transition to `end_conversation`).

---

**References:**
- [LangGraph Basics: Understanding State, Schema, Nodes, and Edges (Medium)](https://medium.com/@vivekvjnk/langgraph-basics-understanding-state-schema-nodes-and-edges-77f2fd17cae5)
- [LangGraph Core Components Explained (Towards AI)](https://pub.towardsai.net/langgraph-core-components-explained-with-a-simple-graph-d822d324c322)
- [LangGraph Docs - Graph API Overview](https://docs.langchain.com/oss/python/langgraph/graph-api)

---

