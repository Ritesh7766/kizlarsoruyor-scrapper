import requests
from sessions.config import COOKIES


class Session:
    headers = None
    session = None
    url = None

    def __init__(self, keyword):
         # Set the URL
        self.url = f'https://www.kizlarsoruyor.com/ara?q={keyword}'

        self.session = requests.Session()

        # Perform an initial GET request to the page to obtain the CSRF token
        response = self.session.get(self.url)
        
        # Extract the CSRF token from the response headers
        csrf_token = response.headers.get('csrf-token')

        # Create headers with the CSRF token
        self.headers = {
            'User-Agent': 'Your User Agent',  # Set your user agent
            'csrf-token': csrf_token,  # Include the CSRF token in the headers
        }

        # Add the cookies to the session's cookie jar
        for name, value in COOKIES.items():
            self.session.cookies.set(name, value)

    
    # Make a get request with the current session
    def get(self, url):
        return self.session.get(url, headers=self.headers)