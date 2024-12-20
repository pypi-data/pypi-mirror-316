import unicodedata

class PluralizerSingularizer:
    """
    This module provides methods to pluralize and singularize Spanish words.

    Note: Corrections to the rules and exceptions are welcome. If you find any 
    incorrect behavior or have suggestions for improvement, please contribute.
    """

    EXCEPTIONS = {
        'país': 'países',
        'luz': 'luces',
        'pez': 'peces',
        'crisis': 'crisis',
        'análisis': 'análisis',
        'dios': 'dioses',
        'menú': 'menús',
        'rubí': 'rubíes',
        'marroquí': 'marroquíes',
        'colibrí': 'colibríes',
        'tabú': 'tabúes',
        'bisturí': 'bisturíes',
        'sacacorchos': 'sacacorchos',
        'paraguas': 'paraguas',
        'tijeras': 'tijeras',
        'gafas': 'gafas',
        'rey': 'reyes',
    }

    REVERSE_EXCEPTIONS = {v: k for k, v in EXCEPTIONS.items()}

    @staticmethod
    def remove_accent(char: str) -> str:
        return unicodedata.normalize('NFD', char)[0]

    @staticmethod
    def pluralize(word: str) -> str:
        if word in PluralizerSingularizer.EXCEPTIONS:
            return PluralizerSingularizer.EXCEPTIONS[word]
        vowels = "aeiouáéíóú"
        if word.endswith(('z')):
            return word[:-1] + 'ces'
        elif word.endswith(('on', 'en', 'an', 'in', 'un')) and word[-3] in 'aeiouáéíóú':
            return word[:-2] + PluralizerSingularizer.remove_accent(word[-2]) + 'nes'
        elif word.endswith('y'):
            return word[:-1] + 'ies'
        elif word.endswith('s'):
            return word
        elif word.endswith(tuple(vowels)):
            return word + 's'
        else:
            return word + 'es'
    
    @staticmethod
    def singularize(word: str) -> str:
        if word in PluralizerSingularizer.REVERSE_EXCEPTIONS:
            return PluralizerSingularizer.REVERSE_EXCEPTIONS[word]
        if word.endswith('nes') and len(word) > 4:
            if word[-4] in 'aeiouáéíóú':
                return word[:-3] + unicodedata.normalize('NFD', word[-4])[0] + 'n'
        if word.endswith('cies') and len(word) > 4:
            return word[:-3] + 'y'
        if word.endswith('ces') and len(word) > 3 and word[-4] != 'z':
            return word[:-3] + 'z'
        elif word.endswith('es') and len(word) > 2:
            if word[-3] not in 'aeiouáéíóú':
                return word[:-2]
            return word[:-1]
        elif word.endswith('s') and len(word) > 1 and word not in PluralizerSingularizer.REVERSE_EXCEPTIONS.keys():
            return word[:-1]
        return word

if __name__ == "__main__":
    print(PluralizerSingularizer.pluralize("flor"))
    print(PluralizerSingularizer.pluralize("luz"))
    print(PluralizerSingularizer.pluralize("país"))
    print(PluralizerSingularizer.pluralize("rey"))
    print(PluralizerSingularizer.pluralize("crisis"))
    print(PluralizerSingularizer.pluralize("pantalón"))
    print(PluralizerSingularizer.singularize("flores"))
    print(PluralizerSingularizer.singularize("luces"))
    print(PluralizerSingularizer.singularize("países"))
    print(PluralizerSingularizer.singularize("reyes"))
    print(PluralizerSingularizer.singularize("crisis"))
    print(PluralizerSingularizer.singularize("pantalones"))
