from typing import List
def below_zero(operations: List[int]) -> bool:
    for operation in operations:
        if operation < 0:
            return True
    return False

print(below_zero([]))
print(below_zero([1, 2, -3, 1, 2, -3]))
print(below_zero([1, 2, -4, 5, 6]))
print(below_zero([1, -1, 2, -2, 5, -5, 4, -4]))
print(below_zero([1, -1, 2, -2, 5, -5, 4, -5]))
print(below_zero([1, -2, 2, -2, 5, -5, 4, -4]))