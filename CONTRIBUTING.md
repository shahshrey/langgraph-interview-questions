# Contributing to LangGraph Interview Questions

First off, thank you for considering contributing to this project! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Question Format](#question-format)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

---

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

---

## How Can I Contribute?

### 🆕 Adding New Questions

1. Check existing questions to avoid duplicates
2. Follow the [Question Format](#question-format) below
3. Place in appropriate difficulty category
4. Include relevant tags

### 🐛 Fixing Errors

- Typos and grammatical errors
- Code bugs or outdated syntax
- Incorrect information
- Broken links

### 📚 Improving Content

- Better explanations
- Additional code examples
- More real-world scenarios
- Updated references

### 🌐 Translations

We welcome translations to other languages. Create a new folder like `questions/es/` for Spanish, etc.

---

## Question Format

Every question should follow this template:

```markdown
## Question [N]: [Question Title]

**Difficulty:** easy | medium | hard | **Tags:** tag1, tag2, tag3

[Brief answer/introduction paragraph]

---

### Key Concepts

- **Concept 1**: Explanation
- **Concept 2**: Explanation

---

### Code Example

```python
# Well-commented, working code example
from langgraph.graph import StateGraph

# ... implementation
```

---

### Best Practices

- Practice 1
- Practice 2

---

### Common Pitfalls

- Pitfall 1
- Pitfall 2

---

### Real-World Example

Description of a practical application scenario.

---

### References

- [Link Title](URL)
- [Link Title](URL)

---

**Summary:**  
One-paragraph summary of the key takeaway.
```

---

## Difficulty Guidelines

| Level | Criteria |
|-------|----------|
| **Easy** | Foundational concepts, basic syntax, getting started topics |
| **Medium** | Implementation details, common patterns, integration tasks |
| **Hard** | System design, optimization, production concerns, edge cases |

---

## Pull Request Process

1. **Fork** the repository at [https://github.com/shahshrey/langgraph-interview-questions](https://github.com/shahshrey/langgraph-interview-questions)
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/langgraph-interview-questions.git
   cd langgraph-interview-questions
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/add-question-73
   # or
   git checkout -b fix/q15-code-example
   ```
4. **Make your changes** following the style guidelines
5. **Test** any code examples you add
6. **Commit** with clear messages:
   ```bash
   git commit -m "Add Q73: How to implement custom checkpointing"
   ```
7. **Push** to your fork:
   ```bash
   git push origin feature/add-question-73
   ```
8. **Open a Pull Request** on GitHub with:
   - Clear title describing the change
   - Description of what was added/changed
   - Any relevant issue numbers (e.g., "Fixes #42")

### For New Questions

When adding a new question, you should:
1. Add it to `answers/langgraph-study-guide.md` following the format
2. Run the split script to generate individual files:
   ```bash
   python3 scripts/split_questions.py
   ```
3. Update links in `README.md` if needed
4. Commit all changes together

---

## Style Guidelines

### Markdown

- Use ATX-style headers (`#`, `##`, `###`)
- Add blank lines before and after code blocks
- Use fenced code blocks with language identifiers

### Code Examples

- Use Python 3.10+ syntax
- Include necessary imports
- Add comments explaining key parts
- Ensure code is runnable
- Use type hints where appropriate

### Tags

Use existing tags when possible:

| Category | Tags |
|----------|------|
| Core | `basics`, `concepts`, `state`, `workflow`, `nodes`, `edges` |
| Agents | `agents`, `agentic ai`, `multi-agent`, `react pattern` |
| Integration | `integration`, `rag`, `tools`, `cloud` |
| Operations | `production`, `deployment`, `monitoring`, `testing` |
| Advanced | `optimization`, `scalability`, `security`, `concurrency` |

---

## Questions?

Feel free to open an issue for any questions about contributing!

---

Thank you for helping make this resource better for everyone! 🙏
