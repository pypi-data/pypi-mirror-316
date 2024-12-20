import unicodedata

class PluralizerSingularizer:
    
    EXCEPTIONS = {
        'люди': 'люди',  # люди (people) - invariable
        'дити': 'дити',  # діти (children) - invariable
        'стіл': 'столи',  # стіл -> столи (table -> tables)
        'брат': 'брати',  # брат -> брати (brother -> brothers)
        'друг': 'друзі',  # друг -> друзі (friend -> friends)
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
            return word[:-1] + 'и'
        elif word.endswith(('о', 'е')):
            return word[:-1] + 'а'
        elif word.endswith(('ь')):
            return word[:-1] + 'і'
        elif word.endswith(('й')):
            return word[:-1] + 'ї'
        elif word.endswith(('ц')):
            return word + 'і'
        elif word.endswith(('ж', 'ч', 'ш', 'щ')):
            return word + 'і'
        else:
            return word + 'и'
    
    @staticmethod
    def singularize(word: str) -> str:
        if word in PluralizerSingularizer.REVERSE_EXCEPTIONS:
            return PluralizerSingularizer.REVERSE_EXCEPTIONS[word]
        if word.endswith(('и')) and len(word) > 1:
            return word[:-1] + 'а'
        if word.endswith(('і')) and len(word) > 1:
            if word[-2] in 'жчшщц':
                return word[:-1]  # Remove 'і'
            return word[:-1] + 'ь'
        if word.endswith(('ї')) and len(word) > 1:
            return word[:-1] + 'й'
        if word.endswith(('а')) and len(word) > 1:
            return word[:-1] + 'о'
        return word


if __name__ == "__main__":
    print(PluralizerSingularizer.pluralize('стіл'))  # 'столи' (tables)
    print(PluralizerSingularizer.pluralize('брат'))  # 'брати' (brothers)
    print(PluralizerSingularizer.pluralize('друг'))  # 'друзі' (friends)
    print(PluralizerSingularizer.singularize('столи'))  # 'стіл' (table)
    print(PluralizerSingularizer.singularize('брати'))  # 'брат' (brother)
    print(PluralizerSingularizer.singularize('друзі'))  # 'друг' (friend)
