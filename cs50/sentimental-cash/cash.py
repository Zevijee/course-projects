from cs50 import get_float

def main():
    cents = get_cents()

    quarters = calculate_quarters(cents)
    cents = round(cents - quarters * .25, 2)

    dimes = calculate_dimes(cents)
    cents = round(cents - dimes * .10, 2)

    nickels = calculate_nickels(cents)
    cents = round(cents - nickels * .05, 2)

    pennies = calculate_pennies(cents)
    cents = round(cents - pennies * .01, 2)

    coins = quarters + dimes + nickels + pennies

    print(coins)

def get_cents():
    cents = get_float("change owed : ")
    while True:
        if cents <= 0:
            cents = get_float("change owed : ")

        return cents


def calculate_quarters(cents):
    return int(cents/.25)


def calculate_dimes(cents):
    return int(cents/.10)


def calculate_nickels(cents):
    return int(cents/.05)


def calculate_pennies(cents):
    return int(cents/.01)

main()