import os

output = []
for i in range(100):
    output.append(os.popen('python main.py').read())

wins = 0
errors = []
for elem in output:
    print(elem)
    if elem == "1\n":
        wins+=1
    elif elem != "0\n":
        errors.append(elem)
print("Winrate:", wins/len(output) * 100 , '%')
for error in errors:
    print(error)