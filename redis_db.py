import redis
import random

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Функция для получения всех цитат по категории
def get_quotes_by_category(category):
    # Получаем все идентификаторы цитат для категории из Redis Set
    quote_ids = redis_client.smembers(f"category:{category}")

    quotes = []

    for quote_id in quote_ids:
        # Получаем данные для каждой цитаты
        quote_data = redis_client.hgetall(quote_id)
        print(f"Data for {quote_id}: {quote_data}")

        # Добавляем их в список
        if quote_data:
            quotes.append({
                'id': quote_id,
                'text': quote_data.get("text"),
                'category': quote_data.get("category"),
                'sentiment': quote_data.get("sentiment")
            })
        else:
            print(f"No data found for quote {quote_id}")

    return quotes

# Функция для получения случайной цитаты
def get_random_quote():
    # Получаем все ключи с цитатами
    keys = redis_client.keys(f"quote:*")

    # Выбираем случайный
    random_key = random.choice(keys)

    # Получаем данные из Redis
    quote_data = redis_client.hgetall(random_key)

    return {
        'text': quote_data.get("text"),
        'category': quote_data.get("category"),
        'sentiment': quote_data.get("sentiment")
    }
# Функция для получения случайных 10 цитат (для начального экрана)
def get_random_quotes(num_quotes=10):
    # Получаем все ключи с цитатами
    keys = redis_client.keys("quote:*")

    random_keys = random.sample(keys, min(num_quotes, len(keys)))

    quotes = []
    for key in random_keys:
        quote_data = redis_client.hgetall(key)
        quotes.append({
            'text': quote_data.get("text"),
            'category': quote_data.get("category"),
            'sentiment': quote_data.get("sentiment")
        })

    return quotes
