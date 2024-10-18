import requests
import threading
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from werkzeug.serving import WSGIRequestHandler

logging.basicConfig(level=logging.DEBUG)

class APITester:
    def __init__(self, url, use_session=False, use_threads=False, http_1_1=False, num_requests=10):
        self.url = url
        self.use_session = use_session
        self.use_threads = use_threads
        self.num_requests = num_requests
        self.session = requests.Session() if use_session else None

        if http_1_1:
            WSGIRequestHandler.protocol_version = "HTTP/1.1"

    def make_request(self):
        """Отправляет запрос с использованием сессии или без неё."""
        if self.use_session:
            response = self.session.get(self.url)
        else:
            response = requests.get(self.url)
        return response.status_code

    def run_test(self):
        """Запускает тест с многопоточностью или без неё."""
        start_time = time.time()

        if self.use_threads:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(self.make_request) for _ in range(self.num_requests)]
                for future in futures:
                    future.result()
        else:
            for _ in range(self.num_requests):
                self.make_request()

        end_time = time.time()
        total_time = end_time - start_time
        return total_time

    def close_session(self):
        if self.session:
            self.session.close()

if __name__ == "__main__":
    url = "http://localhost:5000/api/books"

    configurations = [
        {"http_1_1": False, "use_session": False, "use_threads": False},  # -O -S -T
        {"http_1_1": False, "use_session": False, "use_threads": True},   # -O -S +T
        {"http_1_1": False, "use_session": True, "use_threads": False},   # -O +S -T
        {"http_1_1": False, "use_session": True, "use_threads": True},    # -O +S +T
        {"http_1_1": True,  "use_session": False, "use_threads": False},  # +O -S -T
        {"http_1_1": True,  "use_session": False, "use_threads": True},   # +O -S +T
        {"http_1_1": True,  "use_session": True, "use_threads": False},   # +O +S -T
        {"http_1_1": True,  "use_session": True, "use_threads": True},    # +O +S +T
    ]

    requests_counts = [10, 100, 1000]

    for num_requests in requests_counts:
        print(f"\nResults for {num_requests} requests:")
        for config in configurations:
            tester = APITester(
                url=url,
                use_session=config["use_session"],
                use_threads=config["use_threads"],
                http_1_1=config["http_1_1"],
                num_requests=num_requests
            )
            total_time = tester.run_test()
            print(f"Config -O: {not config['http_1_1']}, -S: {not config['use_session']}, -T: {not config['use_threads']} -> Time taken: {total_time:.2f} seconds")
            tester.close_session()
