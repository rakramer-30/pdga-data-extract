import requests
import pandas as pd

def fetch_pga_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()
    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        return None

    hole_details = data['data']['holes']

    hole_values = [item['HoleOrdinal'] for item in hole_details]
    hole_lengths = [item['Length'] for item in hole_details]
    hole_par = [item['Par'] for item in hole_details]

    column_index = pd.MultiIndex.from_tuples(zip(hole_values, hole_lengths, hole_par))

    df = pd.DataFrame(columns=column_index)

    df.insert(0, 'Place', '')
    df.insert(1, 'Player', '')
    df.insert(2,'Total Par', '')
    df.insert(3, 'Rd', '') 
    df.insert(22, 'Total', '')
    df.insert(23, 'Rd Rating', '')

    player_data = data['data']['scores']

    player_place = [data['RunningPlace'] for data in player_data]
    player_names = [data['Name'] for data in player_data]
    total_to_par = [data['ToPar'] for data in player_data]
    hole_scores = [data['HoleScores'] for data in player_data]
    player_round_par = [data['RoundtoPar'] for data in player_data]
    player_round_score = [data['RoundScore'] for data in player_data]
    player_round_rating = [data['RoundRating'] for data in player_data]
    
    df['Place'] = player_place
    df['Player'] = player_names
    df['Total Par'] = total_to_par
    df['Rd'] = player_round_par
    df['Total'] = player_round_score
    df['Rd Rating'] = player_round_rating
    for row_idx, row_data in enumerate(hole_scores):
        for col_idx, value in enumerate(row_data):
            # Assuming 'df' is your DataFrame
            df.loc[row_idx, col_idx + 1] = value  # Adding 1 to col_idx because column indices start from 1

    return df

# Example usage:
url = 'https://www.pdga.com/apps/tournament/live-api/live_results_fetch_round?TournID=78194&Division=MPO&Round=3'
df = fetch_pga_data(url)

# Hide the DataFrame style
df.style.hide()
