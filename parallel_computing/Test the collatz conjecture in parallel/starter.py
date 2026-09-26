"""
Mặc dù code chạy đúng và không bị lỗi dữ liệu, nhưng hiệu năng của nó cực kỳ tồi tệ. Khối with self.lock: nằm ngay bên trong vòng lặp while True. Nếu một số mất 100 bước để giảm về 1, luồng đó phải tranh giành khóa và mở khóa đúng 100 lần. Với 4 luồng chạy cùng lúc, hệ thống dành 99% thời gian để "chờ nhường đường" thay vì làm toán. Chạy đa luồng kiểu này thậm chí còn chậm hơn chạy đơn luồng (single-thread).
"""

import threading
import time


class BuggyCollatz:
    def __init__(self):
        # 1 is already verified
        self.verified = {1}
        self.lock = threading.Lock()

    def worker(self, start, end):
        for i in range(start, end + 1):
            n = i
            while True:
                # BAD: Acquiring the global lock at EVERY SINGLE mathematical step!
                # This causes massive lock contention between threads.
                with self.lock:
                    if n in self.verified:
                        break
                    self.verified.add(n)

                # Math logic
                if n % 2 == 0:
                    n = n // 2
                else:
                    n = 3 * n + 1


# --- Test the Buggy Implementation ---
buggy_tester = BuggyCollatz()
threads = []

start_time = time.time()

# 4 Threads testing numbers from 1 to 20,000
for i in range(4):
    t = threading.Thread(
        target=buggy_tester.worker, args=(i * 5000 + 1, (i + 1) * 5000)
    )
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Buggy Execution Time: {time.time() - start_time:.3f} seconds")
