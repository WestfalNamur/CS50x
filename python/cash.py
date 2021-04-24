# =============================================================================
# Ask user how much change is owed.
# Return Minumum number of coins nedded to return the cash.
# =============================================================================

COINS = [0.25, 0.1, 0.05, 0.01]

change_input_is_float = False

# Prompt for user input, try to convert it to flaot, if not possible, ask again;
while change_input_is_float == False:
    change_input = input("Change owed: ")
    try:
        change = float(change_input)
        if change >= 0:
            change_input_is_float = True
        else:
            print("Number must be positive.")
    except:
        print("Pleas type a number")

# Iterate through list of COINS form larger to smaller. For each coin find the
# reminder of a possible substraction. Substract that from change, devide change
# by that number and take is as count for that coin. Set the reminder (reminding
# change) as new change.
# ! Floating point errors;
dx = {}
for coin in COINS:
    reminder = round(change % coin, 2)
    dx[coin] = (change - reminder) / coin
    change = reminder

# Print minimal number of coins needed
print(int(sum(dx.values())))
