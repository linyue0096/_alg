def my_map(func, lst):
    """自製 map：對串列中每個元素套用 func"""
    if not lst:
        return []
    # 取第一個元素運算，其餘遞迴處理
    return [func(lst[0])] + my_map(func, lst[1:])


def my_filter(predicate, lst):
    """自製 filter：保留滿足 predicate(x) == True 的元素"""
    if not lst:
        return []
    head, tail = lst[0], lst[1:]
    rest = my_filter(predicate, tail)
    return [head] + rest if predicate(head) else rest


def my_reduce(func, lst, initializer=None):
    """自製 reduce：將二元函數累加套用於所有元素"""
    if not lst:
        if initializer is not None:
            return initializer
        raise TypeError("my_reduce() of empty sequence with no initial value")
    
    if initializer is None:
        accumulator = lst[0]
        remaining = lst[1:]
    else:
        accumulator = initializer
        remaining = lst

    def _reduce_helper(acc, rest):
        if not rest:
            return acc
        return _reduce_helper(func(acc, rest[0]), rest[1:])

    return _reduce_helper(accumulator, remaining)

def bubble_pass(lst):
    """
    內層遞迴：相當於一次內層迴圈
    相鄰兩元素比較，將區間內最大的數一路冒泡至末端
    """
    # 邊界：空或只有 1 個元素，無需再比
    if len(lst) <= 1:
        return lst

    a, b = lst[0], lst[1]
    rest = lst[2:]

    if a > b:
        # 較大的 a 往後移，繼續與後面的串列比較冒泡
        return [b] + bubble_pass([a] + rest)
    else:
        # a 較小保持在原地，換 b 繼續與後面的串列比較冒泡
        return [a] + bubble_pass([b] + rest)


def bubble_sort_no_loop(lst, n=None):
    """
    外層遞迴：相當於外層迴圈
    共需遞迴執行 n 輪 bubble_pass
    """
    if n is None:
        n = len(lst)

    # 終止條件：長度小於 2 或輪次耗盡，已排序完成
    if n <= 1:
        return lst

    # 執行一輪冒泡，此時最右邊的元素已經就位
    passed_list = bubble_pass(lst)

    # 對前 n-1 個元素遞迴排序，並接上最後已就位的最大元素
    return bubble_sort_no_loop(passed_list[:-1], n - 1) + [passed_list[-1]]

# --- 測試 ---
nums = [1, 2, 3, 4, 5]

mapped = my_map(lambda x: x * 2, nums)
print("my_map (* 2):", mapped)

filtered = my_filter(lambda x: x % 2 == 1, nums)
print("my_filter (奇數):", filtered)

reduced = my_reduce(lambda acc, x: acc + x, nums, 0)
print("my_reduce (總和):", reduced)

print("-" * 40)

# --- 測試無迴圈泡沫排序 ---
unsorted = [64, 34, 25, 12, 22, 11, 90, -5, 0]
sorted_result = bubble_sort_no_loop(unsorted)

print("原始數列:", unsorted)
print("排序結果:", sorted_result)