import os

wins = 0
tries = 0
errors = []
for i in range(5):
    print("Running test", i)
    elem = os.popen('python main.py').read()
    tries += 1
    if elem == "1\n":
        wins+=1
    elif elem != "0\n":
        errors.append(elem)
    print("Winrate:", wins / tries * 100, '%')

print("Found", len(errors), "errors")
for error in errors:
    print(error)