"""
Lần này, khi WRITER chạy hàm acquire_write(), nó tăng waiting_writers += 1 trước rồi mới bắt đầu ngủ (vì Reader 1 & 2 vẫn đang đọc).
Lúc Reader 3 đến gọi acquire_read(), vòng lặp while self.waiting_writers > 0: kích hoạt, tước quyền đi vào của Reader 3 và bắt nó đi ngủ. Reader 4 và 5 đến cũng chịu chung số phận.
Ngay khi Reader 2 đọc xong và active_readers == 0, WRITER lập tức tỉnh dậy, cập nhật dữ liệu một cách hiên ngang. Chỉ sau khi WRITER ghi xong và nhả khóa, bầy Reader 3, 4, 5 mới được đánh thức để đọc nốt.
"""

import threading
import time


class WritePreferenceRWLock:
    def __init__(self):
        self.condition = threading.Condition()
        self.read_count = 0
        self.is_writing = False
        self.waiting_writers = 0

    def acquire_read(self):
        with self.condition:
            # Block new readers if someone is writing or if a writer is waiting
            while self.is_writing or self.waiting_writers > 0:
                self.condition.wait()
            self.read_count += 1

    def release_read(self):
        with self.condition:
            self.read_count -= 1
            if self.read_count == 0:
                # Wake up everyone, but waiting writers will grab it first
                self.condition.notify_all()

    def acquire_write(self):
        with self.condition:
            self.waiting_writers += 1
            # Wait until there are no active readers and no active writers
            while self.read_count > 0 and self.is_writing:
                self.condition.wait()
            self.waiting_writers -= 1
            self.is_writing = True

    def release_write(self):
        with self.condition:
            self.is_writing = False
            self.condition.notify_all()


# --- Simulate Write Preference ---
safe_lock = WritePreferenceRWLock()


def safe_reader_task(reader_id):
    print(f"[Reader-{reader_id}] Arrived and trying to read...")
    safe_lock.acquire_read()
    print(f"[Reader-{reader_id}] STARTED reading.")
    time.sleep(1)
    print(f"[Reader-{reader_id}] FINISHED reading.")
    safe_lock.release_read()


def safe_writer_task():
    print(f"[WRITER] Arrived and trying to write... (Setting Preference!)")
    safe_lock.acquire_write()
    print(f"[WRITER] STARTED writing.")
    time.sleep(1)
    print(f"[WRITER] FINISHED writing.")
    safe_lock.release_write()


# Start Reader 1 & 2
threading.Thread(target=safe_reader_task, args=(1,)).start()
time.sleep(0.1)
threading.Thread(target=safe_reader_task, args=(2,)).start()

# Writer arrives
time.sleep(0.1)
threading.Thread(target=safe_writer_task).start()

# Reader 3, 4, 5 arrive later
for i in range(3, 6):
    time.sleep(0.4)
    threading.Thread(target=safe_reader_task, args=(i,)).start()
