def simplify(expr):
    """基本代數化簡函數，去除冗餘的 0 與 1"""
    if not isinstance(expr, tuple):
        return expr

    op = expr[0]
    args = [simplify(arg) for arg in expr[1:]]

    # 常數折疊（兩者皆為純數字）
    if all(isinstance(a, (int, float)) for a in args):
        if op == '+': return args[0] + args[1]
        if op == '-': return args[0] - args[1]
        if op == '*': return args[0] * args[1]
        if op == '/': return args[0] / args[1] if args[1] != 0 else ('/', args[0], args[1])
        if op == '^': return args[0] ** args[1]

    u, v = args[0], args[1] if len(args) > 1 else None

    if op == '+':
        if u == 0: return v
        if v == 0: return u
    elif op == '-':
        if v == 0: return u
        if u == v: return 0
    elif op == '*':
        if u == 0 or v == 0: return 0
        if u == 1: return v
        if v == 1: return u
    elif op == '/':
        if u == 0: return 0
        if v == 1: return u
    elif op == '^':
        if v == 0: return 1
        if v == 1: return u
        if u == 0: return 0

    return (op, *args)


def sym_diff(expr, var='x'):
    """
    對符號運算式 expr 關於變數 var 求導（Recursive Symbolic Differentiation）
    expr 資料格式：
      - 常數: int 或 float (如 5, 3.14)
      - 變數: str (如 'x', 'y')
      - 運算元: (op, arg1, arg2) 或 (op, arg1)
    """
    # 1. Base Case: 常數
    if isinstance(expr, (int, float)):
        return 0

    # 2. Base Case: 變數
    if isinstance(expr, str):
        return 1 if expr == var else 0

    # 3. Recursive Cases: 組合運算式
    op = expr[0]

    # 加法: (u + v)' = u' + v'
    if op == '+':
        u, v = expr[1], expr[2]
        res = ('+', sym_diff(u, var), sym_diff(v, var))

    # 減法: (u - v)' = u' - v'
    elif op == '-':
        u, v = expr[1], expr[2]
        res = ('-', sym_diff(u, var), sym_diff(v, var))

    # 乘法 (Product Rule): (u * v)' = u'*v + u*v'
    elif op == '*':
        u, v = expr[1], expr[2]
        res = ('+', 
               ('*', sym_diff(u, var), v), 
               ('*', u, sym_diff(v, var)))

    # 除法 (Quotient Rule): (u / v)' = (u'*v - u*v') / (v^2)
    elif op == '/':
        u, v = expr[1], expr[2]
        res = ('/', 
               ('-', ('*', sym_diff(u, var), v), ('*', u, sym_diff(v, var))),
               ('^', v, 2))

    # 冪次 (Power Rule + Chain Rule): (u^n)' = n * u^(n-1) * u'
    elif op == '^':
        u, n = expr[1], expr[2]
        if isinstance(n, (int, float)):
            res = ('*', 
                   ('*', n, ('^', u, n - 1)), 
                   sym_diff(u, var))
        else:
            raise NotImplementedError("尚未支援變數次方的指數微分")

    # 自然對數: ln(u)' = u' / u
    elif op == 'ln':
        u = expr[1]
        res = ('/', sym_diff(u, var), u)

    else:
        raise ValueError(f"未知的運算子: {op}")

    # 進行代數化簡後回傳
    return simplify(res)


def expr_to_str(expr):
    """將 AST tuple 轉換成可讀字串"""
    if not isinstance(expr, tuple):
        return str(expr)
    op = expr[0]
    if len(expr) == 3:
        left = expr_to_str(expr[1])
        right = expr_to_str(expr[2])
        return f"({left} {op} {right})"
    elif len(expr) == 2:
        return f"{op}({expr_to_str(expr[1])})"


# 範例 1: f(x) = 3*x^2 + 5*x - 7
# 期待導數: 6*x + 5
expr1 = ('-', 
          ('+', ('*', 3, ('^', 'x', 2)), 
                ('*', 5, 'x')), 
          7)

diff1 = sym_diff(expr1, 'x')
print("原式 1:", expr_to_str(expr1))
print("導函數 1:", expr_to_str(diff1))
# 輸出: ((6 * x) + 5)

print("-" * 40)

# 範例 2: g(x) = x^2 / (x + 1)
# 期待導數: (2*x*(x + 1) - x^2) / (x + 1)^2
expr2 = ('/', ('^', 'x', 2), ('+', 'x', 1))
diff2 = sym_diff(expr2, 'x')
print("原式 2:", expr_to_str(expr2))
print("導函數 2:", expr_to_str(diff2))