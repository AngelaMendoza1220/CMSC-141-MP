import re
variables = []
__printOutTheseValues = []


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

def reset_globals():
    global variables
    variables = []

def isKeyword(word):
    keywords = ["is", "int", "float", "string", "boolean", "char", "print","if","else","elif"]

    if word in keywords:
        return True
    else:
        return False
    
def isBoolean(word):
    keywords = ["TRUE", "FALSE"]

    if word in keywords:
        return True
    else:
        return False
    
def isCharacter(c):
    if len(c) == 3 and c[0] == "'" and c[1].isalpha() and c[2] == "'":
        return True
    else:
        return False
    
def isString(word):

    if word[0] == "\"" and word[len(word)-1] == "\"":
        return True
    else:
        return False
    
def isNumber(num):
    pattern = r'^[+-]?\d+(\.\d+)?$'

    if re.match(pattern, num):
        return True
    else:
        return False
    
def isVariableName(var):
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'

    if re.match(pattern, var):
        return True
    else:
        return False


def isMathOperators(c):
    arithmeticOperators = ["+", "-", "*", "/", "%", "^", "(", ")"]

    if c in arithmeticOperators:
        return True
    else:
        return False
    
def getMathOperator(c):
    if c == "+":
        return "add_operator"
    elif c == "-":
        return "minus_operator"
    elif c == "*":
        return "mult_operator"
    elif c == "/":
        return "div_operator"
    elif c == "%":
        return "mod_operator"
    elif c == "^":
        return "exponent"
    elif c == "(":
        return "open_par"
    elif c == ")":
        return "close_par"

def getNumericalDatatype(num):
    if isinstance(eval(num), int):
        return "int"
    else:
        return "float"

def printOut():
    return __printOutTheseValues

def clearPrintOut():
    __printOutTheseValues.clear()

def lexer(linesOfCode):

    tokens = []

    for line in linesOfCode:  # for every line in the code
        pos = 0
        while pos < len(line):  # for every character in the line
            temp = ""
            
            if line[pos].isdigit():                       # if the character is a digit, append all digits
                while pos < len(line) and (line[pos].isdigit() or line[pos] == "."): 
                    temp += line[pos]    
                    pos += 1
                if isNumber(temp):                        # if the number is valid, add as a token
                    tokens.append(Token(getNumericalDatatype(temp), temp)) 
                else:                                     # if number is invalid, print error
                    tokens.append(Token('ERROR', temp))
                    break
            elif line[pos].isalpha() or line[pos] == "_": 
                while pos < len(line) and (line[pos].isalpha() or line[pos] == "_"):
                    temp += line[pos]
                    pos += 1
                if isKeyword(temp):                       # if the word is a keyword, add as a token
                    tokens.append(Token('keyword', temp))  
                elif isBoolean(temp):                     # if the word is boolean, add as a token
                    tokens.append(Token('boolean', temp))
                elif isVariableName(temp):                # if the word is a valid variable name, add as a token
                    tokens.append(Token('variable', temp))
                else:                                     # if the word is invalid
                    tokens.append(Token('ERROR', temp))
                    break
            elif line[pos] == "'" or line[pos] == "\"":   # if a quotation mark is encountered, could be a char or string
                temp += line[pos]
                pos += 1
                while pos < len(line) and (line[pos] != "'" or line[pos] != "\""):
                    temp += line[pos]
                    pos += 1
                if isCharacter(temp):                     # if the word is a character, add as token
                    tokens.append(Token('char', temp[1]))
                elif isString(temp):                      # if the word is a string, add as token
                    tokens.append(Token('string', temp[1:-1]))  
                else:                                     # if it is invalid
                    tokens.append(Token('ERROR', temp))
                    break
            elif line[pos] == "=":                        # if =, append as token
                next_pos = pos + 1
                if next_pos < len(line) and line[next_pos] == "=":
                    tokens.append(Token('equalto', '=='))
                    pos += 2  # Move to the next position after ==
                else:
                    tokens.append(Token('equals', '='))  # Handle single '='
                    pos += 1
            elif line[pos] == "!":                        # if !, append as token
                next_pos = pos + 1
                if next_pos < len(line) and line[next_pos] == "=":
                    tokens.append(Token('notequalto', '!='))
                    pos += 2  # Move to the next position after !=
            elif line[pos] == "<":                        # if <, append as token
                next_pos = pos + 1
                if next_pos < len(line) and line[next_pos] == "=":
                    tokens.append(Token('lessthanorequalto', '<='))
                    pos += 2  # Move to the next position after <=
                else:
                    tokens.append(Token('lessthan', '<'))  # Handle single '<'
                    pos += 1
            elif line[pos] == ">":  
                next_pos = pos + 1                      # if >, append as token
                if next_pos < len(line) and line[next_pos] == "=":
                    tokens.append(Token('greaterthanorequalto', '>='))
                    pos += 2  # Move to the next position after >=
                else:
                    tokens.append(Token('greaterthan', '>'))  # Handle single '>'
                    pos += 1
            elif re.match(r'^ {4}', line[pos:]):  # Match exactly four spaces at the beginning of the line
                tokens.append(Token('indentation', '    '))
                pos += 4
            elif isMathOperators(line[pos]):              # if it is a math operator, determine the specific operator and add as token
                tokens.append(Token(getMathOperator(line[pos]), line[pos]))
                pos += 1
            elif line[pos] == " ":                        # move to the next position if space is encountered
                pos += 1
            else:                                         # anything else, its probably invalid
                tokens.append(Token('ERROR', temp))
                break
        tokens.append(Token('newline', '\n'))       
    return tokens

##############################################################################

start_index = 0
inner_index = 0
asscheck = 0
#set variables to None initially, then check 
def evaluate_tokens(tokens, start_index, asscheck):
    global variables 
    def apply_operator(operator, operand1, operand2):
        if operator == 'add_operator':
            return operand1 + operand2
        elif operator == 'minus_operator':
            return operand2 - operand1
        elif operator == 'mult_operator':
            return operand1 * operand2
        elif operator == 'div_operator':
            return operand1 / operand2
    #values for operator precedence
    def precedence(operator):
        if operator == '+' or operator == '-':
            return 1
        elif operator == '*' or operator == '/':
            return 2
        else:
            return 0
    #array to store variables
    #function to obtain the next token given a current index
    def get_next_token(current_index):
        if current_index < len(tokens) - 1:
            return tokens[current_index + 1]
        else:
            return None
        
    #function to obtain the previous token given a current index
    def get_prev_token(current_index):
        if current_index < len(tokens) - 1:
            return tokens[current_index - 1]
        else:
            return None
    #function to check whether or not the provided datatype is valid
    def validate_datatype(datatype):
        valid_datatypes = ['int', 'float', 'double', 'char', 'boolean']
        if datatype not in valid_datatypes:
            raise ValueError(f"Invalid datatype '{datatype}' in assignment statement.")

    #adjusting the value based on the datatype provided
    def validate_input_for_datatype(value, datatype):
        try:
            if datatype == 'int':
                int(value)
            elif datatype == 'float':
                float(value)
            elif datatype == 'double':
                float(value)  # You can customize this for double if needed
            elif datatype == 'char':
                str(value)
            elif datatype == 'boolean':
                if value.lower() not in ['true', 'false']:
                    raise ValueError(f"Invalid boolean value '{value}'.")
        except ValueError:
            raise ValueError(f"Invalid input '{value}' for datatype '{datatype}'.")
        
    def evaluate_condition(tokens, index):
      # Extract the operands and operator from the tokens
        operand1 = None
        operand2 = None
        operator = None
        tokenholder = ""
        token = tokens[index]
        for index in range(index, len(tokens)):
            token = tokens[index]
            nexttoken = get_next_token(index)
            if token.type == 'variable':
                for j in range(len(variables)):
                    if (token.value == variables[j][0]):
                        if operand1 is None:   
                            operand1 = int(variables[j][1])
                        else:
                            operand2 = int(variables[j][1])
                            break
            
            elif token.type == 'int':
                if operand1 is None:
                    operand1 = int(token.value)
                else:
                    operand2 = int(token.value)
                    break
            elif token.type == 'float':
                if operand1 is None:
                    operand1 = float(token.value)
                else:
                    operand2 = float(token.value)
                    break
            elif token.value == 'is' and nexttoken.type == 'equalto':
                if nexttoken.value == '==':
                    operator = nexttoken.value
            elif token.value == 'is' and nexttoken.type == 'notequalto':
                if nexttoken.value == '!=':
                    operator = nexttoken.value
            elif token.value == 'is' and nexttoken.type == 'lessthan':
                if nexttoken.value == '<':
                    operator = nexttoken.value
            elif token.value == 'is' and nexttoken.type == 'lessthanorequalto':
                if nexttoken.value == '<=':
                    operator = nexttoken.value
            elif token.value == 'is' and nexttoken.type == 'greaterthan':
                if nexttoken.value == '>':
                    operator = nexttoken.value
            elif token.value == 'is' and nexttoken.type == 'greaterthanorequalto':
                if nexttoken.value == '>=':
                    operator = nexttoken.value
            index += 1  
        # Evaluate the condition based on the operator
        if operator == '==':
            return [operand1 == operand2, index]
        elif operator == '!=':
            return [operand1 != operand2, index]
        elif operator == '>':
            return [operand1 > operand2, index]
        elif operator == '<':
            return [operand1 < operand2, index]
        elif operator == '>=':
            return [operand1 >= operand2, index]
        elif operator == '<=':
            return [operand1 <= operand2, index]
        else:
            # Handle other operators (>, <, !=, etc.) if needed
            raise ValueError(f"Unsupported operator: {operator}")
        
    def skip_code_block(tokens, start_index, current_block_type, other_block_type):
        index = start_index  # Initialize the index to the starting position
        block_depth = 0  # Initialize the block depth counter
        if current_block_type == 'if':
            while index < len(tokens):
                token = tokens[index]  # Get the current token at the current index

                if token.value == current_block_type:
                    block_depth += 1  # Increase the block depth when encountering the start of the block
                elif token.value == other_block_type:
                    if block_depth == 0:
                        break  # If we're at the end of the block (block_depth is 0), exit the loop
                    else:
                        block_depth -= 1  # Decrease the block depth when encountering the end of the block

                index += 1  # Move to the next token
        else:
            while index < len(tokens):
                token = tokens[index]
                nexttoken = get_next_token(index)
                if nexttoken != None:
                    if token.type == 'newline' and nexttoken.type != 'indentation':
                        break
                    else:
                        index += 1
                else: 
                    break
        return index  # Return the index after skipping the code block


###################### EXECUTING CODE BLOCK FOR IF/ELSE AND VARIABLE ASSIGNMENT ##########################
    
    #case here determines if its for variable assignment or for an if/else execute
    def execute_code_block(tokens, start_index, case):
        index = start_index
        while index < len(tokens):
            if case == 0:
                nexttoken = get_next_token(index)
                token = tokens[index]
                if nexttoken != None:
                    index, res = evaluate_tokens(tokens, index, 1)
                    break
            elif case == 1:
                token = tokens[index]
                nexttoken = get_next_token(index)
                if token.type == 'newline' and nexttoken.type == 'indentation':
                    index += 2
                    index, res = evaluate_tokens(tokens, index, 0)
                    break
            elif case == 2:
                nexttoken = get_next_token(index)
                token = tokens[index]
                if nexttoken != None:
                    index, res = evaluate_tokens(tokens, index, 2)
                    break
                
            #if token.type == 'newline' and nexttoken.type == 'indentation':
                #index += 2
                #index, res = evaluate_tokens(tokens, index)
                
        return index, res
    
    operators = []
    output = []
    exitindent = 0

 ############################### TOKEN ITERATION ##################################################
    
    while start_index < len(tokens):
        #later in the code, there is a part specifically for equations as variable assigment i.e. x = x + 5, what this does is
        #loop back to the main code to execute x + 5, set indexes[0] to a value and then checks the value here, setting start_index
        #to the value of indexes[0] and then resetting the value of indexes[0] to 0.
        i = start_index 
        token = tokens[i]
        nexttoken = get_next_token(start_index)
        if asscheck == 1 and token.type == 'newline':
            while operators:
                output.append(apply_operator(operators.pop(), output.pop(), output.pop()))
            return i, output[0] if output else None
        if asscheck == 2 and token.type == 'close_par':
            while operators:
                output.append(apply_operator(operators.pop(), output.pop(), output.pop()))
            return i, output[0] if output else None
        #if the token is a int, append it to the output array, no specific print function yet so print is assumed if no variable
        #declarationexitindent == 1:
        if exitindent == 1:
            if nexttoken != None:
                if tokens[start_index].type == 'newline' and nexttoken.type != 'indentation':
                    while operators:
                        exitindent = 0
                        output.append(apply_operator(operators.pop(), output.pop(), output.pop()))
                        return i, output[0] if output else None
            elif tokens[start_index].type == 'newline':
                while operators:
                    output.append(apply_operator(operators.pop(), output.pop(), output.pop()))
                    return i, output[0] if output else None
        if (token.type == 'int'):
            if(i == 0):
                output.append(int(token.value))
            elif(tokens[i-1].value != '='):
                output.append(int(token.value)) 
        #if the token is an operator, append it to output array, not specific print function yet so print is assumed if no variable
        #declaration
        elif (token.type == 'float'):
            if(i == 0):
                output.append(float(token.value))
            elif(tokens[i-1].value != '='):
                output.append(float(token.value)) 
        #if the token is a variable, check if next value is keyword for assignment
                
########################################## INITIAL VARIABLE DECLARATION ###################################
        elif token.type == 'variable':
            next_token = get_next_token(i)
            if next_token and next_token.value == 'is':
                
                variable_name = token.value
                i += 1  # Skip the 'is' token to check for datatype
                next_next_token = get_next_token(i)
                #raise error if next token is not a datatype
                if not next_next_token or next_next_token.value not in ['int', 'float', 'double', 'char', 'boolean']:
                    raise ValueError("Invalid assignment statement.")
                datatype = next_next_token.value
                validate_datatype(datatype)
                i += 1  # Skip the datatype token to check for equals
                next_token = get_next_token(i)
                if not next_token or next_token.type != 'equals':
                    raise ValueError("Invalid assignment statement.")
                i += 1  # Skip the 'equals' token to check for value to be assigned
                valueplace = get_next_token(i)
                value = valueplace.value
                #gets the value of the next token and stores it in 'value' to be inserted in variables
                validate_input_for_datatype(value, datatype)
                #verifies datatype
                i -=3
                #reduces index by 3 so that the original token.value or "varname" i.e. 'x' can be stored alongside new value i.e. '5'
                #in variables array
                variables.append((token.value, value, datatype))
                #stores the variable name, value and datatype in variables array
                i +=3  #returns to current index

############################################### VARIABLE ASSIGNMENT #####################################
                
            elif next_token and next_token.value == '=' and next_token != None:
            #executes if variable is being assigned to an equation i.e. x = x + 5, no logic yet to check if already defined
                i += 2  # Skip the current and '=' token
                inner_index = i
                #stores current indexyy
                tokenholder = token.value
                typeholder = ""
                for j in range(len(variables)):
                    if (tokenholder == variables[j][0]):
                            typeholder = variables[j][2]
                #store initial value 'x' variable for reassignment later on  
   
                newIndex, res = execute_code_block(tokens, inner_index, 0)
                value = res
                variables = [(x, y, z) for x, y, z in variables if x != tokenholder]
                variables.append((tokenholder, value, typeholder))
                start_index = newIndex

            elif next_token and next_token.type == 'variable':
                for j in range(len(variables)):
                    if (token.value == variables[j][0]):
                            if variables[j][2] == 'int':
                                output.append(int(variables[j][1]))
                            elif variables[j][2] == 'float':
                                output.append(float(variables[j][1]))
                while operators:
                    output.append(apply_operator(operators.pop(), output.pop(), output.pop()))    
            else:
                for j in range(len(variables)):
                    if (token.value == variables[j][0]):
                            if variables[j][2] == 'int':
                                output.append(int(variables[j][1]))
                            elif variables[j][2] == 'float':
                                output.append(float(variables[j][1]))

############################################### PRINTING ############################################
                                
        elif token.value == 'print':
            nexttoken = get_next_token(i)
            if nexttoken.type == 'open_par':
                i += 2
            start_index, res = execute_code_block(tokens, i, 2)
            print(res)
            __printOutTheseValues.append(res)

############################################### IF/ELSE STATEMENTS ################################
            
        elif token.value == 'if':
            condition = evaluate_condition(tokens, i)
            i = condition[1]
            if condition[0]:
                start_index, dont   = execute_code_block(tokens, i + 1, 1)
            else:               
                # Skip the 'if' code block and find the 'else' (if present)
                start_index = skip_code_block(tokens, i + 1, 'if', 'else')              
                start_index, dont= execute_code_block(tokens, start_index+1, 1)
        elif token.value == 'else':              
                start_index = skip_code_block(tokens, i + 1, 'else', '')             
            # Skip the 'else' code block if the 'if' block was executed          
        elif token.type in ['add_operator', 'minus_operator', 'mult_operator', 'div_operator']:
            while operators and  (precedence(operators[-1]) >= precedence(token.value)):
                # Correct the order of operand popping
                operator = operators.pop()
                operand2 = output.pop()
                operand1 = output.pop()
                output.append(apply_operator(operator, operand1, operand2))
            operators.append(token.type)
        elif token.type == 'open_par':
            operators.append(token.type)
        elif token.type == 'close_par':
            while operators and operators[-1] != 'open_par':
                output.append(apply_operator(operators.pop(), output.pop(), output.pop()))
            operators.pop()  # Discard the open parenthesis
        start_index += 1
    while operators:
        output.append(apply_operator(operators.pop(), output.pop(), output.pop()))
    return start_index, output[0] if output else None
