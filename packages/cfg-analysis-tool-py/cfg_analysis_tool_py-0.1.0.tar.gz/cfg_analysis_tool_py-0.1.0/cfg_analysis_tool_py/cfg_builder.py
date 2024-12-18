import os
from tree_sitter import Language, Parser
import tree_sitter_python as tspython
from .cfg import ControlFlowGraph, ExpressionBlock
import networkx as nx
import matplotlib.pyplot as plt
import re

ATOMIC_EXPRESSIONS = {"expression_statement", "comparison_operator", "pass_statement", "true", "false", "identifier", "integer", "string", "none"}
JUMP_EXPRESSIONS = {"return_statement", "continue_statement", "break_statement"}

class CFGBuilder:
    """
    CFGBuilder processes Python code and outputs a directed graph
    representing the flow of code

    Args:
        source_code (str): Input Python code
    """
    def __init__(self, source_code):
        self.__source_code = bytes(source_code)

        # Set-up parser with language file
        PY_LANGUAGE = Language(tspython.language())
        self.__parser = Parser(PY_LANGUAGE)

        self.__tree = self.__parser.parse(self.__source_code)

        self.__returns = set()
        self.__continue_stack = []
        self.__break_stack = []

        self.__unreachable_nodes = []
        self.__variables = {}
        self.__variable_values = {}
        self.__variable_nodes = {}
        self.__conditional_nodes = []
        self.__always_true_nodes = []
        self.__condition_and_consequence = []
        self.__while_nodes = []
        self.__while_and_conditions = []

        # JUMP_EXPRESSIONS is subset of ATOMIC_EXPRESSIONS
        ATOMIC_EXPRESSIONS.update(JUMP_EXPRESSIONS)

        # Control-flow change handlers
        self.__control_flow_handlers = {
            "while_statement": self.__handle_while,
            "for_statement": self.__handle_for,
            "if_statement": self.__handle_if_elif_else,
        }

        self.__counter = 1  # increments after every call to plot
        self.__seenNodes = set()

    @property
    def unreachable_nodes(self):
        """
        Returns a list of nodes that are unreachable

        Returns:
            list: List of unreachable nodes
        """
        return self.__unreachable_nodes

    @property
    def conditional_nodes(self):
        """
        Returns all nodes containing if, elif, or else statements

        Returns:
            list: List of nodes
        """
        return self.__conditional_nodes

    @property
    def while_nodes(self):
        """
        Returns all conditions within while statements

        Returns:
            list: List of nodes
        """
        return self.__while_nodes

    @property
    def while_and_conditions(self):
        """
        Returns all conditions and while conditions

        Returns:
            list: List of nodes
        """
        return self.__while_and_conditions

    @property
    def always_true_nodes(self):
        """
        Returns if and elif statements that will always evaluate to true

        Returns:
            list: List of nodes
        """
        return self.__always_true_nodes

    @property
    def condition_and_consequence_nodes(self):
        """
        Returns a two dimensional list that contains conditionals and their consequences
        For an if statement, includes condition and consequence
        for an elif statementm includes entire elif node, condition, and consequence

        Returns:
            list: two dimensional list of nodes
        """
        return self.__condition_and_consequence

    def __mark_variables(self, node):
        """
        Use RegEx to find variable assignments.
        Adds variables found to variables map and sets the initial value to False

        Args:
            text (str): A block of input code
        """
        # Scan for usage of existing variables in the assignment statement
        text = node.text.decode("UTF8")
        pattern = rf'[\w\s]=(?!=)'
        lines = text.splitlines()
        line = lines[0]
        # Commented code or print statements do not contain variable assignments
        if line.strip().startswith('#') or line.strip().startswith('print('):
            return
        matches = re.finditer(pattern, line)
        for match in matches:
            variable= line[:match.start() + 1].strip()
            value = line[match.end():].strip()
            if value.isnumeric():
                value = int(value)
            self.__variable_values.setdefault(variable, value)
            self.__variable_values[variable] = value

    # Handler functions for control flow statements
    def __handle_if_elif_else(self, if_node):
        """
        Process if condition and corresponding consequence block then
           iterates over any elif or else clauses to add to CFG

        Args:
            if_node: An 'If' conditional statement

        Returns:
            ControlFlowGraph: The control flow graph representing the 'if' block.

        """
        conditions = []

        #keeps track of if statement and its associated condition
        if_and_consequence = []

        condition = if_node.child_by_field_name("condition")
        conditions.append(condition)
        if_and_consequence.append(condition)
        node_text = condition.text.decode("UTF8")
        evaluates_to = self.__safe_eval(node_text, {}, self.__variable_values)
        if (evaluates_to == True):
            self.__always_true_nodes.append(condition)

        consequence = if_node.child_by_field_name("consequence")
        if_and_consequence.append(consequence)
        self.__condition_and_consequence.append(if_and_consequence)


        #keeping track of elif conditions and their consequences
        elif__condition_and_consequence = []
        alternatives = if_node.children_by_field_name(
            "alternative"
        )  # alternatives are both elif and else clauses
        for i in alternatives:
            #keeping track of all alternatives in conditions
            conditions.append(i)
            if i.type == "elif_clause":
                elif__condition_and_consequence.append(i)
                elif_condition = i.child_by_field_name("condition")

                #keeping track of conditions and their associated consequences
                elif__condition_and_consequence.append(elif_condition)
                elif_consequence  = i.child_by_field_name("consequence")
                elif__condition_and_consequence.append(elif_consequence)
                self.__condition_and_consequence.append(elif__condition_and_consequence)

                elif_condition_text = elif_condition.text.decode("UTF8")
                evaluates_to = self.__safe_eval(elif_condition_text, {}, self.__variable_values)
                if (evaluates_to == True):
                    self.__always_true_nodes.append(i)


        self.__conditional_nodes.append(conditions)
        self.__while_and_conditions.append(conditions)

        condition_cfg = self.__traverse_tree(condition)
        consequence_cfg = self.__traverse_tree(consequence)
        elif_cfgs = [] # Array [] of hashmap objects {}
        else_cfg = None

        final_exits = set()  # Stores indices of all leaf blocks
        last_condition_i = set()  # Stores index of last added conditon

        # Split up the elif and else clauses
        for alt in alternatives:
            self.__mark_variables(alt)
            if alt.type == "else_clause":
                else_cfg = self.__traverse_tree(alt.child_by_field_name("body"))
            elif alt.type == "elif_clause":
                elif_cfgs.append(
                    {
                        "condition": self.__traverse_tree(
                            alt.child_by_field_name("condition")
                        ),
                        "consequence": self.__traverse_tree(
                            alt.child_by_field_name("consequence")
                        ),
                    }
                )
            else:
                print(f"Invalid type found as alternative in if block: {alt.type}")

        # Nested Helper Function
        def __add_leaf(cfg):
            """
            Add a leaf block to the overall if statement cfg.

            Args:
                cfg (ControlFlowGraph): The CFG to add to the tree
            """

            nonlocal last_condition_i, condition_cfg, final_exits

            last_condition_i = condition_cfg.exits
            condition_cfg.merge_cfg(cfg)
            final_exits.update(condition_cfg.exits)
            condition_cfg.exits = last_condition_i

        # Add consequence of if statement
        __add_leaf(consequence_cfg)

        # Form tree of elif blocks
        for alternative in elif_cfgs:
            condition_cfg.merge_cfg(alternative["condition"])
            __add_leaf(alternative["consequence"])

        # Add else block to tree if it exists
        if else_cfg:
            __add_leaf(else_cfg)

        # Point head of last conditon block directly to exit if necessary
        if not alternatives or not else_cfg:
            final_exits.update(last_condition_i)

        # Set all final exits
        condition_cfg.exits = final_exits

        self.plot(condition_cfg, "if")

        return condition_cfg

    def __handle_while(self, while_node):
        """
        Associates nodes with while_node to produce a CFG

        Args:
            while_node: A 'while' statement

        Returns:
            ControlFlowGraph: The control flow graph representing the 'while' block
        """
        self.__continue_stack.append(set())
        self.__break_stack.append(set())

        while_and_consequence = []

        condition = while_node.child_by_field_name("condition")
        self.__while_nodes.append(condition)
        self.__while_and_conditions.append([condition])
        while_and_consequence.append(condition)
        node_text = condition.text.decode("UTF8")
        evaluates_to = self.__safe_eval(node_text, {}, self.__variable_values)
        if (evaluates_to == True):
            self.__always_true_nodes.append(condition)

        body = while_node.child_by_field_name("body")
        while_and_consequence.append(body)
        self.__condition_and_consequence.append(while_and_consequence)

        condition_cfg = self.__traverse_tree(condition)
        body_cfg = self.__traverse_tree(body)

        condition_cfg.merge_cfg(body_cfg)


        for exit in condition_cfg.exits:
            # Add an edge from each exit point of the loop's body back to the entrance of the loop
            # This represents a continuation of the loop
            condition_cfg.add_edge(exit, condition_cfg.entrance)
        # Sets the exit point of the loop to the entrance of the loop
        # This visually communicates a loop with a double sided arrow.
        condition_cfg.exits = {condition_cfg.entrance}

        self.__handle_continue(condition_cfg)
        self.__continue_stack.pop()
        self.__handle_break(condition_cfg)
        self.__break_stack.pop()

        self.plot(condition_cfg, "while")

        return condition_cfg

    def __handle_for(self, for_node):
        """
        Associates nodes with for_node to produce a CFG

        Args:
            for_node: A 'for' statement

        Returns:
            ControlFlowGraph: The control flow graph representing the 'for' block
        """

        empty_iterators = {"[]", "{}", "()", '""'}

        self.__continue_stack.append(set())
        self.__break_stack.append(set())

        element = for_node.child_by_field_name("left")
        iterator = for_node.child_by_field_name("right")

        iterator_text = iterator.text.decode("UTF8")

        body = for_node.child_by_field_name("body")

        # checking to see if for loop is trying to iterate through something empty/of length 0
        if iterator_text in empty_iterators:
            self.__unreachable_nodes.append(body)

        if iterator_text in self.__variable_values:
            if self.__variable_values.get(iterator_text) in empty_iterators:
                self.__unreachable_nodes.append(body)

        # Manually add iterator as block
        for_cfg = ControlFlowGraph()
        index = for_cfg.add_node(ExpressionBlock())
        for_cfg.exits = {index}
        for_cfg.last_block.add_expression(iterator)
        for_cfg.last_block.add_expression(element)

        body_cfg = self.__traverse_tree(body)

        for_cfg.merge_cfg(body_cfg)

        for exit in for_cfg.exits:
            for_cfg.add_edge(exit, for_cfg.entrance)

        for_cfg.exits = {for_cfg.entrance}

        self.__handle_continue(for_cfg)
        self.__continue_stack.pop()
        self.__handle_break(for_cfg)
        self.__break_stack.pop()

        self.plot(for_cfg, "for")

        return for_cfg

    def __handle_return(self, cfg):
        """
        Processes return statements in the CFG

        Args:
            cfg (ControlFlowGraph): The current CFG
        """
        for return_node in self.__returns:
            index = cfg.get_block_index(return_node)
            # Mark the current return statement as an exit point for the CFG and delete any forward edges
            cfg.exits.add(index)
            cfg.delete_forward_neighbors(index)

    def __handle_continue(self, cfg):
        """
        Processes continue statements in the CFG

        Args:
            cfg (ControlFlowGraph): The current CFG
        """
        for continue_statement in self.__continue_stack[-1]:
            index = cfg.get_block_index(continue_statement)
            # Remove all edges which ensures that no other statements in the loop CFG is evaluated
            cfg.delete_forward_neighbors(index)
            # Make the next edge the entrance of the loop, resetting the current position to the start
            cfg.add_edge(cfg.get_block_index(continue_statement), cfg.entrance)

    def __handle_break(self, cfg):
        """
        Processes break statements in the CFG

        Args:
            cfg (ControlFlowGraph): The current CFG
        """
        for break_statement in self.__break_stack[-1]:
            index = cfg.get_block_index(break_statement)
            # Marks the current break statement as a valid exit point for the CFG and delete any forward edges
            cfg.exits.add(index)
            cfg.delete_forward_neighbors(index)

    def __safe_eval(self, source, globals, locals):
        """
        Wraps a call to eval within a try-except block, to prevent errors
        with out of scope functions and variables.
        """
        try:
            return eval(source, globals, locals)
        except:
            print("Error with eval function on condition, assuming some reachability")
            return False

    def build_cfg(self):
        """
        Builds the control flow graph for the entire source code

        Returns:
            ControlFlowGraph: The CFG for the source code
        """
        full_cfg = self.__traverse_tree(self.__tree.root_node)

        self.__handle_return(full_cfg)

        return full_cfg

    def __traverse_tree(self, root_node):
        """Evaluates the current node in the tree

        Args:
            root_node: Current expression/node in the tree

        Returns:
            ControlFlowGraph: The control flow graph for the subtree rooted at the given node
        """
        cfg = ControlFlowGraph()

        # If root_node is as low-level as possible (atomic), we're finished recurring
        if root_node.type in ATOMIC_EXPRESSIONS:

            cfg.last_block.add_expression(root_node)

            # Special types of atomic expressions which impact control flow
            if root_node.type == "return_statement":
                self.__returns.add(cfg.last_block)
            elif root_node.type == "continue_statement":
                try:
                    self.__continue_stack[-1].add(cfg.last_block)
                except IndexError:
                    raise Exception("Invalid Code: continue called outside loop")
            elif root_node.type == "break_statement":
                try:
                    self.__break_stack[-1].add(cfg.last_block)
                except IndexError:
                    raise Exception("Invalid Code: break called outside loop")

            return cfg

        control_flow_change = (
            False  # Cause blocks after control flow change to be seperated
        )
        jump_change = False  # Cause nodes after jumps to be marked as unreachable and not included in the CFG

        # for linking adjacent nodes w/ 'and'
        prev_node_index = None 
        
        for node in root_node.children:
            self.__mark_variables(node)
            # Handle code which appears after a jump statement
            if jump_change:
                self.__unreachable_nodes.append(node)
                continue

            if node.type in self.__control_flow_handlers:
                sub_cfg = self.__control_flow_handlers.get(node.type)(node)

                if node.type == "if_statement" and not control_flow_change:
                    cfg.merge_cfg_and_last_block(sub_cfg)
                else:
                    cfg.merge_cfg(sub_cfg)

                control_flow_change = True

            # Add atomic expressions to existing block, or create new one if control flow change
            elif node.type in ATOMIC_EXPRESSIONS:
                # Manually create a new block so expression isn't mixed with existing control flow CFG
                if control_flow_change:
                    index = cfg.add_node(ExpressionBlock())

                    for exit in cfg.exits:
                        cfg.add_edge(exit, index)

                    cfg.exits = {index}

                cfg.last_block.add_expression(node)

                control_flow_change = False

                # Special types of atomic expressions which impact control flow
                if node.type in JUMP_EXPRESSIONS:
                    if node.type == "return_statement":
                        self.__returns.add(cfg.last_block)
                    elif node.type == "continue_statement":
                        try:
                            self.__continue_stack[-1].add(cfg.last_block)
                        except IndexError:
                            raise Exception("Invalid Code: continue called outside loop")
                    elif node.type == "break_statement":
                        try:
                            self.__break_stack[-1].add(cfg.last_block)
                        except IndexError:
                            raise Exception("Invalid Code: break called outside loop")

                    jump_change = True

                # for linking nodes with 'and' to help adjacency issues 
                prev_node_index = cfg.get_block_index(cfg.last_block)

            elif node.type == "and" or node.type == "AND":

                # New block for 'and' + expression (e.g. block = and \n x < 3)
                and_block = ExpressionBlock() 
                and_block.add_expression(node) 
                and_block_index = cfg.add_node(and_block)

                # connects previous node to 'and' block (for adjacency)
                if prev_node_index is not None:
                    cfg.add_edge(prev_node_index, and_block_index)
                
                # create link to blocks 
                for exit in cfg.exits: 
                    cfg.add_edge(exit, and_block_index) 
                
                # update exits to include block 
                cfg.exits = {and_block_index} 

                prev_node_index = and_block_index
                control_flow_change = False

            else:
                print(f"Unhandled node type: {node.type}")

        return cfg

    def plot(self, cfg, type):
        """Plots a graph representing the CFG

        Args:
            cfg: Control Flow Graph
            type: Type of graph to output

        Returns:
            edge_list (list): List of edges
        """
        G = nx.DiGraph()

        # newly created expression blocks will have edge colorings corresponding to the most recent control flow indicator
        # AKA the control flow indicator passed to the plot function as the type variable

        if type == "if":
            edge_color = "red"
        elif type == "while":
            edge_color = "green"
        elif type == "for":
            edge_color = "blue"
        else:
            edge_color = "black"

        for i in range(len(cfg)):

            # if expression block contains default values, assign values to expression block

            if cfg.blocks[i].get_color() == "none":
                cfg.blocks[i].set_color(edge_color)
            if cfg.blocks[i].get_iteration() == 0:
                cfg.blocks[i].set_iteration(self.__counter)

            # label = source code within expression block (what the node says)
            # color = color dictated by the control flow indicator passed into the function
            # order = value of counter when expression block is created (important for edge coloring precedence)

            G.add_node(
                i,
                label=cfg.blocks[i],
                color=cfg.blocks[i].get_color(),
                order=cfg.blocks[i].get_iteration(),
            )

        self.__counter += 1

        ids = nx.get_node_attributes(G, 'id')

        for node_id in ids.items():
            self.__seenNodes.update(node_id)

        if type == "cfg":

            edge_list = []

            G.add_edges_from(cfg.edge_list)

            plt.figure(figsize=(len(G) * 2, len(G) * 2))

            # Forces the graph into a tree shape (for demo purposes)
            pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

            labels = nx.get_node_attributes(G, "label")

            for node, label in labels.items():
                plt.text(
                    pos[node][0],
                    pos[node][1],
                    label,
                    ha="center",
                    va="center",
                    bbox=dict(facecolor="white", edgecolor="black", boxstyle="round"),
                )

            if not G.edges:
                nx.draw(G, pos)
            else:
                for edge in G.edges:

                    # if a more recent node points to an older node, use the color of the more recent node to color the edge
                    # else an older node points to a newer node, so use the color of the more recent node to color the edge

                    if G.nodes[edge[0]]["order"] >= G.nodes[edge[1]]["order"]:
                        edge_color = G.nodes[edge[0]]["color"]
                    else:
                        edge_color = G.nodes[edge[1]]["color"]
                    edge_list.append([edge, edge_color])
                    nx.draw_networkx_edges(
                        G,
                        pos,
                        edgelist=[edge],
                        arrows=True,
                        edge_color=edge_color,
                        arrowsize=50,
                        node_size=1000,
                        node_shape="s",
                    )

            plt.axis("off")
            plt.show()

            return edge_list
