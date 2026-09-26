"""
Started reading concurrently... gần như cùng một khoảnh khắc, và tổng thời gian đọc chỉ mất đúng 1 giây thay vì 3 giây. Reader-1 là người đại diện giữ cửa không cho Writer-1 vào, trong khi mở cửa cho Reader-2 và Reader-3 thoải mái đi chung. Khi tất cả đọc xong, Reader-3 (người cuối cùng) sẽ nhả khóa để Writer-1 được phép tiến hành cập nhật.
"""

import threading
import time


class ReadWriteLock:
    def __init__(self):
        self.read_count = 0
        # Lock to protect the 'read_count' variable
        self.count_lock = threading.Lock()
        # Lock to protect the actual shared resource
        self.resource_lock = threading.Lock()

    def acquire_read(self):
        with self.count_lock:
            self.read_count += 1
            # The FIRST readers locks the resource to keep writers out
            if self.read_count == 1:
                self.resource_lock.acquire()

    def release_read(self):
        with self.count_lock:
            self.read_count -= 1
            # The LAST reader unblocks the resource to let writers in
            if self.read_count == 0:
                self.resource_lock.release()

    def acquire_write(self):
        self.resource_lock.acquire()

    def release_write(self):
        self.resource_lock.release()


class EfficientDatabase:
    def __init__(self):
        self.data = "Initial_data"
        self.rw_lock = ReadWriteLock()

    def read_data(self):
        self.rw_lock.acquire_read()
        try:
            print(
                f"[{threading.current_thread().name}] Started reading concurrently..."
            )
            time.sleep(1)  # Simulate slow read
            print(f"[{threading.current_thread().name}] Finished reading: {self.data}")
        finally:
            self.rw_lock.release_read()

    def write_data(self, new_data):
        self.rw_lock.acquire_write()
        try:
            print(f"[{threading.current_thread().name}] Started write...")
            time.sleep(1)  # Simulate slow write
            self.data = new_data
            print(f"[{threading.current_thread().name}] Finished writing.")
        finally:
            self.rw_lock.release_write()


# --- Test the Fixed Code ---
sefe_db = EfficientDatabase()
threads = []

# 3 Readers
for i in range(3):
    t = threading.Thread(target=sefe_db.read_data, name=f"Reader-{i+1}")
    threads.append(t)
    t.start()

# 1 Writer starts after readers
time.sleep(0.1)
writer = threading.Thread(
    target=sefe_db.write_data, args=("New_data",), name=f"Writer-1"
)
writer.start()
threads.append(writer)

for t in threads:
    t.join()
