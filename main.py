from flask import Flask, render_template, jsonify
import redis_db as db

app = Flask(__name__)

# Начальный экран
@app.route('/')
def index():
    random_quotes = db.get_random_quotes(10)
    return render_template('index.html', quotes=random_quotes)

# Получение всех цитат по категории
@app.route('/quotes/<category>', methods=['GET'])
def get_quotes_by_category(category):
    quotes = db.get_quotes_by_category(category)
    return jsonify(quotes)

# Получение случайной цитаты
@app.route('/random_quote', methods=['GET'])
def random_quote():
    random_quote = db.get_random_quote()
    return jsonify(random_quote)

if __name__ == '__main__':
    app.run(debug=True)
