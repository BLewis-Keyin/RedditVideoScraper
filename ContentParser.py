import requests

url = "https://www.reddit.com/r/Asmongold/comments/16pa3wu/uber_eats_robots_deployed_in_us/.json"
headers = {'User-agent': 'VideoScraper 0.1'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)