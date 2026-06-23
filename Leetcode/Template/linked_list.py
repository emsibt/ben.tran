"""Input is a Linked List
1. Dummy node
2. Two Pointers:  O(n)
3. Fast & Slow Pointers: O(n)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def traverse(head: ListNode) -> ListNode:
    if not head: return
    slow, fast, dummy = head, head, ListNode()
    current = dummy
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return dummy.next