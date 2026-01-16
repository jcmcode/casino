import random
from collections import defaultdict

class BlackjackMartingale:
    def __init__(self, starting_bankroll=1000, base_bet=10, max_bet=500, num_simulations=100):
        self.starting_bankroll = starting_bankroll
        self.base_bet = base_bet
        self.max_bet = max_bet
        self.num_simulations = num_simulations
        
    def create_deck(self):
        """Create a standard 52-card deck (can use multiple decks)"""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = []
        # Using 6 decks like most casinos
        for _ in range(6):
            for suit in suits:
                for rank in ranks:
                    deck.append(rank)
        random.shuffle(deck)
        return deck
    
    def card_value(self, card):
        """Get numeric value of a card"""
        if card in ['J', 'Q', 'K']:
            return 10
        elif card == 'A':
            return 11  # Will adjust for aces later
        else:
            return int(card)
    
    def calculate_hand_value(self, hand):
        """Calculate the value of a hand, handling aces"""
        value = sum(self.card_value(card) for card in hand)
        aces = hand.count('A')
        
        # Adjust for aces if busted
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def play_dealer_hand(self, dealer_hand, deck):
        """Dealer hits on 16 and below, stands on 17+"""
        while self.calculate_hand_value(dealer_hand) < 17:
            if len(deck) == 0:
                deck = self.create_deck()
            dealer_hand.append(deck.pop())
        return dealer_hand
    
    def play_hand(self, deck):
        """Play a single hand of blackjack"""
        if len(deck) < 20:  # Reshuffle if running low
            deck = self.create_deck()
        
        # Deal initial cards
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        
        # Player plays (simplified strategy: hit on 16 or below, stand on 17+)
        while self.calculate_hand_value(player_hand) < 17:
            player_hand.append(deck.pop())
        
        player_value = self.calculate_hand_value(player_hand)
        
        # Check if player busted
        if player_value > 21:
            return -1, deck  # Loss
        
        # Dealer plays
        dealer_hand = self.play_dealer_hand(dealer_hand, deck)
        dealer_value = self.calculate_hand_value(dealer_hand)
        
        # Determine winner
        if dealer_value > 21:
            return 1, deck  # Win
        elif player_value > dealer_value:
            return 1, deck  # Win
        elif player_value < dealer_value:
            return -1, deck  # Loss
        else:
            return 0, deck  # Push
    
    def run_simulation(self):
        """Run a single simulation with martingale betting"""
        bankroll = self.starting_bankroll
        current_bet = self.base_bet
        deck = self.create_deck()
        
        hands_played = 0
        wins = 0
        losses = 0
        pushes = 0
        max_bankroll = bankroll
        min_bankroll = bankroll
        
        # Play until bankroll is depleted or we've played 1000 hands
        while bankroll >= current_bet and hands_played < 1000:
            # Place bet
            bankroll -= current_bet
            
            # Play hand
            result, deck = self.play_hand(deck)
            hands_played += 1
            
            if result == 1:  # Win
                bankroll += current_bet * 2
                wins += 1
                current_bet = self.base_bet  # Reset to base bet after win
            elif result == -1:  # Loss
                losses += 1
                current_bet = min(current_bet * 2, self.max_bet)  # Double bet (martingale)
            else:  # Push
                bankroll += current_bet  # Return bet
                pushes += 1
            
            # Track bankroll extremes
            max_bankroll = max(max_bankroll, bankroll)
            min_bankroll = min(min_bankroll, bankroll)
        
        return {
            'final_bankroll': bankroll,
            'hands_played': hands_played,
            'wins': wins,
            'losses': losses,
            'pushes': pushes,
            'max_bankroll': max_bankroll,
            'min_bankroll': min_bankroll,
            'profit_loss': bankroll - self.starting_bankroll,
            'went_broke': bankroll < self.base_bet
        }
    
    def run_simulations(self):
        """Run multiple simulations and aggregate results"""
        results = []
        
        for i in range(self.num_simulations):
            result = self.run_simulation()
            results.append(result)
        
        return results
    
    def display_results(self, results):
        """Display aggregated results from all simulations"""
        print("\n" + "="*60)
        print("BLACKJACK MARTINGALE SIMULATOR RESULTS")
        print("="*60)
        print(f"\nSimulation Parameters:")
        print(f"  Starting Bankroll: ${self.starting_bankroll}")
        print(f"  Base Bet: ${self.base_bet}")
        print(f"  Maximum Bet: ${self.max_bet}")
        print(f"  Number of Simulations: {self.num_simulations}")
        
        # Aggregate statistics
        total_hands = sum(r['hands_played'] for r in results)
        total_wins = sum(r['wins'] for r in results)
        total_losses = sum(r['losses'] for r in results)
        total_pushes = sum(r['pushes'] for r in results)
        
        avg_final_bankroll = sum(r['final_bankroll'] for r in results) / len(results)
        avg_profit_loss = sum(r['profit_loss'] for r in results) / len(results)
        avg_hands = sum(r['hands_played'] for r in results) / len(results)
        
        went_broke_count = sum(1 for r in results if r['went_broke'])
        came_out_ahead = sum(1 for r in results if r['profit_loss'] > 0)
        
        max_profit = max(r['profit_loss'] for r in results)
        max_loss = min(r['profit_loss'] for r in results)
        
        print(f"\n" + "-"*60)
        print("OVERALL STATISTICS")
        print("-"*60)
        print(f"  Total Hands Played: {total_hands:,}")
        print(f"  Average Hands per Simulation: {avg_hands:.1f}")
        print(f"  Total Wins: {total_wins:,} ({total_wins/total_hands*100:.1f}%)")
        print(f"  Total Losses: {total_losses:,} ({total_losses/total_hands*100:.1f}%)")
        print(f"  Total Pushes: {total_pushes:,} ({total_pushes/total_hands*100:.1f}%)")
        
        print(f"\n" + "-"*60)
        print("FINANCIAL OUTCOMES")
        print("-"*60)
        print(f"  Average Final Bankroll: ${avg_final_bankroll:.2f}")
        print(f"  Average Profit/Loss: ${avg_profit_loss:.2f}")
        print(f"  Best Outcome: ${max_profit:.2f}")
        print(f"  Worst Outcome: ${max_loss:.2f}")
        
        print(f"\n" + "-"*60)
        print("SUCCESS METRICS")
        print("-"*60)
        print(f"  Went Broke: {went_broke_count}/{self.num_simulations} ({went_broke_count/self.num_simulations*100:.1f}%)")
        print(f"  Came Out Ahead: {came_out_ahead}/{self.num_simulations} ({came_out_ahead/self.num_simulations*100:.1f}%)")
        print(f"  Broke Even or Lost: {self.num_simulations - came_out_ahead}/{self.num_simulations} ({(self.num_simulations - came_out_ahead)/self.num_simulations*100:.1f}%)")
        
        # Distribution of outcomes
        print(f"\n" + "-"*60)
        print("PROFIT/LOSS DISTRIBUTION")
        print("-"*60)
        
        # Create buckets for distribution
        buckets = defaultdict(int)
        for r in results:
            pl = r['profit_loss']
            if pl < -500:
                buckets['< -$500'] += 1
            elif pl < -250:
                buckets['-$500 to -$250'] += 1
            elif pl < 0:
                buckets['-$250 to $0'] += 1
            elif pl == 0:
                buckets['$0 (Break Even)'] += 1
            elif pl <= 250:
                buckets['$0 to $250'] += 1
            elif pl <= 500:
                buckets['$250 to $500'] += 1
            else:
                buckets['> $500'] += 1
        
        for bucket in ['< -$500', '-$500 to -$250', '-$250 to $0', '$0 (Break Even)', 
                       '$0 to $250', '$250 to $500', '> $500']:
            count = buckets[bucket]
            if count > 0:
                pct = count / self.num_simulations * 100
                bar = '█' * int(pct / 2)
                print(f"  {bucket:20s}: {count:3d} ({pct:5.1f}%) {bar}")
        
        print("="*60 + "\n")


def main():
    # Create simulator with parameters
    simulator = BlackjackMartingale(
        starting_bankroll=1000,
        base_bet=10,
        max_bet=500,
        num_simulations=100
    )
    
    print("\nRunning simulations...")
    results = simulator.run_simulations()
    simulator.display_results(results)


if __name__ == "__main__":
    main()
