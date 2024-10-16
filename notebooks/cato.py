"""
cato.py

A simple wrapper for Cato API queries.
"""

import certifi
import gzip
import json
import ssl
import urllib.parse
import urllib.request



class API:
	"""
	Simple class to make API queries. Includes:

	* Automatic response compression.
	* Error handling.

	"""


	def __init__(self, key):
		"""
		Instantiate object with API key.
		"""
		self.key = key


	def send(self, operation, variables, query):
		"""
		Send an API request and return the response as a Python object.

		Returns a tuple consisting of a boolean success flag, and a Python object
		converted from the JSON response.
		"""
		body = json.dumps({
			"operationName": operation,
			"query":query,
			"variables":variables
		}).encode("ascii")
		headers = {
			"Content-Type": "application/json",
			"Accept-Encoding": "gzip, deflate, br",
			"X-api-key": self.key
		}
		try:
			request = urllib.request.Request(
				url='https://api.catonetworks.com/api/v1/graphql2',
				data=body,
				headers=headers
			)
			response = urllib.request.urlopen(
				request, 
				context=ssl.create_default_context(cafile=certifi.where()),
				timeout=10
			)
			response_data = gzip.decompress(response.read())
			response_obj = json.loads(response_data.decode('utf-8','replace'))
		except Exception as e:
			return False, {"error":f'{e}'}
		if "errors" in response_obj:
			return False, response_obj
		else:
			return True, response_obj

