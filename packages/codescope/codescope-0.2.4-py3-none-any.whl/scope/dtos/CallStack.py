from typing import List
from scope.dtos.Definition import Definition


class CallStack(object):
    def __init__(self, stack: List[Definition]):
        self.stack = stack

    def __str__(self):
        stack_str = []
        for defn in self.stack:
            stack_str.append(f">  {defn.pprint()}")
        return "\n".join(stack_str)

    def __len__(self) -> int:
        return len(self.stack)

    def slice(self, start: int, end: int) -> "CallStack":
        if start < 0 or end > len(self.stack):
            raise ValueError(f"Invalid slice: start={start}, end={end}")
        return CallStack(self.stack[start:end])

    def root(self) -> Definition:
        return self.stack[0]

    def tail(self) -> Definition:
        return self.stack[-1]
