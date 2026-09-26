"""Lệnh self.count += 1 không hề diễn ra trong một nhịp. Python biên dịch nó thành 3 thao tác: Đọc giá trị - Cộng thêm 1 - Ghi đè lại.
Giả sử count đang là 10. Thread-1 đọc giá trị 10 vào bộ nhớ tạm, nhưng chưa kịp cộng thì Hệ điều hành tạm dừng nó lại để cho Thread-2 chạy. Thread-2 cũng đọc giá trị hiện tại (vẫn là 10), thực hiện cộng thành 11 và ghi đè count = 11. Lúc này Thread-1 tỉnh dậy, nó mang số 10 trong bộ nhớ tạm ra cộng 1 thành 11, rồi ghi đè lên biến count.
Kết quả: 2 luồng đều đã thực hiện thao tác cộng, nhưng giá trị biến chỉ tăng 1 đơn vị. Đây chính là hiện tượng mất mát dữ liệu do các bước thực thi bị xen kẽ (interleaved).
"""

import threading


class UnsynchronizedCounter:
    def __init__(self):
        self.count = 0

    def increment(self):
        for _ in range(1000000):
            # This looks like one step, but it is actually three:
            # 1. Read self.count
            # 2. Add 1 to thye read value
            # 3. Write the new value back to self.count
            self.count += 1


# --- Test the Buggy Code ---
buggy_counter = UnsynchronizedCounter()

t1 = threading.Thread(target=buggy_counter.increment, name="Thread-1")
t2 = threading.Thread(target=buggy_counter.increment, name="Thread-2")

t1.start()
t2.start()

t1.join()
t2.join()

print(f"Buggy final count: {buggy_counter.count} (Expected: 2000000)")
