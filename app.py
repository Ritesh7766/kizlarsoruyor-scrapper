from sessions.sessions import Session
from scrapper.scrapper import Scrapper
import json


# Retured the scrapped data in json format.
def scrap_data(keyword):
    # Create a session
    session = Session(keyword)

    # Create a web scrapper for the given website
    scrapper = Scrapper(session)
    
    data = scrapper.parse_page()

    # Store the results in a json file.
    with open(f'./results/discussions_{keyword}.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Scrapped data can be found in ./results/discussions_{keyword}.json")
    return data


if __name__ == '__main__':
    scrap_data(keyword='nestle')