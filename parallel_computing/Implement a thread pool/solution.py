"""
Khi một worker bắt đầu, nó đi vào khối with self.condition: và kiểm tra hàng đợi. Nếu hàng đợi rỗng, lệnh self.condition.wait() buộc thread đó nhả khóa và đi ngủ (sử dụng 0% CPU). Khi bạn gọi hàm submit(), hệ thống đưa tác vụ vào hàng đợi và kích hoạt notify(). Lệnh này đóng vai trò như một chiếc chuông báo thức, gọi đúng một worker đang ngủ dậy. Worker đó lấy tác vụ ra một cách an toàn, bước ra khỏi vùng khóa (lock) để xử lý tác vụ (giúp các worker khác không bị chặn lại), rồi lại quay vòng lên kiểm tra hàng đợ
"""

import threading
import time


def sample_task(task_id):
    print(f"[{threading.current_thread().name}] Executing task {task_id}")
    time.sleep(0.1)


class FixedThreadPool:
    def __init__(self, num_threads):
        self.tasks = []
        self.workers = []
        self.is_active = True
        self.condition = threading.Condition()

        for i in range(num_threads):
            t = threading.Thread(target=self.worker_loop, name=f"Worker-{i+1}")
            t.start()
            self.workers.append(t)

    def submit(self, task, task_id):
        with self.condition:
            self.tasks.append((task, task_id))
            self.condition.notify()

    def worker_loop(self):
        while True:
            with self.condition:
                # Go to sleep if there are no tasks and the pool is still active
                while len(self.tasks) == 0 and self.is_active:
                    self.condition.wait()

                # If pool is shutting down and no tasks remain, exit the thread
                if len(self.tasks) == 0 and not self.is_active:
                    break

                task, task_id = self.tasks.pop(0)

            task(task_id)

    def shutdown(self):
        with self.condition:
            self.is_active = False
            # Wake up ALL sleeping workers so they can see is_active=False and exit
            self.condition.notify_all()

        for t in self.workers:
            t.join()
            print("Thread pool shut down gracefully.")


# --- Test the Fixed Pool ---
print("Starting Fixed Thread Pool...")
safe_pool = FixedThreadPool(num_threads=3)

for i in range(5):
    safe_pool.submit(sample_task, i)

time.sleep(1)
safe_pool.shutdown()
