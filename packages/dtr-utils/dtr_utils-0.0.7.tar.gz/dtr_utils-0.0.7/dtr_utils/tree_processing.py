from dtr_utils.ecd_score import alignment_score
from anytree import Node, PreOrderIter


def get_max_depth(node, depth=0):
    """
    Calculates the maximum depth of a tree.

    Args:
        node (Node): The root node of the tree or subtree.
        depth (int): The current depth in the traversal.

    Returns:
        int: The maximum depth of the tree.
    """
    if not node.children:
        return depth  # Return current depth if the node has no children
    return max(get_max_depth(child, depth + 1) for child in node.children)


def prune_to_max_depth(node, current_depth=0, max_depth=None):
    """
    Prunes the tree to keep only the nodes at the maximum depth.

    Args:
        node (Node): The current node of the tree.
        current_depth (int): The current depth in the tree traversal.
        max_depth (int): The maximum depth of the tree. If None, it will be calculated.

    Returns:
        bool: True if the node should be kept, False otherwise.
    """
    if max_depth is None:
        # Calculate max depth of the tree
        # max_depth = max((len(ancestor_path) for ancestor_path in node.iter_path()))
        max_depth = get_max_depth(node, depth=0)

    # Base case: Leaf nodes
    if not node.children:
        return current_depth == max_depth

    # Recursively check children and prune them if not at max depth
    to_keep = []
    for child in node.children:
        if prune_to_max_depth(child, current_depth + 1, max_depth):
            to_keep.append(child)

    # Replace children with the filtered list
    node.children = to_keep
    return current_depth == max_depth or bool(to_keep)


def find_parent_of_lowest_score(root):
    # Collect all leaf nodes
    leaf_nodes = root.leaves

    if not leaf_nodes:
        print("No leaf nodes found.")
        return None

    # Find the leaf node with the lowest score (assuming name is numeric)
    min_score_node = min(leaf_nodes, key=lambda n: float(n.name))

    # Return the parent of the node with the lowest score
    return min_score_node.parent, float(min_score_node.name)


def sanitize_word(word):
    # Create a translation table for characters to be replaced
    translation_table = str.maketrans(
        {
            "<": "lesser than",
            ">": "greater than",
            "\n": " ",
            "\t": " ",
            "\\": "",
            "\r": "",
        }
    )
    return word.translate(translation_table)


def final_tree_generate_dual(input_root, true_context):
    """
    Generates a plain tree by copying nodes from the input tree and computing alignment scores.

    Args:
        input_root (Node): The root node of the input tree (prebuilt using anytree). Its name is the initial context.
        true_context (str): The true context to compute alignment scores.

    Returns:
        root_plain: The root node of the plain tree.
    """
    # Initialize root node for the plain tree
    initial_context = input_root.name  # Initial context is the name of the input root
    root_plain = Node(f"ROOT_PLAIN = {initial_context}")

    Step = 1

    def traverse_and_copy(node, parent_plain, path_plain):
        """
        Recursively traverses the input tree and copies nodes to the plain tree.

        Args:
            node (Node): Current node in the input tree.
            parent_plain (Node): Current parent node in the plain tree.
            path_plain (list): Accumulated plain text path.
        """
        # Extract node details
        node_name = node.name
        if isinstance(node_name, tuple):
            word, score, llm_tokens, ngram_tokens, typ = node_name
            path_plain.append(word)
            sanitized_word = sanitize_word(word)
        else:
            word = node_name
            path_plain.append(word)
            sanitized_word = sanitize_word(word)

        # Create a new node in the plain tree
        new_plain_node = Node(f"{sanitized_word}", parent=parent_plain)

        # Traverse children
        for child in node.children:
            traverse_and_copy(child, new_plain_node, path_plain)

        # If it's a leaf node, finalize the path and add alignment score
        if not node.children:
            complete_text_plain = "".join(path_plain)

            # Add the complete text to the tree
            final_plain_node = Node(f"{complete_text_plain}", parent=new_plain_node)

            # Compute alignment score
            score = alignment_score(complete_text_plain, true_context)
            Node(score, parent=final_plain_node)

            print(f"\n\n\Step: {Step}")
            print("Complete Text (Plain):", complete_text_plain)
            print("Alignment Score:", score)
            Step += 1

        # Pop the current node from the path as we backtrack
        path_plain.pop()

    # Start recursive traversal
    traverse_and_copy(input_root, root_plain, [])

    return root_plain
