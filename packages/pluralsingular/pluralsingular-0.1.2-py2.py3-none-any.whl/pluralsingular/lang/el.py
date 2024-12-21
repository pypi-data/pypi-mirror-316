import unicodedata

class PluralizerSingularizer:
    
    EXCEPTIONS = {
        'ανθρωπος': 'ανθρωποι',  # άνθρωπος -> άνθρωποι (man -> men)
        'παιδι': 'παιδια',  # παιδί -> παιδιά (child -> children)
        'μητερα': 'μητερες',  # μητέρα -> μητέρες (mother -> mothers)
        'γυναίκα': 'γυναίκες',  # γυναίκα -> γυναίκες (woman -> women)
        'παιδί': 'παιδιά',
    }

    REVERSE_EXCEPTIONS = {v: k for k, v in EXCEPTIONS.items()}

    @staticmethod
    def remove_accent(char: str) -> str:
        return unicodedata.normalize('NFD', char)[0]

    @staticmethod
    def pluralize(word: str) -> str:
        if word in PluralizerSingularizer.EXCEPTIONS:
            return PluralizerSingularizer.EXCEPTIONS[word]
        if word.endswith(('ος')):
            return word[:-2] + 'οι'
        elif word.endswith(('η', 'α')):
            return word[:-1] + 'ες'
        elif word.endswith(('ον')):
            return word[:-2] + 'α'
        else:
            return word + 'ες'
    
    @staticmethod
    def singularize(word: str) -> str:
        if word in PluralizerSingularizer.REVERSE_EXCEPTIONS:
            return PluralizerSingularizer.REVERSE_EXCEPTIONS[word]
        if word.endswith(('οι')) and len(word) > 2:
            return word[:-2] + 'ος'
        if word.endswith(('ες')) and len(word) > 2:
            if word[:-2].endswith(('η', 'α')):
                return word[:-2] + 'η'
            return word[:-2] + 'α'
        if word.endswith(('α')) and len(word) > 1:
            return word[:-1] + 'ον'
        return word


if __name__ == "__main__":
    print(PluralizerSingularizer.pluralize('ανθρωπος'))  # 'άνθρωποι' (men)
    print(PluralizerSingularizer.pluralize('παιδι'))  # 'παιδιά' (children)
    print(PluralizerSingularizer.pluralize('μητερα'))  # 'μητέρες' (mothers)
    print(PluralizerSingularizer.pluralize('γυναίκα'))  # 'γυναίκες' (women)
    print(PluralizerSingularizer.singularize('ανθρωποι'))  # 'άνθρωπος' (man)
    print(PluralizerSingularizer.singularize('παιδια'))  # 'παιδί' (child)
    print(PluralizerSingularizer.singularize('μητερες'))  # 'μητέρα' (mother)
    print(PluralizerSingularizer.singularize('γυναίκες'))  # 'γυναίκα' (woman)
