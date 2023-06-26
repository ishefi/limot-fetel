from grapheme.finder import GraphemeIterator
from typing import Iterator

class GraphemeString:
    @property
    def graphemes(self) -> Iterator[GraphemeIterator]: ...
