import re
from collections import defaultdict

ASSIGNMENT_OPERATOR_MODIFIERS = r'(\+|-|\*|/|%|//|\*\*|&|\||\^|>>|<<|:)?'
VARIABLE_ASSIGNMENT_PATTERN = r'((\w+)(\s*,\s*\w+)*)\s*'+ASSIGNMENT_OPERATOR_MODIFIERS+r'=([^=]\s*(.*))'

EXPRESSION_OPERATORS = r'((\+|-|\*|/|%|\*\*|//|==|!=|>|<|>=|<=|&|\||\^|<<|>>)|(\s(is not|is|not in|in|and|or)\s))'
SINGULAR_OPERATORS = r'(~|(\snot\s))'
NUMBER_PATTERN = r'-?((\d+(\.\d*)?)|(\.\d+))'
TERM_PATTERN = fr'(\w+|{NUMBER_PATTERN})'
EXPRESSION_PATTERN = fr'(({TERM_PATTERN}\s*{EXPRESSION_OPERATORS})|{SINGULAR_OPERATORS})\s*{TERM_PATTERN}(?:\s*{EXPRESSION_OPERATORS}\s*{SINGULAR_OPERATORS}*\s*{TERM_PATTERN})*'

class Path:
    def __init__(self, index):
        """Represents a code execution path comprised of ExpressionBlocks

        Args:
            index (int): Index of path
        """
        self.__index = index
        self.__path = []            #List of block IDs for traversal
        self.__path_blocks = []     #List of blocks in the path
        self.__variable_names_defined = []

        self.__variable_assignments = []    #[tree-sitter.Node, block_index, variable assigned, value (str)]
        self.__expressions = []             #2-D list, each sublist has structure [tree-sitter.Node, block_index, expression (str), [list of vars in expression]]
        self.__variables_used = []          #2-D list, each sublist has structure [tree-sitter.Node, block_index, [list of variables used]]

    def __str__(self):
        blocks = []
        for block in self.__path:
            blocks.append(str(block) + "\n")
        return "".join(blocks) + "\n"

    @property
    def index(self):
        return self.__index

    @property
    def path(self):
        return self.__path

    @property
    def variable_assignments(self):
        # nodes, variables, values = [], [], []
        # variables_map = defaultdict(list)

        # for assignment in self.__variable_assignments:
        #     nodes.append(assignment[0])
        #     variables.append(assignment[2])
        #     values.append(assignment[3])
        #     variables_map[assignment[2]].append(assignment[0])

        return self.__variable_assignments
        # return (nodes, variables, values, variables_map)

    @property
    def expressions(self):
        # nodes, expressions = [], []
        # expressions_nodes_map = defaultdict(list)
        # expressions_map = defaultdict(list)
        # nodes_map = defaultdict(list)
        # for assignment in self.__expressions:
        #     nodes.append(assignment[0])
        #     expressions.append(assignment[2])
        #     # Map block to node
        #     expressions_nodes_map[assignment[4]].append(assignment[0])
        #     # Map block to expression
        #     expressions_map[assignment[4]].append(assignment[2])
        #     # Map expression to nodes
        #     nodes_map[assignment[2]].append(assignment[0])
        return self.__expressions
        # return (nodes, expressions, expressions_nodes_map, expressions_map, nodes_map)

    @property
    def variable_usage(self):
        # nodes, variables = [], []
        # for assignment in self.__variables_used:
        #     nodes.append(assignment[0])
        #     variables.append(assignment[1])
        return self.__variables_used
        # return (nodes, variables)

    def add_block(self, block, index):
        self.__path.append(index)
        self.__path_blocks.append(block)
        self.__evaluate(block, index)

    def __evaluate(self, block, block_index):
        """Get path attributes such as variables used

        Args:
            block (ExpressionBlock): Current ExpressionBlock on the path
        """
        for node in block.expressions:
            assignment_found = self.__find_assignments(node, block_index)
            #Only checks for variable usage if the node is not a variable assignment, otherwise, find_assignments handles this
            if not assignment_found:
                self.__find_variable_usage(node, block_index)
            expressions = self.__find_expression(node, block_index)
        # TODO, implement more helper functions to use the line by line analysis

    def __find_assignments(self, node, block_index):
        """Uses RegEx to match variable assignments and
           hashes to self.__variables

        Args:
            node (tree-sitter.Node): AST node representing line of code

        Returns:
            list: Variables used in the line
        """
        line = node.text.decode("utf8")
        match_found = False
        assignment_matches = re.finditer(VARIABLE_ASSIGNMENT_PATTERN, line)
        for match in assignment_matches:
            match_found = True
            # Left side of the assignment
            assigned_variables = list(map(lambda string: string.strip(), match.group(1).strip().split(",")))
            # Right side of the assignment
            value = match.group(5).strip()

            for variable in assigned_variables: #Multi-line assignments, add the node once for each assigned variable
                self.__variable_assignments.append([node, block_index, variable, value])
                if variable not in self.__variable_names_defined:
                    self.__variable_names_defined.append(variable)

            self.__find_variable_usage(node, block_index, value)

        return match_found

    def __find_expression(self, node, block_index):
        """Uses RegEx to match "variable operator variable" expressions

        Args:
            node (tree-sitter.Node): AST Node representing line of code

        Returns:
            list: list of expressions used
        """
        line = node.text.decode("utf8")
        expression_match = re.search(EXPRESSION_PATTERN, line)
        if expression_match:
            expression = expression_match.group(0)
            variables = self.__find_vars_in_string(expression)
            #print(expression)
            #print(variables)
            self.__expressions.append([node, block_index, expression.replace(" ",""), variables])
            return expression
        return None

    def __find_vars_in_string(self, line):
        variables_found = []

        # if len(self.__variable_names_defined) > 0:

        #     variables = '|'.join(self.__variable_names_defined)
        pattern = r'(?=(\W|^)([a-zA-Z_]\w*)(\W|$))'
        variable_usage_match = re.finditer(pattern, line)

        for match in variable_usage_match:
            variables_found.append(match.group(2).strip())

        return variables_found

    def __find_variable_usage(self, node, block_index, line = None):

        #line included such that subsets of a node can be analyzed for variable usage, can give string to be analyzed instead of node
        if line == None:
            line = node.text.decode("utf8")

        variables_found = self.__find_vars_in_string(line)

        if len(variables_found) > 0:
            self.__variables_used.append([node, block_index, variables_found])
