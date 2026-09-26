"""
Nếu bạn chạy đoạn code này, Thread-1 (tính "apple") sẽ chạy trước. Thread-2 (tính "banana") muốn chạy nhưng bị chặn lại ở cửa with self.lock:. Nó phải đợi đúng 2 giây cho đến khi Thread-1 tính xong mới được vào tính tiếp. Hệ thống đa luồng của chúng ta bỗng nhiên biến thành chạy tuần tự (chậm rề rề).
"""
import threading
import time

def slow_computation(word):
    print(f"[{threading.current_thread().name}] Computing result for '{word}' (takes 2 seconds)...")
    time.sleep(2)
    return f"PROCESSED_{word}"

class BuggyOneItemCache:
    def __init__(self):
        self.last_word = None
        self.last_result = None
        self.lock = threading.Lock()

    def process_request(self, word):
        # BAD: The lock covers the entire process, including the slow computation.
        with self.lock:
            result = None
            if word == self.last_word:
                print(f"[{threading.current_thread().name}] Cache HIT for '{word}'!")
                result = self.last_result
            
            if result is None:
                # Other threads must wait here even if they query a different word!
                result = slow_computation(word)
                self.last_word = word
                self.last_result = result
                
        return result

# --- Test the Buggy Code ---
cache = BuggyOneItemCache()
threads = []
words_to_process = ["apple", "banana", "apple"]

for i, word in enumerate(words_to_process):
    t = threading.Thread(target=cache.process_request, args=(word,), name=f"Thread-{i+1}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()