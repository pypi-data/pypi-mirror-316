import unicodedata

class PluralizerSingularizer:
    
    EXCEPTIONS = {
        'человек': 'люди',  # человек -> люди (man -> people)
        'ребёнок': 'дети',  # ребёнок -> дети (child -> children)
        'брат': 'братья',  # брат -> братья (brother -> brothers)
        'стул': 'стулья',  # стул -> стулья (chair -> chairs)
    }

    REVERSE_EXCEPTIONS = {v: k for k, v in EXCEPTIONS.items()}

    @staticmethod
    def remove_accent(char: str) -> str:
        return unicodedata.normalize('NFD', char)[0]

    @staticmethod
    def pluralize(word: str) -> str:
        if word in PluralizerSingularizer.EXCEPTIONS:
            return PluralizerSingularizer.EXCEPTIONS[word]
        if word.endswith(('а', 'я')):
            return word[:-1] + 'ы'
        elif word.endswith(('ь')):
            return word[:-1] + 'и'
        elif word.endswith(('о', 'е')):
            return word[:-1] + 'а'
        elif word.endswith(('й')):
            return word[:-1] + 'и'
        elif word.endswith(('ж', 'ч', 'ш', 'щ')):
            return word + 'и'
        elif word.endswith(('ц')):
            return word + 'ы'
        else:
            return word + 'ы'
    
    @staticmethod
    def singularize(word: str) -> str:
        if word in PluralizerSingularizer.REVERSE_EXCEPTIONS:
            return PluralizerSingularizer.REVERSE_EXCEPTIONS[word]
        if word.endswith(('ы')) and len(word) > 1:
            return word[:-1] + 'а'
        if word.endswith(('и')) and len(word) > 1:
            if word[-2] in 'жчшщ':
                return word[:-1]  # Remove 'и'
            return word[:-1] + 'ь'
        if word.endswith(('а')) and len(word) > 1:
            return word[:-1] + 'о'
        if word.endswith(('я')) and len(word) > 1:
            return word[:-1] + 'й'
        return word


if __name__ == "__main__":
    print(PluralizerSingularizer.pluralize('человек'))  # 'люди' (people)
    print(PluralizerSingularizer.pluralize('ребёнок'))  # 'дети' (children)
    print(PluralizerSingularizer.pluralize('брат'))  # 'братья' (brothers)
    print(PluralizerSingularizer.pluralize('стул'))  # 'стулья' (chairs)
    print(PluralizerSingularizer.singularize('люди'))  # 'человек' (person)
    print(PluralizerSingularizer.singularize('дети'))  # 'ребёнок' (child)
    print(PluralizerSingularizer.singularize('братья'))  # 'брат' (brother)
    print(PluralizerSingularizer.singularize('стулья'))  # 'стул' (chair)
