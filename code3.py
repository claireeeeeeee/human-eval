from typing import List
def below_zero(operations: List[int]) -> bool:
    for operation in operations:
        if operation < 0:
            return True
    return False

METADATA = {
    'author': 'jt',
    'dataset': 'test'
}

def check(candidate):
    assert candidate([]) == False
    assert candidate([1, 2, -3, 1, 2, -3]) == False
    assert candidate([1, 2, -4, 5, 6]) == True
    assert candidate([1, -1, 2, -2, 5, -5, 4, -4]) == False
    assert candidate([1, -1, 2, -2, 5, -5, 4, -5]) == True
    assert candidate([1, -2, 2, -2, 5, -5, 4, -4]) == True

# 使用 check 函数来测试 below_zero 函数
check(below_zero)

print("All tests passed!")  # 如果所有测试通过，会打印 "All tests passed!"
