## Question 37: Describe the process of upgrading a LangChain project to LangGraph.

**Difficulty:** medium | **Tags:** migration

### Upgrading a LangChain Project to LangGraph

**Key Concepts**

- **LangGraph** is a new framework from the LangChain team, designed for building agentic and multi-step LLM workflows using a graph-based approach.
- **Migration** involves updating dependencies, refactoring code to use new APIs, and adapting to architectural changes.

---

#### Migration Process

1. **Update Dependencies**
   - Upgrade your packages to the latest versions:
     ```bash
     pip install -U langgraph langchain-core
     ```
   - For JavaScript/TypeScript projects, update import paths:
     ```js
     // Old
     import { createReactAgent } from "@langchain/langgraph/prebuilts";
     // New
     import { createAgent } from "langchain";
     ```

2. **Refactor Agent Creation**
   - The `create_react_agent` function is deprecated. Use `create_agent` instead.
   - Example (Python):
     ```python
     # Old
     from langchain.agents import create_react_agent
     agent = create_react_agent(...)
     
     # New
     from langchain.agents import create_agent
     agent = create_agent(...)
     ```

3. **Update State Management**
   - Replace custom or Pydantic-based agent states with the new `AgentState` from `langchain.agents`.
   - If you used `AgentStatePydantic` or similar, migrate to the new state model.

4. **Refactor Prompts and Middleware (JS/TS)**
   - The `prompt` parameter is now `systemPrompt`.
   - Pre/post-model hooks are replaced by middleware (`beforeModel`, `afterModel`).

5. **Pin and Test Versions**
   - Temporarily pin your LangChain version (e.g., `langchain>=0.2,<0.3`) before moving to the latest LangGraph.
   - Run your test suite to catch breaking changes early.

6. **Compile and Cache Graphs**
   - For performance, compile your graph (agent executor) at application start to avoid cold-start overhead.

---

#### Best Practices

- **Define State Schemas**: Use TypedDict (Python) or Zod (JS/TS) for your graph state to catch breaking changes.
- **Use LangSmith for Testing**: Integrate LangSmith’s pytest plugin to log run trees and score outputs with metrics.
- **Read Official Migration Guides**: Refer to the [LangGraph v1 migration guide](https://docs.langchain.com/oss/python/migrate/langgraph-v1) for detailed steps.

---

#### Common Pitfalls

- **Deprecation Issues**: Using deprecated functions like `create_react_agent` will break your code.
- **State Model Mismatches**: Not updating your agent state models can cause runtime errors.
- **Import Path Errors**: Failing to update import paths in JS/TS projects leads to module not found errors.

---

#### Real-World Example

Suppose you have a classic LangChain agent that uses `create_react_agent` and a custom Pydantic state. To migrate:

1. Update your dependencies.
2. Refactor agent creation to use `create_agent`.
3. Replace your Pydantic state with the new `AgentState`.
4. Update your tests and ensure everything passes.

---

**References:**
- [LangGraph v1 migration guide (Python)](https://docs.langchain.com/oss/python/migrate/langgraph-v1)
- [LangChain vs LangGraph: The Complete Migration Guide (Medium)](https://medium.com/@khankamranalwi/langchain-vs-langgraph-the-complete-migration-guide-7e78f2e8c570)
- [Migrating Classic LangChain Agents to LangGraph (Focused.io)](https://focused.io/lab/a-practical-guide-for-migrating-classic-langchain-agents-to-langgraph)

---

By following these steps and best practices, you can smoothly upgrade your LangChain project to leverage the advanced capabilities of LangGraph.

---

