import unicodedata

class PluralizerSingularizer:
    
    EXCEPTIONS = {
        'Mann': 'Männer',
        'Kind': 'Kinder',
        'Buch': 'Bücher',
        'Licht': 'Lichter',
        'Haus': 'Häuser',
        'Kuh': 'Kühe',
    }

    REVERSE_EXCEPTIONS = {v: k for k, v in EXCEPTIONS.items()}

    @staticmethod
    def remove_accent(char: str) -> str:
        return unicodedata.normalize('NFD', char)[0]

    @staticmethod
    def pluralize(word: str) -> str:
        if word in PluralizerSingularizer.EXCEPTIONS:
            return PluralizerSingularizer.EXCEPTIONS[word]
        if word.endswith(('er', 'el', 'en')):
            return word  # No change for these endings
        elif word.endswith(('a', 'i', 'o', 'u')):
            return word + 's'
        elif word.endswith(('e')):
            return word + 'n'
        else:
            return word + 'e'
    
    @staticmethod
    def singularize(word: str) -> str:
        if word in PluralizerSingularizer.REVERSE_EXCEPTIONS:
            return PluralizerSingularizer.REVERSE_EXCEPTIONS[word]
        if word.endswith(('er', 'el', 'en')) and len(word) > 2:
            return word  # No change for these endings
        if word.endswith('n') and len(word) > 2:
            return word[:-1]  # Remove 'n'
        if word.endswith('e') and len(word) > 1:
            return word[:-1]  # Remove 'e'
        if word.endswith('s') and len(word) > 1:
            return word[:-1]  # Remove 's'
        return word


if __name__ == "__main__":
    print(PluralizerSingularizer.pluralize("Mann"))  # 'Männer'
    print(PluralizerSingularizer.pluralize("Kind"))  # 'Kinder'
    print(PluralizerSingularizer.pluralize("Buch"))  # 'Bücher'
    print(PluralizerSingularizer.singularize("Männer"))  # 'Mann'
    print(PluralizerSingularizer.singularize("Kinder"))  # 'Kind'
    print(PluralizerSingularizer.singularize("Bücher"))  # 'Buch'
