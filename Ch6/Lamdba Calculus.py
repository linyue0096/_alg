import re

# ==========================================
# 1. AST 定義 (Abstract Syntax Tree)
# ==========================================
class Var:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

class Abs:
    def __init__(self, param: str, body):
        self.param = param
        self.body = body

    def __str__(self):
        return f"(\\{self.param}.{self.body})"

class App:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.right})"

# ==========================================
# 2. 自由變數與替換運算 (含避免捕獲的 Alpha-conversion)
# ==========================================
def free_vars(expr):
    """取得運算式中的自由變數集合"""
    if isinstance(expr, Var):
        return {expr.name}
    elif isinstance(expr, Abs):
        return free_vars(expr.body) - {expr.param}
    elif isinstance(expr, App):
        return free_vars(expr.left) | free_vars(expr.right)
    return set()

def all_vars(expr):
    """取得運算式中出現過的所有變數名稱"""
    if isinstance(expr, Var):
        return {expr.name}
    elif isinstance(expr, Abs):
        return {expr.param} | all_vars(expr.body)
    elif isinstance(expr, App):
        return all_vars(expr.left) | all_vars(expr.right)
    return set()

def fresh_var(base: str, used: set) -> str:
    """生成未在 used 集合出現的新變數名稱 (例如 x -> x1 -> x2)"""
    i = 1
    candidate = f"{base}{i}"
    while candidate in used:
        i += 1
        candidate = f"{base}{i}"
    return candidate

def substitute(expr, var_name: str, replacement):
    """
    [var_name := replacement] expr
    在 expr 中，將自由出現的 var_name 替換為 replacement
    """
    if isinstance(expr, Var):
        return replacement if expr.name == var_name else expr

    elif isinstance(expr, App):
        return App(
            substitute(expr.left, var_name, replacement),
            substitute(expr.right, var_name, replacement)
        )

    elif isinstance(expr, Abs):
        if expr.param == var_name:
            # 變數被重新綁定，停止向下替換
            return expr
        
        # 檢查變數捕獲 (Variable Capture)
        if expr.param in free_vars(replacement):
            # 發生變數名稱衝突，執行 alpha-conversion 重新命名參數
            used = free_vars(expr.body) | free_vars(replacement) | {var_name}
            new_param = fresh_var(expr.param, used)
            renamed_body = substitute(expr.body, expr.param, Var(new_param))
            return Abs(new_param, substitute(renamed_body, var_name, replacement))
        else:
            return Abs(expr.param, substitute(expr.body, var_name, replacement))

# ==========================================
# 3. 單步正規歸約 (Normal Order Reduction)
# ==========================================
def reduce_step(expr):
    """
    執行一步最外層最左側的 Beta-reduction。
    回傳 (new_expr, has_reduced)
    """
    # 規則 1: 遇到 Redex: ((\x. body) arg)
    if isinstance(expr, App) and isinstance(expr.left, Abs):
        return substitute(expr.left.body, expr.left.param, expr.right), True

    # 規則 2: 嘗試在 App 的左子樹化簡
    if isinstance(expr, App):
        new_left, reduced = reduce_step(expr.left)
        if reduced:
            return App(new_left, expr.right), True
        
        # 左子樹無法再化簡，嘗試化簡右子樹
        new_right, reduced = reduce_step(expr.right)
        if reduced:
            return App(expr.left, new_right), True

    # 規則 3: 若為抽象函式，嘗試化簡其函數體 (body)
    if isinstance(expr, Abs):
        new_body, reduced = reduce_step(expr.body)
        if reduced:
            return Abs(expr.param, new_body), True

    return expr, False

def evaluate(expr, max_steps=50):
    """逐步執行化簡並輸出完整過程"""
    current = expr
    print(f"Step 0: {current}")
    for step in range(1, max_steps + 1):
        next_expr, reduced = reduce_step(current)
        if not reduced:
            print(f"=> 已達正規形式 (Normal Form)！共 {step - 1} 步。")
            return current
        current = next_expr
        print(f"Step {step}: {current}")

    print(f"=> 超過最大步數限制 ({max_steps} 步)，可能存在無窮迴圈/非終止運算。")
    return current

# ==========================================
# 4. 語法解析器 (Lexer & Recursive Descent Parser)
# 語法支援: \x. y、λx. y、括號與函式套用
# ==========================================
def tokenize(code: str):
    token_spec = [
        ('LAMBDA', r'\\|λ'),
        ('DOT',    r'\.'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('ID',     r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('SKIP',   r'\s+'),
    ]
    regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    tokens = []
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        if kind != 'SKIP':
            tokens.append((kind, match.group()))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def consume(self, expected_kind=None):
        kind, val = self.peek()
        if expected_kind and kind != expected_kind:
            raise SyntaxError(f"預期 {expected_kind}，但得到 {kind}")
        self.pos += 1
        return val

    def parse(self):
        expr = self.parse_expression()
        if self.pos < len(self.tokens):
            raise SyntaxError(f"未預期的符號: {self.peek()[1]}")
        return expr

    def parse_expression(self):
        # Expression ::= Application
        return self.parse_application()

    def parse_application(self):
        # Application ::= Atom+ (左結合)
        expr = self.parse_atom()
        while True:
            kind, _ = self.peek()
            if kind in ('LAMBDA', 'ID', 'LPAREN'):
                right = self.parse_atom()
                expr = App(expr, right)
            else:
                break
        return expr

    def parse_atom(self):
        kind, val = self.peek()
        if kind == 'LAMBDA':
            self.consume('LAMBDA')
            param = self.consume('ID')
            self.consume('DOT')
            body = self.parse_expression()
            return Abs(param, body)
        elif kind == 'ID':
            self.consume('ID')
            return Var(val)
        elif kind == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        else:
            raise SyntaxError(f"非預期的 Token: {val}")

def parse(code: str):
    tokens = tokenize(code)
    return Parser(tokens).parse()

if __name__ == "__main__":
    examples = [
        (
            "布林值條件選擇 (IF TRUE A B => A)",
            # TRUE = \x.\y.x, FALSE = \x.\y.y
            # (\t.\f.t) A B
            r"((\x.\y.x) A) B"
        ),
        (
            "變數捕獲與 Alpha 轉換測試 (防止 y 被外層 capture)",
            # (\x.\y.x) y  -> 應自動將內層 y 轉為 y1，得到 \y1.y
            r"(\x.\y.x) y"
        ),
        (
            "Church 數字加法運算 (1 + 1 = 2)",
            # PLUS = \m.\n.\f.\x. m f (n f x)
            # ONE  = \f.\x. f x
            # PLUS ONE ONE
            r"(\m.\n.\f.\x. m f (n f x)) (\f.\x. f x) (\f.\x. f x)"
        ),
        (
            "Church 數字乘法運算 (2 * 2 = 4)",
            # MULT = \m.\n.\f. m (n f)
            # TWO  = \f.\x. f (f x)
            # MULT TWO TWO
            r"(\m.\n.\f. m (n f)) (\f.\x. f (f x)) (\f.\x. f (f x))"
        ),
    ]

    for title, code in examples:
        print("=" * 60)
        print(f"範例：{title}")
        print(f"輸入表達式: {code}")
        print("-" * 60)
        ast = parse(code)
        evaluate(ast)
        print()