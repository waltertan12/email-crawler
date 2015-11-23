# Email Scraper

### Description

A command line utility to scrape emails from a web page using Python 3.4.3. You can download Python3 [here](https://www.python.org/downloads/). If you're not sure what version of Python you're using, type `$ python --version` or `$ python3 --version` in the terminal.

It's dependent on the following external libraries:
- Beautiful Soup
- Selenium

### Setup

To install the libraries, type the following in the terminal:
````bash
$ sudo pip3 install beautifulsoup4
$ sudo pip3 install selenium
````
This implementation also requires Firefox to be installed on the computer. If you don't have Firefox, you can download it [here](https://www.mozilla.org/en-US/firefox/desktop/).

#### Approach and Limitations
This crawler traverses the relative links of a URL. For example, given `website.com`, the crawler will only continue to search pages with URLs of the form `website.com/some/other/page` if there is a tag `<a href="/some/other/page"></a>`.

Because this crawler relies on anchor tags with a hypertext reference beginning with a `/`, this crawler is unable to pick up clickable links provided by some front-end frameworks. More specifically, it is unable to traverse `ng-click="ChanceRoute("some/route")"` and hash routes `<a href="#/some/route"></a>`.

### Parallelization
**Using EmailScraper**

Here are some considerations trying parallelizing the EmailScraper class (runners, in the context, is an instance of the EmailScraper):
- How many runners should be sent out?
- What are the starting positions / URLs of each runner
- Can each runner produce more runners? Or is there a set number?
- How do we prevent runners from crawling over URLs a different runner has already crawled?

In a simple approach, we could create a set number of EmailScraper instances each with a differing starting URL, then let them crawl. To prevent rework, we could create a Hash Set and store it as a class variable. Each instance could then check the shared Hash Set before adding new URLs to crawl. *Note: There might be collisions or race-conditions if two crawlers try to add the same URL at the same time. These would need to be resolved.*

Deciding the starting URLs of each EmailScraper is fairly challenging. The goal might be to have each one start as far away from each other as possible. However, this requires some knowledge of the web and might not be feasible.

Memory may also prove to be an issue. The Hash Set storing all unique URLs would potentially have to store every URL on the web. Storing all that information in Python memory does not sound like a great idea. I have not really worked with Redis or MongoDB, but storing URLs in a database might be more reasonable. Compressing the URLs might also be a viable option to reduce memory.

**Other Methods**

The previous approach relies on using the EmailScraper class. However, there might be a better method that has a completely different approach. For example, maybe instead of having each individual crawler decide which URLs it needs to crawl, we could create a dispatcher which gives the crawlers a list of URLs scrape.