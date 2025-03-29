import random
import redis
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Загрузка необходимых моделей для NLP
nltk.download('vader_lexicon')
nltk.download("punkt")

sia = SentimentIntensityAnalyzer()

# Подключение к Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

CATEGORIES = [
    "любовь",
    "жизнь",
    "мудрость",
    "успех",
    "мотивация"
]

MOODS = ["positive", "negative", "neutral"]

# Функция для получения цитат с сайта (пример для https://quotes.toscrape.com/)
def get_quotes():
    url = "https://statham.fun/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = []
    for quote_block in soup.find_all("div", class_="quote"):
        text = quote_block.text.strip()
        quotes.append(text)

    print(f'Quotes got: {len(quotes)}')
    return quotes

# Функция для определения настроения цитаты
def choose_mood_and_tag():
    tag = random.choice(CATEGORIES)
    mood = random.choice(MOODS)
    return tag, mood

# Основная функция обработки
def process_quotes():
    redis_client.flushdb()  # Очищаем Redis перед загрузкой

    quotes = get_quotes()

    for i, quote in enumerate(quotes):
        category, sentiment = choose_mood_and_tag()

        # Сохраняем цитату как хэш в Redis
        quote_id = f"quote:{i}"
        redis_client.hset(quote_id, mapping={
            "text": quote,
            "category": category,
            "sentiment": sentiment
        })

        # Добавляем идентификатор цитаты в множество для соответствующей категории
        redis_client.sadd(f"category:{category}", quote_id)

        # Добавляем идентификатор цитаты в множество для соответствующей тональности
        redis_client.sadd(f"sentiment:{sentiment}", quote_id)

    print(f"Загружено {len(quotes)} цитат в Redis.")

# Запуск скрипта
if __name__ == "__main__":
    process_quotes()
