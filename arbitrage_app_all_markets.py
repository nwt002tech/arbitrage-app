
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Live Arbitrage Finder (All Markets)", layout="wide")
st.title("⚡ Live Sports Betting Arbitrage Finder (All Markets)")

API_KEY = "cb35e55c78aa7add1ec4a12325b5cbed"

# Supported markets
MARKETS = ["h2h", "spreads", "totals"]

def get_odds_all_markets():
    all_matches = []
    for market in MARKETS:
        url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?apiKey={API_KEY}&regions=us&markets={market}&oddsFormat=decimal"
        res = requests.get(url)
        if res.status_code != 200:
            continue
        data = res.json()
        for game in data:
            match_name = f"{game['home_team']} vs {game['away_team']}"

            bookmakers = game.get("bookmakers", [])
            if len(bookmakers) < 2:
                continue

            for i in range(len(bookmakers) - 1):
                for j in range(i + 1, len(bookmakers)):
                    try:
                        bm1 = bookmakers[i]
                        bm2 = bookmakers[j]
                        outcomes1 = bm1["markets"][0]["outcomes"]
                        outcomes2 = bm2["markets"][0]["outcomes"]
                        if len(outcomes1) != 2 or len(outcomes2) != 2:
                            continue
                        o1a = outcomes1[0]["price"]
                        o1b = outcomes2[1]["price"]

                        all_matches.append({
                            "match": match_name,
                            "market": market,
                            "book_1": bm1["title"],
                            "odds_1": o1a,
                            "book_2": bm2["title"],
                            "odds_2": o1b
                        })
                    except Exception:
                        continue
    return all_matches

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

total_bet = st.number_input("💰 Total bet amount ($)", value=100)

odds_data = get_odds_all_markets()
records = []
for game in odds_data:
    has_arb, roi, profit, stake_1, stake_2 = calculate_arbitrage(game["odds_1"], game["odds_2"], total_bet)
    if has_arb:
        records.append({
            "Match": game["match"],
            "Market": game["market"],
            "Book 1": f'{game["book_1"]} @ {game["odds_1"]}',
            "Stake 1 ($)": stake_1,
            "Book 2": f'{game["book_2"]} @ {game["odds_2"]}',
            "Stake 2 ($)": stake_2,
            "ROI %": roi,
            "Profit ($)": profit
        })

if records:
    st.success(f"✅ {len(records)} Arbitrage Opportunities Found!")
    df = pd.DataFrame(records)
    st.dataframe(df)
else:
    st.warning("No arbitrage opportunities found right now. Try refreshing in a few seconds.")
