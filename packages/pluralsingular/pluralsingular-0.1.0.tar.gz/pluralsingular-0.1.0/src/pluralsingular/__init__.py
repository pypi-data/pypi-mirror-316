"""
This module provides functionality to pluralize and singularize words
in multiple languages using dynamically loaded backends.

Main functions:
- `pluralize(word: str, lang: str = 'en')`: Pluralizes a given word.
- `singularize(word: str, lang: str = 'en')`: Singularizes a given word.

By default, the module supports English (`en`) and can be extended
to other languages by adding appropriate backend modules in the
`pluralsingular.lang` namespace.

Example usage:
    >>> pluralize("dog")
    'dogs'
    >>> singularize("dogs")
    'dog'
    >>> pluralize("futbol", lang="es")
    'futboles'
    >>> singularize("futboles", lang="es")
    'futbol'
"""

__version__ = '0.1.0'

import importlib

# Cache to store loaded backends to avoid repeated imports
_BACKEND_CACHE = {}

def _get_backend(lang: str):
    """Load the language-specific backend and cache it."""
    if lang not in _BACKEND_CACHE:
        try:
            _BACKEND_CACHE[lang] = importlib.import_module(f'pluralsingular.lang.{lang}')
        except ModuleNotFoundError:
            raise ValueError(f"Language '{lang}' not supported.")
    return _BACKEND_CACHE[lang]

def pluralize(word: str, lang: str = 'en') -> str:
    """
    Pluralize a word based on the given language.

    Args:
        word (str): The word to be pluralized.
        lang (str): The language to be used for pluralization (default is 'en').

    Returns:
        str: The pluralized form of the word.

    Usage:
        >>> pluralize("dog")
        'dogs'
        >>> pluralize("futbol", lang="es")
        'futboles'
    """
    backend = _get_backend(lang)
    return backend.PluralizerSingularizer.pluralize(word)

def singularize(word: str, lang: str = 'en') -> str:
    """
    Singularize a word based on the given language.

    Args:
        word (str): The word to be singularized.
        lang (str): The language to be used for singularization (default is 'en').

    Returns:
        str: The singularized form of the word.

    Usage:
        >>> singularize("dogs")
        'dog'
        >>> singularize("futboles", lang="es")
        'futbol'
    """
    backend = _get_backend(lang)
    return backend.PluralizerSingularizer.singularize(word)
