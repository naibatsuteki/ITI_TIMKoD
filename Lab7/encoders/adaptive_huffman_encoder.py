import bitarray as ba
from typing import Tuple, Optional
from encoders.basic_encoder import BasicEncoder


class TreeNode:
    def __init__(self, value=None, weight=0, left=None, right=None, parent=None, l_child=None):
        self.value = value
        self.weight = weight
        self.left: Optional[TreeNode] = left
        self.right: Optional[TreeNode] = right
        self.parent: Optional[TreeNode] = parent
        self.l_child = l_child


class AdaptiveHuffmanCodeTree:

    def ibfs(self, minimal_weight=0):
        queue = [self.tree]
        while len(queue):
            next_node = queue.pop(0)
            if next_node.weight > minimal_weight:
                if next_node.right is not None:
                    queue.append(next_node.right)
                if next_node.left is not None:
                    queue.append(next_node.left)
            yield next_node

    def __init__(self):
        self.tree: TreeNode = TreeNode(weight=0)
        self.code_dict = {}
        self.NYT_node: TreeNode = self.tree

    def add_character(self, character: str):
        if character in self.code_dict.keys():
            node2update: TreeNode = self.code_dict[character]
            self._update_tree(node2update)
        else:
            self.NYT_node.left = TreeNode(parent=self.NYT_node, l_child=True)  # New NYT node
            self.NYT_node.right = TreeNode(value=character, weight=1, parent=self.NYT_node, l_child=False)
            self.NYT_node.weight += 1
            self.code_dict[character] = self.NYT_node.right
            node2update = self.NYT_node.parent
            self.NYT_node = self.NYT_node.left
            if node2update is not None:
                self._update_tree(node2update)

    def get_code(self):
        pass

    def _get_node_to_swap(self, updated_node) -> Optional[TreeNode]:
        try:
            # potential = [node for node in self.ibfs(updated_node.weight) if
            #              node.parent is not None
            #              and node is not updated_node.parent
            #              and node is not updated_node
            #              and node.weight == updated_node.weight]
            potential = []
            for node in self.ibfs(updated_node.weight):
                if node is updated_node:
                    break
                if node.parent is None or node is updated_node.parent:
                    continue
                if node.weight == updated_node.weight:
                    potential.append(node)
            return potential[0]
        except IndexError:
            return None

    def _swap_nodes(self, node_1: TreeNode, node_2: TreeNode):
        # Freeze key values.
        node_1_parent = node_1.parent
        node_2_parent = node_2.parent
        node_1_l_child = node_1.l_child
        node_2_l_child = node_2.l_child

        if node_1.l_child:
            node_1_parent.left = node_2
        else:
            node_1_parent.right = node_2
        node_2.parent = node_1_parent

        if node_2.l_child:
            node_2_parent.left = node_1
        else:
            node_2_parent.right = node_1
        node_1.parent = node_2_parent

        node_1.l_child = node_2_l_child
        node_2.l_child = node_1_l_child

    def _update_tree(self, updated_node: TreeNode):
        if updated_node.parent is None:
            updated_node.weight += 1
            return
        node2swap = self._get_node_to_swap(updated_node)
        if node2swap is not None:
            self._swap_nodes(updated_node, node2swap)
        updated_node.weight += 1
        self._update_tree(updated_node.parent)


class AdaptiveHuffmanEncoder(BasicEncoder):

    def __init__(self):
        super(AdaptiveHuffmanEncoder, self).__init__()
        state = None

    def create(self, text: str) -> None:
        """
        docstring
        """
        pass

    def encode(self, text: str) -> ba.bitarray:
        """
        docstring
        """
        result = ba.bitarray()
        for c in text:
            result.extend(self.code[c])
        return result

    def decode(self, coded_text: ba.bitarray) -> str:
        """
        docstring
        """
        # This method is not obligatory in this task
        pass


# Local testing
if __name__ == '__main__':
    ahct = AdaptiveHuffmanCodeTree()
    ahct.add_character('b')
    ahct.add_character('o')
    ahct.add_character('o')
    ahct.add_character('k')
    ahct.add_character('k')
    ahct.add_character('e')
    ahct.add_character('e')
    ahct.add_character('p')
    ahct.add_character('e')
    ahct.add_character('r')

    for i in ahct.ibfs():
        print(i.value)
