# Uses the following libraries:
#   bs4 to find new links
#   re to create regular expression for emails
#   sys to get command line arguments
#   time to wait until HTML Document is fully loaded
#   deque to store which URLs to visit and traverse page breadth-first
#   selenium to receive HTML response
#   collections to store visited URLs and discovered emails
import bs4, re, sys, time
from selenium import webdriver 
from collections import deque

EMAIL_REGEX = re.compile(r'[\w+\-.]+@[a-z\d\-.]+\.[a-z]+')
DRIVER = webdriver.Firefox()
DELAY = 5

def scrape(url):
  base_url = url

  to_visit = deque([base_url])

  visited = set(base_url)
  unique_emails = set()

  print("Found the following emails")

  while len(to_visit) > 0:
    current_url = to_visit.popleft()

    DRIVER.get(current_url)
    time.sleep(DELAY) # Wait for page to load
    soup = bs4.BeautifulSoup(DRIVER.page_source)

    parse_emails(soup, unique_emails)
    get_child_urls(base_url, soup, to_visit, visited)

  DRIVER.close()

def get_child_urls(base_url, soup, to_visit, visited):
  href_tags = soup.select("a[href^=/]") # / for relative links

  for tag in href_tags:
    full_url = base_url + tag["href"]
    
    if tag["href"] not in visited:
      visited.add(full_url)
      to_visit.append(full_url)

def parse_emails(soup, unique_emails):
  emails = EMAIL_REGEX.findall(soup.text)
  for email in emails:
    if email not in unique_emails:
      unique_emails.add(email)
      print(email)

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