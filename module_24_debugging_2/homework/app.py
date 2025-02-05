from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Метрика для отслеживания количества запросов
counter = metrics.counter(
    'request_count', 'Количество запросов на эндпоинт', labels={'code': lambda r: r.status_code}
)

@app.route('/metrics-test')
@counter
def test_endpoint():
    return "Hello, Prometheus!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
