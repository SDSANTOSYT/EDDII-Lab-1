from typing import Optional, Tuple
from .node import Node
from .film import Film

# Clase de arbol binario
class BinaryTree:
    def __init__(self, root: Optional["Node"] = None) -> None:
        self.root = root
    # Recorridos

    # Recorrido en perorden recursivo
    def preorder(self) -> None:
        self.__preorder_r(self.root)
        print()

    def __preorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            print(node.data.title, end = ' ')
            self.__preorder_r(node.left)
            self.__preorder_r(node.right)
    
    # Función para guardar los elementos del arbol en una lista
    def tree_in_list(self) -> list[Film]:
        elements = []
        self.__preorder_r2(self.root,elements)
        return elements

    def __preorder_r2(self, node: Optional["Node"], elements: list[Film]) -> list[Film]:
        if node is not None:
            elements.append(node.data)
            self.__preorder_r2(node.left, elements)
            self.__preorder_r2(node.right, elements)
        return elements
    
    # Recorrido en inorden recursivo
    def inorder(self) -> None:
        self.__inorder_r(self.root)
        print()

    def __inorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            self.__inorder_r(node.left)
            print(node.data.title, end = ' ')
            self.__inorder_r(node.right)
    
    # Recorrido en postorden recursivo     
    def postorder(self) -> None:
        self.__postorder_r(self.root)
        print()

    def __postorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            self.__postorder_r(node.left)
            self.__postorder_r(node.right)
            print(node.data.title, end = ' ')
    
    # Función de altura de un nodo
    def height(self, node) -> int:
        return self.__height_r(node)
    
    def __height_r(self, node: Optional["Node"]) -> int:
        if node is None:
            return 0
        return 1 + max(self.__height_r(node.left), self.__height_r(node.right))

    # Recorrido por niveles recursivo
    def levels(self) ->list[str]:
        def inter (node: Optional["Node"], level, result):
            if node is not None:
                if len(result) <= level:
                    result.append([])
                result[level].append(node.data.title)
                inter(node.left, level+1, result)
                inter(node.right,level+1,result)
        result = []
        inter(self.root,0,result)
        return[item for sublist in result for item in sublist]

# Clase de arbol binario de busqueda
class BST(BinaryTree):
    def __init__(self, root: Optional["Node"] = None) -> None:
        super().__init__(root)
    
    # Función de busqueda por el titulo   
    def search(self, title: str) -> Tuple[Optional["Node"], Optional["Node"]]:
        p, pad = self.root, None
        while p is not None:
            if title == p.data.title:
                return p, pad
            else:
                pad = p
                if title < p.data.title:
                    p = p.left
                else:
                    p = p.right
        return p, pad
    
    # Función de inserción
    def insert(self, data: Film) -> bool:
        to_insert = Node(data)
        if self.root is None:
            self.root = to_insert
            return True
        else:
            p, pad = self.search(data.title)
            if p is not None:
                return False
            else:
                if data.title < pad.data.title:
                    pad.left = to_insert
                else:
                    pad.right = to_insert
                return True
    
    # Función de eliminación
    def delete(self, title: str, mode: bool = True) -> bool:
        p, pad = self.search(title)
        if p is not None:
            if p.left is None and p.right is None:
                if pad != None:
                    if p == pad.left:
                        pad.left = None
                    else:
                        pad.right = None
                self.root=None
                del p

            elif p.left is None and p.right is not None:
                if pad != None:
                    if p == pad.left:
                        pad.left = p.right
                    else:
                        pad.right = p.right
                else:
                    self.root = p.right
                del p
            elif p.left is not None and p.right is None:
                if pad != None:
                    if p == pad.left:
                        pad.left = p.left
                    else:
                        pad.right = p.left
                else:
                    self.root = p.left
                del p
            else:
                if mode:
                    pred, pad_pred, son_pred = self.__pred(p)
                    p.data = pred.data
                    if p == pad_pred:
                        pad_pred.left = son_pred
                    else:
                        pad_pred.right = son_pred
                    del pred
                else:
                    sus, pad_sus, son_sus = self.__sus(p)
                    p.data = sus.data
                    if p == pad_sus:
                        pad_sus.right = son_sus
                    else:
                        pad_sus.left = son_sus
                    del sus
            return True
        return False

    # Función de predecesor
    def __pred(self, node: "Node") -> Tuple["Node", "Node", Optional["Node"]]:
        p, pad = node.left, node
        while p.right is not None:
            p, pad = p.right, p
        return p, pad, p.left

    # Función de sucesor
    def __sus(self, node: "Node") -> Tuple["Node", "Node", Optional["Node"]]:
        p, pad = node.right, node
        while p.left is not None:
            p, pad = p.left, p
        return p, pad, p.right
    

# Clase de arbol AVL
class AVLT(BST):
    def __init__(self, root: Optional["Node"] = None) -> None:
        super().__init__(root)
    
    # Función para calcular el balance de un nodo
    def calculate_balance(self, node: Optional["Node"]) -> None:
        node.balance = self.height(node.right) - self.height(node.left)
    
    # Función para calcular el balance de todo el arbol
    def calculate_balance_tree(self) -> None:
        self.__calculate_balance_tree_r(self.root)
    
    def __calculate_balance_tree_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            self.calculate_balance(node)
            self.__calculate_balance_tree_r(node.left)
            self.__calculate_balance_tree_r(node.right)
    
    # Función para encontrar nodo con desbalance
    def find_disbalance(self, node: Node) -> Node:
        while(node):
            if abs(node.balance) == 2:
                break
            else:
                node = self.find_parent(node)
        return node
    
    # Función para rebalancear por medio de rotaciones
    def rebalance(self, node: Node) -> None:
        pad = self.search(node.data.title)[1]
        if node.balance == 2:
            
            # Rotación simple izquierda
            if node.right.balance >= 0:
                if pad is None:
                    self.root = self.slr(node)
                else:
                    if pad.right == node:
                        pad.right = self.slr(node)
                    else:
                        pad.left = self.slr(node)
            
            # Rotacion doble derecha - izquierda
            else:
                if pad is None:
                    self.root = self.drlr(node)
                else:
                    if pad.right == node:
                        pad.right = self.drlr(node)
                    else:
                        pad.left = self.drlr(node)
            
        elif node.balance == -2:
            self.calculate_balance(node.left)
            # Rotación simple derecha
            if node.left.balance <= 0:
                if pad is None:
                    self.root = self.srr(node)
                else:
                    if pad.right == node:
                        pad.right = self.srr(node)
                    else:
                        pad.left = self.srr(node)
            
            # Rotación doble izquierda - derecha
            else:
                if pad is None:
                    self.root = self.dlrr(node)
                else:
                    if pad.right == node:
                        pad.right = self.dlrr(node)
                    else:
                        pad.left = self.dlrr(node)
        self.calculate_balance_tree()
    
    # Rotaciones
    def slr(self, node: Node) -> Node:
        aux = node.right 
        node.right = aux.left
        aux.left = node
        return aux
    
    def srr(self, node:Node) -> Node:
        aux = node.left
        node.left = aux.right
        aux.right = node
        return aux
    
    def drlr(self, node:Node) -> Node:
        node.right = self.srr(node.right)
        return(self.slr(node))
    
    def dlrr (self, node: Node) -> Node:
        node.left = self.slr(node.left)
        return(self.srr(node))

    #Insertar/balancear 
    def insert(self, data: Film) -> bool:
        if super().insert(data):
            node = self.search(data.title)[0]
            self.calculate_balance_tree()
            p = self.find_disbalance(node)
            if p is not None:
                self.rebalance(p)
                return True
            else:
                return True
        else:
            return False
    
    #Borrar/balancear
    def delete(self, title: str) -> bool:
        if super().delete(title):
            node = self.search(title)[1]
            p = self.find_disbalance(node)
            if p is not None:
                self.rebalance(p)
                return True
            else:
                return True
        else:
            return False
        
    # Función para encontrar el padre del nodo
    def find_parent(self, node: Node) -> Node:
        return self.search(node.data.title)[1]
    
    # Función para encontrar el abuelo de un nodo
    def find_grandparent(self, node: Node) -> Node:
        return self.find_parent(self.find_parent(node))
    
    # Función para encontrar el tio de un nodo
    def find_uncle(self, node: Node) -> Node:
        gp = self.find_grandparent(node)
        if gp is not None:
            return gp.left if gp.right == self.find_parent(node) else gp.right
        return None

    # Función para tener el nivel de un nodo
    def calculate_level(self, node: Node) -> int:
        level = 0
        while node is not self.root:
            level = level+1
            node = self.find_parent(node)
        return level

    # Función para visualizar el arbol en consola (QUITAR DESPUES)
    def __repr__(self):
        return self.__print_tree(self.root)

    def __print_tree(self, node, level=0, side="root"):
        if node is None:
            return ""
        
        indent = " " * 4 * level

        # Define colors
        color_reset = "\033[0m"
        color_root = "\033[1;32m"    
        color_left = "\033[1;34m"    
        color_right = "\033[1;31m"   
        color_title = "\033[1;37m"   

        if side == "root":
            result = f"{indent}{color_root}(root){color_reset} -> {color_title}{node.data.title}{color_reset} {node.balance}\n"
        elif side == "left":
            result = f"{indent}{color_left}(left){color_reset} -> {color_title}{node.data.title}{color_reset} {node.balance}\n"
        else:  # right
            result = f"{indent}{color_right}(right){color_reset} -> {color_title}{node.data.title}{color_reset} {node.balance}\n"
        
        result += self.__print_tree(node.left, level + 1, "left")
        result += self.__print_tree(node.right, level + 1, "right")
        
        return result