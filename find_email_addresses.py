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

class EmailScraper():
  EMAIL_REGEX = re.compile(r'[\w+\-.]+@[a-z\d\-.]+\.[a-z]+')
  DELAY = 5

  def __init__(self, base_url):
    self.base_url = self.__format_url(base_url)
    self.to_visit = deque([self.base_url])
    self.visited = set()
    self.unique_emails = set()
    self.driver = webdriver.Firefox()

  def run(self):
    print("Found the following emails:")

    while len(self.to_visit) > 0:
      current_url = self.to_visit.popleft()

      self.driver.get(current_url)
      time.sleep(EmailScraper.DELAY) # Wait for page to load
      soup = bs4.BeautifulSoup(self.driver.page_source)

      self._parse_emails(soup)
      self._get_child_urls(soup)

    self.driver.close()

  def _get_child_urls(self, soup):
    href_tags = soup.select("a[href^=/]") # / for relative links

    for tag in href_tags:
      full_url = self.base_url + tag["href"]
      
      if tag["href"] not in self.visited:
        self.visited.add(full_url)
        self.to_visit.append(full_url)

  def _parse_emails(self, soup):
    emails = EmailScraper.EMAIL_REGEX.findall(soup.text)
    for email in emails:
      if email not in self.unique_emails:
        self.unique_emails.add(email)
        print(email)

  def _format_url(self, url):
    if "http://" not in url:
      url = "http://" + url

    return url

if __name__ == '__main__':
  if len(sys.argv) > 1:
    EmailScraper(sys.argv[1]).run()
  else:
    print("Please supply a URL")