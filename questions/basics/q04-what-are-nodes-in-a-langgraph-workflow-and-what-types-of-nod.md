## Question 4: What are nodes in a LangGraph workflow, and what types of nodes are commonly used?

**Difficulty:** easy | **Tags:** workflow, nodes

**Nodes in a LangGraph Workflow**

**Key Concepts:**
- In LangGraph, a **node** is a fundamental building block representing a single step or operation in a workflow.
- Each node acts like a "station" in a workflow, receiving input (state), performing a specific task, and outputting a new or updated state.
- Nodes are connected by **edges**, which define the flow of data and logic between steps.

**Common Types of Nodes:**
1. **LLM (Language Model) Nodes:**  
   These nodes invoke a language model (like OpenAI's GPT) to process input and generate output. For example, a node might generate a story, joke, or poem based on user input.

2. **Router/Decision Nodes:**  
   These nodes decide which path or node to send the workflow to next, based on the current state or input. They are often used for conditional logic or branching.

3. **Function/Processing Nodes:**  
   These nodes perform specific computations or transformations on the state, such as formatting data, calling APIs, or running custom logic.

4. **Start and End Nodes:**  
   - **START**: The entry point of the workflow.
   - **END**: The exit point, where the workflow concludes.

**Code Example:**
```python
def llm_call_1(state):
    # Node that generates a story
    result = llm.invoke(state["input"])
    return {"output": result.content}

def llm_call_router(state):
    # Node that routes to the appropriate next node
    decision = router.invoke([
        SystemMessage(content="Route the input to story, joke, or poem."),
        HumanMessage(content=state["input"]),
    ])
    return {"decision": decision.step}
```
Nodes are added to the workflow graph and connected via edges:
```python
builder.add_node("story_node", llm_call_1)
builder.add_node("router_node", llm_call_router)
builder.add_edge(START, "router_node")
builder.add_conditional_edges("router_node", route_decision)
builder.add_edge("story_node", END)
```

**Best Practices:**
- Keep each node focused on a single responsibility for clarity and maintainability.
- Use router/decision nodes to manage complex branching logic.
- Ensure the state schema passed between nodes is well-defined and consistent.

**Common Pitfalls:**
- Overloading nodes with too many responsibilities, making debugging and maintenance harder.
- Inconsistent state schemas between nodes, leading to errors in data flow.

**Real-World Example:**
A customer support workflow might have:
- An LLM node to draft a response.
- A router node to decide if the response needs human review or can be sent automatically.
- Function nodes to fetch customer history or relevant documentation.

**References:**
- [LangGraph Docs: Workflows and Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
- [LangGraph Basics: Understanding State, Schema, Nodes, and Edges (Medium)](https://medium.com/@vivekvjnk/langgraph-basics-understanding-state-schema-nodes-and-edges-77f2fd17cae5)
- [Understanding Core Concepts of LangGraph (Dev.to)](https://dev.to/raunaklallala/understanding-core-concepts-of-langgraph-deep-dive-1d7h)

In summary, nodes in LangGraph are modular steps in a workflow, commonly including LLM nodes, router/decision nodes, function nodes, and start/end nodes, all working together to enable flexible, multi-step AI workflows.

---

