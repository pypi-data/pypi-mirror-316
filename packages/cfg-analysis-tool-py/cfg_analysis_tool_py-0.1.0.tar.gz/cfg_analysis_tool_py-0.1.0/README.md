# CSCI 435 Control Flow Graph Analysis Tool

## Installation

### Pypi
```sh
pip install cfg-analysis-tool-py
```

## Library Usage

### Importing

The analysis tool has 3 modules: analyzer, cfg, and cfg_builder. To use these modules, import them from the cfg_analysis_tool_py package
```sh
import cfg_analysis_tool_py.analyzer
import cfg_analysis_tool_py.cfg
import cfg_analysis_tool_py.cfg_builder
```
This focuses on the analyzer module, but documentation for cfg and cfg_builder can be found here: [CFG Documentation](https://docs.google.com/document/d/1w3uWruvjMnaIv3f6g6Ioawa1yeD4k75b2gcN4uX3MCs/edit?usp=sharing)

The analyzer module contains the class CodeAnalyzer, as well as 2 helper methods: print_nodes and get_start. These can be used from analyzer, or imported as such:
```sh
from cfg_analysis_tool_py.analyzer import CodeAnalyzer, print_nodes, get_start
```

### Code Analyzer
Code Anlayzer is the main class in the library, containing the main 4 analysis methods.

#### General Limitations
- Static Analysis
  -> It is difficult to accurately assess the state of our program at each code execution path
  -> Cannot analyze function calls or data structure behavior
  -> Cannot simulate behavior of imported packages
- Input Format
  -> User input is limited to code snippets rather than entire functions or programs

#### Initialization
To initialize the class, it takes source code byte encoded as utf8 as its input, as such:
```sh
from cfg_analysis_tool_py.analyzer import CodeAnalyzer

source_code = bytes(
    """
    a = 10
    b = 5
    print(a + b)
""",
    "utf8",
)

code_analyzer = CodeAnalyzer(source_code)
```

#### Control Flow Graph
Upon initilization, the CodeAnalyzer class will generate a control flow graph object using cfg_builder.py. This CFG can be accessed with the method get_cfg:
```sh
code_analyzer = CodeAnalyzer(source_code)

cfg = code_analyzer.get_cfg()
```

### Analysis Methods
The 4 main analysis methods in CodeAnalyzer include:
- get_unreachable_definitions
- get_unused_variables
- get_dead_code
- get_very_busy_expressions
<a/>
Each of these methods return a list of tree-sitter.Node objects, each node representing a line or block of the source code identified by the analysis methods.

#### Unreachable Definitions
Unreachable definitions Identifies section of code that cannot be reached on any execution path, such as code following a return, break, or continue statement, or condition statements hardcoded to false. This method can be used as such:
```sh
code_analyzer = CodeAnalyzer(source_code)
unreachable_definitions = code_analyzer.get_unreachable_definitions()
```

#### Unused Variables
Unused variables identifies variable definitions that are never used in the program, including ones that are always redefined before they are used. This method can be used as such:
```sh
code_analyzer = CodeAnalyzer(source_code)
unused_variables = code_analyzer.get_unused_variables()
```

#### Dead Code
Identifies code that does not contribute to the program, including all code identified by unreachable definitions and unused variables, as well as expressions in the code that are not assigned to variables. This method can be used as such:
```sh
code_analyzer = CodeAnalyzer(source_code)
dead_code = code_analyzer.get_dead_code()
```

#### Very Busy Expression
Identifies expressions in the code that are always repeated or called on all paths before the values of any of their variables change. This method can be used as such:
```sh
code_analyzer = CodeAnalyzer(source_code)
very_busy_expressions = code_analyzer.get_very_busy_expressions()
```

### Helper Methods

#### print_nodes
This method is availiable to help visualize the nodes returned by the analysis methods in CodeAnalyzer. It takes in a list of tree-sitter.Node objects, and optionally, a string that it will print before the nodes. For each node in the list, it will print the node's line number, the node's code, and the node itself.
```sh
code_analyzer = CodeAnalyzer(source_code)
dead_code = code_analyzer.get_dead_code()
print_nodes(dead_code, "Dead Code")
```

#### get_start
This method gets the starting point of an individual tree-sitter.Node object. It returns a tuple in which the first entry is the line number, and the second entry is position in the line.
```sh
code_analyzer = CodeAnalyzer(source_code)
dead_code = code_analyzer.get_dead_code()
start = get_start(dead_code[1])
```

### Examples

#### Unreachable Definitions

##### Code:
```sh
from cfg_analysis_tool_py.analyzer import CodeAnalyzer, print_nodes

source_code = bytes(
    """
    a = 10
    if a == 10:
        print(a)
    elif a == 5:
        c = 9
    else:
        print("Hello World")
    b = a + 6
    return b
    print(a + b)
""",
"utf8",
)

code_analyzer = CodeAnalyzer(source_code)
unreachable_definitions = code_analyzer.get_unreachable_definitions()
print_nodes(unreachable_definitions, "Unreachable Definitions")
```

##### Output:
```sh
Unreachable Definitions
Line 4   |  elif a == 5:                                       <Node type=elif_clause, start_point=(4, 4), end_point=(5, 13)>
                c = 9
Line 6   |  else:                                              <Node type=else_clause, start_point=(6, 4), end_point=(7, 28)>
                print("Hello World")
Line 10  |  print(a + b)                                       <Node type=expression_statement, start_point=(10, 4), end_point=(10, 16)>
```

#### Unused Variables

##### Code:
```sh
from cfg_analysis_tool_py.analyzer import CodeAnalyzer, print_nodes

source_code = bytes(
    """
    a = 10
    a += 5
    b = a + 9
    c = a + 10
    return a + c
""",
"utf8",
)

code_analyzer = CodeAnalyzer(source_code)
unused_variables = code_analyzer.get_unused_variables()
print_nodes(unused_variables, "Unused Variables")
```

##### Output:
```sh
Unused Variables
Line 1   |  a = 10                                             <Node type=expression_statement, start_point=(1, 4), end_point=(1, 10)>
Line 3   |  b = a + 9                                          <Node type=expression_statement, start_point=(3, 4), end_point=(3, 13)>
```

#### Dead Code

##### Code:
```sh
from cfg_analysis_tool_py.analyzer import CodeAnalyzer, print_nodes

source_code = bytes(
    """
    a = 10
    if a == 10:
        b = 9
        c = 10
        a + b
    else:
        c = 11
        return c
""",
"utf8",
)

code_analyzer = CodeAnalyzer(source_code)
dead_code = code_analyzer.get_dead_code()
print_nodes(dead_code, "Dead Code")
```

##### Output:
```sh
Dead Code
Line 4   |  c = 10                                             <Node type=expression_statement, start_point=(4, 8), end_point=(4, 14)>
Line 5   |  a + b                                              <Node type=expression_statement, start_point=(5, 8), end_point=(5, 13)>
Line 6   |  else:                                              <Node type=else_clause, start_point=(6, 4), end_point=(8, 16)>
                c = 11
                return c
```

#### Very Busy Expressions

##### Code:
```sh
from cfg_analysis_tool_py.analyzer import CodeAnalyzer, print_nodes

source_code = bytes(
    """
    a = 10
    b = 20
    print(a + b)
    c = a + b
    if a == 10:
        print(c - a)
        a = 9
        print(c - a)
    else:
        print(c - a)
""",
"utf8",
)

code_analyzer = CodeAnalyzer(source_code)
very_busy_expressions = code_analyzer.get_very_busy_expressions()
print_nodes(very_busy_expressions, "Very Busy Expressions")
```

##### Output:
```sh
Very Busy Expressions
Line 3   |  print(a + b)                                       <Node type=expression_statement, start_point=(3, 4), end_point=(3, 16)>
Line 4   |  c = a + b                                          <Node type=expression_statement, start_point=(4, 4), end_point=(4, 13)>
Line 6   |  print(c - a)                                       <Node type=expression_statement, start_point=(6, 8), end_point=(6, 20)>
Line 10  |  print(c - a)                                       <Node type=expression_statement, start_point=(10, 8), end_point=(10, 20)>
```

## Limitations of the Library

### Format of Input
This library is designed to analyze Python code. The inputted code should be code snippets, rather than entire functions or programs. Below are examples of invalid and valid input for the library's analysis functions.

#### Invalid Input
```sh
def example_function(a, b):
  c = a + b
  d = 12
  return c
```
This example is invalid because it includes the function definition.
#### Valid Input
```sh
a = 1
b = 2
c = a + b
d = 12
return c
```
This example is valid because it is just the code that would be found within a function, and does not include the function definition.

Because of the required input format for the library's analysis functions, calls to other function within the inputted code snippets are not within the scope of our analysis.

### Static Analysis
This library is deisgned to be a static analysis tool, so there are some more dynamic cases that are out of the scope of our analysis.

For example, the code snippet below would be valid input, but the analysis of this could would not be as complete as that of a more static code snippet because of the changes the the value of the variable a within the while loop.

```sh
a = 1
while (a < 5):
  if a == 4:
    print(a)
  a += 1
```
Due to the nature of static analyis tools, our library cannot handle and analyze external dependencies, such as library calls or user input.

### Limitations Specific to Each Type of Analysis
#### Unused Variables
We have not identified any limitations specific to the analysis of unused variables, but the same limitations mentioned above still apply to this form of analysis.

#### Unreachable Definitions
Due to the constraints of static analysis, our identification of unreachable definitions does not account for changes to variables that happen within iterations of a loop, other than the first iteration. This means that the identification of lines of code within a loop is determined based on the values of variables at the time of the first iteration of the loop.

For example, in the analysis of the code snippet below, the line 'print(a)' would be identified as an unreachable definition, even though after 10 iterations of the loop, this line would be reached. On the first iteration though, it is unreached.

```sh
a = 1
b = 2
while True:
  if a == 10:
    print(a)
  else:
    print(b)
  a += 1
```

#### Very Busy Expressions
For our analysis of very busy expressions, expressions are considered very busy if they are repeated and each instance is exactly the same, other than any difference in whitespace.

For example, in our analysis, 'a + b' and 'b + a' would not be considered as the same expressions, because the order of 'a' and 'b' is swapped.

In regards to whitespace, 'a + b' and 'a+b' would be considered as the same expression, despite the difference in spacing.

Lastly, it is important to note that 'a + b' and 'a + b + c' would not be condisered busy together in our analysis, despita 'a + b' being part of both expressions.

#### Dead Code
Our dead code analysis function inherits functionality from the other analysis functions, and thus inherits the same limitations.
