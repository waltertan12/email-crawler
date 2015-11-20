# Uses the following libraries:
#   request to get HTML response
#   bs4 to find new links
#   re to create regular expression for emails
#   sys to get command line arguments
#   deque to store which URLs to visit and traverse page breadth-first
#   collections to store visited URLs and discovered emails
import requests, bs4, re, sys 
from collections import deque

EMAIL_REGEX = r'[\w+\-.]+@[a-z\d\-.]+\.[a-z]+'

def scrape(url):
  base_url = url

  to_visit = deque([base_url])

  visited = set(base_url)
  unique_emails = set()

  while len(to_visit) > 0:
    current_url = to_visit.popleft()
    get_child_urls
    response = requests.get(current_url)
    print(response.text)

def get_child_urls(base_url, response, to_visit, visited):
  soup = bs4.BeautifulSoup(response.text)
  href_tags = soup.select("a[href^=/]") # / for relative links

  for tag in href_tags:
    full_url = base_url + tag["href"]
    
    if tag["href"] not in visited:
      visited.add(full_url)
      to_visit.append(full_url)

def parse_emails():
  pass

def format_url(url):
  if "http://" not in url:
    url = "http://" + url

  return url

if __name__ == '__main__':
  if len(sys.argv) > 1:
    url = format_url(sys.argv[1])
    scrape(url)
  else:
    print("Please supply a URL")