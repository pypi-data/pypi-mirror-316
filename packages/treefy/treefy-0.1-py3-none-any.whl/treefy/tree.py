from collections import deque

def type_check(func):
    def wrapper(tree, *args, **kwargs):
        # Ensure the first argument is either a TreeNode or BinaryTree
        if not isinstance(tree, (TreeNode, BinaryTree)):
            raise TypeError(f"Function '{func.__name__}' expects TreeNode or BinaryTree, got {type(tree).__name__}")
        return func(tree, *args, **kwargs)
    return wrapper


class TreeNode:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"TreeNode({self.value})"

    def is_leaf(self):
        """Returns True if the node is a leaf (no children)."""
        return not self.left and not self.right


class BinaryTree:
    def __init__(self, root_value=None):
        """Initializes the tree with an optional root node."""
        self.root = TreeNode(root_value) if root_value is not None else None
        self.custom_functions = {}

    def add_node(self, parent_node, value, is_left=True):
        """
        Adds a node to the tree as a left or right child of the given parent node.
        :param parent_node: TreeNode to which the new node will be attached
        :param value: Value of the new node
        :param is_left: If True, the new node is added as the left child
        """
        if not isinstance(parent_node, TreeNode):
            raise ValueError("parent_node must be an instance of TreeNode")
        
        new_node = TreeNode(value)
        if is_left:
            if parent_node.left is not None:
                raise ValueError("Left child already exists!")
            parent_node.left = new_node
        else:
            if parent_node.right is not None:
                raise ValueError("Right child already exists!")
            parent_node.right = new_node
        return new_node
    
    def attach_subtree(self, parent, subtree, is_left=True):
        """
        Attaches a subtree to the specified parent node in the current tree.
        
        :param parent: Node in the current tree to which the subtree will be attached.
        :param subtree: Subtree to attach. Can be either a TreeNode or a Tree (BinaryTree) object.
        :param is_left: Boolean indicating whether to attach the subtree as the left or right child.
        :return: None
        """
        if parent is None:
            raise ValueError("Parent node cannot be None")
        
        # If the subtree is a Tree object, extract its root node
        if isinstance(subtree, BinaryTree):
            subtree_root = subtree.root
        elif isinstance(subtree, TreeNode):
            subtree_root = subtree
        else:
            raise TypeError("Subtree must be either a Tree or TreeNode instance")
        
        if is_left:
            if parent.left is not None:
                raise ValueError("Left child already exists. Remove it before attaching a new subtree.")
            parent.left = subtree_root
        else:
            if parent.right is not None:
                raise ValueError("Right child already exists. Remove it before attaching a new subtree.")
            parent.right = subtree_root


    def generate_tree_from_array(self, arr):
        """
        Function to generate a binary tree from a list (array).
        This assumes a complete binary tree representation.
        :param arr: List of values representing the binary tree in level order.
        :return: The root of the generated tree.
        """
        if not arr:
            return None
        
        # Create the root from the first element
        self.root = TreeNode(arr[0])
        
        # Queue to hold nodes while connecting children
        queue = [self.root]
        
        i = 1  # Start from the second element in the array
        while i < len(arr):
            node = queue.pop(0)  # Get the current node from the queue
            
            # If there is a left child, create it and add it to the queue
            if i < len(arr) and arr[i] is not None:
                node.left = TreeNode(arr[i])
                queue.append(node.left)
            i += 1
            
            # If there is a right child, create it and add it to the queue
            if i < len(arr) and arr[i] is not None:
                node.right = TreeNode(arr[i])
                queue.append(node.right)
            i += 1

        return self.root

    def register_function(self, name, func):
        """Allows users to add their custom function."""
        self.custom_functions[name] = type_check(func)

    def call_function(self, name, *args, **kwargs):
        """Calls the registered custom function."""
        if name in self.custom_functions:
            return self.custom_functions[name](self, *args, **kwargs)
        else:
            raise ValueError(f"Function '{name}' not found!")

    def get_height(self, node=None):
        """
            Calculates the height of the tree/subtree.
            :param node: Starting node for calculating height (defaults to the root)
        """
        if node is None:
            return 0  # Base case: a None node has a height of 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def level_order_traversal(self, node=None):
        """
            Performs a level-order traversal (breadth-first traversal) of the tree.
            Returns a list of node values in level order.
        """
        if node is None:
            return []

        result = []
        queue = deque([node])  # Use a queue to manage the nodes to visit

        while queue:
            current_node = queue.popleft()  # Dequeue the front node
            result.append(current_node.value)

            # Enqueue the left and right children if they exist
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

        return result
    
    def preorder_traversal(self, node):
        """
        Preorder Traversal: Root -> Left -> Right
        """
        if node is None:
            return []
        return [node.value] + self.preorder_traversal(node.left) + self.preorder_traversal(node.right)

    def inorder_traversal(self, node):
        """
        Inorder Traversal: Left -> Root -> Right
        """
        if node is None:
            return []
        return self.inorder_traversal(node.left) + [node.value] + self.inorder_traversal(node.right)

    def postorder_traversal(self, node):
        """
        Postorder Traversal: Left -> Right -> Root
        """
        if node is None:
            return []
        return self.postorder_traversal(node.left) + self.postorder_traversal(node.right) + [node.value]
    
    def draw_tree(self, node=None, level=0, width=64):
        if node is None:
            node = self.root

        # Width for spacing between nodes
        node_spacing = width // (2 ** (level + 1))

        # Recursively get lines for left and right subtrees
        left_lines = self.draw_tree(node.left, level + 1, width) if node.left else []
        right_lines = self.draw_tree(node.right, level + 1, width) if node.right else []

        # Create the current level line with the node value
        line = " " * (node_spacing - 1) + str(node.value) + " " * (node_spacing - 1)

        # Combine all lines for output
        result = [line]

        # Merge left and right subtree lines, padding shorter ones with spaces
        for i in range(max(len(left_lines), len(right_lines))):
            left_part = left_lines[i] if i < len(left_lines) else " " * node_spacing
            right_part = right_lines[i] if i < len(right_lines) else " " * node_spacing
            result.append(left_part + " " * (2 * node_spacing - len(left_part) - len(right_part)) + right_part)

        return result

    def print_tree(self, node):
        """
        Helper function to print the tree drawing.
        """
        lines = self.draw_tree(node)
        for line in lines:
            print(line)

    def __repr__(self):
        return f"Tree(root={self.root})"