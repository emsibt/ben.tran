"""
Khi Thread-2 (chẵn) vào trước, nó thấy 1 % 2 != 0. Nó gọi self.condition.wait(). Lệnh này lập tức cho Thread-2 đi ngủ và tạm thời nhả khóa ra. CPU lúc này nhàn rỗi 100%.
Thread-1 (lẻ) vào, in ra số 1, tăng lên 2, rồi gọi self.condition.notify(). Lệnh này đánh thức Thread-2 dậy.
Việc nhường - nhận giữa 2 thread diễn ra tuần tự, hoàn hảo mà không lãng phí bất kỳ chu kỳ CPU nào.
"""

import threading


class SynchronizedPrinter:
    def __init__(self, limit):
        self.limit = limit
        self.cur = 1
        self.condition = threading.Condition()

    def print_odd(self):
        while self.cur <= self.limit:
            with self.condition:
                # If it's an even number, it's not my turn. Go to sleep.
                while self.cur % 2 == 0 and self.cur <= self.limit:
                    self.condition.wait()

                if self.cur <= self.limit:
                    print(f"[{threading.current_thread().name}] Odd: {self.cur}")
                    self.cur += 1
                    # Wake up the other thread
                    self.condition.notify()

    def print_even(self):
        while self.cur <= self.limit:
            with self.condition:
                # If it's an odd number, it's not my turn. Go to sleep.
                while self.cur % 2 != 0 and self.cur <= self.limit:
                    self.condition.wait()
            
                if self.cur <= self.limit:
                    print(f"[{threading.current_thread().name}] Even: {self.cur}")
                    self.cur += 1
                    # Wake up the other thread
                    self.condition.notify()


# --- Test the Buggy Code ---
printer = SynchronizedPrinter(10)

# Thread-1 prints Odds, Thread-2 prints Evens
t1 = threading.Thread(target=printer.print_odd, name="Thread-1")
t2 = threading.Thread(target=printer.print_even, name="Thread-2")

t1.start()
t2.start()

t1.join()
t2.join()
