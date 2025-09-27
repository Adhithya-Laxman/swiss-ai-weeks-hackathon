# # # web_scraper.py
# # from bs4 import BeautifulSoup
# # import requests
# # from urllib.parse import urljoin
# # from requests_html import HTMLSession

# # session = HTMLSession()

# # class DisasterNewsScraper:
# #     def __init__(self, sources):
# #         # sources is a dict like {"category": {"name": "url"}}
# #         self.sources = sources

# #     def scrape_all(self, category=None):
# #         all_news = {}
# #         target_sources = self.sources if not category else {category: self.sources.get(category, {})}
# #         for cat, sites in target_sources.items():
# #             all_news[cat] = {}
# #             for name, url in sites.items():
# #                 try:
# #                     news = self.scrape_site(url)
# #                     all_news[cat][name] = news
# #                 except Exception as e:
# #                     all_news[cat][name] = f"Error scraping {url}: {e}"
# #         return all_news

# #     # def scrape_site(self, url, max_items=10):
# #     #     headers = {'User-Agent': 'Mozilla/5.0'}  # To avoid blocking
# #     #     page = requests.get(url, headers=headers)
# #     #     page.raise_for_status()  # Raise error if not 200
# #     #     r = session.get(url)
# #     #     r.html.render(timeout=20,sleep=2)  # executes JavaScript
# #     #     soup = BeautifulSoup(r.html.html, "html.parser")

# #     #     # soup = BeautifulSoup(page.content, 'html.parser')
# #     #     print(soup)
# #     #     news_items = []
# #     #     # Generic selector; customize per site if needed (e.g., ReliefWeb uses 'article' tags)
# #     #     for item in soup.find_all(['article', 'div'], class_=['news-item', 'article', 'post'])[:max_items]:
# #     #         print(item)
# #     #         headline = item.find(['h1', 'h2', 'h3', 'a'])
# #     #         link = item.find('a', href=True)
# #     #         summary = item.find('p')  # Extract short summary if available
# #     #         if headline and link:
# #     #             title = headline.get_text(strip=True)
# #     #             href = link['href']
# #     #             if not href.startswith('http'):
# #     #                 href = urljoin(url, href)
# #     #             desc = summary.get_text(strip=True) if summary else ""
# #     #             news_items.append({'title': title, 'url': href, 'summary': desc})
# #     #     print(news_items)
# #     #     return news_items
# #     from urllib.parse import urlparse

# #     def scrape_site(self, url, max_items=10):
# #         from urllib.parse import urlparse
# #         headers = {'User-Agent': 'Mozilla/5.0'}
# #         r = session.get(url)
# #         r.html.render(timeout=20, sleep=2)
# #         soup = BeautifulSoup(r.html.html, "html.parser")
# #         print("SOUP: \n", soup)
# #         domain = urlparse(url).netloc

# #         news_items = []

# #         if "reliefweb.int" in domain:
# #             for article in soup.find_all("article", class_="rw-river-article")[:max_items]:
# #                 title_tag = article.find("h3", class_="rw-river-article__title")
# #                 link_tag = title_tag.find("a") if title_tag else None
# #                 status = article.find("dd", class_="rw-entity-meta__tag-value--status")
# #                 country = article.find("dd", class_="rw-entity-meta__tag-value--country")

# #                 if title_tag and link_tag:
# #                     news_items.append({
# #                         "title": title_tag.get_text(strip=True),
# #                         "url": urljoin(url, link_tag["href"]),
# #                         "status": status.get_text(strip=True) if status else "",
# #                         "country": country.get_text(strip=True) if country else ""
# #                     })

# #         else:
# #             # Fallback generic case
# #             for item in soup.find_all(['article', 'div'], class_=['news-item', 'article', 'post'])[:max_items]:
# #                 headline = item.find(['h1', 'h2', 'h3', 'a'])
# #                 link = item.find('a', href=True)
# #                 summary = item.find('p')
# #                 if headline and link:
# #                     href = link['href']
# #                     if not href.startswith('http'):
# #                         href = urljoin(url, href)
# #                     news_items.append({
# #                         'title': headline.get_text(strip=True),
# #                         'url': href,
# #                         'summary': summary.get_text(strip=True) if summary else ""
# #                     })

# #         return news_items

# # # Example integration with reliable_sources.py
# # if __name__ == "__main__":
# #     from reliable_sources import reliable_news_sources  # Import your sources dict
# #     scraper = DisasterNewsScraper(reliable_news_sources)
# #     news_data = scraper.scrape_all(category="Asia")  # Scrape only Asia for a user's locality
# #     print(news_data)  # Output: Dict of scraped data, ready for RAG processing


# # web_scraping.py
# from bs4 import BeautifulSoup
# import requests
# from urllib.parse import urljoin, urlparse
# from requests_html import HTMLSession

# session = HTMLSession()

# class DisasterNewsScraper:
#     def __init__(self, sources):
#         self.sources = sources

#     def scrape_all(self, category=None):
#         all_news = {}
#         target_sources = self.sources if not category else {category: self.sources.get(category, {})}
#         for cat, sites in target_sources.items():
#             all_news[cat] = {}
#             for name, url in sites.items():
#                 try:
#                     news = self.scrape_site(url)
#                     all_news[cat][name] = news
#                 except Exception as e:
#                     all_news[cat][name] = f"Error scraping {url}: {e}"
#         return all_news

#     def scrape_site(self, url, max_items=10):
#         headers = {'User-Agent': 'Mozilla/5.0'}
#         try:
#             r = session.get(url, headers=headers, timeout=15)
#             r.html.render(timeout=20, sleep=2)  # Render JavaScript if needed
#             soup = BeautifulSoup(r.html.html, "html.parser")
#         except Exception as e:
#             print(f"Request failed for {url}: {e}")
#             return []

#         domain = urlparse(url).netloc
#         news_items = []

#         if "reliefweb.int" in domain:
#             # Specific to ReliefWeb's structure (from your HTML)
#             for article in soup.find_all("article", class_="rw-river-article--card rw-river-article rw-river-article--disaster")[:max_items]:
#                 header = article.find("header", class_="rw-river-article__header")
#                 title_tag = header.find("h3", class_="rw-river-article__title") if header else None
#                 link_tag = title_tag.find("a") if title_tag else None

#                 footer = article.find("footer", class_="rw-river-article__footer")
#                 status_tag = footer.find("dd", class_="rw-entity-meta__tag-value--status") if footer else None
#                 country_tag = footer.find("dd", class_="rw-entity-meta__tag-value--country") if footer else None

#                 if title_tag and link_tag:
#                     title = title_tag.get_text(strip=True)
#                     href = urljoin(url, link_tag["href"])
#                     status = status_tag.get_text(strip=True) if status_tag else "N/A"
#                     country = country_tag.get_text(strip=True) if country_tag else "N/A"
#                     news_items.append({
#                         'title': title,
#                         'url': href,
#                         'status': status,
#                         'country': country
#                     })
#         else:
#             # Generic fallback for other sites
#             for item in soup.find_all(['article', 'div'], class_=['news-item', 'article', 'post', 'item'])[:max_items]:
#                 headline = item.find(['h1', 'h2', 'h3', 'a'])
#                 link = item.find('a', href=True)
#                 summary = item.find('p') or item.find('div', class_='snippet')
#                 if headline and link:
#                     title = headline.get_text(strip=True)
#                     href = urljoin(url, link['href'])
#                     desc = summary.get_text(strip=True) if summary else title  # Fallback to title if no summary
#                     news_items.append({
#                         'title': title,
#                         'url': href,
#                         'summary': desc
#                     })

#         if not news_items:
#             print(f"No items found for {url} - check selectors or page structure.")
#         return news_items

# # Example test
# if __name__ == "__main__":
#     from reliable_sources import reliable_news_sources
#     scraper = DisasterNewsScraper(reliable_news_sources)
#     news_data = scraper.scrape_all(category="Asia")
#     print(news_data)


# web_scraping.py
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
from requests_html import HTMLSession


session = HTMLSession()


class DisasterNewsScraper:
    def __init__(self, sources):
        self.sources = sources


    def scrape_all(self, category=None):
        all_news = {}
        target_sources = self.sources if not category else {category: self.sources.get(category, {})}
        for cat, sites in target_sources.items():
            all_news[cat] = {}
            for name, url in sites.items():
                try:
                    news = self.scrape_site(url)
                    all_news[cat][name] = news
                except Exception as e:
                    all_news[cat][name] = f"Error scraping {url}: {e}"
        return all_news


    # def scrape_site(self, url, max_items=10):
    #     headers = {'User-Agent': 'Mozilla/5.0'}
    #     try:
    #         r = session.get(url, headers=headers, timeout=15)
    #         r.html.render(timeout=20, sleep=2)  # Render JavaScript if needed
    #         soup = BeautifulSoup(r.html.html, "html.parser")
    #     except Exception as e:
    #         print(f"Request failed for {url}: {e}")
    #         return []


    #     domain = urlparse(url).netloc
    #     news_items = []


    #     if "reliefweb.int" in domain:
    #         # Specific to ReliefWeb's structure (from your HTML)
    #         for article in soup.find_all("article", class_="rw-river-article--card rw-river-article rw-river-article--disaster")[:max_items]:
    #             header = article.find("header", class_="rw-river-article__header")
    #             title_tag = header.find("h3", class_="rw-river-article__title") if header else None
    #             link_tag = title_tag.find("a") if title_tag else None


    #             footer = article.find("footer", class_="rw-river-article__footer")
    #             status_tag = footer.find("dd", class_="rw-entity-meta__tag-value--status") if footer else None
    #             country_tag = footer.find("dd", class_="rw-entity-meta__tag-value--country") if footer else None


    #             if (title_tag and link_tag) :
    #                 title = title_tag.get_text(strip=True)
    #                 href = urljoin(url, link_tag["href"])
    #                 status = status_tag.get_text(strip=True) if status_tag else "N/A"
    #                 country = country_tag.get_text(strip=True) if country_tag else "N/A"
    #                 # Additional check for the specified section class
    #                 description = ""
    #                 try:
    #                     # Fetch the individual article page
    #                     article_r = session.get(href, headers=headers, timeout=15)
    #                     article_r.html.render(timeout=20, sleep=2)
    #                     article_soup = BeautifulSoup(article_r.html.html, "html.parser")
    #                     # Search for the section with matching classes
    #                     overview_section = article_soup.find(
    #                         'section', 
    #                         class_="rw-entity-text--collapsible rw-entity-text--collapsible--last rw-entity-text rw-entity-text--overview"
    #                     )
    #                     if overview_section:
    #                         content_div = overview_section.find('div', id='overview-content')
    #                         if content_div:
    #                             description = content_div.get_text(strip=True)
    #                 except Exception as desc_e:
    #                     print(f"Error fetching description for {href}: {desc_e}")
                    
    #                 news_items.append({
    #                     'title': title,
    #                     'url': href,
    #                     'status': status,
    #                     'country': country,
    #                     'description': description  # Added field for the extracted content
    #                 })
    #     else:
    #         # Generic fallback for other sites
    #         for item in soup.find_all(['article', 'div'], class_=['news-item', 'article', 'post', 'item'])[:max_items]:
    #             headline = item.find(['h1', 'h2', 'h3', 'a'])
    #             link = item.find('a', href=True)
    #             summary = item.find('p') or item.find('div', class_='snippet')
    #             if headline and link:
    #                 title = headline.get_text(strip=True)
    #                 href = urljoin(url, link['href'])
    #                 desc = summary.get_text(strip=True) if summary else title  # Fallback to title if no summary
    #                 news_items.append({
    #                     'title': title,
    #                     'url': href,
    #                     'summary': desc
    #                 })


    #     if not news_items:
    #         print(f"No items found for {url} - check selectors or page structure.")
    #     return news_items

    def scrape_site(self, url, max_items=10):
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = session.get(url, headers=headers, timeout=15)
            r.html.render(timeout=20, sleep=2)  # Render JavaScript if needed
            soup = BeautifulSoup(r.html.html, "html.parser")
        except Exception as e:
            print(f"Request failed for {url}: {e}")
            return []


        domain = urlparse(url).netloc
        news_items = []


        if "reliefweb.int" in domain:
            # Specific to ReliefWeb's structure (from your HTML)
            for article in soup.find_all("article", class_="rw-river-article--card rw-river-article rw-river-article--disaster")[:max_items]:
                header = article.find("header", class_="rw-river-article__header")
                title_tag = header.find("h3", class_="rw-river-article__title") if header else None
                link_tag = title_tag.find("a") if title_tag else None


                footer = article.find("footer", class_="rw-river-article__footer")
                status_tag = footer.find("dd", class_="rw-entity-meta__tag-value--status") if footer else None
                country_tag = footer.find("dd", class_="rw-entity-meta__tag-value--country") if footer else None


                if title_tag and link_tag:
                    title = title_tag.get_text(strip=True)
                    href = urljoin(url, link_tag["href"])
                    status = status_tag.get_text(strip=True) if status_tag else "N/A"
                    country = country_tag.get_text(strip=True) if country_tag else "N/A"
                    news_items.append({
                        'title': title,
                        'url': href,
                        'status': status,
                        'country': country
                    })

            # New separate loop for the specified section class
            for section in soup.find_all("section", class_="rw-entity-text--collapsible rw-entity-text--collapsible--last rw-entity-text rw-entity-text--overview"):
                h2 = section.find("h2", class_="cd-block-title rw-entity-text__title")
                div = section.find("div", id="overview-content")
                if h2 and div:
                    section_title = h2.get_text(strip=True)
                    section_content = div.get_text(strip=True)
                    news_items.append({
                        'section_title': section_title,
                        'section_content': section_content
                    })
        else:
            # Generic fallback for other sites
            for item in soup.find_all(['article', 'div'], class_=['news-item', 'article', 'post', 'item'])[:max_items]:
                headline = item.find(['h1', 'h2', 'h3', 'a'])
                link = item.find('a', href=True)
                summary = item.find('p') or item.find('div', class_='snippet')
                if headline and link:
                    title = headline.get_text(strip=True)
                    href = urljoin(url, link['href'])
                    desc = summary.get_text(strip=True) if summary else title  # Fallback to title if no summary
                    news_items.append({
                        'title': title,
                        'url': href,
                        'summary': desc
                    })


        if not news_items:
            print(f"No items found for {url} - check selectors or page structure.")
        return news_items

# Example test
if __name__ == "__main__":
    from reliable_sources import reliable_news_sources
    scraper = DisasterNewsScraper(reliable_news_sources)
    news_data = scraper.scrape_all(category="Asia")
    print(news_data)
