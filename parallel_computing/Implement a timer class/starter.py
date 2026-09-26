"""
Khi bạn chạy đoạn code trên, Long_Task_A (5 giây) được đưa vào trước. Luồng Dispatcher tính toán và gọi time.sleep(5). Ngay sau đó, bạn đưa Quick_Task_B (1 giây) vào. Vì luồng Dispatcher đang bị kẹt cứng trong giấc ngủ 5 giây, nó không hề biết có tác vụ mới. Kết quả là Quick_Task_B bị "giam lỏng" và chỉ được in ra cùng lúc với Long_Task_A ở giây thứ 5. Việc lên lịch hoàn toàn thất bại.
"""

import threading
import time


def print_task(name):
    print(f"[{time.strftime('%H:%M:%S')}] Task '{name}' executed!")


class BuggyTimer:
    def __init__(self):
        self.tasks = []
        self.lock = threading.Lock()

        # Start the background dispatcher thread
        self.dispatcher = threading.Thread(
            target=self._run, name="Dispatcher", daemon=True
        )
        self.dispatcher.start()

    def schedule(self, task, delay_seconds, name):
        execute_at = time.time() + delay_seconds
        with self.lock:
            self.tasks.append((execute_at, task, name))
            # Sort by execution time (earliest first)
            self.tasks.sort(key=lambda x: x[0])
        print(
            f"[{time.strftime('%H:%M:%S')}] Scheduled '{name}' to run in {delay_seconds}s"
        )

    def _run(self):
        while True:
            sleep_duration = 0
            task_to_run = None

            with self.lock:
                if self.tasks:
                    now = time.time()
                    if self.tasks[0][0] <= now:
                        # Time is up, pop the task
                        execute_at, task, name = self.tasks.pop(0)
                        task_to_run = (task, name)
                    else:
                        # Calculate time to sleep until the first task is ready
                        sleep_duration = self.tasks[0][0] - now

            if task_to_run:
                task, name = task_to_run
                task(name)
            elif sleep_duration > 0:
                # BUG: The thread goes into an UNINTERRUPTIBLE sleep.
                # If a new, shorter task arrives now, it won't be processed on time!
                time.sleep(sleep_duration)
            else:
                time.sleep(0.1)


# --- Test the Buggy Timer ---
timer = BuggyTimer()

# Schedule a long task first (5 seconds delay)
timer.schedule(print_task, 5, "Long_Task_A")

# Wait a tiny bit to ensure the dispatcher goes to sleep for 5 seconds
time.sleep(0.5)

# Now schedule a quick task (1 second delay)
# EXPECTATION: Quick_Task_B runs before Long_Task_A.
# REALITY: It gets blocked because the dispatcher is stuck in time.sleep(5)
timer.schedule(print_task, 1, "Quick_Task_B")

# Keep main thread alive long enough to see the output
time.sleep(6)
