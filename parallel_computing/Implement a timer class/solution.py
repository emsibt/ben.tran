"""
Lần này, khi Long_Task_A (5 giây) đi vào, Dispatcher gọi self.condition.wait(timeout=5.0). Nửa giây sau, Quick_Task_B (1 giây) được đẩy vào. Hàm schedule nhận thấy Quick_Task_B đang đứng đầu hàng đợi (cần chạy sớm nhất), nó liền gọi self.condition.notify().
Luồng Dispatcher lập tức tỉnh dậy (chỉ sau 0.5 giây ngủ), vòng lặp while quay lại tính toán thời gian mới, và thấy rằng nó chỉ cần ngủ thêm tầm 0.5 giây nữa là đến hạn của Quick_Task_B. Kết quả in ra sẽ chuẩn xác: Quick_Task_B chạy đúng ở giây thứ 1, và Long_Task_A thong thả chạy ở giây thứ 5.
"""

import threading
import time
import heapq


def print_task(name):
    print(f"[{time.strftime('%H:%M:%S')}] Task '{name}' executed!")


class FixedTimer:
    def __init__(self):
        self.tasks = []  # Min-heap
        self.condition = threading.Condition()
        self.task_counter = 0  # To handle ties in heap sorting

        self.dispatcher = threading.Thread(
            target=self._run, name="Dispatcher", daemon=True
        )
        self.dispatcher.start()

    def schedule(self, task, delay_seconds, name):
        execute_at = time.time() + delay_seconds

        with self.condition:
            self.task_counter += 1
            # Push into min-heap. Ordered by execution time.
            heapq.heappush(self.tasks, (execute_at, self.task_counter, task, name))

            # CRITICAL FIX: If the new task is the very first one in the heap
            # (meaning it needs to run sooner than whatever is currently scheduled),
            # wake up the dispatcher thread so it can adjust its sleep time!
            if self.tasks[0][1] == self.task_counter:
                self.condition.notify()

        print(
            f"[{time.strftime('%H:%M:%S')}] Scheduled '{name}' to run in {delay_seconds}s"
        )

    def _run(self):
        while True:
            task_to_run = None

            with self.condition:
                while not self.tasks:
                    self.condition.wait()  # Sleep indefinitely until a task arrives

                now = time.time()
                execute_at = self.tasks[0][0]

                if execute_at <= now:
                    # Time is up! Pop and prepare to run
                    _, _, task, name = heapq.heappop(self.tasks)
                    task_to_run = (task, name)
                else:
                    # Sleep interruptibly until it's time for the first task
                    sleep_duration = execute_at - now
                    self.condition.wait(timeout=sleep_duration)

            # Execute outside the lock to prevent blocking
            if task_to_run:
                task, name = task_to_run
                task(name)


# --- Test the Fixed Timer ---
safe_timer = FixedTimer()

safe_timer.schedule(print_task, 5, "Long_Task_A")
time.sleep(0.5)

# This time, Quick_Task_B will wake up the dispatcher and run first!
safe_timer.schedule(print_task, 1, "Quick_Task_B")

time.sleep(6)
