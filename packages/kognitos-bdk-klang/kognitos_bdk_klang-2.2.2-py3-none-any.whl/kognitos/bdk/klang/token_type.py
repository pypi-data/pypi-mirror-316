from enum import Enum


class TokenType(Enum):
    POSSESSIVE_SUFFIX = 0
    ASTERISK = 1
    OPEN_PAREN = 2
    CLOSE_PAREN = 3
    PIPE = 4
    COMMA = 5
    DETERMINER = 6
    SPECIAL_DETERMINER = 7
    PREPOSITION = 8
    WORD = 9
    PUNCT = 10
    CONJUNCTION_OR = 11
    CONJUNCTION_AND = 12
    CONJUNCTION_IF = 13
    EOF = 14

    def __str__(self):
        # Customize the string representation here
        if self == TokenType.POSSESSIVE_SUFFIX:
            return "'s'"

        if self == TokenType.ASTERISK:
            return "*"

        if self == TokenType.OPEN_PAREN:
            return "("

        if self == TokenType.CLOSE_PAREN:
            return ")"

        if self == TokenType.PIPE:
            return "|"

        if self == TokenType.COMMA:
            return ","

        if self == TokenType.DETERMINER:
            return "<determiner>"

        if self == TokenType.SPECIAL_DETERMINER:
            return "<special_determiner>"

        if self == TokenType.PREPOSITION:
            return "<preposition>"

        if self == TokenType.WORD:
            return "<word>"

        if self == TokenType.PUNCT:
            return "<punctuation>"

        if self == TokenType.CONJUNCTION_AND:
            return "and"

        if self == TokenType.CONJUNCTION_OR:
            return "or"

        if self == TokenType.CONJUNCTION_IF:
            return "if"

        if self == TokenType.EOF:
            return "<eof>"

        return "<unknown>"
