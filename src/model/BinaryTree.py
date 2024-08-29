from typing import Optional, Tuple
from Node import Node

class BinaryTree:
    def __init__(self, root: Optional["Node"] = None) -> None:
        self.root = root
    
    def preorder(self) -> None:
        self.__preorder_r(self.root)
        print()

    def __preorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            print(node.data.title, end = ' ')
            self.__preorder_r(node.left)
            self.__preorder_r(node.right)
    
    def inorder(self) -> None:
        self.__inorder_r(self.root)
        print()

    def __inorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            self.__inorder_r(node.left)
            print(node.data.title, end = ' ')
            self.__inorder_r(node.right)
            
    def postorder(self) -> None:
        self.__postorder_r(self.root)
        print()

    def __postorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            self.__postorder_r(node.left)
            self.__postorder_r(node.right)
            print(node.data.title, end = ' ')
    
    def height(self) -> int:
        return self.__height_r(self.root)
    
    def __height_r(self, node: Optional["Node"]) -> int:
        if node is None:
            return 0
        return 1 + max(self.__height_r(node.left), self.__height_r(node.right))

class BST(BinaryTree):
    def __init__(self, root: Optional["Node"] = None) -> None:
        super().__init__(root)
        
    def search(self, data: str) -> Tuple[Optional["Node"], Optional["Node"]]:
        p, pad = self.root, None
        while p is not None:
            if data == p.data.title:
                return p, pad
            else:
                pad = p
                if data < p.data:
                    p = p.left
                else:
                    p = p.right
        return p, pad