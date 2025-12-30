import random

import matplotlib.pyplot as plt

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

def run_simulation(simulations, start_balance, target_balance):
    results = {
        'hit_target': 0,
        'went_broke': 0,
        'final_balances': [],
        'rounds_played': []
    }

    for _ in range(simulations):
        final_balance, rounds = roulette_strategy_one(start_balance, target_balance)
        
        results['final_balances'].append(final_balance)
        results['rounds_played'].append(rounds)
        
        if final_balance >= target_balance:
            results['hit_target'] += 1
        else:
            results['went_broke'] += 1
            
    return results

# --- CONFIGURATION ---
sim_count = 100
start_money = 1000
target_money = 2000

data = run_simulation(sim_count, start_money, target_money)

# --- STATISTICS OUTPUT ---
print(f"Simulations Run: {sim_count}")
print(f"Target Hit: {data['hit_target']} times ({data['hit_target']/sim_count*100}%)")
print(f"Went Broke: {data['went_broke']} times ({data['went_broke']/sim_count*100}%)")
print(f"Avg Rounds Played: {sum(data['rounds_played']) / sim_count}")

# --- MATPLOTLIB VISUALIZATION ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Chart 1: Win/Loss Ratio
labels = ['Hit Target', 'Went Broke']
counts = [data['hit_target'], data['went_broke']]
ax1.bar(labels, counts, color=['green', 'red'])
ax1.set_title('Win vs Loss Distribution')
ax1.set_ylabel('Count')

# Chart 2: Rounds Survived Histogram
ax2.hist(data['rounds_played'], bins=20, color='skyblue', edgecolor='black')
ax2.set_title('Distribution of Rounds Played')
ax2.set_xlabel('Rounds Survived')
ax2.set_ylabel('Frequency')

plt.tight_layout()
plt.show()