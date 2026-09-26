"""Cả Thread-1 (gửi từ ACC-1 sang ACC-2) và Thread-2 (gửi từ ACC-2 sang ACC-1) đều bị ép phải lấy khóa của ACC-1 đầu tiên (vì "ACC-1" < "ACC-2").
Nếu Thread-1 nhanh tay lấy được khóa ACC-1, thì Thread-2 lập tức bị chặn ngay ở bước đầu tiên và phải chờ. Thread-1 thoải mái đi tiếp, lấy khóa ACC-2, trừ tiền, cộng tiền rồi nhả cả hai khóa ra. Lúc này Thread-2 mới được phép bắt đầu. Deadlock hoàn toàn bị triệt tiêu.
"""

import threading
import time


class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()


def fixed_transfer(from_account, to_account, amount):
    # CRITICAL FIX: Always lock accounts in the same order (e.g., alphabetically by ID)
    # This prevents the circular wait condition.
    first_lock, second_lock = sorted(
        [from_account, to_account], key=lambda acc: acc.account_id
    )

    print(
        f"[{threading.current_thread().name}] Attempting to lock {first_lock.account_id} first..."
    )

    with first_lock.lock:
        print(
            f"[{threading.current_thread().name}] Locked {first_lock.account_id}. Simulating delay..."
        )
        time.sleep(0.1)

        print(
            f"[{threading.current_thread().name}] Attempting to lock {second_lock.account_id}..."
        )
        with second_lock.lock:
            from_account.balance -= amount
            to_account.balance += amount
            print(
                f"[{threading.current_thread().name}] Success: Transferred {amount} from {from_account.account_id} to {to_account.account_id}"
            )


# --- Test the Fixed Code ---
safe_acc1 = Account("ACC-1", 1000)
safe_acc2 = Account("ACC-2", 1000)

t1 = threading.Thread(
    target=fixed_transfer, args=(safe_acc1, safe_acc2, 100), name="Thread-1"
)
t2 = threading.Thread(
    target=fixed_transfer, args=(safe_acc2, safe_acc1, 100), name="Thread-2"
)

t1.start()
t2.start()

t1.join()
t2.join()
print(f"Final Balances -> ACC-1: {safe_acc1.balance}, ACC-2: {safe_acc2.balance}")
