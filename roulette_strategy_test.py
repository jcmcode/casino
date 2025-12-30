import random

def get_payout_multiplier(outcome, bet_type):
    definitions = {
        'first_dozen': (range(1, 13), 3),
        'second_dozen': (range(13, 25), 3),
        'third_dozen': (range(25, 37), 3),
        'first_half': (range(1, 19), 2),
        'second_half': (range(19, 37), 2),
        'individual': (range(outcome, outcome + 1), 36)
    }
    
    if bet_type in definitions:
        winning_numbers, multiplier = definitions[bet_type]
        if outcome in winning_numbers:
            return multiplier
    return 0

def roulette_strategy_one(balance, target):
    current_balance = balance
    
    while 0 < current_balance < target:
        spin = random.randint(0, 36)
        
        bets = [
            {'type': 'second_half', 'amount': 120},
            {'type': 'first_dozen', 'amount': 80}
        ]
        
        total_wagered = sum(bet['amount'] for bet in bets)
        
        if current_balance < total_wagered:
            break

        current_balance -= total_wagered
        
        round_winnings = 0
        for bet in bets:
            multiplier = get_payout_multiplier(spin, bet['type'])
            round_winnings += bet['amount'] * multiplier
            
        current_balance += round_winnings

    return current_balance

if __name__ == "__main__":
    starting_balance = 500
    target_balance = 1000
    roulette_strategy_one(starting_balance, target_balance)