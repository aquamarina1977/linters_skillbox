import threading
import time
import random
from queue import PriorityQueue

class Task:
    def __init__(self, priority, function, *args):
        self.priority = priority
        self.function = function
        self.args = args

    def __lt__(self, other):
        return self.priority < other.priority

    def run(self):
        print(f'>running Task(priority={self.priority}).\t{self.function.__name__}{self.args}')
        self.function(*self.args)

class Producer(threading.Thread):
    def __init__(self, queue: PriorityQueue, num_tasks: int):
        super().__init__()
        self.queue = queue
        self.num_tasks = num_tasks

    def run(self):
        print("Producer: Running")
        for i in range(self.num_tasks):
            priority = random.randint(0, 6)
            task = Task(priority, time.sleep, random.random())
            self.queue.put(task)
        print("Producer: Done")

class Consumer(threading.Thread):
    def __init__(self, queue: PriorityQueue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("Consumer: Running")
        while not self.queue.empty():
            task = self.queue.get()
            task.run()
            self.queue.task_done()
        print("Consumer: Done")

def main():
    task_queue = PriorityQueue()

    num_tasks = 10

    producer = Producer(task_queue, num_tasks)
    consumer = Consumer(task_queue)

    producer.start()
    producer.join()

    consumer.start()
    consumer.join()

if __name__ == '__main__':
    main()
