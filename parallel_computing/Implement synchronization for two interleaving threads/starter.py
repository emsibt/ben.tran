"""
Đoạn code trên chạy ra kết quả đúng, nhưng nó cực kỳ tốn tài nguyên. Giả sử Thread-2 (chẵn) được Hệ điều hành cho chạy trước. Nó thấy self.current đang là 1, không phải số chẵn. Thay vì đi ngủ để nhường CPU cho Thread-1, nó lại chạy vòng lặp while hàng triệu lần một giây chỉ để hỏi đi hỏi lại: "Đã đến số 2 chưa? Chưa à? Đã đến số 2 chưa?...". Điều này làm quạt tản nhiệt máy tính của bạn rống lên vì CPU phải làm việc vô ích.
"""

import threading


class BusyWaitPrinter:
    def __init__(self, limit):
        self.limit = limit
        self.cur = 1

    def print_odd(self):
        while self.cur <= self.limit:
            if self.cur % 2 != 0:
                print(f"[{threading.current_thread().name}] Odd: {self.cur}")
                self.cur += 1

    def print_even(self):
        while self.cur <= self.limit:
            if self.cur % 2 == 0:
                print(f"[{threading.current_thread().name}] Even: {self.cur}")
                self.cur += 1


# --- Test the Buggy Code ---
printer = BusyWaitPrinter(10)

# Thread-1 prints Odds, Thread-2 prints Evens
t1 = threading.Thread(target=printer.print_odd, name="Thread-1")
t2 = threading.Thread(target=printer.print_even, name="Thread-2")

t1.start()
t2.start()

t1.join()
t2.join()
