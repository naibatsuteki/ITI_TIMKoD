import bitarray as ba
from typing import Optional
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

    # TODO (?): Typing for generator?
    def ibfs(self):
        """
        List tree level by level from top to bottom, from right to left.
        :return:
        """
        queue = [self.tree]
        while len(queue):
            next_node = queue.pop(0)
            if next_node.right is not None:
                queue.append(next_node.right)
            if next_node.left is not None:
                queue.append(next_node.left)
            yield next_node

    def __init__(self):
        self.tree: TreeNode = TreeNode(weight=0)
        self.seen_character_dict = {}
        self.NTY_node: TreeNode = self.tree

    def add_character(self, character: str) -> None:
        """
        Add character to tree.
        If character was seen before then increment node value.
        If character wasn't seen before then create new node from NTY node.
        In both cases check is tree after modification is valid tree.
        :param character:
        :return:
        """
        if character in self.seen_character_dict.keys():
            node2update: TreeNode = self.seen_character_dict[character]
            self._update_tree(node2update)
        else:
            # Adding new nodes is edge case witch can't be handled strait forward by _update_tree method.
            # All not handled behaviour is handled here then normal procedure is run.
            self.NTY_node.left = TreeNode(parent=self.NTY_node, l_child=True)
            self.NTY_node.right = TreeNode(value=character, weight=1, parent=self.NTY_node, l_child=False)
            self.NTY_node.weight += 1
            self.seen_character_dict[character] = self.NTY_node.right
            node2update = self.NTY_node.parent
            self.NTY_node = self.NTY_node.left
            # Edge case for root node.
            if node2update is not None:
                self._update_tree(node2update)

    def get_code(self):
        pass

    def _get_node_to_swap(self, updated_node) -> Optional[TreeNode]:
        """
        Check witch node should be swapped to restore valid tree structure.
        If tree is valid return None, in other case return node witch should be swapped with updated node.
        """
        for node in self.ibfs():
            if node is updated_node:
                break
            if node.parent is None or node is updated_node.parent:
                continue
            if node.weight == updated_node.weight:
                return node
        return None

    def _swap_nodes(self, node_1: TreeNode, node_2: TreeNode) -> None:
        """
        Swap place 2 nodes in the tree.
        """
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

    def _update_tree(self, updated_node: TreeNode) -> None:
        """
        Update weight in
        """
        # Root node edge case.
        if updated_node.parent is None:
            updated_node.weight += 1
            return

        node2swap = self._get_node_to_swap(updated_node)

        if node2swap is not None:
            # Modification is required
            self._swap_nodes(updated_node, node2swap)

        # Update weight modified node.
        updated_node.weight += 1
        # Recursive repeat procedure for updated node parent.
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
    # ahct.add_character('b')
    # ahct.add_character('o')
    # ahct.add_character('o')
    # ahct.add_character('k')
    # ahct.add_character('k')
    # ahct.add_character('e')
    # ahct.add_character('e')
    # ahct.add_character('p')
    # ahct.add_character('e')
    # ahct.add_character('r')

    ahct.add_character('m')
    ahct.add_character('i')
    ahct.add_character('s')
    ahct.add_character('s')
    ahct.add_character('i')
    ahct.add_character('s')
    ahct.add_character('s')
    ahct.add_character('i')
    ahct.add_character('p')
    ahct.add_character('p')
    ahct.add_character('i')

    for i in ahct.ibfs():
        print(i.value)
