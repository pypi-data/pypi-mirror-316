import re
from collections import deque

from kognitos.bdk.klang.token_type import TokenType

DETERMINERS = [
    "the",
    "a",
    "an",
    "this",
    "that",
    "these",
    "those",
    "my",
    "your",
    "his",
    "her",
    "its",
    "our",
    "their",
    "a few",
    "a little",
    "much",
    "many",
    "a lot of",
    "most",
    "some",
    "any",
    "enough",
    "one",
    "ten",
    "thirty",
    "both",
    "half",
    "either",
    "neither",
    "each",
    "every",
    "other",
    "such",
    "what",
    "rather",
    "quite",
]
SPECIAL_DETERMINERS = ["another", "all"]
PREPOSITIONS = [
    "aboard",
    "about",
    "above",
    "across",
    "after",
    "against",
    "along",
    "amid",
    "among",
    "anti",
    "around",
    "as",
    "at",
    "before",
    "behind",
    "below",
    "beneath",
    "beside",
    "besides",
    "between",
    "beyond",
    "but",
    "by",
    "despite",
    "down",
    "during",
    "except",
    "for",
    "from",
    "in",
    "inside",
    "into",
    "like",
    "minus",
    "near",
    "of",
    "off",
    "on",
    "onto",
    "opposite",
    "outside",
    "over",
    "past",
    "per",
    "plus",
    "since",
    "than",
    "through",
    "to",
    "toward",
    "towards",
    "under",
    "underneath",
    "unlike",
    "until",
    "up",
    "upon",
    "versus",
    "via",
    "with",
    "within",
    "without",
]
MARK_AS_WORD_SYMBOL = "~"

CONJUNCTION_AND = ["and"]
CONJUNCTION_OR = ["or"]
CONJUNCTION_IF = ["if"]
DETERMINERS_PATTERN = r"\b(" + "|".join(map(re.escape, DETERMINERS)) + r")\b"
SPECIAL_DETERMINERS_PATTERN = r"\b(" + "|".join(map(re.escape, SPECIAL_DETERMINERS)) + r")\b"
PREPOSITIONS_PATTERN = f"{MARK_AS_WORD_SYMBOL}?" + r"\b(" + "|".join(map(re.escape, PREPOSITIONS)) + r")\b"
CONJUNCTIONS_AND_PATTERN = r"\b(" + "|".join(map(re.escape, CONJUNCTION_AND)) + r")\b"
CONJUNCTIONS_OR_PATTERN = r"\b(" + "|".join(map(re.escape, CONJUNCTION_OR)) + r")\b"
CONJUNCTIONS_IF_PATTERN = r"\b(" + "|".join(map(re.escape, CONJUNCTION_IF)) + r")\b"


class KlangLexer:
    def __init__(self, text: str):
        self.text = text
        self.token_pattern = re.compile(
            rf"""
            ('s\b)           |  # Match possessive suffix
            (\*)             |  # Match asterisks
            (\()             |  # Match open parenthesis
            (\))             |  # Match close parenthesis
            (\|)             |  # Match pipe
            (,)              |  # Match comma
            {DETERMINERS_PATTERN} | # Match determiners
            {SPECIAL_DETERMINERS_PATTERN} | # Match special determiners
            {PREPOSITIONS_PATTERN} | # Match prepositions
            {CONJUNCTIONS_AND_PATTERN} | # Match and conjunctions
            {CONJUNCTIONS_OR_PATTERN} | # Match or conjunctions
            {CONJUNCTIONS_IF_PATTERN} |  # Match if conjunctions
            \b\w+\b          |  # Match whole words
            [^\w\s'()*]+       # Match other punctuation (excluding the special cases above)
            """,
            re.VERBOSE,
        )

        self.matches = self.token_pattern.finditer(self.text)
        self.next_match = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_match is None:  # Fetch the next match
            self.next_match = next(self.matches, None)

        if self.next_match is None:
            raise StopIteration

        current_match = self.next_match
        token = current_match.group(0)

        match_groups = self.next_match.groups()
        self.next_match = None  # Reset for the next iteration

        # Determine token type based on the regex group matched
        if match_groups[0]:
            return TokenType.POSSESSIVE_SUFFIX, token, current_match.span()

        if match_groups[1]:
            return TokenType.ASTERISK, token, current_match.span()

        if match_groups[2]:
            return TokenType.OPEN_PAREN, token, current_match.span()

        if match_groups[3]:
            return TokenType.CLOSE_PAREN, token, current_match.span()

        if match_groups[4]:
            return TokenType.PIPE, token, current_match.span()

        if match_groups[5]:
            return TokenType.COMMA, token, current_match.span()

        if match_groups[6]:
            return TokenType.DETERMINER, token, current_match.span()

        if match_groups[7]:
            return TokenType.SPECIAL_DETERMINER, token, current_match.span()

        if match_groups[8]:
            if token.startswith(MARK_AS_WORD_SYMBOL):
                return TokenType.WORD, token[1:], current_match.span()

            return TokenType.PREPOSITION, token, current_match.span()

        if match_groups[9]:
            return TokenType.CONJUNCTION_AND, token, current_match.span()

        if match_groups[10]:
            return TokenType.CONJUNCTION_OR, token, current_match.span()

        if match_groups[11]:
            return TokenType.CONJUNCTION_IF, token, current_match.span()

        if token.isalnum():
            return TokenType.WORD, token, current_match.span()

        return TokenType.PUNCT, token, current_match.span()


class LookaheadLexer:
    def __init__(self, lexer: KlangLexer):
        self.lexer = lexer
        self.buffer = deque()

    def __iter__(self):
        return self

    def __next__(self):
        if self.buffer:
            return self.buffer.popleft()

        return next(self.lexer)

    def peek(self, k=1):
        while len(self.buffer) < k:
            try:
                self.buffer.append(next(self.lexer))
            except StopIteration:
                eof_position = len(self.lexer.text)
                self.buffer.append((TokenType.EOF, None, (eof_position, eof_position)))
        return self.buffer[k - 1][0]
