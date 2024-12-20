import os
import pytest
from pluralsingular import pluralize, singularize

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.txt')

def load_test_data():
    """Load test data from a unified file and return a list of (lang, singular, plural) triplets."""
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return [tuple(line.strip().split(',')) for line in file if line.strip()]

@pytest.mark.parametrize("lang,singular,plural", load_test_data())
def test_pluralize_singularize(lang, singular, plural):
    """Test pluralize and singularize for all supported languages."""
    assert pluralize(singular, lang=lang) == plural, f"Failed to pluralize '{singular}' in '{lang}'"
    assert singularize(plural, lang=lang) == singular, f"Failed to singularize '{plural}' in '{lang}'"

if __name__ == "__main__":
    pytest.main(["-v"])
