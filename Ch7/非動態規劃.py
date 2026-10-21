def diff_myers(a, b):
    n, m = len(a), len(b)
    max_d = n + m
    # v 陣列儲存各對角線 k 上能到達的最遠 x 座標
    # k 的範圍是 -max_d 到 max_d
    v = {1: 0}
    trace = []

    for d in range(max_d + 1):
        v_copy = v.copy()
        trace.append(v_copy)
        for k in range(-d, d + 1, 2):
            # 判斷是從上面 (k+1) 往下走，還是從左邊 (k-1) 往右走
            # 貪婪選擇 x 較大的點
            if k == -d or (k != d and v.get(k - 1, 0) < v.get(k + 1, 0)):
                x = v.get(k + 1, 0)  # 向下 (Insert)
            else:
                x = v.get(k - 1, 0) + 1  # 向右 (Delete)

            y = x - k

            # Snake: 只要字元相同，貪婪地沿對角線狂奔 (成本為 0)
            while x < n and y < m and a[x] == b[y]:
                x += 1
                y += 1

            v[k] = x

            # 到達終點
            if x >= n and y >= m:
                return backtrack_myers(trace, a, b, n, m)


def backtrack_myers(trace, a, b, n, m):
    diff = []
    x, y = n, m

    for d in range(len(trace) - 1, 0, -1):
        v = trace[d]
        k = x - y

        # 找出前一個狀態是來自 k-1 還是 k+1
        if k == -d or (k != d and v.get(k - 1, 0) < v.get(k + 1, 0)):
            prev_k = k + 1
        else:
            prev_k = k - 1

        prev_x = trace[d - 1].get(prev_k, 0)
        prev_y = prev_x - prev_k

        # 回溯對角線（相同的部分）
        while x > prev_x and y > prev_y:
            diff.append(f"  {a[x - 1]}")
            x -= 1
            y -= 1

        # 回溯向右或向下的那一步
        if d > 0:
            if x == prev_x:
                diff.append(f"+ {b[y - 1]}")
                y -= 1
            elif y == prev_y:
                diff.append(f"- {a[x - 1]}")
                x -= 1

    # 處理開頭的對角線
    while x > 0 and y > 0:
        diff.append(f"  {a[x - 1]}")
        x -= 1
        y -= 1

    return list(reversed(diff))