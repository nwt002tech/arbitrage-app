import streamlit as st
import pandas as pd

st.title("⚡ Sports Betting Arbitrage Finder")

# Sample odds data (replace with live data or API integration later)
sample_data = [
    {"match": "Lakers vs Celtics", "team_1": "Lakers", "team_2": "Celtics",
     "book_1": "FanDuel", "odds_1": 2.10, "book_2": "DraftKings", "odds_2": 1.95},
    {"match": "Yankees vs Red Sox", "team_1": "Yankees", "team_2": "Red Sox",
     "book_1": "BetMGM", "odds_1": 2.20, "book_2": "Caesars", "odds_2": 1.80},
    {"match": "Warriors vs Suns", "team_1": "Warriors", "team_2": "Suns",
     "book_1": "PointsBet", "odds_1": 2.05, "book_2": "Barstool", "odds_2": 2.00}
]

def calculate_arbitrage(odds_1, odds_2, total_bet=100):
    implied_prob = (1 / odds_1) + (1 / odds_2)
    has_arb = implied_prob < 1
    if has_arb:
        stake_1 = total_bet / (1 + (odds_1 / odds_2))
        stake_2 = total_bet - stake_1
        profit = min(stake_1 * odds_1, stake_2 * odds_2) - total_bet
        roi = (profit / total_bet) * 100
        return True, round(roi, 2), round(profit, 2), round(stake_1, 2), round(stake_2, 2)
    return False, 0, 0, 0, 0

# UI for total bet input
total_bet = st.number_input("💰 Enter total bet amount ($):", value=100)

records = []
for game in sample_data:
    has_arb, roi, profit, stake_1, stake_2 = calculate_arbitrage(game["odds_1"], game["odds_2"], total_bet)
    if has_arb:
        records.append({
            "Match": game["match"],
            "Book 1": f'{game["book_1"]} @ {game["odds_1"]}',
            "Stake 1 ($)": stake_1,
            "Book 2": f'{game["book_2"]} @ {game["odds_2"]}',
            "Stake 2 ($)": stake_2,
            "ROI %": roi,
            "Profit ($)": profit
        })

if records:
    st.success("✅ Arbitrage opportunities found!")
    df = pd.DataFrame(records)
    st.dataframe(df)
else:
    st.warning("❌ No arbitrage opportunities found.")
