# Get user input
n = input("Height: ")

try:
    while int(n) not in range(1, 9, 1):
        print('Proved a positive integer bewtween 1 and 8')
        n = input()
except:
    print('Proved a positive integer bewtween 1 and 8')
    n = input("Height: ")
    
n = int(n)

# Print pyramide ==============================================================
for i in range(0, n, 1):
    print(" " * (n - (i + 1)), "#" * (i + 1), "  ", "#" * (i + 1), sep='')