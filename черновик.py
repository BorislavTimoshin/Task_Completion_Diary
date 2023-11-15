from bisect import bisect_left

h = [10, 8, 7, 5, 4, 3, 2, 1]
num = 6
print(bisect_left(h[::-1], num))
