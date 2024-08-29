from typing import Optional
import Film

class Node:
    def __init__(self, data: Film):
        self.data = data
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.balance: float = 0
