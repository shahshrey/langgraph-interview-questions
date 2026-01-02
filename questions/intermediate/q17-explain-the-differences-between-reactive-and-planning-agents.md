## Question 17: Explain the differences between reactive and planning agents in LangGraph.

**Difficulty:** medium | **Tags:** agentic ai, agents

**Differences Between Reactive and Planning Agents in LangGraph**

---

### **Key Concepts**

#### **Reactive Agents**
- **Definition**: Reactive agents respond immediately to inputs without maintaining memory or long-term strategy.
- **Behavior**: They operate in a "thought-act-observe" loop, making decisions based solely on the current input and environment.
- **Use Cases**: Best for simple, short-lived tasks such as summarizing text, translating, or tagging emails.
- **Example**: A chatbot that answers a single question or performs a one-step action.

#### **Planning Agents**
- **Definition**: Planning agents take a goal, break it into sub-tasks, and execute them iteratively, often using memory and feedback loops.
- **Behavior**: They devise a multi-step plan, execute each step, observe results, and adjust the plan as needed. They can checkpoint state and recover from errors.
- **Use Cases**: Ideal for complex, long-running workflows like research assistants, customer support bots that recall past conversations, or agents managing multi-step business processes.
- **Example**: An agent that researches a topic, gathers sources, summarizes findings, and compiles a report.

---

### **Code Example (Pseudocode)**

**Reactive Agent:**
```python
def reactive_agent(input):
    action = decide_action(input)
    result = execute_action(action)
    return result
```

**Planning Agent:**
```python
def planning_agent(goal):
    plan = create_plan(goal)
    for step in plan:
        result = execute_step(step)
        update_plan_based_on(result)
    return final_result
```

---

### **Best Practices**
- **Choose Reactive Agents** for fast, lightweight, and stateless tasks.
- **Choose Planning Agents** when tasks require memory, error recovery, or multi-step reasoning.
- **Hybrid Approaches**: For some workflows, start with a planning agent to break down the task, then use reactive agents for each sub-task.

---

### **Common Pitfalls**
- Using reactive agents for complex tasks can lead to incomplete or unreliable results.
- Overengineering with planning agents for simple tasks can add unnecessary complexity and cost.

---

### **Real-World Example**
- **Reactive**: A support bot that answers "What are your business hours?" instantly.
- **Planning**: A customer service agent that tracks a user's previous issues, follows up on unresolved tickets, and coordinates with other systems to resolve complex problems.

---

### **References**
- [Magic of Agent Architectures in LangGraph](https://www.cohorte.co/blog/magic-of-agent-architectures-in-langgraph-building-smarter-ai-systems)
- [Plan-and-Execute Agents in LangGraph](https://blog.langchain.com/planning-agents/)
- [Planning vs Reactivity: Architecting Agent Behavior](https://softbuilds.medium.com/planning-vs-reactivity-architecting-agent-behavior-76c9f1e1ee11)
- [Planning vs ReAct AI Agents: Choosing the Right Approach](https://www.linkedin.com/posts/lewisowain_how-to-build-an-ai-agent-activity-7402339630764941312-_G5h)

---

**Summary**:  
Reactive agents in LangGraph are best for quick, stateless responses, while planning agents excel at handling complex, multi-step tasks with memory and adaptability. The choice depends on the complexity and requirements of your workflow.

---

