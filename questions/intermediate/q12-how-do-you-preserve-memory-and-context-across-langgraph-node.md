## Question 12: How do you preserve memory and context across LangGraph nodes?

**Difficulty:** medium | **Tags:** memory, context

### Preserving Memory and Context Across LangGraph Nodes

**Key Concepts**

- **State Management:** In LangGraph, memory and context are preserved by maintaining a shared state object that is passed between nodes. Each node receives the current state, can read from it, and update it as needed.
- **Thread-Scoped Checkpoints:** LangGraph uses thread-scoped checkpoints to persist the agent’s state, ensuring that memory is maintained across different steps and even across different runs or threads.
- **Memory Stores:** LangGraph supports various memory backends (e.g., in-memory, Redis, or custom stores) to persist and retrieve context, conversation history, or other relevant data.

---

**How It Works**

- **State Object:** The state is typically a dictionary-like object (e.g., Python’s TypedDict or a custom class) that holds all relevant information, such as user input, conversation history, and any intermediate results.
- **Node Functions:** Each node in the graph is a function that takes the current state as input and returns an updated state. This allows nodes to add, modify, or use context as needed.
- **Persistence Layer:** For long-term or cross-session memory, LangGraph can use persistent stores (like Redis or a database) in combination with the checkpointer, which saves and restores state at each node transition.

---

**Code Example**

```python
from langgraph.graph import StateGraph

class MemoryState(TypedDict):
    input: str
    history: str

def process_input(state: MemoryState) -> MemoryState:
    user_input = state['input']
    prev_history = state.get('history', '')
    new_history = prev_history + "\n" + user_input
    return {"input": user_input, "history": new_history}

builder = StateGraph(MemoryState)
builder.add_node("input_handler", process_input)
builder.set_entry_point("input_handler")
builder.add_edge("input_handler", "END")
graph = builder.compile()

# Each invocation preserves and updates the context
result = graph.invoke({"input": "Hello", "history": ""})
```

For persistent memory, you might use Redis:

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def redis_node(state: dict) -> dict:
    user_id = state["user_id"]
    prev_history = r.get(f"user:{user_id}:history") or ""
    new_history = prev_history + "\n" + state["input"]
    r.set(f"user:{user_id}:history", new_history)
    return {"user_id": user_id, "input": state["input"], "history": new_history}
```

---

**Best Practices**

- **Design State Carefully:** Ensure your state object contains all information needed for downstream nodes.
- **Use Persistent Stores for Long-Term Memory:** For applications requiring memory across sessions or users, integrate a persistent backend.
- **Minimize State Size:** Only store what’s necessary to avoid performance bottlenecks.

---

**Common Pitfalls**

- **State Overwrites:** Accidentally overwriting state fields can lead to loss of context. Always merge or append to existing state where appropriate.
- **Concurrency Issues:** When using persistent stores, ensure thread safety and handle concurrent updates properly.

---

**Real-World Example**

- **Conversational Agents:** A chatbot built with LangGraph can remember previous user messages, preferences, or tasks by storing them in the state and/or a persistent memory store. Each node (e.g., intent detection, response generation) accesses and updates this shared context, enabling coherent multi-turn conversations.

---

**References**
- [LangGraph Memory Overview (LangChain Docs)](https://docs.langchain.com/oss/python/langgraph/memory)
- [LangGraph Memory Management Example (Medium)](https://sangeethasaravanan.medium.com/langgraph-memory-management-add-context-awareness-to-llm-workflows-16ff71f13d10)
- [LangGraph Persistence (LangChain Docs)](https://docs.langchain.com/oss/python/langgraph/persistence)

LangGraph’s approach to memory and context is both flexible and robust, making it suitable for complex, stateful AI workflows.

---

