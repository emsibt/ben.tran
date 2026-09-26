"""
Thread-1 khóa ACC-1 thành công, sau đó đi ngủ 0.1 giây.
Thread-2 bắt đầu, khóa ACC-2 thành công, sau đó cũng đi ngủ 0.1 giây.
Thread-1 tỉnh dậy, muốn khóa ACC-2 để hoàn tất giao dịch, nhưng ACC-2 đang bị Thread-2 giữ. Nó đứng chờ.
Thread-2 tỉnh dậy, muốn khóa ACC-1 để hoàn tất giao dịch, nhưng ACC-1 đang bị Thread-1 giữ. Nó cũng đứng chờ.
"""

import threading
import time


class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()


def buggy_transfer(from_account: Account, to_account: Account, amount: int):
    print(
        f"[{threading.current_thread().name}] Attempting to lock {from_account.account_id}..."
    )

    # Step 1: Lock the sender's account
    with from_account.lock:
        print(
            f"[{threading.current_thread().name}] Locked {from_account.account_id}. Simulating delay..."
        )
        # Force a context switch to ensure the other thread starts
        time.sleep(0.1)

        print(
            f"[{threading.current_thread().name}] Attempting to lock {to_account.account_id}..."
        )
        # Step 2: Lock the receiver's account
        with to_account.lock:
            from_account.balance -= amount
            to_account.balance += amount
            print(
                f"[{threading.current_thread().name}] Success: Transferred {amount} from {from_account.account_id} to {to_account.account_id}"
            )


# --- Test the Buggy Code ---
acc1 = Account("ACC-1", 1000)
acc2 = Account("ACC-2", 1000)

# Thread-1 locks ACC-1, then tries to lock ACC-2
t1 = threading.Thread(target=buggy_transfer, args=(acc1, acc2, 100), name="Thread-1")
# Thread-2 locks ACC-2, then tries to lock ACC-1
t2 = threading.Thread(target=buggy_transfer, args=(acc2, acc1, 200), name="Thread-2")

t1.start()
t2.start()

t1.join()
t2.join()
print("This line will NEVER be printed because the program is deadlocked.")
