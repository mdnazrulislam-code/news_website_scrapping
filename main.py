import pandas as pd
import requests
from bs4 import BeautifulSoup

pages = 1

articles = []
categories = ['news', 'metro-plus', 'video', 'sports', 'politics']
for category in categories:
    for page in range(1, pages+1):
        url = f'https://punchng.com/topics/{category}/'
        response = requests.get(url).text

        soup = BeautifulSoup(response, 'html.parser')
        article_container = soup.find('div', class_='latest-news-timeline-section')

        article_temp = article_container.find_all_next('article')

        for article in article_temp:
            title = article.find('h1', 'post-title').text.strip().replace(' ', '')
            excerpt = article.find('p', 'post-excerpt').text.strip().replace(' ', '')
            date = article.find('span', 'post-date').text.strip()
            link = article.find('a')['href']

            articles.append({
                'category': category,
                'title': title,
                'excerpt': excerpt,
                'date': date,
                'link': link
            })

        for article in articles:
            article_page = requests.get(article['link']).text.strip()

            article_soup = BeautifulSoup(article_page, 'html.parser')
            article['author'] = article_soup.find('span', class_='post-author').text.strip().replace('By  ', '')
            article['content'] = article_soup.find('div', class_='post-content').text.strip().replace(' ', '')
            if article_soup.find('div', class_='post-image-wrapper') is None:
                article['image'] = ''
            else:
                article['image'] = article_soup.find('div', class_='post-image-wrapper').find_next('figure').find_next('img')['src']
        print(f'Page {page} completed' )
    print(f'Category {category} completed')
punch_df = pd.DataFrame(articles)
punch_df.to_csv('punch.csv', index=False)
print('Done')