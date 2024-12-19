def max_subarray_brute_force(arr):
    n = len(arr)
    max_sum = float('-inf')

    for start in range(n):
        for end in range(start, n):
            current_sum = sum(arr[start:end + 1])
            max_sum = max(max_sum, current_sum)
    return max_sum

def max_subarray_divide_and_conquer(arr, low, high):
    if low == high:
        return arr[low]  # Base case: o array tem apenas um elemento

    mid = (low + high) // 2
    left_max = max_subarray_divide_and_conquer(arr, low, mid)
    right_max = max_subarray_divide_and_conquer(arr, mid + 1, high)
    cross_max = max_crossing_sum(arr, low, mid, high)

    return max(left_max, right_max, cross_max)

def max_crossing_sum(arr, low, mid, high):
    left_sum = float('-inf')
    right_sum = float('-inf')
    total = 0

    for i in range(mid, low - 1, -1):
        total += arr[i]
        if total > left_sum:
            left_sum = total

    total = 0
    for i in range(mid + 1, high + 1):
        total += arr[i]
        if total > right_sum:
            right_sum = total

    return left_sum + right_sum
