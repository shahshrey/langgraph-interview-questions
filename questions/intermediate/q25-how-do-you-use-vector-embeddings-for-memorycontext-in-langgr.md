## Question 25: How do you use vector embeddings for memory/context in LangGraph?

**Difficulty:** medium | **Tags:** embeddings, memory

**Using Vector Embeddings for Memory/Context in LangGraph**

LangGraph leverages vector embeddings to enable long-term and context-aware memory for AI agents. Here’s how it works and how you can implement it:

---

### **Key Concepts**

- **Vector Embeddings**: These are numerical representations of text (such as conversation history, user facts, or documents) that capture semantic meaning. They allow for similarity search and retrieval of relevant information.
- **Memory Store**: LangGraph's long-term memory API is the `Store` (`InMemoryStore` for development, `PostgresStore` for production, Redis-backed stores via `langgraph-checkpoint-redis`). When configured with an embedding `index`, the store supports semantic (vector similarity) search over stored memories.
- **Contextual Retrieval**: When an agent needs context, it queries the vector store for embeddings similar to the current conversation or query, retrieving relevant past information to inform its response.

---

### **How It Works in LangGraph**

1. **Storing Memories**:
   - Configure the store with an embedding `index`; when an agent encounters new information (e.g., user input, facts, or events) and writes it with `put`, the store generates and indexes an embedding automatically.
   - Memories are organized by namespace (e.g., per user) with metadata.
   - Example (Python):
     ```python
     from langgraph.store.memory import InMemoryStore
     from langchain.embeddings import init_embeddings

     store = InMemoryStore(
         index={"embed": init_embeddings("openai:text-embedding-3-small"), "dims": 1536}
     )
     store.put(("memories", user_id), mem_id, {"content": content, "context": context})
     ```

2. **Retrieving Context**:
   - When the agent needs to recall relevant information, it searches the store with a natural-language query; the store embeds the query and performs a vector similarity search to find the most relevant past memories.
   - Example:
     ```python
     memories = store.search(("memories", user_id), query=current_query, limit=5)
     # Use retrieved memories to augment the agent's context
     ```

3. **Integrating with Agent State**:
   - The store is passed to `compile(store=...)` and accessed inside nodes (e.g., via the runtime), so retrieved memories can be injected into the agent’s state or prompt for more informed, context-aware responses.

---

### **Best Practices**

- **Choose the Right Store Backend**: For production, use persistent backends like `PostgresStore` (pgvector-backed) or Redis instead of `InMemoryStore` for scalability and reliability.
- **Namespace Memories**: Organize embeddings by user or session to avoid cross-contamination of context.
- **Update Regularly**: Continuously update the memory store with new embeddings as conversations progress.
- **Filter and Rank**: Use metadata and similarity scores to filter and rank retrieved memories for relevance.

---

### **Common Pitfalls**

- **Storing Too Much Data**: Unfiltered storage can lead to performance issues. Regularly prune or archive old or irrelevant embeddings.
- **Poor Embedding Quality**: Use high-quality embedding models (e.g., OpenAI, HuggingFace) to ensure semantic relevance.
- **Lack of Namespacing**: Not separating user or session data can cause context leakage between users.

---

### **Real-World Example**

- **AI Assistant with Long-Term Memory**: An AI assistant built with LangGraph and Redis stores embeddings of every user interaction. When a user returns, the assistant retrieves relevant past conversations using vector similarity, enabling personalized and coherent interactions over time.
  - See: [YouTube Tutorial: Long-Term Memory with LangGraph & Redis](https://www.youtube.com/watch?v=fsENEq4F55Q)
  - Example code: [LangGraph apps with Redis (GitHub)](https://github.com/redis-developer/langgraph-apps-with-redis)

---

**References:**
- [LangGraph Memory Overview](https://docs.langchain.com/oss/python/langgraph/memory)
- [Comprehensive Guide: Long-Term Agentic Memory With LangGraph (Medium)](https://medium.com/@anil.jain.baba/long-term-agentic-memory-with-langgraph-824050b09852)
- [Built-in PostgreSQL Store for Long-Term Memory & Vector Similarity Search (LangChain Forum)](https://forum.langchain.com/t/langgraph-cloud-using-the-built-in-postgresql-store-for-long-term-memory-ltm-and-vector-similarity-search/245)

---

**Summary:**  
LangGraph uses vector embeddings to store and retrieve relevant memories, enabling agents to maintain context across sessions. This is achieved by embedding content, storing it in a vector store, and performing similarity searches to retrieve contextually relevant information for each new interaction. Proper management of the vector store and embedding quality is crucial for effective memory.

---

