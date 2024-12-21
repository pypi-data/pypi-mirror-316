import unicodedata

class PluralizerSingularizer:
    
    EXCEPTIONS = {
        'cheval': 'chevaux',
        'travail': 'travaux',
        'bijou': 'bijoux',
        'caillou': 'cailloux',
        'chou': 'choux',
        'genou': 'genoux',
        'hibou': 'hiboux',
        'joujou': 'joujoux',
        'pou': 'poux',
        'cão': 'cães',
        'pão': 'pães',
        'alemão': 'alemães',
        'capitão': 'capitães',
        'cristão': 'cristãos',
        'mão': 'mãos',
        'irmão': 'irmãos',
        'cidadão': 'cidadãos',
        'leão': 'leões',
        'limão': 'limões',
        'melão': 'melões',
        'canhão': 'canhões',
        'barracão': 'barracões',
    }

    REVERSE_EXCEPTIONS = {v: k for k, v in EXCEPTIONS.items()}

    @staticmethod
    def remove_accent(char: str) -> str:
        return unicodedata.normalize('NFD', char)[0]

    @staticmethod
    def pluralize(word: str) -> str:
        if word in PluralizerSingularizer.EXCEPTIONS:
            return PluralizerSingularizer.EXCEPTIONS[word]
        if word.endswith(('al')):
            return word[:-2] + 'aux'
        elif word.endswith(('eau', 'au', 'eu')):
            return word + 'x'
        elif word.endswith(('s', 'x', 'z')):
            return word
        else:
            return word + 's'
    
    @staticmethod
    def singularize(word: str) -> str:
        if word in PluralizerSingularizer.REVERSE_EXCEPTIONS:
            return PluralizerSingularizer.REVERSE_EXCEPTIONS[word]
        if word.endswith('aux') and len(word) > 3:
            return word[:-3] + 'al'
        if word.endswith(('eaux', 'aux', 'eux')) and len(word) > 3:
            return word[:-1]  # Remove 'x'
        elif word.endswith(('s', 'x', 'z')) and len(word) > 1:
            return word[:-1]  # Remove 's', 'x', or 'z'
        return word


if __name__ == "__main__":
    print(PluralizerSingularizer.pluralize("cheval"))  # 'chevaux'
    print(PluralizerSingularizer.pluralize("travail"))  # 'travaux'
    print(PluralizerSingularizer.pluralize("bijou"))  # 'bijoux'
    print(PluralizerSingularizer.singularize("chevaux"))  # 'cheval'
    print(PluralizerSingularizer.singularize("travaux"))  # 'travail'
    print(PluralizerSingularizer.singularize("bijoux"))  # 'bijou'
