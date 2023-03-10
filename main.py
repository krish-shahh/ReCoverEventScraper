import requests
from bs4 import BeautifulSoup
import json

# Create an empty list to store the event data
event_data = []

id_counter = 1

# Loop through multiple pages
for i in range(1, 20):   # Loop through the first 3 pages

    # Make a request to the website
    url = f'https://www.eventbrite.com/d/online/addiction-recovery/?page={i}'
    response = requests.get(url)

    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all event cards on the page
    event_cards = soup.find_all('div', {'class': 'search-event-card-wrapper'})

    # Loop through each event card and extract the desired data
    for j, card in enumerate(event_cards):
        event_name = card.find('div', {'class': 'eds-event-card__formatted-name--is-clamped eds-event-card__formatted-name--is-clamped-three eds-text-weight--heavy'}).text.strip()
        event_organizer_elem = card.find('div', {'data-subcontent-key': 'organizerName'})
        event_organizer = event_organizer_elem.text.strip() if event_organizer_elem is not None else 'N/A'
        event_date_elem = card.find('div', {'class': 'eds-event-card-content__sub-title eds-text-color--primary-brand eds-l-pad-bot-1 eds-l-pad-top-2 eds-text-weight--heavy eds-text-bm'})
        event_date = event_date_elem.text.strip().split('(')[0] if event_date_elem is not None else 'N/A'
        event_url_elem = card.find('a', {'class': 'eds-event-card-content__action-link'})
        event_url = event_url_elem['href'] 

        # Print the data
        # print('Event Name:', event_name)
        # print('Event Date:', event_date)
        # print('Event Url:', event_url)
        # print('\n')

        # Create a dictionary of the event data and append it to the event_data list
        event_dict = {
            'id': id_counter,
            'name': event_name,
            'host': event_organizer,
            'date': event_date,
            'url': event_url
        }
        event_data.append(event_dict)

        id_counter += 1

# Save the event data to a JSON file
with open('event_data.json', 'w') as f:
    json.dump(event_data, f)
