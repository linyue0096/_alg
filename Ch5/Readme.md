# 遞迴，函數式編程， Lambda Calculus

## 課堂繳交
## 程式碼使用gemini幫我寫，readme是查維基百科在用gemini整理資料再改自己撰寫
## Gemini連結:https://share.gemini.google/8Uuz11tUCUbC
-------------------------------------------------------------

### 1.河內塔問題（遞迴 vs. 非遞迴顯式堆疊）
1. 問題背景：
    源自古老印度傳說，有三根柱子（來源柱、輔助柱、目標柱）及由大到小疊放的 $n$ 個圓盤。目標是將所有圓盤從來源柱移至目標柱
2. 規則約束：
    - 每次只能移動一個圓盤
    - 任何時候大盤子都不能壓在小盤子上方。
3. 時間與空間複雜度：
    - 移動 $n$ 個盤子所需的最少移動步數為 $2^n - 1$，時間複雜度為 $O(2^n)$
    - 遞迴空間複雜度取決於呼叫堆疊深度，為 $O(n)$

### 演算法
1. 架構遞迴解法 (hanoi_recursive)：
    * Base Case：$n = 1$ 時，直接將盤子從來源柱移到目標柱
    * Recursive Step：
        1. 將前 $n-1$ 個盤子從來源柱借助目標柱移到輔助柱。
        2. 將第 $n$ 個盤子直接從來源柱移到目標柱。
        3. 將輔助柱上的 $n-1$ 個盤子借助來源柱移到目標柱。
        
2. 非遞迴解法（顯式堆疊模擬）：
    * 使用自建的串列模擬系統呼叫堆疊，堆疊元素為 (盤子數, 來源, 目標, 輔助)
    * 地雷點：因為堆疊是後進先出，為了保持與遞迴呼叫相同的順序，壓入堆疊的順序必須與執行步驟完全相反

### 測試
* 程式碼(遞迴解法)
```
def hanoi_recursive(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    hanoi_recursive(n - 1, source, auxiliary, target)
    print(f"Move disk {n} from {source} to {target}")
    hanoi_recursive(n - 1, auxiliary, target, source)
print("--- 測試：3 個盤子由 A 移到 C (遞迴) ---")
hanoi_recursive(3, 'A', 'C', 'B')
```
* 輸出：
```
--- 測試：3 個盤子由 A 移到 C (遞迴) ---
Move disk 1 from A to C
Move disk 2 from A to B
Move disk 1 from C to B
Move disk 3 from A to C
Move disk 1 from B to A
Move disk 2 from B to C
Move disk 1 from A to C
```

* 程式碼(非遞迴解法)
```
def hanoi_stack(n, source, target, auxiliary):
    stack = [(n, source, target, auxiliary)]
    while stack:
        disks, src, tgt, aux = stack.pop()
        if disks == 1:
            print(f"Move disk 1 from {src} to {tgt}")
        else:
            # LIFO: 反向推入堆疊
            stack.append((disks - 1, aux, tgt, src))
            stack.append((1, src, tgt, aux))
            stack.append((disks - 1, src, aux, tgt))
print("\n--- 測試：3 個盤子由 A 移到 C (非遞迴堆疊) ---")
hanoi_stack(3, 'A', 'C', 'B')
```
* 輸出：
```
--- 測試：3 個盤子由 A 移到 C (非遞迴堆疊) ---
Move disk 1 from A to C
Move disk 2 from A to B
Move disk 1 from C to B
Move disk 3 from A to C
Move disk 1 from B to A
Move disk 2 from B to C
Move disk 1 from A to C
```
* 學習：
    遞迴與堆疊本質相同：系統呼叫遞迴時底層本來就是利用 Call Stack 儲存環境變數。透過手動維護 stack，除了解除 Python 預設遞迴深度限制外，也能更透徹理解電腦執行時序倒推的運作方式

--------------------------------------------------------------
### 2.符號數學式微分（遞迴遍歷 AST 語法樹與代數化簡）
1. 數值微分 vs. 符號微分：
    - 數值微分使用極限差分 $\frac{f(x+h) - f(x)}{h}$ 近似，容易產生浮點數截斷與捨入誤差
    - 符號微分則是將數學式視為抽象語法樹 (Abstract Syntax Tree, AST)，透過代數微分公式做精確推導，產出解析解（Analytical Solution）。
2. 微分法則的遞迴特性：
    - 算式是樹狀結構，每個節點是運算子（如 +, *, ^），子節點為運算元
    - 對樹的根節點求微分，天然對應樹的後序遍歷：先遞迴求出左右子樹的導數，再利用乘法定則、除法定則或連鎖律組裝起來

### 測試
* 程式碼
```
# 測試 1: f(x) = 3*x^2 + 5*x - 7
expr1 = ('-', ('+', ('*', 3, ('^', 'x', 2)), ('*', 5, 'x')), 7)
diff1 = sym_diff(expr1, 'x')
print("原式 1:", expr_to_str(expr1))
print("導函數 1:", expr_to_str(diff1))
```
* 輸出：
```
(((3 * (x ^ 2)) + (5 * x)) - 7)
導函數 : ((6 * x) + 5)
```

* 程式碼
```
# 測試 2: g(x) = x^2 / (x + 1)
expr2 = ('/', ('^', 'x', 2), ('+', 'x', 1))
diff2 = sym_diff(expr2, 'x')
print("\n原式 2:", expr_to_str(expr2))
print("導函數 2:", expr_to_str(diff2))
```
* 輸出：
```
((x ^ 2) / (x + 1))
導函數 : ((((2 * x) * (x + 1)) - (x ^ 2)) / ((x + 1) ^ 2))
```
-------------------------------------------------------------
### 3.自製高階函數（map, filter, reduce）與純遞迴無迴圈泡沫排序
什麼是純函數式風格

1. 禁絕狀態改變與迴圈：
- 函數式程式設計提倡使用純函數與不可變資料結構
- 禁止使用 for / while，迴圈反覆執行的邏輯改由頭尾拆分或尾遞迴來完成

2. 高階函數三大核心：
- Map：一對一轉換 ($[a] \to [b]$)
- Filter：條件篩選保留 ($[a] \to [a']$)
- 地雷點：計算總和時切記要跳過對角線項 $j = i$ 本身，扣除完後再除以 $a_{ii}$。

### 測試
1. 測試 1：一般對角優勢方程組（驗證原地更新的收斂性）
* 測資：
$$\begin{cases} 4x_1 - x_2 + x_3 = 7 \\ 4x_1 - 8x_2 + x_3 = -21 \\ -2x_1 + x_2 + 5x_3 = 15 \end{cases}$$
* 程式碼：
```python
nums = [1, 2, 3, 4, 5]

print("--- 測試自製高階函數 ---")
print("my_map (* 2):", my_map(lambda x: x * 2, nums))
print("my_filter (只留奇數):", my_filter(lambda x: x % 2 == 1, nums))
print("my_reduce (加總):", my_reduce(lambda acc, x: acc + x, nums, 0))

print("\n--- 測試無迴圈泡沫排序 ---")
unsorted = [64, 34, 25, 12, 22, 11, 90, -5, 0]
print("排序前:", unsorted)
print("排序後:", bubble_sort_no_loop(unsorted))
```

* 輸出：
```
--- 測試自製高階函數 ---
my_map (* 2): [2, 4, 6, 8, 10]
my_filter (只留奇數): [1, 3, 5]
my_reduce (加總): 15

--- 測試無迴圈泡沫排序 ---
排序前: [64, 34, 25, 12, 22, 11, 90, -5, 0]
排序後: [-5, 0, 11, 12, 22, 25, 34, 64, 90]
```
* 學習:
    - 思考模式的切換：平時寫程式依賴迴圈變數（如 i, j）遞增與暫存變數交換（Swap）。改用完全不使用迴圈的遞迴寫法後，必須將問題拆解成「當前頭部與剩餘尾部」，這也是 Lisp、Haskell 等純函數式語言的核心基礎。

    - 效能考量：在 Python 中進行串列切片（lst[1:]）會產生新物件的複製成本，且沒有預設尾遞迴優化 (TCO)，因此這類寫法主要用於演算法思維訓練與證明宣告式編程的完備性。