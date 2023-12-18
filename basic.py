import re


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


def isKeyword(word):
    keywords = ["is", "int", "float", "string", "boolean", "char", "print"]

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
                    print("The number " + temp + " is invalid")
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
                else:
                    print("Invalid syntax")
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
                else:
                    print("Invalid syntax")
                    break
            elif line[pos] == "=":                        # if =, append as token
                tokens.append(Token('equals', line[pos]))
                pos += 1
            elif isMathOperators(line[pos]):              # if it is a math operator, determine the specific operator and add as token
                tokens.append(Token(getMathOperator(line[pos]), line[pos]))
                pos += 1
            elif line[pos] == " ":                        # move to the next position if space is encountered
                pos += 1
            elif line[pos] == "\n":
                tokens.append(Token('newline', line[pos]))
            else:
                print("Invalid syntax")
                break
                
    return tokens