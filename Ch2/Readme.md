# 遞迴關係式求解與演算法複雜度分析

## 解題觀念

分析遞迴關係式通常包含以下兩個步驟：
1. **反覆代入法**：自頂向下連續展開，觀察常數項與係數的累積規律（通常為等差級數或等比級數
2. **終止邊界代換**：找出讓問題回到邊界條件（如 $T(1)$）時的展開步數 $k$，求出完全消除遞迴的精確封閉解

### 遞迴結構判斷口訣：
- **$n \to n - 1$**：遞迴樹深度為 $O(n)$。
  - 若分支數為 1 $\implies O(n)$（如 Q1）。
  - 若分支數為 2 $\implies O(2^n)$ 指數增長（如 Q2）。
- **$n \to n / 2$**：遞迴樹深度為 $O(\log n)$。
  - 若分支數為 1 $\implies O(\log n)$（如 Q4）。
  - 若分支數為 2 $\implies O(n)$ 節點總數（如 Q3）。

---

## 第一題：線性遞減常數加法 (線性搜尋模型)

### 1. 遞迴關係式
- **遞迴式**：$T(n) = T(n-1) + 8$
- **邊界條件**：$T(1) = 1$

### 2. 展開推導
利用反覆代入展開：

$$
\begin{aligned}
T(n) &= T(n-1) + 8 \\
&= [T(n-2) + 8] + 8 = T(n-2) + 2 \times 8 \\
&= [T(n-3) + 8] + 2 \times 8 = T(n-3) + 3 \times 8 \\
&\;\;\vdots \\
&= T(1) + (n-1) \times 8
\end{aligned}
$$

代入邊界條件 $T(1) = 1$：

$$
\begin{aligned}
T(n) &= 1 + 8(n - 1) \\
&= 8n - 7
\end{aligned}
$$

### 3. 理解與應用
- **幾何直覺**：此結構不是樹狀，而是一條長度為 $n$ 的單向鏈結
- **複雜度**：$T(n) = O(n)$
- **對應演算法**：常見於單層線性遍歷、線性搜尋或單重遞迴計算階乘/累加。

---

## 第二題：線性遞減雙分支加法 (指數爆炸模型)

### 1. 遞迴關係式
- **遞迴式**：$T(n) = 2T(n-1) + 9$
- **邊界條件**：$T(1) = 1$

### 2. 展開推導
逐步展開並提出常數係數：

$$
\begin{aligned}
T(n) &= 2T(n-1) + 9 \\
&= 2[2T(n-2) + 9] + 9 = 2^2 T(n-2) + 9(2 + 1) \\
&= 2^2[2T(n-3) + 9] + 9(2 + 1) = 2^3 T(n-3) + 9(2^2 + 2 + 1) \\
&\;\;\vdots \\
&= 2^{n-1} T(1) + 9 \sum_{i=0}^{n-2} 2^i
\end{aligned}
$$

利用等比級數求和公式 $\sum_{i=0}^{k-1} 2^i = 2^k - 1$：

$$
T(n) = 2^{n-1} T(1) + 9(2^{n-1} - 1)
$$

代入邊界條件 $T(1) = 1$：

$$
\begin{aligned}
T(n) &= 2^{n-1} \cdot 1 + 9 \cdot 2^{n-1} - 9 \\
&= 10 \cdot 2^{n-1} - 9 \\
&= 5 \cdot 2^n - 9
\end{aligned}
$$

### 3. 理解與應用
- **幾何直覺**：樹深為 $n$，每一層節點數以 $2^k$ 倍增，計算總量完全被底層龐大的葉節點數量支配。
- **複雜度**：$T(n) = O(2^n)$
- **對應演算法**：未加記憶化快取的樸素費氏數列、窮舉所有子集合問題、河內塔問題

---

## 第三題：分治法雙分支展開
### 1. 遞迴關係式
- **遞迴式**：$T(n) = 2T\left(\frac{n}{2}\right) + 1$
- **邊界條件**：$T(1) = 1$

### 2. 展開推導
逐步展開子問題：

$$
\begin{aligned}
T(n) &= 2\left[2T\left(\frac{n}{4}\right) + 1\right] + 1 = 4T\left(\frac{n}{4}\right) + 2 + 1 \\
&= 4\left[2T\left(\frac{n}{8}\right) + 1\right] + 2 + 1 = 8T\left(\frac{n}{8}\right) + 4 + 2 + 1 \\
&\;\;\vdots \\
&= 2^k T\left(\frac{n}{2^k}\right) + (2^{k-1} + 2^{k-2} + \dots + 2 + 1) \\
&= 2^k T\left(\frac{n}{2^k}\right) + (2^k - 1)
\end{aligned}
$$

令終止條件 $\frac{n}{2^k} = 1 \implies 2^k = n \implies k = \log_2 n$：

$$
\begin{aligned}
T(n) &= n \times T(1) + (n - 1) \\
&= n \times 1 + n - 1 \\
&= 2n - 1
\end{aligned}
$$

### 3. 理解與應用
- **幾何直覺**：一棵深度為 $\log_2 n$ 的完整二元樹，葉節點共有 $n$ 個，內部節點共有 $n-1$ 個，總節點數為 $2n - 1$。
- **複雜度**：$T(n) = O(n)$
- **主定理驗證 (Master Theorem)**：
  - 形式：$T(n) = aT(n/b) + f(n)$，此處 $a=2, b=2, f(n)=1$
  - 臨界項：$n^{\log_b a} = n^{\log_2 2} = n^1$
  - 因 $f(n) = O(n^0)$ 嚴格小於 $n^1$，屬於 Case 1 $\implies T(n) = \Theta(n)$。
- **對應演算法**：完整二元樹的節點遍歷（Tree Traversal）。

---

## 第四題：分治法單分支展開 

### 1. 遞迴關係式
- **遞迴式**：$T(n) = T\left(\frac{n}{2}\right) + 1$
- **邊界條件**：$T(1) = 1$

### 2. 展開推導
逐步展開單分支：

$$
\begin{aligned}
T(n) &= \left[T\left(\frac{n}{4}\right) + 1\right] + 1 = T\left(\frac{n}{4}\right) + 2 \\
&= \left[T\left(\frac{n}{8}\right) + 1\right] + 2 = T\left(\frac{n}{8}\right) + 3 \\
&\;\;\vdots \\
&= T\left(\frac{n}{2^k}\right) + k
\end{aligned}
$$

令 $\frac{n}{2^k} = 1 \implies 2^k = n \implies k = \log_2 n$：

$$
\begin{aligned}
T(n) &= T(1) + \log_2 n \\
&= 1 + \log_2 n
\end{aligned}
$$

### 3. 理解與應用
- **幾何直覺**：每次折半問題規模，只保留一邊探索，展開步驟直接等於折半次數（即樹高）。
- **複雜度**：$T(n) = O(\log n)$
- **主定理驗證 (Master Theorem)**：
  - $a=1, b=2, f(n)=1$
  - 臨界項：$n^{\log_b a} = n^{\log_2 1} = n^0 = 1$
  - 因 $f(n) = \Theta(n^{\log_b a}) = \Theta(1)$，屬於 Case 2 $\implies T(n) = \Theta(\log n)$。
- **對應演算法**：二分搜尋法（Binary Search）、平衡二元搜尋樹（AVL / Red-Black Tree）的單路徑查詢。
