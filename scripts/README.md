# Scripts

Utility scripts for managing the LangGraph Interview Questions repository.

## split_questions.py

Automatically splits the monolithic study guide into individual question files organized by difficulty.

### Usage

```bash
python3 scripts/split_questions.py
```

### What it does

1. Reads `full-guide/langgraph-study-guide.md`
2. Extracts all 72 questions
3. Creates individual `.md` files in:
   - `questions/basics/` for easy questions
   - `questions/intermediate/` for medium questions
   - `questions/advanced/` for hard questions
4. Generates category README files with navigation

### When to use

- After adding new questions to the study guide
- After updating existing questions
- To regenerate all individual files from the master document

### Output

```
✓ Created basics/q01-what-is-langgraph-and-how-does-it-differ-from-langchain.md
✓ Created basics/q02-explain-the-core-concept-of-a-stategraph-in-langgraph.md
...
✓ Created basics/README.md
✓ Created intermediate/README.md
✓ Created advanced/README.md
```

## Future Scripts

Planned utility scripts:
- `validate_links.py` - Check all markdown links are valid
- `generate_stats.py` - Generate repository statistics
- `check_format.py` - Validate question format consistency
