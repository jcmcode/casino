import random

def payouts(balance, target):

    first_dozen = [1,2,3,4,5,6,7,8,9,10,11,12]
    second_dozen = [13,14,15,16,17,18,19,20,21,22,23,24]
    third_dozen = [25,26,27,28,29,30,31,32,33,34,35,36]
    
    all_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,
                   13,14,15,16,17,18,19,20,21,22,23,24,
                   25,26,27,28,29,30,31,32,33,34,35,36,0]
    
    payouts = {first_dozen: 3,
               second_dozen: 3,
               third_dozen: 3,
               'red': 2,
               'black': 2,
               'even': 2,
               'odd': 2,
               'individual': 36}
    

def roulette_strategy(balance, target):
    while balance > 0 or balance < target:
        


if __name__ == "__main__":
    starting_balance = 500
    target_balance = 1000
    roulette_strategy(starting_balance, target_balance)