# Getting kizlarsoruyor discussions

The project's goal is to retrieve all discussions relevant to a particular keyword from the Kizlarsoruyor website. Additionally, it aims to gather various attributes associated with each discussion thread, such as the date of posting, comments, and the gender of commenters. The code is designed to extract this information and present it in JSON format as the output.

### How it works?
After analyzing the website's structure, it becomes evident that the discussion results are structured in a paginated format. To be precise, the website displays 20 discussions per page, each enclosed within a div element bearing the "filter-section" class. The link to access the next page of discussions can be located within a div marked with the "show-more" class.

Moreover, to access comments within a discussion, user authentication is required. The comments are presented on the website in an unordered list format, specifically identified by the "comments-ul" class. Furthermore, the replies to these comments can be found within another unordered list, marked with the "comment-answers-ul" class.

Utilizing this information, we can retrieve all discussions from the provided website following the logic outlined in the following pseudocode:

```
while there is a next page:
    fetch the HTML content of the current page using a GET request
    for each discussion on the page:
        parse the discussion
        if the discussion contains comments:
            parse the comments
    obtain the URL of the next page
        
```

## The following classes are defined in the code:
### Session class

The Python code defines a class called Session that is designed to facilitate making HTTP requests using the requests library. It sets up a session with specific headers and cookies to mimic the behavior of a logged-in user when interacting with a website.

### Scrapper class

This Python code defines a class named Scrapper, which is designed to scrape and parse discussions and comments from the specified website.

Overall, this code is a web scraper designed to navigate through discussion pages on a website, extract relevant information about discussions and comments, and structure the data into a format that can be used for further analysis or storage, such as a list of dictionaries. It utilizes the requests library for making HTTP requests and BeautifulSoup for HTML parsing. Additionally, it handles errors that may occur during the scraping process and provides informative error messages.

#### Usage

To retrieve all the discussions along with their associated attributes, you can utilize the scrap_data function, which is defined as follows. This function takes a keyword as input and provides all the discussions and their respective details in JSON format. Additionally, the results are saved to a JSON file located in a predetermined directory.

```python
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
```

### The resulting json has the following structure:
```json
[
    {
        "topic": {
            "name": "Sa\u011fl\u0131k & Diyet",
            "url": "https://www.kizlarsoruyor.com/saglik"
        },
        "discussion": {
            "title": " Sizce Nestle Oral \u0130mpact Ne Kadar Etkili Olur? ",
            "content": "G\u00fcnde 1 ya da 2 tane Nestle Oral \u0130mpact i\u00e7iyorum. Sizce nas\u0131l bir i\u00e7ecek? 237 ml de 341 kalori bulunuyor.",
            "featured-image": "https://www.kizlarsoruyor.com/saglik/q11456969-sizce-nestle-oral-impact-ne-kadar-etkili-olur"
        },
        "posted-by": {
            "username": "DegdirenBerber",
            "gender": "male",
            "profile-link": "https://www.kizlarsoruyor.com/uye/degdirenberber"
        },
        "comments": [
            {
                "commenter": {
                    "username": "___Eyl\u00fcll___",
                    "profile-url": "https://www.kizlarsoruyor.com/uye/___eylull___",
                    "gender": "female"
                },
                "opinion": " Ne bu ",
                "replies": [
                    {
                        "commenter": {
                            "username": "DegdirenBerber",
                            "profile-url": "https://www.kizlarsoruyor.com/uye/degdirenberber",
                            "gender": "male"
                        },
                        "opinion": " \u0130\u00e7ecek \ud83e\udd14 Eczanelerde sat\u0131l\u0131yor "
                    },
                    {
                        "commenter": {
                            "username": "___Eyl\u00fcll___",
                            "profile-url": "https://www.kizlarsoruyor.com/uye/___eylull___",
                            "gender": "female"
                        },
                        "opinion": " Ne i\u00e7in ama "
                    },
                    {
                        "commenter": {
                            "username": "DegdirenBerber",
                            "profile-url": "https://www.kizlarsoruyor.com/uye/degdirenberber",
                            "gender": "male"
                        },
                        "opinion": " Ek g\u0131da i\u015fte "
                    }
                ]
            }
        ]
    },
    {
        "topic": {
            "name": "E\u011fitim & Kariyer",
            "url": "https://www.kizlarsoruyor.com/egitim-kariyer"
        },
        "discussion": {
            "title": " F\u0130NANS UZMANI MAA\u015eI NE KADAR ACABA? ? ",
            "content": "B\u00fcy\u00fck \u015firketlerde \u00e7al\u0131\u015fan sabanc\u0131 nestle pepsico ko\u00e7 \u00fclker tarz\u0131 yerlerde \u00e7al\u0131\u015fan finans uzman\u0131 ne kadar maa\u015f al\u0131r ortalama?",
            "featured-image": null
        },
        "posted-by": {
            "username": "anonymous user",
            "gender": "female",
            "profile-link": null
        },
        "comments": [
            {
                "commenter": {
                    "username": "kullanannnn",
                    "profile-url": "https://www.kizlarsoruyor.com/uye/kullanannnn",
                    "gender": "male"
                },
                "opinion": " 2, 3,, tok ",
                "replies": null
            }
        ]
    },
    ...
```

#### The scrap_data function can be conveniently used to fetch data from the given web site as shown below.


```python
from app import scrap_data
```


```python
scrapped_data = scrap_data('nestle')
```

    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=2&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=3&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=4&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=5&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=6&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=7&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=8&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=9&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=10&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=11&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=12&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=13&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=14&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=15&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=16&t=tumu
    Scrapping...  https://www.kizlarsoruyor.com/ara?q=nestle&p=17&t=tumu
    


```python
scrapped_data[0]
```




    {'topic': {'name': 'Sağlık & Diyet',
      'url': 'https://www.kizlarsoruyor.com/saglik'},
     'discussion': {'title': ' Sizce Nestle Oral İmpact Ne Kadar Etkili Olur? ',
      'content': 'Günde 1 ya da 2 tane Nestle Oral İmpact içiyorum. Sizce nasıl bir içecek? 237 ml de 341 kalori bulunuyor.',
      'featured-image': 'https://www.kizlarsoruyor.com/saglik/q11456969-sizce-nestle-oral-impact-ne-kadar-etkili-olur'},
     'posted-by': {'username': 'DegdirenBerber',
      'gender': 'male',
      'profile-link': 'https://www.kizlarsoruyor.com/uye/degdirenberber'},
     'comments': [{'commenter': {'username': '___Eylüll___',
        'profile-url': 'https://www.kizlarsoruyor.com/uye/___eylull___',
        'gender': 'female'},
       'opinion': ' Ne bu ',
       'replies': [{'commenter': {'username': 'DegdirenBerber',
          'profile-url': 'https://www.kizlarsoruyor.com/uye/degdirenberber',
          'gender': 'male'},
         'opinion': ' İçecek 🤔 Eczanelerde satılıyor '},
        {'commenter': {'username': '___Eylüll___',
          'profile-url': 'https://www.kizlarsoruyor.com/uye/___eylull___',
          'gender': 'female'},
         'opinion': ' Ne için ama '},
        {'commenter': {'username': 'DegdirenBerber',
          'profile-url': 'https://www.kizlarsoruyor.com/uye/degdirenberber',
          'gender': 'male'},
         'opinion': ' Ek gıda işte '}]}]}


