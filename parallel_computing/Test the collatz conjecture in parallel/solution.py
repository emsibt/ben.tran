"""
Khi bạn chạy thử, bạn sẽ thấy Fixed Execution Time nhanh hơn gấp nhiều lần so với bản Buggy.
Bằng cách dùng local_path, luồng tính toán hoàn toàn tự do thực hiện các phép chia và nhân trong không gian riêng của nó mà không bị ai cản trở. Việc sử dụng update() cho phép Python chèn hàng chục con số vào bộ nhớ chung bằng tốc độ của ngôn ngữ C bên dưới, giúp thời gian luồng giữ Lock chỉ tính bằng micro-giây.
"""

import threading
import time


class EfficientCollatz:
    def __init__(self):
        self.global_verified = {1}
        self.lock = threading.Lock()

    def worker(self, start, end):
        for i in range(start, end + 1):
            n = i
            # Thread-local storage to keep track of the current sequence
            local_path = set()

            while n != 1:
                # OPTIMIZATION 1: Only check global cache if n dips below our starting number i.
                # Numbers >= i are likely unexplored, so we don't waste time locking to check them.
                if n < i:
                    with self.lock:
                        if n in self.global_verified:
                            break

                local_path.add(n)

                # Math logic
                if n % 2 == 0:
                    n = n // 2
                else:
                    n = 3 * n + 1

            # OPTIMIZATION 2: Batch update.
            # We acquire the lock just ONCE per number 'i' to update the global set.
            with self.lock:
                self.global_verified.update(local_path)


# --- Test the Fixed Implementation ---
fixed_tester = EfficientCollatz()
threads = []

start_time = time.time()

# 4 Threads testing numbers from 1 to 20,000
for i in range(4):
    t = threading.Thread(
        target=fixed_tester.worker, args=(i * 5000 + 1, (i + 1) * 5000)
    )
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Fixed Execution Time: {time.time() - start_time:.3f} seconds")
