import requests
from bs4 import BeautifulSoup

class MakeSoup():
    def __init__(self):
        self.collected_data = self.collect_data()

    def collect_data(self):
        response = requests.get("https://www.news24.com/news24/southafrica")
        news_24_data = response.text
        
        soup = BeautifulSoup(news_24_data, "html.parser")
        
        img_tags = soup.select(".article-item__image img")
        img_sources = []
        for tag in img_tags:
            source = tag.get("src")
            data_source = tag.get("data-src")
            if "https" in source:
                img_sources.append(source)
            else:
                img_sources.append(data_source)

        span_tags = soup.select(".article-item__title span")
        article_texts = [tag.string.strip() for tag in span_tags]
        
        p_tags = soup.select(".article-item__date")
        article_release_dates = [tag.string for tag in p_tags]

        article_data = list(zip(img_sources, article_texts, article_release_dates))
        arranged_article_data = {f"article{num + 1}": article_data[num] for num in range(len(article_data))}
        return arranged_article_data
        
makesoup = MakeSoup()
print(makesoup.collected_data)
    

