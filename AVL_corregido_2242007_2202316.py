# AVL_corregido.py
#Implementación completa y corregida de un árbol AVL.

"""
Incluye:
- Clase Node
- Inserción (con rotaciones y rebalanceo correcto)
- Eliminación (con rebalanceo)
- Recorrido in-order
- Visualización simple por niveles (print_tree)
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

def getHeight(node):
    return node.height if node else 0

def getBalance(node):
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)

def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))

def rotate_right(y):
    x = y.left
    T2 = x.right

    # rotación
    x.right = y
    y.left = T2

    # actualizar alturas
    updateHeight(y)
    updateHeight(x)

    return x

def rotate_left(x):
    y = x.right
    T2 = y.left

    # rotación
    y.left = x
    x.right = T2

    # actualizar alturas
    updateHeight(x)
    updateHeight(y)

    return y

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            # valores duplicados: no insertamos
            return node

        updateHeight(node)
        balance = getBalance(node)

        # Left Left
        if balance > 1 and getBalance(node.left) >= 0:
            node = rotate_right(node)
        # Left Right
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            node = rotate_right(node)
        # Right Right
        elif balance < -1 and getBalance(node.right) <= 0:
            node = rotate_left(node)
        # Right Left
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            node = rotate_left(node)

        return node

    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if not node:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # nodo encontrado
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # nodo con dos hijos: obtener sucesor in-order (mínimo del subárbol derecho)
                temp = self._get_min_node(node.right)
                node.value = temp.value
                node.right = self._delete_recursive(node.right, temp.value)

        # si el árbol tenía un solo nodo
        if not node:
            return node

        # actualizar altura y rebalancear
        updateHeight(node)
        balance = getBalance(node)

        # Left Left
        if balance > 1 and getBalance(node.left) >= 0:
            node = rotate_right(node)
        # Left Right
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            node = rotate_right(node)
        # Right Right
        elif balance < -1 and getBalance(node.right) <= 0:
            node = rotate_left(node)
        # Right Left
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            node = rotate_left(node)

        return node

    def _get_min_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def inorder(self):
        res = []
        self._inorder_recursive(self.root, res)
        return res

    def _inorder_recursive(self, node, res):
        if not node:
            return
        self._inorder_recursive(node.left, res)
        res.append(node.value)
        self._inorder_recursive(node.right, res)

    def print_tree(self):
        #Imprime el árbol nivel por nivel mostrando valor (h, bf) donde h=altura y bf=factor de balance.\"\"\"
        if not self.root:
            print(\"<árbol vacío>\")
            return

        from collections import deque
        q = deque([(self.root, 0)])
        current_level = 0
        line = []
        while q:
            node, lvl = q.popleft()
            if lvl != current_level:
                print(\"Nivel\", current_level, \":\", \"  \".join(line))
                line = []
                current_level = lvl
            bf = getBalance(node)
            line.append(f\"{node.value} (h={node.height}, bf={bf})\")
            if node.left: q.append((node.left, lvl+1))
            if node.right: q.append((node.right, lvl+1))
        if line:
            print(\"Nivel\", current_level, \":\", \"  \".join(line))

if __name__ == '__main__':
    # Demo simple
    avl = AVLTree()
    values_to_insert = [10, 20, 30, 40, 50, 25]
    for v in values_to_insert:
        avl.insert(v)

    print(\"Insertados:\", values_to_insert)
    avl.print_tree()
    print(\"In-order:\", avl.inorder())

    # Prueba de eliminación
    avl.delete(50)
    print(\"\\nDespués de eliminar 50:\")
    avl.print_tree()
    print(\"In-order:\", avl.inorder())
