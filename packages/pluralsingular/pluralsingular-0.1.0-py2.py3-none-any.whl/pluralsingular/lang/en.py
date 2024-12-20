import inflect

class PluralizerSingularizer:
    """
    A backend for English pluralization and singularization using the `inflect` library.
    """

    _inflector = inflect.engine()

    @staticmethod
    def pluralize(word: str) -> str:
        return PluralizerSingularizer._inflector.plural(word)

    @staticmethod
    def singularize(word: str) -> str:
        singular_form = PluralizerSingularizer._inflector.singular_noun(word)
        return singular_form if singular_form else word

if __name__ == "__main__":
    print(PluralizerSingularizer.pluralize("dog"))
    print(PluralizerSingularizer.pluralize("person"))
    print(PluralizerSingularizer.singularize("dogs"))
    print(PluralizerSingularizer.singularize("people"))
