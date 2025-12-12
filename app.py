from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# API-ключ и город (можно задать через переменные окружения)
API_KEY = os.getenv('WEATHER_API_KEY', 'your_api_key_here')
CITY = os.getenv('CITY', 'Moscow')

@app.route('/')
def get_weather():
    try:
        # Отправляем запрос к OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            return jsonify({
                'city': CITY,
                'temperature': temp,
                'unit': '°C',
                'status': 'success'
            })
        else:
            return jsonify({
                'error': 'Не удалось получить данные о погоде',
                'status': 'error'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': f'Произошла ошибка: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'работает'}), 200

if __name__ == '__main__':
    # Запускаем приложение на всех интерфейсах (0.0.0.0) и порту 5000
    app.run(host='0.0.0.0', port=5000)
