import random

def payouts(outcome, bet_type,):
    first_dozen = range(1, 13)
    second_dozen = range(13, 25)
    third_dozen = range(25, 37)
    first_half = range(1, 19)
    second_half = range(19, 37)
    payouts = {first_dozen: 3,
               second_dozen: 3,
               third_dozen: 3,
                first_half: 2,
                second_half: 2,
               'red': 2,
               'black': 2,
               'even': 2,
               'odd': 2,
               'individual': 36}
    
    if outcome in bet_type:
        return payouts[bet_type]
    else:    
        return 0
    
    

def roulette_strategy(balance, target):
    bet_type = ['first_dozen'
                'second_dozen'
                ]
    while balance > 0 or balance < target:
        print(1)


if __name__ == "__main__":
    starting_balance = 500
    target_balance = 1000
    roulette_strategy(starting_balance, target_balance)