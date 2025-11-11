"""
Test the improved class name generation
Shows before/after examples
"""

def old_method(title: str) -> str:
    """Old method - creates very long names"""
    words = title.replace("-", " ").replace("_", " ").split()
    return "".join(word.capitalize() for word in words if word.isalnum())


def new_method(title: str) -> str:
    """New method - creates concise names"""
    skip_words = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
        'could', 'may', 'might', 'must', 'can', 'to', 'of', 'in', 'on', 'at',
        'by', 'for', 'with', 'from', 'as', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'between', 'under', 'again', 'further', 'then',
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'both',
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'write',
        'create', 'update', 'delete', 'add', 'remove', 'get', 'fetch', 'make',
        'new', 'this', 'that', 'these', 'those', 'mention', 'below', 'above'
    }
    
    words = title.replace("-", " ").replace("_", " ").split()
    meaningful_words = []
    
    for word in words:
        clean_word = ''.join(c for c in word if c.isalnum()).lower()
        if clean_word and clean_word not in skip_words and len(clean_word) > 2:
            meaningful_words.append(clean_word.capitalize())
    
    if meaningful_words:
        if len(meaningful_words) > 3:
            meaningful_words = meaningful_words[-3:]
        return "".join(meaningful_words)
    
    words = [w.capitalize() for w in words if w.isalnum()][:3]
    return "".join(words) if words else "Default"


# Test cases
test_titles = [
    "Write a wrapper for below mention api in s_digitcare",
    "Create user authentication service",
    "Update the product inventory management system",
    "Add validation for payment gateway integration",
    "Implement real-time notification feature",
    "Fix bug in order processing module",
    "Develop REST API for customer data"
]

print("=" * 80)
print("CLASS NAME COMPARISON - Old vs New")
print("=" * 80)
print()

for title in test_titles:
    old_name = old_method(title)
    new_name = new_method(title)
    
    print(f"Title: {title}")
    print(f"  ❌ OLD: {old_name}Service.java")
    print(f"  ✅ NEW: {new_name}Service.java")
    print(f"  Reduction: {len(old_name)} → {len(new_name)} chars ({len(old_name) - len(new_name)} chars shorter)")
    print()

print("=" * 80)
print("EXAMPLE FILE NAMES GENERATED")
print("=" * 80)
print()

example_title = "Write a wrapper for below mention api in s_digitcare"
new_name = new_method(example_title)

files = [
    f"{new_name}Controller.java",
    f"{new_name}Service.java",
    f"{new_name}Repository.java",
    f"{new_name}DTO.java",
    f"{new_name}Entity.java"
]

print(f"For issue: '{example_title}'")
print(f"\nGenerated files:")
for file in files:
    print(f"  📄 {file}")

print("\n" + "=" * 80)
print("✅ Much more concise and readable!")
print("=" * 80)
