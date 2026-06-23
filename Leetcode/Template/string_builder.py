"""String Concatenation
1. String.join(): O(n) (Python)
2. StringBuilder: O(n) (Java, C#, etc.)
"""


def string_builder(s: str) -> str:
    array = []
    for char in s:
        array.append(char)

    return "".join(array)
