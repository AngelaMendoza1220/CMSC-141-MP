import re


class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


def isKeyword(word):
    keywords = ["is", "int", "float", "double", "string", "boolean"]

    if word in keywords:
        return True
    else:
        return False
    
def isNumberValid(num):
    pattern = r'^[+-]?\d+(\.\d+)?$'

    if re.match(pattern, num):
        return True
    else:
        return False
    
def isVariableNameValid(var):
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


def lexer(linesOfCode):

    tokens = []

    for line in linesOfCode:  # for every line in the code
        pos = 0
        while pos < len(line):  # for every character in the line
            temp = ""
            if line[pos].isdigit(): # if the character is a digit, append all digits
                while pos < len(line) and (line[pos].isdigit() or line[pos] == "."): 
                    temp += line[pos]    
                    pos += 1
                if isNumberValid(temp):         # if the number is valid, add as a token
                    tokens.append(token('number', temp)) 
                else:                           # if number is invalid, print error
                    print("The number " + temp + " is invalid")
                    break
            elif line[pos].isalpha() or line[pos] == "_":
                while pos < len(line) and (line[pos].isalpha() or line[pos] == "_"):
                    temp += line[pos]
                    pos += 1
                if isKeyword(temp):             # if the word is a keyword, add as a token
                    tokens.append(token('keyword', temp))  
                elif isVariableNameValid(temp): # if the word is a valid variable name, add as a token
                    tokens.append(token('variable', temp))
                else:
                    print("Invalid syntax")
                    break
            elif line[pos] == "=":
                tokens.append(token('equals', line[pos]))
                pos += 1
            elif isMathOperators(line[pos]):
                tokens.append(token(getMathOperator(line[pos]), line[pos]))
                pos += 1
            elif line[pos] == " ":
                pos += 1
            else:
                print("Invalid syntax")
                break
                
    return tokens