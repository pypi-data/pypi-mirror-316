import unicodedata

class PluralizerSingularizer:
    
    EXCEPTIONS = {
        'stad': 'steden',
        'lid': 'leden',
        'kind': 'kinderen',
        'goed': 'goederen',
        'ei': 'eieren',
    }

    REVERSE_EXCEPTIONS = {v: k for k, v in EXCEPTIONS.items()}

    @staticmethod
    def remove_accent(char: str) -> str:
        return unicodedata.normalize('NFD', char)[0]

    @staticmethod
    def pluralize(word: str) -> str:
        if word in PluralizerSingularizer.EXCEPTIONS:
            return PluralizerSingularizer.EXCEPTIONS[word]
        if word.endswith(('heid')):
            return word[:-4] + 'heden'
        elif word.endswith(('f')):
            return word[:-1] + 'ven'
        elif word.endswith(('s', 'x', 'z')):
            return word + 'en'
        elif word.endswith(('a', 'i', 'o', 'u', 'y')):
            return word + "'s"
        elif word.endswith(('el', 'em', 'en', 'er', 'je')):
            return word
        else:
            return word + 'en'
    
    @staticmethod
    def singularize(word: str) -> str:
        if word in PluralizerSingularizer.REVERSE_EXCEPTIONS:
            return PluralizerSingularizer.REVERSE_EXCEPTIONS[word]
        if word.endswith('heden') and len(word) > 6:
            return word[:-5] + 'heid'
        if word.endswith('ven') and len(word) > 3:
            return word[:-3] + 'f'
        if word.endswith('en') and len(word) > 2:
            return word[:-2]
        if word.endswith("'s") and len(word) > 2:
            return word[:-2]
        return word


if __name__ == "__main__":
    print(PluralizerSingularizer.pluralize("stad"))  # 'steden'
    print(PluralizerSingularizer.pluralize("lid"))  # 'leden'
    print(PluralizerSingularizer.pluralize("kind"))  # 'kinderen'
    print(PluralizerSingularizer.pluralize("goed"))  # 'goederen'
    print(PluralizerSingularizer.pluralize("ei"))  # 'eieren'
    print(PluralizerSingularizer.singularize("steden"))  # 'stad'
    print(PluralizerSingularizer.singularize("leden"))  # 'lid'
    print(PluralizerSingularizer.singularize("kinderen"))  # 'kind'
    print(PluralizerSingularizer.singularize("goederen"))  # 'goed'
    print(PluralizerSingularizer.singularize("eieren"))  # 'ei'
