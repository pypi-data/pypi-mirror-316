import inflect

class PluralizerSingularizer:
    """
    A backend for English pluralization and singularization using the `inflect` library.
    """
    PLURALIZE_EXCEPTIONS = {
        'thief': 'thieves',
    }

    SINGULARIZE_EXCEPTIONS = {}
    for singular, plural in PLURALIZE_EXCEPTIONS.items():
        SINGULARIZE_EXCEPTIONS.setdefault(plural, singular)

    _inflector = inflect.engine()

    @staticmethod
    def pluralize(word: str) -> str:
        if word in PluralizerSingularizer.PLURALIZE_EXCEPTIONS:
            return PluralizerSingularizer.PLURALIZE_EXCEPTIONS[word]
        return PluralizerSingularizer._inflector.plural(word)

    @staticmethod
    def singularize(word: str) -> str:
        if word in PluralizerSingularizer.SINGULARIZE_EXCEPTIONS:
            return PluralizerSingularizer.SINGULARIZE_EXCEPTIONS[word]
        singular_form = PluralizerSingularizer._inflector.singular_noun(word)
        return singular_form if singular_form else word

if __name__ == "__main__":
    print(PluralizerSingularizer.pluralize("dog"))
    print(PluralizerSingularizer.pluralize("person"))
    print(PluralizerSingularizer.singularize("dogs"))
    print(PluralizerSingularizer.singularize("people"))
