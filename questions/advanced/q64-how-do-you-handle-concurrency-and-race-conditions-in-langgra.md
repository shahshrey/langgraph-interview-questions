## Question 64: How do you handle concurrency and race conditions in LangGraph?

**Difficulty:** hard | **Tags:** concurrency

### Handling Concurrency and Race Conditions in LangGraph

**Key Concepts**

- **Concurrency in LangGraph**: LangGraph enables parallel execution of nodes (tasks/agents) within a workflow graph. This is essential for multi-agent orchestration, where multiple tools or agents may need to run simultaneously.
- **Race Conditions**: These occur when multiple concurrent branches try to read or write shared state, potentially leading to inconsistent or unpredictable results.

---

#### How LangGraph Handles Concurrency

1. **Parallel Nodes and Deferred Execution**
   - LangGraph allows you to dispatch multiple branches in parallel using explicit graph constructs.
   - The `defer` mechanism ensures that certain nodes (like a supervisor or reducer) only execute after all parallel branches have completed. This acts as a synchronization barrier, preventing premature access to incomplete results.
   - Example (from [Medium: Parallel Nodes in LangGraph](https://medium.com/@gmurro/parallel-nodes-in-langgraph-managing-concurrent-branches-with-the-deferred-execution-d7e94d03ef78)):

     ```python
     builder.add_node("supervisor", supervisor, defer=True)
     # supervisor waits for all parallel branches to finish
     ```

2. **Reducers: The Core Mechanism for Safe Parallel Writes**
   - LangGraph enforces strict update protocols to shared state. Each node returns a partial state update, and updates are merged in a controlled manner.
   - **Reducers** declared on state keys (e.g., `results: Annotated[list, operator.add]`, or `Annotated[list, add_messages]` for chat messages) define how concurrent updates to the same key are combined. With a reducer, parallel branches can safely write to the same key — their updates are merged deterministically.
   - **Without a reducer**, if two nodes in the same super-step write to the same state key, LangGraph raises an `InvalidUpdateError` rather than silently letting one write clobber the other. This makes parallel-write conflicts explicit instead of producing race conditions.

3. **Dynamic Fan-out with the Send API**
   - `Send` (from `langgraph.types`) dispatches a variable number of parallel tasks at runtime (map-reduce style), each with its own payload, from a conditional edge or a `Command(goto=[...])`.
   - Combined with reducers on the accumulating state keys, this enables safe, dynamic concurrency.

4. **Error Handling and Observability**
   - LangGraph provides mechanisms to observe and debug workflows, making it easier to detect and recover from concurrency issues or tool failures.
   - If a tool or agent fails, LangGraph can recover gracefully, ensuring the overall workflow remains robust ([source](https://medium.com/@bhagyarana80/llm-agents-and-race-conditions-debugging-multi-tool-ai-with-langgraph-b0dcbf14fa67)).

---

#### Code Example: Parallel Branches with Synchronization

```python
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

class State(TypedDict):
    tasks: list
    # Reducer merges concurrent writes; without it, parallel writes
    # to "results" would raise InvalidUpdateError
    results: Annotated[list, operator.add]

def dispatch(state: State):
    # Dynamic fan-out: one parallel branch per task
    return [Send("worker", {"task": t}) for t in state["tasks"]]

def worker(state: dict):
    return {"results": [f"done: {state['task']}"]}

def aggregate(state: State):
    return {"results": [f"summary of {len(state['results'])} results"]}

builder = StateGraph(State)
builder.add_node("worker", worker)
# defer=True: aggregate waits until all pending parallel tasks finish
builder.add_node("aggregate", aggregate, defer=True)
builder.add_conditional_edges(START, dispatch, ["worker"])
builder.add_edge("worker", "aggregate")
builder.add_edge("aggregate", END)

graph = builder.compile()
graph.invoke({"tasks": ["search", "calculate", "api_call"], "results": []})
```
- Here, `Send` dispatches parallel branches, the reducer on `results` merges their writes safely, and the deferred `aggregate` node only runs once all branches have finished, preventing race conditions.

---

#### Best Practices

- **Declare reducers** on every state key that parallel branches may write to; otherwise LangGraph raises `InvalidUpdateError` on concurrent writes.
- **Use deferred execution** (`defer=True`) for nodes that aggregate or depend on parallel results.
- **Design explicit synchronization points** (reducers, deferred aggregators) to ensure all branches complete before merging state.
- **Avoid direct shared state mutation** in parallel branches; return partial update dicts and let reducers merge them.
- **Monitor and log** workflow execution to detect and debug concurrency issues early.

---

#### Common Pitfalls

- Failing to synchronize branches can lead to incomplete or inconsistent state aggregation.
- Writing to the same state key from parallel branches without a reducer fails at runtime with `InvalidUpdateError`; forgetting reducers is the most common concurrency mistake.
- Not handling tool/agent failures in parallel branches can leave the workflow in a stuck or inconsistent state.

---

#### Real-World Example

- In a multi-tool LLM agent scenario, LangGraph can run search, calculator, and API calls in parallel. By deferring the aggregation node, it ensures all results are collected before proceeding, thus avoiding race conditions and ensuring reliable, consistent outputs ([source](https://medium.com/@bhagyarana80/llm-agents-and-race-conditions-debugging-multi-tool-ai-with-langgraph-b0dcbf14fa67)).

---

**Summary**:  
LangGraph handles concurrency and race conditions by providing explicit constructs for parallel execution, deferred synchronization, and controlled state management. By enforcing these patterns, it enables robust, scalable, and reliable multi-agent workflows.

---

