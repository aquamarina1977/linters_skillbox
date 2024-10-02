
import threading
import time
import requests
from queue import Queue

log_queue = Queue()

def get_date_from_server(timestamp):
    try:
        response = requests.get(f'http://127.0.0.1:8080/timestamp/{timestamp}')
        if response.status_code == 200:
            return response.text.strip()
    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {e}"
    return None

def worker(thread_id, log_queue):
    end_time = time.time() + 20
    while time.time() < end_time:
        timestamp = time.time()
        date = get_date_from_server(int(timestamp))
        if date:
            log_entry = f"{timestamp} {date}"
            log_queue.put((timestamp, log_entry))
        time.sleep(1)

def log_writer(log_queue):
    with open('log.txt', 'w') as log_file:
        while True:
            try:
                timestamp, log_entry = log_queue.get(timeout=30)
                log_file.write(log_entry + "\n")
                log_queue.task_done()
            except:
                break

def start_threads():
    writer_thread = threading.Thread(target=log_writer, args=(log_queue,), daemon=True)
    writer_thread.start()

    threads = []
    for i in range(10):
        thread = threading.Thread(target=worker, args=(i, log_queue))
        thread.start()
        threads.append(thread)
        time.sleep(1)

    for thread in threads:
        thread.join()

    log_queue.join()

if __name__ == "__main__":
    start_threads()
