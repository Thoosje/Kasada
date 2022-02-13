from dataclasses import dataclass
from typing import Any

@dataclass(init=False)
class Empty():
    Empty = True

class Expandable_List(list):
    def __init__(self, _size: int = 0) -> None:
        if _size > 0:
            for i in range(_size):
                self.append(Empty())       
    
    def __setitem__(self, index: int, value: Any) -> Any:
        _wantedIndex = index
        _originalSize = len(self) - 1

        while _wantedIndex > _originalSize:
            self.append(Empty())
            _originalSize += 1

        return super(Expandable_List, self).__setitem__(index, value)