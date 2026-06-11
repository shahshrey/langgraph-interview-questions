## Question 53: How do rollback and retry mechanisms work in LangGraph?

**Difficulty:** hard | **Tags:** rollback, retry

**Rollback and Retry Mechanisms in LangGraph**

---

### **Key Concepts**

#### **Retry Mechanism**
- **Purpose:** Automatically re-attempts failed node executions in a LangGraph workflow, making agent systems more resilient to transient errors (e.g., network hiccups, temporary API failures).
- **How it Works:**
  - Each node in a LangGraph can be assigned a **Retry Policy**.
  - The policy specifies:
    - **Number of retry attempts** (`max_attempts`)
    - **Backoff between retries** (`initial_interval`, `backoff_factor`, `max_interval`, `jitter`)
    - **Types of errors to retry on** (`retry_on` — e.g., timeouts, connection errors, rate limits, or a custom predicate)
  - If a node fails, LangGraph will retry it according to the policy. If it succeeds on a later attempt, the workflow continues as normal.
  - If all retries are exhausted, the failure is treated as final, and the workflow can either halt or trigger fallback/error handling logic.

**Example:**
```python
from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy

retry_policy = RetryPolicy(
    max_attempts=3,
    initial_interval=2.0,  # seconds before first retry
    backoff_factor=2.0,    # exponential backoff
    retry_on=(TimeoutError, ConnectionError),
)

def call_api_node(state):
    # API call logic here
    ...

builder = StateGraph(State)
builder.add_node("call_api", call_api_node, retry_policy=retry_policy)
```
- **Best Practices:**
  - Use retries for transient errors, not for critical or persistent failures.
  - Log all retry attempts for observability.
  - Combine with fallback nodes for graceful degradation.

#### **Rollback Mechanism (Checkpointing and Time Travel)**
- **Purpose:** Restores the workflow to a previous stable state after an error, allowing for error recovery or alternative execution paths.
- **How it Works:**
  - Rollback is built on LangGraph's **persistence layer**: compile the graph with a checkpointer (e.g., `InMemorySaver`, `PostgresSaver`), and a checkpoint is saved at every super-step of execution for the given `thread_id`.
  - Use **time travel** to roll back: `graph.get_state_history(config)` lists all prior checkpoints, `graph.update_state(config, values)` edits state (creating a new forked checkpoint), and invoking the graph with a config containing a specific `checkpoint_id` replays/forks execution from that point.
  - If a run crashes mid-execution, simply re-invoking the graph with the same `thread_id` resumes from the last successful checkpoint — only incomplete nodes are re-executed.
  - **Durability modes** control when checkpoints are written: `durability="exit"` (only at run end), `"async"` (written in the background, the default), or `"sync"` (written before the next step — most durable).
  - Rollback is typically triggered when retries are exhausted or a critical error is detected.
  - After rollback, the workflow can either retry the failed branch, switch to a fallback, or halt for manual intervention.

**Example:**
```python
from langgraph.checkpoint.memory import InMemorySaver

graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "1"}}
graph.invoke(input_state, config, durability="sync")

# Roll back: pick an earlier checkpoint and resume/fork from it
history = list(graph.get_state_history(config))
past = history[2]  # some earlier checkpoint
graph.invoke(None, past.config)  # replay/fork from that checkpoint

# Or repair the state first, then continue
graph.update_state(config, {"status": "retry_pending"})
```

- **Best Practices:**
  - Always compile with a checkpointer in production so every step is recoverable.
  - Note that forking from an earlier checkpoint abandons (does not merge) the work done after it on that branch.
  - Use rollback in combination with error logging and alerting for critical failures.

---

### **Real-World Example**

Suppose you have a LangGraph workflow for sending emails:
- The "Send Email" node is wrapped with a retry policy (e.g., retry up to 3 times on network errors).
- If all retries fail, the workflow rolls back to the state before the email was attempted and triggers a fallback node (e.g., log the failure and notify an admin).

---

### **Common Pitfalls**
- **Overusing retries:** Can lead to long delays or rate limit issues if not bounded.
- **Relying solely on rollback:** Since rollback discards intermediate state, important context may be lost.
- **Not handling persistent errors:** Retries are for transient issues; persistent failures require different handling (e.g., alerting, manual intervention).

---

### **References**
- [LangGraph Durable Execution / Retry Policies](https://docs.langchain.com/oss/python/langgraph/durable-execution)
- [LangGraph Persistence (Checkpointers)](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph Time Travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel)
- [A Beginner's Guide to Handling Errors in LangGraph with Retry Policies (dev.to)](https://dev.to/aiengineering/a-beginners-guide-to-handling-errors-in-langgraph-with-retry-policies-h22)

---

**Summary:**  
LangGraph's retry mechanism provides structured, policy-driven retries for failed nodes, while rollback allows restoration to previous states after critical errors. Both are essential for building robust, fault-tolerant agent workflows, but must be used thoughtfully to avoid data loss and ensure graceful error handling.

---

