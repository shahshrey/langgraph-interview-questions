#!/usr/bin/env python3
"""
Script to split the monolithic study guide into individual question files
organized by difficulty level.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


def parse_study_guide(file_path: Path) -> List[Dict[str, str]]:
    """Parse the study guide and extract all questions."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by question headers (## Question N:)
    question_pattern = r'(## Question \d+:.*?)(?=## Question \d+:|$)'
    questions = re.findall(question_pattern, content, re.DOTALL)
    
    parsed_questions = []
    
    for question_text in questions:
        # Extract question number and title
        match = re.match(r'## Question (\d+): (.+?)\n', question_text)
        if not match:
            continue
            
        question_num = int(match.group(1))
        question_title = match.group(2).strip()
        
        # Extract difficulty and tags
        difficulty_match = re.search(r'\*\*Difficulty:\*\* (\w+)', question_text)
        tags_match = re.search(r'\*\*Tags:\*\* (.+)', question_text)
        
        difficulty = difficulty_match.group(1) if difficulty_match else 'medium'
        tags = tags_match.group(1) if tags_match else ''
        
        # Create filename from title
        filename_base = question_title.lower()
        # Remove special characters and replace spaces with hyphens
        filename_base = re.sub(r'[^\w\s-]', '', filename_base)
        filename_base = re.sub(r'[\s]+', '-', filename_base)
        filename_base = re.sub(r'-+', '-', filename_base)
        filename_base = filename_base[:60]  # Limit length
        
        filename = f"q{question_num:02d}-{filename_base}.md"
        
        parsed_questions.append({
            'number': question_num,
            'title': question_title,
            'difficulty': difficulty,
            'tags': tags,
            'filename': filename,
            'content': question_text
        })
    
    return parsed_questions


def get_category_folder(difficulty: str) -> str:
    """Map difficulty to folder name."""
    mapping = {
        'easy': 'basics',
        'medium': 'intermediate',
        'hard': 'advanced'
    }
    return mapping.get(difficulty.lower(), 'intermediate')


def write_question_files(questions: List[Dict], base_path: Path):
    """Write individual question files to appropriate folders."""
    
    stats = {'easy': 0, 'medium': 0, 'hard': 0}
    
    for q in questions:
        category = get_category_folder(q['difficulty'])
        folder = base_path / 'questions' / category
        folder.mkdir(parents=True, exist_ok=True)
        
        file_path = folder / q['filename']
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(q['content'])
        
        stats[q['difficulty'].lower()] = stats.get(q['difficulty'].lower(), 0) + 1
        print(f"✓ Created {category}/{q['filename']}")
    
    return stats


def create_category_indexes(questions: List[Dict], base_path: Path):
    """Create index files for each category."""
    
    categories = {
        'basics': {'title': '🟢 Easy Questions', 'questions': []},
        'intermediate': {'title': '🟡 Medium Questions', 'questions': []},
        'advanced': {'title': '🔴 Hard Questions', 'questions': []}
    }
    
    # Group questions by category
    for q in questions:
        category = get_category_folder(q['difficulty'])
        categories[category]['questions'].append(q)
    
    # Create index for each category
    for category, data in categories.items():
        if not data['questions']:
            continue
            
        folder = base_path / 'questions' / category
        index_path = folder / 'README.md'
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f"# {data['title']}\n\n")
            f.write(f"Total questions: **{len(data['questions'])}**\n\n")
            f.write("---\n\n")
            f.write("## Questions\n\n")
            f.write("| # | Question | Tags |\n")
            f.write("|---|----------|------|\n")
            
            for q in sorted(data['questions'], key=lambda x: x['number']):
                f.write(f"| Q{q['number']} | [{q['title']}]({q['filename']}) | `{q['tags']}` |\n")
            
            f.write("\n---\n\n")
            f.write("[← Back to All Questions](../README.md)\n")
        
        print(f"✓ Created {category}/README.md")


def main():
    """Main execution."""
    print("🔍 Parsing study guide...\n")
    
    base_path = Path(__file__).parent.parent
    study_guide_path = base_path / 'answers' / 'langgraph-study-guide.md'
    
    if not study_guide_path.exists():
        print(f"❌ Study guide not found at {study_guide_path}")
        return
    
    # Parse questions
    questions = parse_study_guide(study_guide_path)
    print(f"Found {len(questions)} questions\n")
    
    print("📝 Writing individual question files...\n")
    stats = write_question_files(questions, base_path)
    
    print(f"\n📊 Creating category indexes...\n")
    create_category_indexes(questions, base_path)
    
    print(f"\n✅ Done!")
    print(f"\nStatistics:")
    print(f"  🟢 Easy:   {stats.get('easy', 0)} questions")
    print(f"  🟡 Medium: {stats.get('medium', 0)} questions")
    print(f"  🔴 Hard:   {stats.get('hard', 0)} questions")
    print(f"  📚 Total:  {len(questions)} questions")


if __name__ == '__main__':
    main()
