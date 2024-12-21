import unicodedata

class PluralizerSingularizer:

    EXCEPTIONS = {
        'irmá': 'irmáns',
        'mán': 'máns',
        'pé': 'pés',
        'canción': 'cancións',
        'león': 'leóns',
        'nai': 'nais',
        'can': 'canes',
        'árbol': 'árbores',
        'luz': 'luces',
        'pez': 'peces',
        'árbol': 'árbores',
        'capital': 'capitais',
        'carne': 'carnes',
        'cidade': 'cidades',
        'home': 'homes',
        'presidente': 'presidentes',
    }

    REVERSE_EXCEPTIONS = {v: k for k, v in EXCEPTIONS.items()}

    @staticmethod
    def remove_accent(char: str) -> str:
        return unicodedata.normalize('NFD', char)[0]

    @staticmethod
    def pluralize(word: str) -> str:
        if word in PluralizerSingularizer.EXCEPTIONS:
            return PluralizerSingularizer.EXCEPTIONS[word]
        if word.endswith(('z')):
            return word[:-1] + 'ces'
        elif word.endswith(('r', 'd', 'l')):
            return word + 'es'
        elif word.endswith(('n')) and word != 'can':
            return word + 's'
        elif word.endswith(('n')) and word == 'can':
            return word[:-1] + 'anes'  # Handle "can" → "canes"
        elif word.endswith(('l')):
            return word[:-1] + 'res'  # Handle "árbol" → "árbores"
        elif word.endswith(('s', 'x', 'ch', 'sh')):
            return word  # No change for these endings
        else:
            return word + 's'
    
    @staticmethod
    def singularize(word: str) -> str:
        if word in PluralizerSingularizer.REVERSE_EXCEPTIONS:
            return PluralizerSingularizer.REVERSE_EXCEPTIONS[word]
        if word.endswith('ces') and len(word) > 3:
            return word[:-3] + 'z'
        if word.endswith('ns') and len(word) > 2:
            return word[:-1]  # Remove 's' from 'ns'
        if word.endswith('is') and len(word) > 2:
            return word[:-2] + 'l'
        if word.endswith('es') and len(word) > 2 and word[-3] not in 'aeiouáéíóú':
            return word[:-2]  # Remove 'es'
        if word.endswith('s') and len(word) > 1 and not word.endswith(('ns', 'is')):
            return word[:-1]  # Remove 's'
        return word


if __name__ == "__main__":
    # Pluralize test cases
    print(PluralizerSingularizer.pluralize("irmá"))  # 'irmáns'
    print(PluralizerSingularizer.pluralize("mán"))  # 'máns'
    print(PluralizerSingularizer.pluralize("pé"))  # 'pés'
    print(PluralizerSingularizer.pluralize("canción"))  # 'cancións'
    print(PluralizerSingularizer.pluralize("león"))  # 'leóns'
    print(PluralizerSingularizer.pluralize("can"))  # 'canes' (exception)
    print(PluralizerSingularizer.pluralize("árbol"))  # 'árbores' (exception)
    print(PluralizerSingularizer.pluralize("luz"))  # 'luces' (exception)
    print(PluralizerSingularizer.pluralize("pez"))  # 'peces' (exception)
    
    # Singularize test cases
    print(PluralizerSingularizer.singularize("irmáns"))  # 'irmá'
    print(PluralizerSingularizer.singularize("máns"))  # 'mán'
    print(PluralizerSingularizer.singularize("pés"))  # 'pé'
    print(PluralizerSingularizer.singularize("cancións"))  # 'canción'
    print(PluralizerSingularizer.singularize("leóns"))  # 'león'
    print(PluralizerSingularizer.singularize("canes"))  # 'can'
    print(PluralizerSingularizer.singularize("árbores"))  # 'árbol'
    print(PluralizerSingularizer.singularize("luces"))  # 'luz'
    print(PluralizerSingularizer.singularize("peces"))  # 'pez'
