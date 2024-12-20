from typing import List, Optional, Set, Tuple

from .lexer import SPECIAL_DETERMINERS, KlangLexer, LookaheadLexer
from .parser_signature import ParserSignature
from .token_type import TokenType

NounPhrase = Tuple[str, Optional[List[str]]]
NounPhrases = List[NounPhrase]


class KlangParser:
    def __init__(self, english: str):
        self.english = english
        self.lexer = LookaheadLexer(KlangLexer(english))
        self.current_token: Tuple[TokenType, str, Tuple[int, int]] = (TokenType.EOF, "<EOF>", (0, 0))
        self._next_token()

    def _highlight_current_token_in_text(self):
        """Highlights the position of the current token in the `self.text` value"""
        span = self.current_token[2]
        prefix, current_token, postfix = self.english[0 : span[0]], self.english[span[0] : span[1]], self.english[span[1] :]
        return prefix + f"~~{current_token}~~" + postfix

    def _next_token(self):
        """Advance to the next token from the generator"""
        try:
            self.current_token = next(self.lexer)
        except StopIteration:
            eof_position = len(self.lexer.lexer.text)
            self.current_token = (TokenType.EOF, "<EOF>", (eof_position, eof_position))

    def _looakahead_token(self):
        return self.lexer.peek(1)

    def _expect(self, token_type: TokenType, value: Optional[str] = None):
        """Ensure the current token matches token_type and advance to the next token"""
        if self.current_token[0] != token_type:
            raise SyntaxError(f"expected token type `{token_type}`, but found `{self.current_token[0]}` while parsing '{self._highlight_current_token_in_text()}'")

        token_value = self.current_token[1]
        if value and self.current_token[1] != value:
            raise SyntaxError(f"expected token value '{value}', but found '{self.current_token[1]}' while parsing '{self._highlight_current_token_in_text()}'")

        self._next_token()

        return token_value

    def _expect_one_of(self, token_types_values: List[Tuple[TokenType, Optional[str]]]):
        """Ensure the current token matches one of the token_types and advance to the next token"""
        for token_type, value in token_types_values:
            if self.current_token[0] == token_type:
                if value and self.current_token[1] != value:
                    continue

                token_value = self.current_token[1]
                self._next_token()

                return token_value

        expected = ", ".join([f"{token_type}({value})" if value else f"{token_type}" for token_type, value in token_types_values])
        raise SyntaxError(f"expected one of `{expected}`, but found `{self.current_token[0]}` while parsing '{self._highlight_current_token_in_text()}'")

    def _optional(self, token_type, value: Optional[str] = None) -> Optional[str]:
        """Optionally match and consume a token of token_type, returning True if matched"""
        if self.current_token[0] == token_type:
            if value and self.current_token[1] != value:
                return None

            token_value = self.current_token[1]
            self._next_token()

            return token_value
        return None

    def _optional_one_of(self, token_types: List[TokenType]) -> Optional[str]:
        """Optionally match and consume a token of token_type, returning True if matched"""
        for token_type in token_types:
            if self.current_token[0] == token_type:
                token_value = self.current_token[1]
                self._next_token()

                return token_value
        return None

    def _repeat(self, token_type):
        """Repeat matching and accepting a token while it matches token_type"""
        values = []
        while self.current_token[0] == token_type:
            values.append(self.current_token[1])
            self._next_token()
        return values

    def _parse_verbs(self) -> List[str]:
        verbs = [self._expect(TokenType.WORD)]

        if self._optional(TokenType.CONJUNCTION_OR):
            verbs.extend(self._parse_verbs())

        return verbs

    def _parse_words(self) -> Tuple[List[str], bool]:
        """Returns a tuple of words and a boolean indicating if the words are a proper noun"""
        is_proper_noun = self._optional(TokenType.ASTERISK)

        if is_proper_noun:
            words = self._repeat(TokenType.WORD)
        else:
            words = [self._expect(TokenType.WORD)]

        if is_proper_noun:
            self._expect(TokenType.ASTERISK)

            words = [" ".join(words)]

        return words, bool(is_proper_noun)

    def _parse_optional_special_determiner_noun_phrase(self) -> Tuple[NounPhrase, str]:
        """Parses a noun phrase with an optional special determiner. The expected english to be parsed is `Optional[SPECIAL_DETERMINER] NOUN_PHRASE`."""
        special_determiner = self._optional(TokenType.SPECIAL_DETERMINER)
        noun_phrase, proper_noun = self._parse_noun_phrase()
        return (noun_phrase if not special_determiner else self._add_determiner_to_noun_phrase(noun_phrase, special_determiner), proper_noun)

    def _parse_noun_phrase(self) -> Tuple[NounPhrase, str]:
        words = []
        proper_noun = ""

        while self.current_token[0] == TokenType.ASTERISK or self.current_token[0] == TokenType.WORD:
            _words, is_proper_noun = self._parse_words()
            words.append(_words)

            if is_proper_noun:
                proper_noun = " ".join(_words)

        if len(words) < 1:
            raise SyntaxError(f"expected `{TokenType.ASTERISK}` or `{TokenType.WORD}`. Got `{self.current_token[0]}` instead in '{self._highlight_current_token_in_text()}'")

        np_head = " ".join(words[-1])
        np_modifiers = [" ".join(w) for w in words[0:-1]]

        return ((np_head, np_modifiers), proper_noun)

    def _parse_determiner_output_noun_phrases(self) -> Tuple[NounPhrases, Optional[NounPhrases], Set[str]]:
        closed = False
        output = None

        determiner = self._optional_one_of([TokenType.DETERMINER, TokenType.SPECIAL_DETERMINER])

        is_output = bool(self._optional(TokenType.OPEN_PAREN))

        noun_phrase, proper_noun = self._parse_noun_phrase()
        noun_phrases = [noun_phrase]
        proper_nouns = [proper_noun] if proper_noun else []

        if is_output:
            closed = bool(self._optional(TokenType.CLOSE_PAREN))
            if closed:
                output = noun_phrases.copy()

        if self._optional(TokenType.POSSESSIVE_SUFFIX):
            _noun_phrases, _proper_nouns = self._parse_noun_phrases()
            noun_phrases.extend(_noun_phrases)
            proper_nouns.extend(_proper_nouns)

            if is_output and not closed:
                closed = bool(self._optional(TokenType.CLOSE_PAREN))
                if closed:
                    output = noun_phrases.copy()

        if determiner and determiner in SPECIAL_DETERMINERS and len(noun_phrases) == 1:
            noun_phrases = [self._add_determiner_to_noun_phrase(noun_phrases[0], determiner)]

        if is_output and not closed:
            self._expect(TokenType.CLOSE_PAREN)
            output = noun_phrases.copy()

        return noun_phrases, output if is_output else None, set(proper_nouns)

    def _parse_determiner_noun_phrase(self) -> Tuple[NounPhrase, str]:
        self._expect_one_of([(TokenType.DETERMINER, None), (TokenType.SPECIAL_DETERMINER, None)])

        return self._parse_noun_phrase()

    def _parse_output_determiner_noun_phrases(self) -> Tuple[NounPhrases, Optional[NounPhrases], Set[str]]:
        is_output = bool(self._optional(TokenType.OPEN_PAREN))

        noun_phrases, output, proper_nouns = self._parse_determiner_output_noun_phrases()

        if is_output:
            self._expect(TokenType.CLOSE_PAREN)

        return noun_phrases, noun_phrases if is_output else output, proper_nouns

    def _add_determiner_to_noun_phrase(self, noun_phrase: NounPhrase, determiner: str) -> NounPhrase:
        if noun_phrase[1]:
            modifiers = [determiner] + noun_phrase[1]
        else:
            modifiers = [determiner]
        return (noun_phrase[0], modifiers)

    def _parse_noun_phrases(self) -> Tuple[NounPhrases, Set[str]]:
        _noun_phrase, proper_noun = self._parse_optional_special_determiner_noun_phrase()
        noun_phrases = [_noun_phrase]
        proper_nouns = [proper_noun]

        if self._optional(TokenType.POSSESSIVE_SUFFIX):
            _noun_phrases, _proper_nouns = self._parse_noun_phrases()
            noun_phrases.extend(_noun_phrases)
            proper_nouns.extend(_proper_nouns)

        return noun_phrases, set(filter(None, proper_nouns))

    def _parse_determiner_noun_phrases(self) -> Tuple[NounPhrases, Set[str]]:
        determiner = self._expect_one_of([(TokenType.DETERMINER, None), (TokenType.SPECIAL_DETERMINER, None)])

        noun_phrases, proper_nouns = self._parse_noun_phrases()

        if determiner and determiner in SPECIAL_DETERMINERS and len(noun_phrases) == 1:
            noun_phrases = [self._add_determiner_to_noun_phrase(noun_phrases[0], determiner)]

        return noun_phrases, proper_nouns

    def _parse_outputs(self) -> Tuple[List[NounPhrases], Set[str]]:
        self._expect(TokenType.WORD, "get")

        _output, _, _proper_nouns = self._parse_output_determiner_noun_phrases()

        outputs = [_output]
        proper_nouns = _proper_nouns

        while self.current_token[0] == TokenType.COMMA or self.current_token[0] == TokenType.CONJUNCTION_AND:
            self._next_token()
            _output, _, _proper_nouns = self._parse_output_determiner_noun_phrases()
            outputs.append(_output)
            proper_nouns.update(_proper_nouns)

        return outputs, proper_nouns

    def _parse_signature(self) -> ParserSignature:
        target_output = None
        target = None
        proper_nouns = set()

        self._expect(TokenType.PREPOSITION, "to")

        verbs = self._parse_verbs()

        obj, object_output, _proper_nouns = self._parse_output_determiner_noun_phrases()

        proper_nouns.update(_proper_nouns)

        preposition = self._optional(TokenType.PREPOSITION)

        if preposition:
            target, target_output, _proper_nouns = self._parse_output_determiner_noun_phrases()
            proper_nouns.update(_proper_nouns)

        conj = self._optional(TokenType.CONJUNCTION_AND)

        if conj:
            outputs, _proper_nouns = self._parse_outputs()
            proper_nouns.update(_proper_nouns)
        else:
            outputs = [object_output] if object_output else [target_output] if target_output and target else None

        self._expect(TokenType.EOF)

        return ParserSignature(
            english=self.english,
            verbs=verbs,
            object=obj,
            preposition=preposition,
            target=target,
            outputs=outputs,
            proper_nouns=proper_nouns if proper_nouns else None,
        )

    @classmethod
    def parse_noun_phrases(cls, text: str) -> Tuple[NounPhrases, Set[str]]:
        parser = KlangParser(text)
        noun_phrases, proper_nouns = parser._parse_noun_phrases()
        return noun_phrases, proper_nouns

    @classmethod
    def parse_determiner_noun_phrases(cls, text: str) -> Tuple[NounPhrases, Set[str]]:
        parser = KlangParser(text)
        noun_phrases, proper_nouns = parser._parse_determiner_noun_phrases()
        return noun_phrases, proper_nouns

    @classmethod
    def parse_signature(cls, text: str) -> ParserSignature:
        parser = KlangParser(text)
        procedure_signature = parser._parse_signature()
        return procedure_signature
