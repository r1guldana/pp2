import re
stringg = "ncjk@mkl21"
n = re.findall("@", stringg) 
print(n)

f = open("text.txt", "r")

line = f.readlines()
print(len(line))
