import logging
import random
import threading
import time

TOTAL_TICKETS: int = 10
MAX_SEATS: int = 50

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, condition: threading.Condition):
        super().__init__()
        self.sem = semaphore
        self.condition = condition
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self):
        global TOTAL_TICKETS
        is_running = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.getName()} sold one; {TOTAL_TICKETS} left')

                if TOTAL_TICKETS <= 5:
                    with self.condition:
                        self.condition.notify_all()

        logger.info(f'Seller {self.getName()} sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, condition: threading.Condition):
        super().__init__()
        self.sem = semaphore
        self.condition = condition
        logger.info('Director started work')

    def run(self):
        global TOTAL_TICKETS
        while True:
            with self.condition:
                self.condition.wait()
                with self.sem:
                    if TOTAL_TICKETS <= 5 and TOTAL_TICKETS + 6 <= MAX_SEATS:
                        TOTAL_TICKETS += 6
                        logger.info(f'Director added tickets. Now {TOTAL_TICKETS} tickets available')
                    elif TOTAL_TICKETS >= MAX_SEATS:
                        break


def main():
    semaphore = threading.Semaphore(1)
    condition = threading.Condition()

    director = Director(semaphore, condition)
    director.start()

    sellers = []
    for _ in range(3):
        seller = Seller(semaphore, condition)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()

    with condition:
        condition.notify_all()

    director.join()


if __name__ == '__main__':
    main()

