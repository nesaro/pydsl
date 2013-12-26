class Idea(object):
    pass


class UnicodeCharacter(Idea):
    def __init__(self, character):
        if not isinstance(character, str):
            raise TypeError
        if len(character) != 1:
            raise ValueError
        self.character = character

    def __str__(self):
        return self.character
