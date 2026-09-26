"""
hi áp dụng đoạn mã này, kết quả sẽ luôn luôn chuẩn xác là 2,000,000 bất kể bạn chạy bao nhiêu lần. Thread-1 bước vào khối with self.lock, cánh cửa đóng lại, nó thong thả đọc - cộng - ghi. Thread-2 dù có được cấp CPU đi nữa cũng chỉ có thể đứng chờ ngoài cửa cho đến khi Thread-1 làm xong toàn bộ chuỗi hành động và nhả khóa ra.
"""

import threading


class SynchronizedCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        for _ in range(1000000):
            # Lock ensures that Read, Add, and Write happen without interruption
            with self.lock:
                self.count += 1


# --- Test the Fixed Code ---
safe_counter = SynchronizedCounter()

t1 = threading.Thread(target=safe_counter.increment, name="Thread-1")
t2 = threading.Thread(target=safe_counter.increment, name="Thread-2")

t1.start()
t2.start()

t1.join()
t2.join()

print(f"Fixed final count: {safe_counter.count} (Expected: 2000000)")
