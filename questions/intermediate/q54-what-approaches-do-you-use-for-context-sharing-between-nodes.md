## Question 54: What approaches do you use for context sharing between nodes in a graph?

**Difficulty:** medium | **Tags:** context sharing

### Approaches for Context Sharing Between Nodes in LangGraph

**Key Concepts**

- **State Object**: In LangGraph, the primary mechanism for sharing context between nodes is the mutable "state" object. This object is passed from node to node and can be updated at each step, allowing nodes to read from and write to a shared context as the workflow progresses.
- **Static vs. Dynamic Context**:
  - **Static Runtime Context**: Immutable data (e.g., user metadata, tool handles, DB connections) passed at the start of a run via the `context` argument to `invoke` or `stream`. This context is available to all nodes but cannot be changed during the run.
  - **Dynamic Runtime Context (State)**: Mutable data that evolves during a single run, managed through the LangGraph state object. This is the main way nodes share and update information.

**How Context Sharing Works**

- When a run starts, a static context is initialized and remains constant throughout the run.
- The state object is passed between nodes. Each node can:
  - Read from the state to access context set by previous nodes.
  - Update the state with new information, which will be available to subsequent nodes.
- Nodes can format and combine different pieces of context (e.g., search results, user history) into prompts or actions for downstream nodes.

**Code Example**

```python
def draft_response(state: EmailAgentState) -> Command[Literal["human_review", "send_reply"]]:
    # Access context from state
    context_sections = []
    if state.get('search_results'):
        formatted_docs = "\n".join([f"- {doc}" for doc in state['search_results']])
        context_sections.append(f"Relevant documentation:\n{formatted_docs}")
    if state.get('customer_history'):
        context_sections.append(f"Customer tier: {state['customer_history'].get('tier', 'standard')}")
    # Build prompt with context
    draft_prompt = f"""
    Draft a response to this customer email:
    {state['email_content']}
    {chr(10).join(context_sections)}
    """
    response = llm.invoke(draft_prompt)
    # Update state with new response
    return Command(update={"draft_response": response.content})
```

**Best Practices**

- **Keep State Structured**: Use clear, well-defined keys in the state object to avoid accidental overwrites or confusion between nodes.
- **Immutable Static Context**: Use static context for configuration or resources that should not change during a run.
- **Avoid Mid-Run Context Mutation**: The static context should not be mutated mid-run to prevent inconsistencies, especially in orchestrations with multiple agents or subgraphs.
- **Explicit Updates**: Always explicitly update the state object with new data rather than relying on side effects.

**Common Pitfalls**

- **Mixing Static and Dynamic Context**: Confusing the immutable static context with the mutable state can lead to bugs.
- **Overwriting State**: Accidentally overwriting important state keys can break downstream nodes.
- **Not Passing Required Context**: Failing to include all necessary context in the state can cause nodes to lack the information they need.

**Real-World Example**

- In an email agent workflow, one node might add search results and customer history to the state. The next node formats these into a prompt for an LLM, generates a draft response, and updates the state with the draft. The final node decides whether to send the reply or escalate for human review, all based on the evolving shared state.

**References**
- [LangGraph Context Overview (LangChain Docs)](https://docs.langchain.com/oss/python/concepts/context)
- [Thinking in LangGraph (LangChain Docs)](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
- [LangGraph Forum: Passing Runtime Context](https://forum.langchain.com/t/support-passing-runtime-context-in-send-api/1735)

This approach ensures robust, flexible, and traceable context sharing between nodes in LangGraph workflows.

---

