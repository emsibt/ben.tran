def traverse(head: ListNode) -> None:
    if not head: return
    slow, fast, dummy = head, head, ListNode(0, head)
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next