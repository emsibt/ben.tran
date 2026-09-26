"""
Nếu bạn chạy đoạn code này, dòng ERROR: Tried to pop from empty list! gần như chắc chắn sẽ xuất hiện. Worker-1 và Worker-2 cùng lúc đi qua dòng if len(self.tasks) > 0 và thấy rằng đang có 1 tác vụ cuối cùng. Worker-1 thực thi pop(0) và lấy tác vụ đó đi. Ngay lập tức, Worker-2 cũng gọi pop(0), nhưng list lúc này đã rỗng, dẫn đến lỗi IndexError.
Ngoài ra, khi không có tác vụ nào, vòng lặp while vẫn chạy điên cuồng hàng triệu lần mỗi giây (Busy waiting), đẩy CPU của bạn lên mức 100% một cách vô íc
"""
import threading
import time


def sample_task(task_id):
    print(f"[{threading.current_thread().name}] Executing task {task_id}")
    time.sleep(0.1)


class BuggyThreadPool:
    def __init__(self, num_threads):
        self.tasks = []
        self.workers = []
        self.is_active = True

        for i in range(num_threads):
            t = threading.Thread(target=self.worker_loop, name=f"Worker-{i+1}")
            t.start()
            self.workers.append(t)

    def submit(self, task, task_id):
        self.tasks.append((task, task_id))

    def worker_loop(self):
        while self.is_active or len(self.tasks) > 0:
            if len(self.tasks) > 0:
                try:
                    # RACE CONDITION: Worker-1 and Worker-2 both see len > 0.
                    # Worker-1 pops the only item. Worker-2 tries to pop and crashes.
                    task, task_id = self.tasks.pop()
                    task(task_id)
                except IndexError:
                    print(
                        f"[{threading.current_thread().name}] ERROR: Tried to pop from empty list! Race condition caught."
                    )

    def shutdown(self):
        self.is_active = False
        for t in self.workers:
            t.join()


# --- Test the Buggy Pool ---
print("Starting Buggy Thread Pool...")
buggy_pool = BuggyThreadPool(num_threads=3)

# Submit 5 tasks concurrently
for i in range(5):
    buggy_pool.submit(sample_task, i)

time.sleep(1)
buggy_pool.shutdown()
