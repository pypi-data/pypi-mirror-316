from dataclasses import dataclass
from typing import List, Optional, Set, Tuple


@dataclass
class ParserSignature:
    english: Optional[str]
    verbs: List[str]
    object: List[Tuple[str, Optional[List[str]]]]
    preposition: Optional[str]
    outputs: Optional[List[List[Tuple[str, Optional[List[str]]]]]]
    target: Optional[List[Tuple[str, Optional[List[str]]]]]
    proper_nouns: Optional[Set[str]]
