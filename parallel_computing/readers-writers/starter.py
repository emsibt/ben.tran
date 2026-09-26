"""
Khi bạn chạy code, Reader-1 sẽ giữ Lock trong 1 giây. Reader-2 và Reader-3 dù chỉ muốn đọc (không làm thay đổi dữ liệu) vẫn phải xếp hàng chờ đợi tổng cộng 3 giây mới xong. Điều này đi ngược lại hoàn toàn với mục đích của lập trình song song.
"""

import threading
import time


class InefficientDatabase:
    def __init__(self):
        self.data = "Initial_data"
        self.lock = threading.Lock()

    def read_data(self):
        # A reader locks out other readers
        with self.lock:
            print(f"[{threading.current_thread().name}] Started reading...")
            time.sleep(1)  # Simulate slow read
            print(f"[{threading.current_thread().name}] Finished reading: {self.data}")

    def write_data(self, new_data):
        with self.lock:
            print(f"[{threading.current_thread().name}] Started writing...")
            time.sleep(1)  # Simulate slow write
            self.data = new_data
            print(f"[{threading.current_thread().name}] Finished writing.")


# --- Test the Inefficient Code ---
db = InefficientDatabase()
threads = []

# 3 Readers trying to read at the same time
for i in range(3):
    t = threading.Thread(target=db.read_data, name=f"Reader-{i+1}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()
