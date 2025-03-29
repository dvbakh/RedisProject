import random
import redis
import requests
from bs4 import BeautifulSoup

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

CATEGORIES = [
    "любовь",
    "жизнь",
    "мудрость",
    "успех",
    "мотивация"
]

MOODS = ["positive", "negative", "neutral"]

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

# В итоге просто случайное определение
def choose_mood_and_tag():
    tag = random.choice(CATEGORIES)
    mood = random.choice(MOODS)
    return tag, mood

def process_quotes():
    # Очищаем Redis перед загрузкой
    redis_client.flushdb()

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

        # Добавляем id цитаты в множество для соответствующей категории
        redis_client.sadd(f"category:{category}", quote_id)

        # Добавляем id цитаты в множество для соответствующей тональности
        redis_client.sadd(f"sentiment:{sentiment}", quote_id)

    print(f"Загружено {len(quotes)} цитат в Redis.")

if __name__ == "__main__":
    process_quotes()
