def hanoi_stack(n, source, target, auxiliary):
    """
    使用顯式堆疊（Stack）模擬遞迴調用
    """
    # 堆疊元素：(盤子數, 來源, 目標, 輔助)
    stack = [(n, source, target, auxiliary)]

    while stack:
        disks, src, tgt, aux = stack.pop()
        
        if disks == 1:
            print(f"Move disk 1 from {src} to {tgt}")
        else:
            # 由於堆疊是 LIFO（後進先出），放入順序需與執行順序相反：
            # 目標順序：(disks-1, src->aux) -> (1, src->tgt) -> (disks-1, aux->tgt)
            stack.append((disks - 1, aux, tgt, src))
            stack.append((1, src, tgt, aux))
            stack.append((disks - 1, src, aux, tgt))

print("--- 非遞迴（堆疊模擬）---")
hanoi_stack(3, 'A', 'C', 'B')