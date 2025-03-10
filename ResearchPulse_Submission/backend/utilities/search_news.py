from GoogleNews import GoogleNews


class SearchNews:
    def __init__(self):
        pass

    def fetch_top_news(self, query, num_results=1):
        googlenews = GoogleNews(lang='en', period='7d')
        googlenews.clear()
        googlenews.search(query + " Europe")  # Explicitly mention Europe in query
        news_results = googlenews.results(sort=True)[:num_results]

        search_info = ""
        for idx, article in enumerate(news_results, start=1):
            search_info += f"{idx}. Title: {article['title']}\n"
            search_info += f"Link: {article['link']}\n"
            search_info += f"Date: {article['date']}\n"
            search_info += "-"*20 + "\n"

        return search_info