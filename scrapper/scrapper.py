import requests
from bs4 import BeautifulSoup




class Scrapper:
	session = None

	# Accepts an object of type Session.
	def __init__(self, session):
		self.session = session


	# The function accepts an object of type Session and returns the list of discussions.
	def parse_page(self):
		discussions_url = self.session.url

		result = []

		# Keep fetching discussions until we ran out of page.
		while True:
			print('Scrapping... ', discussions_url)

			try:
				# Make a GET request to fetch the discussions in the current page.
				response = self.session.get(discussions_url)

				# Parse the page.
				soup = BeautifulSoup(response.text, 'html.parser')

				# Get all discussions in the current page.
				# (The results of the page are wrapped in a div with filter-section class)
				discussions = soup.find('div', class_='filter-section')

				# parse discussions
				try:
					_ = self.parse_discussions(discussions, result)
				except Exception as e:
					print(f"Error parsing discussions: {e}")
					break

				# Get the div containing the URL of the next page.
				show_more_div = discussions.find('div', class_='show-more')

			except requests.exceptions.RequestException as e:
				print(f"Error fetching {discussions_url}: {e}")
				break

			# If all pages have been explored, then stop.
			if not show_more_div:
				break

			# Get URL of the next page.
			discussions_url = show_more_div.find('a')['href']

		return result
	

	def parse_discussions(self, discussions, result=[]):
		# I am interested in the topic the discussion belongs to.
		# The user who started the discussion.
		# The gender of the user.
		# The actual content of the discussion.
		# This includes the question header, actual question, featured image and comments.

		# Todo fetch all comment details of a discussion.

		# Get all questions.
		questions = discussions.find_all('div', class_='question')

		for question in questions:
			data = {}

			# Extract the topic and its co-oresponding link.
			topic = question.find('div', class_='colgag-topics').find('a')
			data['topic'] = {
			'name': topic.text,
			'url': topic['href']
			}

			# Extract the question title and its content.
			question_header = question.find('div', class_='list-item-content')
			# Extract any image if any
			image = question.find('div', class_='featured-image')
			data['discussion'] = {
				'title': question_header.find('h3', class_='content-title').text,
				'content': question_header.find('div', class_='details').text,
				'featured-image': image.find('a')['href'] if image else None
			}

			# Extract the user details
			user = question.find('div', class_='user-info')
			user_details = user.find('div', class_='info').find('a', class_='username')
			data['posted-by'] = {
				'username': user_details.text if user_details else 'anonymous user',
				'gender': 'male' if 'guy' in user.get('class') else 'female',
				'profile-link': user_details['href'] if user_details else None
			}

			# Extract the comment urls
			comments_url = question.find('span', class_='ibar-opcounters').find('a')['href']
			try:
				response = self.session.get(comments_url)
				if response.status_code == 200:
					comments = self.parse_comments(BeautifulSoup(response.text, 'html.parser') )
					data['comments'] = comments
			except requests.exceptions.RequestException as e:
				print(f"Error fetching {comments_url}: {e}")
				break

			result.append(data)

		return result


	# Fetch all comments to a discussion.
	def parse_comments(self, comments_page):
		# All comments are enclosed inside divs with class "comments-ul"
		result = []

		comment_lists = comments_page.find_all('ul', class_='comments-ul')
		for comment_list in comment_lists:
			comments = comment_list.find_all('article', class_='g-g-answer')
			for comment in comments:
				user_details = {}

				# Fetch the user details of the commenter.
				user = comment.find('a', class_='name')
				user_details['username'] = user.text if user else 'Private Member'
				user_details['profile-url'] = user['href'] if user else None
				user_details['gender'] = 'male' if comment.find_parent('li', class_='guy') else 'female'

				# Fetch all the replies to the comment if any.
				comment_answers = comment.find('ul', class_='comment-answers-ul')

				replies = None
				if comment_answers:
					replies = self.parse_replies(comment_answers)

				result.append({
					'commenter': user_details,
					'opinion': comment.find('div', class_='opinion-body').text,
					'replies': replies
				})

		return result


	# Fetch all replies to a comment.
	def parse_replies(self, comment_answers):
		result = []
		for comment in comment_answers.find_all('div', class_='g-g-comment-answer'):
			user_details = {}

			# Fetch the user details of the commenter.
			user = comment.find('a', class_='username')
			user_details['username'] = user.text if user else 'Private Member'
			user_details['profile-url'] = user['href'] if user else None
			user_details['gender'] = 'male' if comment.find_parent('li', class_='guy') else 'female'

			result.append({
				'commenter': user_details,
				'opinion': comment.find('div', class_='opinion-body').text
			})

		return result