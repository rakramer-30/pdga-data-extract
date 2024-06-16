from bs4 import BeautifulSoup
import requests
import pandas as pd

def fetch_pdga_data(url, output_csv_file):
    # Make the request to the URL
    page = requests.get(url)
    
    # Check if the request was successful
    if page.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page.text, 'html.parser')

        # Extract additional event information
        event_name_div = soup.find('div', class_='pane-page-title').text
        event_name = event_name_div.strip()

        event_date_list = soup.find('li', class_='tournament-date').text
        event_year = event_date_list.split('-')[-1].strip()

        event_location_list = soup.find('li', class_='tournament-location').text
        location_parts = event_location_list.replace('Location: ', '').split(',')
        event_city = location_parts[0].strip()
        event_state = location_parts[1].strip()
        event_country = location_parts[2].strip()

        # Find the table you would like to analyze
        pdga = soup.find('table', class_='results')

        # Continue down the HTML tree to find the column titles
        pdga_thead = pdga.find('thead')
        pdga_columns = pdga_thead.find_all('th')
        pdga_column_titles = [columns.text for columns in pdga_columns]
        new_titles = []

        # Since the Rd Ratings are hidden, iterate over the empty
        # strings to give these columns a title
        empty_counter = 0

        for title in pdga_column_titles:
            if title == '':
                empty_counter += 1
                if empty_counter == 1:
                    new_titles.append('Rd1 Rating')
                elif empty_counter == 2:
                    new_titles.append('Rd2 Rating')
                elif empty_counter == 3:
                    new_titles.append('Rd3 Rating')
                elif empty_counter == 4:
                    new_titles.append('FinalRd Rating')
                else:
                    new_titles.append(title)
            else:
                new_titles.append(title)

        # Find all table rows (tr) of data in the original table                    
        pdga_rows = pdga.find_all('tr')

        # Collect all the table data
        data = []
        for row in pdga_rows[1:]:
            row_data = row.find_all('td')
            individual_row_data = [data.text for data in row_data]
            data.append(individual_row_data)
        
        # Convert to a DataFrame
        df = pd.DataFrame(data, columns=new_titles)
        
        # Add the additional event information to each row
        df['Event'] = event_name
        df['Year'] = event_year
        df['City'] = event_city
        df['State'] = event_state
        df['Country'] = event_country
        
        # Save the DataFrame to a CSV file
        df.to_csv(output_csv_file, index=False)
        print(f"Data saved to {output_csv_file}")
        
        return df
    else:
        print(f"Failed to retrieve data: Status code {page.status_code}")
        return None

# URL to fetch the data from and what to save the CSV file as
url = 'https://www.pdga.com/tour/event/77763'
output_csv_file = 'pdga_event_data.csv'

# Call the function and save the DataFrame to a CSV file
pdga_df = fetch_pdga_data(url, output_csv_file)

# Print the DataFrame
print(pdga_df)
