"""
Lúc này, Thread-1 và Thread-2 sẽ lướt qua Lock 1 rất nhanh vì cache đang trống. Sau đó, cả 2 thread sẽ cùng lúc in ra dòng "Computing result...". Hệ thống đã thực sự chạy song song. Đến khi tính xong, chúng mới xếp hàng lần lượt qua Lock 2 để lưu kết quả. Riêng Thread-3 do chạy sau một chút, khi quét qua Lock 1 sẽ thấy "apple" đã nằm trong cache nên xuất hiện Cache Hit.
"""
import threading
import time


def slow_computation(word):
    print(
        f"[{threading.current_thread().name}] Computing result for '{word}' (takes 2 seconds)..."
    )
    time.sleep(2)
    return f"PROCESSED_{word}"


class FixedOneItemCache:
    def __init__(self):
        self.last_word = None
        self.last_result = None
        self.lock = threading.Lock()

    def process_request(self, word):
        res = None

        # Lock 1: Only lock when checking the cache (extremely fast)
        with self.lock:
            if word == self.last_word:
                print(f"[{threading.current_thread().name}] Cache HIT for '{word}'!")
                res = self.last_result

        # Computation is outside the lock
        if res is None:
            res = slow_computation(word)

            # Lock 2: Only lock when updating the cache (extremely fast)
            with self.lock:
                self.last_word = word
                self.last_result = res

        return res


# --- Test the Fixed Code ---
safe_cache = FixedOneItemCache()
threads = []
words_to_process = ["apple", "banana", "apple"]

for i, word in enumerate(words_to_process):
    t = threading.Thread(
        target=safe_cache.process_request, args=(word,), name=f"Thread-{i+1}"
    )
    threads.append(t)
    t.start()

for t in threads:
    t.join()
