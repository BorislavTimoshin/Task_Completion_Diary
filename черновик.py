numbers = [10, 9, 8, 7, 4, 2, 1]
item = 12
end = len(numbers)
start = 0

while start < end:
    mid = (start + end) // 2
    if numbers[mid] > item:
        start = mid + 1
    else:
        end = mid

print(start)
numbers.insert(start, item)
print(numbers)

from PyQt5.QtCore import QTime

print(QTime(12, 22, 34) > QTime(10, 3, 10))

