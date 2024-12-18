from .cfg_builder import CFGBuilder
from .path import Path
from collections import defaultdict
import re

def print_nodes(node_list, title = ""):
    print(title)
    for node in node_list:
        text = node.text.decode("utf8").splitlines()
        print("Line %-4s| " % node.start_point[0], "%-50s" % text[0])
        for line in text[1:]:
            print("               ", "%-50s" % line.strip())

def get_start(node):
    return node.start_point

class CodeAnalyzer:
    """
    Class of functions used to analyze source code
    """
    def __init__(self, source_code=None):
        """
        Instantiates the CFGAnalyzer class

        Args:
            source_code (multi-line str): Python source code represented in string format
        """
        self.__cfg_builder = CFGBuilder(source_code)
        self.__cfg = self.__cfg_builder.build_cfg()
        self.__paths = set()
        self.__path_indices = []
        self.__analyze_paths()

        self.__very_busy_expressions = []


    def get_cfg(self):
        """
        Gets the CFG built from the source code

        Returns:
            ControlFlowGraph: ControlFlowGraph object representation of the source_code
        """
        return self.__cfg

    def get_paths(self):
        return self.__path_indices

    def __find_paths(self, cfg):
        """Get all possible code execution paths for the given CFG

        Args:
            cfg (ControlFlowGraph): ControlFlowGraph to evaulate

        Returns:
            paths (list): List of possible CFG traversals represented
                          by indices corresponding to ExpressionBlock objects
        """
        edge_list = set(cfg.edge_list)
        exits = set(cfg.exits)
        paths = []
        # Base case where code does not branch. Simply append the 0th index
        if not edge_list and exits:
           paths.append([0])

        def dfs(block_index, path, visited_edges):
            """Recursive traverse edges until an exit node is found

            Args:
                block_index (int): Represents index of an ExpressionBlock
                path (list): Represents the current path
                visited_edges (list): List of visited edges
            """
            path.append(block_index)
            # If we've reached an exit node, store the path
            if block_index in exits:
                paths.append(list(path))
            for (src, dest) in edge_list:
                if src == block_index and (src, dest) not in visited_edges:
                    # Mark this edge as used in the current path
                    visited_edges.add((src, dest))
                    dfs(dest, path, visited_edges)
                    # Backtrack by removing the edge from visited_edges
                    visited_edges.remove((src, dest))

            # Backtrack by removing the node from the path
            path.pop()

        for edge in edge_list:
            if edge[0] == 0: # Find a code execution path starting from block 0
                dfs(edge[1], [0], set())

        return paths

    def __analyze_paths(self):
        """Instantiates a new Path object for each code execution path
           Then evaluates the path block by block
        """
        paths = self.__find_paths(self.__cfg)
        self.__path_indices = paths

        for i in range(len(paths)):
            cur_path = Path(i)
            self.__paths.add(cur_path)
            for index in paths[i]:
                block = self.__cfg.get_block(index)
                cur_path.add_block(block, index)
                #cur_path.evaluate(block, index)

    def get_unused_variables(self):
        """
        Gets a list of unused variables

        Returns:
            list: List of unused variables
        """

        all_variables = []
        used_variables = []

        for path in self.__paths:
            loop_blocks = {} #Dict of loop blocks, each entry has format:
                            #[[list of blocks in loop], [set of variables assigned before usage], [variables unused at end of loop], [set of variables used]]

            #Get all block indicies inside a loop, store in dict under loop block
            for block in path.path:
                if path.path.count(block) > 1:
                    loop_blocks[block] = []

                    block_index_1 = path.path.index(block)
                    block_index_2 = path.path[block_index_1+1:].index(block) + block_index_1 + 1
                    loop_blocks[block].append(path.path[block_index_1:block_index_2])
                    loop_blocks[block].append(set())
                    loop_blocks[block].append([])
                    loop_blocks[block].append(set())

            #Get data from Path
            variable_assignments = path.variable_assignments
            assignments_length = len(variable_assignments)
            variable_usage = path.variable_usage
            usage_length = len(variable_usage)

            next_assignment = 0
            next_usage = 0

            active_assignments = []

            while(True):
                #Handle all variable assignments and usages
                if next_assignment == assignments_length and next_usage == usage_length:
                    break
                elif next_assignment == assignments_length:
                    handling_assignment = False
                elif next_usage == usage_length:
                    handling_assignment = True
                else:
                    if variable_usage[next_usage][0].start_point <= variable_assignments[next_assignment][0].start_point:
                        handling_assignment = False
                    else:
                        handling_assignment = True

                if handling_assignment:
                    current_assignment = variable_assignments[next_assignment]

                    #Adds all variable assignments to all_variables
                    if current_assignment not in all_variables:
                        all_variables.append(current_assignment)

                    # If a previous variable assignment assigns the same variable, current assignment overwrites it as active
                    for assignment in active_assignments:
                        if assignment[2] == current_assignment[2]:
                            active_assignments.remove(assignment)
                            break
                    active_assignments.append(current_assignment)

                    #Handle Looping, if the current assignment is in a loop, adds relevant info to the loop dictionary entry
                    for loop in loop_blocks.keys():
                        if current_assignment[1] in loop_blocks[loop][0]:
                            loop_blocks[loop][2].append(current_assignment)
                            if current_assignment[2] not in loop_blocks[loop][3]:
                                loop_blocks[loop][1].add(current_assignment[2])

                    next_assignment += 1

                else:
                    current_usage = variable_usage[next_usage]

                    #Any active assignments are deactivated if their variable is used
                    assignments_to_remove = []
                    for assignment in active_assignments:
                        if assignment[2] in current_usage[2]:
                            used_variables.append(assignment)
                            assignments_to_remove.append(assignment)
                    for assignment in assignments_to_remove:
                        active_assignments.remove(assignment)
                    next_usage += 1

                    #Handle Looping, if used variables are in a loop, add info to loop dict entry
                    for loop in loop_blocks.keys():
                        if current_usage[1] in loop_blocks[loop][0]:
                            for var in current_usage[2]:
                                loop_blocks[loop][3].add(var)

            #Handle Looping, if a variable assinment is active at the end of a loop, is used in the loop,
            #  and not redefined at the beginning of the loop, it is considered used.
            for loop in loop_blocks.keys():
                for active_assignment in loop_blocks[loop][2]:
                    if active_assignment[2] in loop_blocks[loop][3] and active_assignment[2] not in loop_blocks[loop][1]:
                        used_variables.append(active_assignment)

        # Any variable not used are unused
        unused_variables = []
        for variable in all_variables:
            if variable not in used_variables and variable[0] not in unused_variables:
                unused_variables.append(variable[0])

        unused_variables.sort(key=get_start)
        return unused_variables

    def get_unreachable_definitions(self):
        """
        Gets a list of unreached

        Returns:
            list: List of unreached definitions
        """

        unreachable_definitions = []

        def handle_returns_within_always_true_conditions(condition):
            #getting the consequence of this condition

            for if_and_consequence_pair in self.__cfg_builder.condition_and_consequence_nodes:
                if condition == if_and_consequence_pair[0]:
                    consequence = if_and_consequence_pair[-1]

            #checking for return statements in the consequence of this always true condition
            returns_in_always_true_block = False
            for node in consequence.children:
                if node.type == "return_statement":
                    returns_in_always_true_block = True

            if returns_in_always_true_block:
                node = condition.parent
                while node.parent is not None:
                    while node.next_sibling is not None:
                        unreachable_definitions.append(node.next_sibling)
                        node = node.next_sibling
                    node = node.parent

            return

        def handle_repeated_nodes(old_list):
            new_list = []
            nodes_to_remove = []

            #iterating through all the nodes that have been added to unreachable definitions
            for node in old_list:
                #checking to see if exact node is already in the new list
                if node not in new_list:
                    new_list.append(node)

            for node in new_list:
                start_line = node.start_point[0]
                end_line = node.end_point[0]

                for other_node in new_list:
                    if other_node != node:
                        if other_node.start_point[0] >= start_line and other_node.end_point[0] <= end_line:
                            nodes_to_remove.append(other_node)

            new_list = [node for node in new_list if node not in nodes_to_remove]
            return new_list

        #adding previous groups implementation of unreachable nodes - covers broad control flow
        #also accounts for trying to iterate through something empty - this analysis is done in cfg_builder
        for i in self.__cfg_builder.unreachable_nodes:
            unreachable_definitions.append(i)

        #looping through sets of conditionalss
        for condition_set in self.__cfg_builder.conditional_nodes:
            others_are_unreached = False
            for condition in condition_set:
                #see if a different condition was already found to be always true, and thus the other conditions and their consequences will be unreached
                if others_are_unreached == True:
                    unreachable_definitions.append(condition)

                #if a condition that will always be true has not yet been found, check if this condition is always true
                else :

                    #if this is the last condition, and no conditions have been found to be true, then else would be reached
                    if (condition.type == "else_clause"):

                        #checking if there is a return in this clause and addressing it
                        returns_in_always_true_block = False
                        for node in condition.child_by_field_name("body").children:
                            if node.type == "return_statement":
                                returns_in_always_true_block = True

                        if returns_in_always_true_block:
                            node = condition.parent
                            while node.parent is not None:
                                while node.next_sibling is not None:
                                    unreachable_definitions.append(node.next_sibling)
                                    node = node.next_sibling
                                node = node.parent

                        #otherwise exit - nothing else will be unreachable
                        break

                    #checking if the condition is always true
                    elif condition in self.__cfg_builder.always_true_nodes:
                        others_are_unreached = True

                    #if the condition is not always true
                    else:
                        #if this is an if or elif statement, need to add the consequence to unreached definitions
                        for if_and_consequence_pair in self.__cfg_builder.condition_and_consequence_nodes:
                            if condition == if_and_consequence_pair[0]:
                                unreachable_definitions.append(if_and_consequence_pair[-1])
                                break

        for while_condition in self.__cfg_builder.while_nodes:
            #checking if the condition is not true
            if while_condition not in self.__cfg_builder.always_true_nodes:
                for condition_and_consequence_pair in self.__cfg_builder.condition_and_consequence_nodes:
                    if while_condition == condition_and_consequence_pair[0]:
                            unreachable_definitions.append(condition_and_consequence_pair[-1])
                            break


        #find the conditions that are not in unreachable_definitions
        not_unreachable = []
        for condition_set in self.__cfg_builder.while_and_conditions:
            for condition in condition_set:
                #making sure the exact node isn't already in unreachable definitions
                if condition not in unreachable_definitions:
                    for node in unreachable_definitions:
                        if condition.start_point[0] >= node.start_point[0] and condition.end_point[0] <= node.end_point[0]:
                            continue
                        else:
                            not_unreachable.append(condition)

        for condition in not_unreachable:
            if condition in self.__cfg_builder.always_true_nodes and condition.type != "else_clause":
                handle_returns_within_always_true_conditions(condition)

        unreachable_definitions = handle_repeated_nodes(unreachable_definitions)
        unreachable_definitions.sort(key=lambda node: node.start_point[0])
        return unreachable_definitions


    def get_dead_code(self):
        def already_marked(node, dead_code):
            node_marked = node in dead_code
            node_marked = node_marked or node.text in [dc.text for dc in dead_code]
            return node_marked
    
        # Combine with unused variables and unreachable definitions
        dead_code = self.get_unused_variables()
        dead_code.extend(ud for ud in self.get_unreachable_definitions() if not already_marked(ud, dead_code))

        floating_expressions = []

        for path in self.__paths:

            variable_assignments = [node[0] for node in path.variable_assignments]
            variable_usage = [node[0] for node in path.variable_usage]
            expressions = [node[0] for node in path.expressions]

            # Floating expressions: expressions that aren't assigned or used in anything
            # Expressions that don't use variables
            floating_expressions.extend([node for node in expressions
                                         if node not in floating_expressions and
                                         node.type == "expression_statement" and
                                         b"print(" not in node.text and
                                         node not in variable_assignments + variable_usage])
            # Expressions in variable usage of type expression_statement that don't have =
            floating_expressions.extend([node for node in variable_usage
                                         if node not in floating_expressions and
                                         node.type == "expression_statement" and
                                         b"print(" not in node.text and
                                         b"=" not in node.text])
            # Special case: expressions with == that aren't comparison operators
            floating_expressions.extend([node for node in variable_usage
                                         if node not in floating_expressions and
                                         b"==" in node.text and
                                         node.type != "comparison_operator"])

            floating_expressions = sorted(floating_expressions, key=lambda n: n.start_point[0])

        for node in floating_expressions:
            if node not in dead_code:
                dead_code.append(node)
        dead_code.sort(key=get_start)

        return dead_code

    def __analyze_busy_expressions_in_block(self, path, block_index):
        """
        Gets expression information related to busy expressions analysis for a block

        Args:
            path (Path): Path containing the relevant block and information, needed for the expression information stored upon path creation
            block_index: int representing the block being analyzed
        Returns:
            tuple: (unchanged_expressions, active_expressions, changed_variables)
                unchanged_expressions: List of expressions that are called before their variables change values
                active_expressions: List of expressions that are called in the block and whose values do not change before the block exits
                changed_variables: Set of variables that are changed in the block
        """
        #Get all expressions and assignments from current block being analyzed
        block_expressions, block_assignments = [], []
        for expression in path.expressions:
            if expression[1] == block_index:
                block_expressions.append(expression)
                #print(expression)
        for assignment in path.variable_assignments:
            if assignment[1] == block_index:
                block_assignments.append(assignment)

        #analyze expressions and variables
        changed_variables = set()
        unchanged_expressions = []
        active_expressions = []
        expression_index, assignment_index = 0, 0
        for i in range(len(block_expressions) + len(block_assignments)):

            #Gets information on next assignment and next expressions. If there are none left, sets to None
            if expression_index < len(block_expressions):
                current_expression = block_expressions[expression_index]
                #print(current_expression)
            else:
                current_expression = None
            if assignment_index < len(block_assignments):
                current_assignment = block_assignments[assignment_index]
            else:
                current_assignment = None

            #If there are no more assignments or the next expression comes before the next assignment, mark expression as active
            if not current_assignment or (current_expression and current_expression[0].start_point <= current_assignment[0].start_point):
                #Check and see if expression is active, if so, add both to very busy expressions
                busy = False
                for expression in active_expressions:
                    if expression[2] == current_expression[2] and expression != current_expression:
                        if expression not in self.__very_busy_expressions:
                            self.__very_busy_expressions.append(expression)
                        busy = True
                if busy and current_expression not in self.__very_busy_expressions:
                    self.__very_busy_expressions.append(current_expression)

                active_expressions.append(current_expression)
                #If the expression does not contain any variables changed in the block, mark the expression as unchanged
                if not set(current_expression[3]).intersection(changed_variables):
                    unchanged_expressions.append(current_expression)
                expression_index += 1
            else:
                #If variable assignment, check all active expressions to see if they contain the changed variable, deactivate expression if changed
                remove_expression = []
                for expression in active_expressions:
                    if current_assignment[2] in expression[3]:
                        remove_expression.append(expression)
                for expression in remove_expression:
                    active_expressions.remove(expression)
                changed_variables.add(current_assignment[2])
                assignment_index += 1

        return unchanged_expressions, active_expressions, changed_variables

    def __search_for_busy_expressions(self, paths, current_block_index = 0, current_depth = 0, loop_blocks = []):
        """
        Recursive function that searches through the various paths in self.__paths for nodes that contain very busy expressions,
        searches one block at a time, and recursively calls as the control flow splits. Merges the data as recursive calls return.

        Args:
            paths (set): set of Path objects to be searched and analyzed
            current_block_index: int describing the current block being analyzed
            current_depth: Index for the current block in the Path objects in paths
            loop_blocks: stack of block indicies indicating blocks where loops begin
        Returns:
            tuple: (unchanged_expressions, active_expressions, changed_variables)
                unchanged_expressions: List of expressions that are always called on all paths in paths before their variables change
                active_expressions: List of expressions that are always called on all paths in paths whose values do not change before the path or loop exits
                changed_variables: Set of variables that are changed on all paths in paths
        """
        current_path = next(iter(paths))

        #If loop block is reencounterd (full loop has occured), return
        if loop_blocks and current_block_index == loop_blocks[-1]:
            return ([],[],[])

        #Analyze the current block
        unchanged_expressions, active_expressions, changed_variables = self.__analyze_busy_expressions_in_block(current_path, current_block_index)

        #Split paths based on next block
        path_split_1, path_split_2 = set(), set()
        finished_paths = set()
        current_block_loops = False
        for path in paths:
            if current_depth >= len(path.path)-1:
                finished_paths.add(path)
                continue
            if current_block_index in path.path[current_depth+1:len(path.path)]:
                current_block_loops = True #current block is beginning of loop if, in some path, the block appears again
                loop_blocks.append(current_block_index)
            if(path.path[current_depth+1] == current_block_index+1):
                path_split_1.add(path)
            else:
                path_split_2.add(path)

        #Recursively analyze and merge data
        path_1_unchanged_expressions, path_1_active_expressions, path_1_changed_variables = [], [], set()
        path_2_unchanged_expressions, path_2_active_expressions, path_2_changed_variables = [], [], set()
        returned_unchanged_expressions, returned_active_expressions, returned_changed_variables = [], [], set()

        #Recursively Get information on expression usage from both split paths
        if path_split_1:
            path_1_data = self.__search_for_busy_expressions(path_split_1, current_block_index+1, current_depth+1, loop_blocks)
            path_1_unchanged_expressions, path_1_active_expressions, path_1_changed_variables = path_1_data
            if current_block_loops:
                #If current block is a loop point, consider all expressions within as very busy if their variables are not changed at all in the loop
                for unchanged in path_1_unchanged_expressions:
                    if unchanged in path_1_active_expressions and unchanged not in self.__very_busy_expressions and not set(unchanged[3]).intersection(path_1_changed_variables):
                        self.__very_busy_expressions.append(unchanged)
                loop_blocks.pop()
        if path_split_2:
            next_block_index = next(iter(path_split_2)).path[current_depth+1]
            path_2_data = self.__search_for_busy_expressions(path_split_2, next_block_index, current_depth+1, loop_blocks)
            path_2_unchanged_expressions, path_2_active_expressions, path_2_changed_variables = path_2_data

        #If both path have active blocks, merge the data
        if path_split_1 and path_split_2:
            paths_unchanged_expressions = []
            #If an expressions is guaranteed to be called in boths paths before changing, add to busy expressions and unchanged paths
            for expression_1 in path_1_unchanged_expressions:
                for expression_2 in path_2_unchanged_expressions:
                    if expression_1[2] == expression_2[2]:
                        if expression_1 not in self.__very_busy_expressions:
                            self.__very_busy_expressions.append(expression_1)
                        if expression_2 not in self.__very_busy_expressions:
                            self.__very_busy_expressions.append(expression_2)
                        if expression_1 not in paths_unchanged_expressions:
                            paths_unchanged_expressions.append(expression_1)
                        if expression_2 not in paths_unchanged_expressions:
                            paths_unchanged_expressions.append(expression_2)
        else:
            paths_unchanged_expressions = path_1_unchanged_expressions + path_2_unchanged_expressions
        paths_active_expressions = path_1_active_expressions + path_2_active_expressions
        paths_changed_variables = path_1_changed_variables.union(path_2_changed_variables)

        for unchanged in paths_unchanged_expressions:
            for active in active_expressions:
                #If an active expression matches an unchanged expressions across the paths, both are busy
                if unchanged[2] == active[2] and unchanged != active:
                    if active not in self.__very_busy_expressions:
                        self.__very_busy_expressions.append(active)
                    if unchanged not in self.__very_busy_expressions:
                        self.__very_busy_expressions.append(unchanged)

        #If an active or unchanged expression in the split paths is not modified in the current block, still considered active/unchanged
        for expression in paths_active_expressions:
            if not set(expression[3]).intersection(changed_variables):
                active_expressions.append(expression)
        for expression in paths_unchanged_expressions:
            if not set(expression[3]).intersection(changed_variables):
                unchanged_expressions.append(expression)
        changed_variables = changed_variables.union(paths_changed_variables)
        
        return (unchanged_expressions, active_expressions, changed_variables)


    def get_very_busy_expressions(self):
        """
        Gets a list of nodes that contain expressions that, from some point p,
        are called more than once or on every branching path before their variables change values

        Returns:
            list: List of tree-sitter nodes representing very busy expressions
        """
        analysis_paths = self.__paths

        self.__search_for_busy_expressions(analysis_paths, 0, 0, [])
        node_list = [expression[0] for expression in self.__very_busy_expressions]
        node_list.sort(key=get_start)
        return node_list
