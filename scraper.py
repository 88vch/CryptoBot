import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
 
# DexScreener API endpoint
DEXSCREENER_API_URL = "https://api.dexscreener.com/latest/dex/tokens/"
 
# Function to fetch token data (= trades) from DexScreener
def fetch_token_data(token_address):
    try:
        response = requests.get(f"{DEXSCREENER_API_URL}{token_address}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for token {token_address}: {e}")
        return None
 
# Function to filter tokens based on DexScreener criteria
def filter_tokens_dexscreener(token_data) -> list:
    filtered_tokens = []
    current_time = datetime.now(datetime.timezone.utc)
    twenty_four_hours_ago = current_time - timedelta(hours=24)
 
    for token in token_data:
        pair_created_at = datetime.fromtimestamp(token['pairCreatedAt'] / 1000)
        # [1.27.2025] - Skip tokens created more than 24 hours ago
        if pair_created_at < twenty_four_hours_ago:
            continue
 
        txns_last_hour = token.get('txns', {}).get('h1', 0)
        txns_last_5min = token.get('txns', {}).get('m5', 0)
 
        if txns_last_hour >= 100 and txns_last_5min >= 20:
            filtered_tokens.append({
                'token_address': token['baseToken']['address'],
                'token_name': token['baseToken']['name'],
                'token_symbol': token['baseToken']['symbol'],
                'pair_created_at': pair_created_at.isoformat(),
                'txns_last_hour': txns_last_hour,
                'txns_last_5min': txns_last_5min
            })
 
    return filtered_tokens
 
# [1.27.2025] - todays the day this guy posted the code online but [tweetscout.io] alr has a [v2] version
# - so I'm wondering if the code is outdated here (also repalced) [https://api.tweetscout.io/v2/search-tweets] (POST)

# Function to fetch token social activity from tweetscout.io
def fetch_token_social_activity(token_name):
    url = f"https://tweetscout.io/token/{token_name}"  # Replace with actual URL structure
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token social activity: {e}")
        return None
 
# Function to parse social activity and filter influencers
def parse_social_activity(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    influencers = []
 
    influencer_cards = soup.find_all("div", class_="influencer-card")  # Replace with actual class or tag
    for card in influencer_cards:
        name = card.find("span", class_="influencer-name").text.strip()  # Replace with actual class or tag
        followers = card.find("span", class_="influencer-followers").text.strip()  # Replace with actual class or tag
        followers_count = int(followers.replace(",", "").replace(" followers", ""))
 
        if followers_count >= 40000:
            influencers.append({
                "name": name,
                "followers": followers_count
            })
 
    return influencers
 
# Function to fetch token contract analysis from rugcheck.xyz
def fetch_token_contract_analysis(token_address):
    url = f"https://rugcheck.xyz/tokens/{token_address}"  # Replace with actual URL structure
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token contract analysis: {e}")
        return None
 
# Function to parse contract analysis and check safety
def parse_contract_analysis(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    analysis_data = {}
 
    safety_score_element = soup.find("div", class_="safety-score")  # Replace with actual class or tag
    if safety_score_element:
        safety_score = safety_score_element.text.strip().replace("%", "")
        analysis_data["safety_score"] = float(safety_score)
    else:
        analysis_data["safety_score"] = 0.0
 
    liquidity_burned_element = soup.find("div", class_="liquidity-burned")  # Replace with actual class or tag
    if liquidity_burned_element:
        analysis_data["liquidity_burned"] = "Yes" in liquidity_burned_element.text.strip()
    else:
        analysis_data["liquidity_burned"] = False
 
    mintable_element = soup.find("div", class_="mintable")  # Replace with actual class or tag
    if mintable_element:
        analysis_data["mintable"] = "Yes" in mintable_element.text.strip()
    else:
        analysis_data["mintable"] = False
 
    pausable_element = soup.find("div", class_="pausable")  # Replace with actual class or tag
    if pausable_element:
        analysis_data["pausable"] = "Yes" in pausable_element.text.strip()
    else:
        analysis_data["pausable"] = False
 
    return analysis_data
 
# Function to save final results to a CSV file
def save_to_csv(data, filename="final_token_analysis.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
 
# Main function to run the combined analysis
def main():
    # List of token addresses to analyze (replace with actual token addresses)
    token_addresses = [
        '0xYourTokenAddress1',
        '0xYourTokenAddress2',
        # Add more token addresses as needed
    ]
 
    final_results = []
 
    for token_address in token_addresses:
        # Step 1: Fetch and filter tokens from DexScreener
        token_data = fetch_token_data(token_address)
        if not token_data:
            continue
 
        filtered_tokens = filter_tokens_dexscreener(token_data['pairs'])
        if not filtered_tokens:
            print(f"No tokens matched DexScreener criteria for {token_address}.")
            continue
 
        # Step 2: Analyze social activity on tweetscout.io
        token_name = filtered_tokens[0]['token_name']  # Use the first filtered token
        html_content = fetch_token_social_activity(token_name)
        if not html_content:
            continue
 
        influencers = parse_social_activity(html_content)
        if not influencers:
            print(f"No influencers found for {token_name}.")
            continue
 
        # Step 3: Analyze contract safety on rugcheck.xyz
        html_content = fetch_token_contract_analysis(token_address)
        if not html_content:
            continue
 
        contract_analysis = parse_contract_analysis(html_content)
        if contract_analysis["safety_score"] < 85:
            print(f"Token {token_name} has a safety score below 85%: {contract_analysis['safety_score']}%")
            continue
 
        # Combine results
        final_results.append({
            "token_address": token_address,
            "token_name": token_name,
            "token_symbol": filtered_tokens[0]['token_symbol'],
            "pair_created_at": filtered_tokens[0]['pair_created_at'],
            "txns_last_hour": filtered_tokens[0]['txns_last_hour'],
            "txns_last_5min": filtered_tokens[0]['txns_last_5min'],
            "influencers": len(influencers),
            "safety_score": contract_analysis["safety_score"],
            "liquidity_burned": contract_analysis["liquidity_burned"],
            "mintable": contract_analysis["mintable"],
            "pausable": contract_analysis["pausable"]
        })
 
        # Handle rate limits
        time.sleep(1)
 
    if final_results:
        save_to_csv(final_results)
    else:
        print("No tokens matched all criteria.")
 
if __name__ == "__main__":
    main()