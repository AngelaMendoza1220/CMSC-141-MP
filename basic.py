
class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


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
    
def isKeyword(word):
    keywords = ["int", "float", "double", "str", "bool", "is"]

    if word in keywords:
        return True
    else:
        return False

def lexer(linesOfCode):

    tokens = []

    for line in linesOfCode:  # for every line in the code
        i = 0
        while i < len(line):  # for every character in the line
            identifier = ""
            number = ""
            if line[i].isdigit():
                while i < len(line) and line[i].isdigit():
                    number = number + line[i]
                    i = i + 1
                tokens.append(token('number', number)) 
            elif line[i].isalpha() or line[i] == "_":
                while i < len(line) and (line[i].isalpha() or line[i] == "_"):
                    identifier = identifier + line[i]
                    i = i + 1
                if isKeyword(identifier):
                    tokens.append(token('keyword', identifier))  
                else:
                    tokens.append(token('variable', identifier))
            elif line[i] == "=":
                tokens.append(token('equals', line[i]))
            elif isMathOperators(line[i]):
                tokens.append(token(getMathOperator(line[i]), line[i]))
                
            i = i + 1
        
    return tokens

#code = ['x is int = 1', 'x + y']
#lex = lexer(code)       

#for obj in lex:
    #print(obj.type, obj.value, sep=' ')