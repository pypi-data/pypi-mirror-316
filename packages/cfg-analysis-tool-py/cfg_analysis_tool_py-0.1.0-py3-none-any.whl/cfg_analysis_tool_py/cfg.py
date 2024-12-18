from tree_sitter import Node
import uuid


class ExpressionBlock:
    """Storage container for a maximal sequence of expressions for a CFG."""

    def __init__(self):
        self._expressions = []
        self._color = "none"
        self._iteration = 0

    def __len__(self):
        return len(self._expressions)

    def __str__(self) -> str:
        return " \n ".join([node.text.decode() for node in self._expressions])

    def __repr__(self) -> str:
        return str(self)

    @property
    def expressions(self):
        return self._expressions

    @expressions.deleter
    def expressions(self):
        self._expressions = []

    def add_expression(self, expression):
        assert isinstance(expression, Node)

        self._expressions.append(expression)

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def get_iteration(self):
        return self._iteration

    def set_iteration(self, iteration_number):
        self._iteration = iteration_number


class ControlFlowGraph:
    """
    Connector of ExpressionBlock objects for visualization and static analysis.
    Structure represents a directed graph.
    """

    def __init__(self):
        # Nodes (blocks) & adjacency connections
        self._blocks = []
        self._next = []
        self._prev = []

        # Entrance & exit(s) indices
        self._entrance = 0
        self._exits = {}

    def __len__(self):
        return len(self._blocks)

    def __str__(self):
        return "\n".join(
            [
                f"{block_i}: {str(self.blocks[block_i])}"
                for block_i in self.traverse_forward(self.entrance)
            ]
        )

    @property
    def blocks(self):
        return self._blocks

    @property
    def last_block(self):
        """Return reference to exit block, create one if there are multiple exists"""

        # Create new exit block if there are currently multiple exits or if there aren't any exits
        if len(self._exits) > 1 or not len(self):
            last = self.add_node(ExpressionBlock())
            for exit in self._exits:
                self.add_edge(exit, last)

            self._exits = {last}

        else:
            last = next(iter(self._exits))  # Quick method to get the only exit

        return self._blocks[last]

    @property
    def adjacency(self):
        return self._next

    @property
    def edge_list(self):
        """Generate an edge list from the next adjacency list."""
        edges = []

        for from_index, to_indices in enumerate(self._next):
            edges += [(from_index, to_index) for to_index in sorted(to_indices)]

        return edges

    @property
    def entrance(self):
        return self._entrance

    @property
    def exits(self):
        return self._exits

    @exits.setter
    def exits(self, indices):
        assert all(
            [isinstance(index, int) and index <= len(self) for index in indices]
        ), "Exit indices must be numbers referring to valid blocks"

        self._exits = set(indices)

    def get_block_index(self, block):
        """Get the index of an ExpressionBlock in cfg.blocks."""

        return self._blocks.index(block)

    def get_block(self, block_index):
        return self._blocks[block_index]

    def add_node(self, block):
        """
        Add a block to block list and
        create a new list for next and previous adjacency.
        """

        self._blocks.append(block)
        self._next.append(set())
        self._prev.append(set())

        return len(self._blocks) - 1

    def add_edge(self, from_index, to_index):
        """Connect two blocks by their indexes."""

        self._next[from_index].add(to_index)
        self._prev[to_index].add(from_index)

    def merge_cfg(self, cfg):
        """Graft an existing CFG structure following block index."""

        assert len(cfg) != 0, "Cannot merge empty CFG"

        # First add all blocks to CFG to get their indexes for edge creation
        new_indices = [self.add_node(block) for block in cfg.blocks]

        # Now we can re-map edges using new indexes for blocks
        for old_index, next_indices in enumerate(cfg.adjacency):
            new_index = new_indices[old_index]  # Get new index for the target block

            # Map old indexes to new before adding edges
            new_next_indices = map(
                lambda old_index: new_indices[old_index], next_indices
            )

            # Add connections from target block to next blocks
            for next_index in new_next_indices:
                self.add_edge(new_index, next_index)

        # Connect from exits to first block of merge CFG
        for exit in self._exits:
            self.add_edge(exit, new_indices[0])

        # Set exits of merge CFG as exits for existing CFG
        self.exits = list(map(lambda old_index: new_indices[old_index], cfg._exits))

    def merge_cfg_and_last_block(self, cfg):
        """Graft an existing CFG structure following block index.

        Combines the last block of existing CFG with the first block of merge CFG.
        """

        assert len(cfg) != 0, "Cannot merge empty CFG"
        assert (
                len(self._next[self.blocks.index(self.last_block)]) == 0
        ), "Cannot merge if last block has adjacency"

        # Copy last block expressions and then remove that block
        last_block_expressions = self.last_block.expressions
        last_block_prev = self._prev[-1]
        self._blocks = self._blocks[:-1]
        self._next = self._next[:-1]
        self._prev = self._prev[:-1]

        # Add all blocks to CFG to get their indexes for edge creation
        new_indices = [self.add_node(block) for block in cfg.blocks]

        # Paste expressions from last block of existing CFG to first block of merge CFG
        first_block = self.blocks[new_indices[0]]
        first_block_expressions = first_block.expressions
        del first_block.expressions
        last_block_expressions.extend(first_block_expressions)

        for expression in last_block_expressions:
            first_block.add_expression(expression)

        # Cleanup first block edges
        self._prev[new_indices[0]] = last_block_prev

        # Now we can re-map edges using new indexes for blocks
        for old_index, next_indices in enumerate(cfg.adjacency):
            new_index = new_indices[old_index]  # Get new index for the target block

            # Map old indexes to new before adding edges
            new_next_indices = map(
                lambda old_index: new_indices[old_index], next_indices
            )

            # Add connections from target block to next blocks
            for next_index in new_next_indices:
                self.add_edge(new_index, next_index)

        # Set exits of merge CFG as exits for existing CFG
        self.exits = list(map(lambda old_index: new_indices[old_index], cfg._exits))

    def get_next_neighbors(self, block_index):
        """Get the neighbors of a given node in the forward direction."""

        return self._next[block_index]

    def get_prev_neighbors(self, block_index):
        """Get the neighbors of a given node in the backward direction."""

        return self._prev[block_index]

    def delete_forward_neighbors(self, block_index):
        """Delete both the next and prev connections which represent the forward neighbors of a block."""

        self._next[block_index] = set()

        for p in self._prev:
            p.discard(block_index)

    def traverse_forward(self, block_index, visited=None):
        """
        Traverse the CFG in the forward direction using a recursive DFS approach.
        This function acts as a generator so it can be used in a for loop.
        """

        if block_index >= len(self):
            return
        if visited is None:
            visited = set()

        # Keep track of already visited blocks to avoid infinite cycles
        visited.add(block_index)
        yield block_index

        # Recursively path to all neighbors
        for neighbor in self.get_next_neighbors(block_index):
            if neighbor not in visited:
                yield from self.traverse_forward(neighbor, visited)

    def traverse_backward(self, block_index, visited=None):
        """
        Traverse the CFG in the backward direction using a recursive DFS approach.
        This function acts as a generator so it can be used in a for loop.
        """

        if block_index >= len(self):
            return
        if visited is None:
            visited = set()

        # Keep track of already visited blocks to avoid infinite cycles
        visited.add(block_index)
        yield block_index

        # Recursively path to all neighbors
        for neighbor in self.get_prev_neighbors(block_index):
            if neighbor not in visited:
                yield from self.traverse_backward(neighbor, visited)


# Testing
if __name__ == "__main__":
    # Test CFG contruction

    cfg = ControlFlowGraph()

    block1 = ExpressionBlock()
    block2 = ExpressionBlock()
    block3 = ExpressionBlock()

    b1 = cfg.add_node(block1)
    b2 = cfg.add_node(block2)
    b3 = cfg.add_node(block3)

    cfg.add_edge(b1, b2)
    cfg.add_edge(b1, b3)

    cfg.exits = {b3}

    add_cfg = ControlFlowGraph()

    add1 = ExpressionBlock()
    add2 = ExpressionBlock()
    add3 = ExpressionBlock()
    add4 = ExpressionBlock()

    a1 = add_cfg.add_node(add1)
    a2 = add_cfg.add_node(add2)
    a3 = add_cfg.add_node(add3)
    a4 = add_cfg.add_node(add4)

    add_cfg.add_edge(a1, a2)
    add_cfg.add_edge(a1, a3)
    add_cfg.add_edge(a2, a4)
    add_cfg.add_edge(a4, a1)

    cfg.merge_cfg(add_cfg)

    print("Forward traversal")
    for node in cfg.traverse_forward(0):
        print(node)

    print("Backward traversal")
    for node in cfg.traverse_backward(5):
        print(node)

    # Visualization with NetworkX package
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()

    nodes = G.add_nodes_from([i for i in range(len(cfg))])
    edges = G.add_edges_from(cfg.edge_list)

    # Forces the graph into a tree shape (for demo purposes)
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

    nx.draw_networkx(G, pos, arrows=True)
    plt.show()
