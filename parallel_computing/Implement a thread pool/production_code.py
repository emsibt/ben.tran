"""
Quản lý vòng đời tự động: Khối with tự động dọn dẹp và ngầm gọi shutdown() khi tất cả công việc hoàn thành hoặc khi chương trình gặp lỗi. Bạn không bao giờ sợ quên đóng pool gây rò rỉ tài nguyên.
Quản lý kết quả trả về (Future): Hàm submit() trả về một đối tượng Future. Nó cho phép luồng chính (Main Thread) dễ dàng lấy được giá trị return của hàm chạy bên trong luồng phụ (điều mà code thủ công của chúng ta chưa làm được), đồng thời bắt các exception một cách an toàn mà không làm sập toàn bộ chương trình.
Tối ưu hóa ngầm định: Các vấn đề về đồng bộ hóa hàng đợi đều được xử lý ngầm định ở tầng sâu bằng module queue.Queue rất tối ưu của Python.
"""

import concurrent.futures
import time
import threading


def sample_task(task_id):
    print(f"[{threading.current_thread().name}] Executing task {task_id}")
    time.sleep(0.1)
    # The built-in pool easily handles return values
    return f"Result_of_{task_id}"


# --- Using the built-in ThreadPoolExecutor ---
print("Starting Built-in Thread Pool...")

# The 'with' statement automatically handles starting and gracefully shutting down the pool
with concurrent.futures.ThreadPoolExecutor(
    max_workers=3, thread_name_prefix="Worker"
) as executor:

    # Submit tasks and collect their 'futures' (promises of a future result)
    futures = [executor.submit(sample_task, i) for i in range(5)]

    # Safely retrieve results as they complete
    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            print(f"[Main-Thread] Received: {result}")
        except Exception as e:
            print(f"Task generated an exception: {e}")

print("Thread pool shut down automatically.")
