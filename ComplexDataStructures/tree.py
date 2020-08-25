class TreeNode:
    def __init__(self, value):
        print('initializing node...')
        self.value = value
        self.children = []

    def add_child(self, child_node):
        print('adding', child_node.value)
        self.children.append(child_node)

    def remove_child(self, child_node):
        print('removing', child_node.value, 'from', self.value)
        new_children = [child for child in self.children if child is not child_node]
        self.children = new_children

    def traverse(self):
        nodes_to_visit = [self]
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop()
            print(current_node.value)
            nodes_to_visit += current_node.children
