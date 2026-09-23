from typing import List, Dict, Optional, Set

# 定義
Clause = List[int]
CNFFormula = List[Clause]
Assignment = Dict[int, bool]


# 公式簡化函式
def simplify(formula: CNFFormula, literal: int) -> Optional[CNFFormula]:
   
    new_formula = []
    neg_literal = -literal  # 相反的文字

    for clause in formula:
        # 情況 1：子句已被滿足，直接省略該子句
        if literal in clause:
            continue

        # 情況 2：子句內含有必為 False 的相反文字，需剔除該文字
        if neg_literal in clause:
            reduced_clause = [lit for lit in clause if lit != neg_literal]
            
            # 若剔除後子句空了，代表矛盾發生（無法滿足）
            if not reduced_clause:
                return None
            
            new_formula.append(reduced_clause)
        else:
            # 情況 3：子句與該文字無關，原封不動保留
            new_formula.append(clause)

    return new_formula


# 規則 
def find_unit_literal(formula: CNFFormula) -> Optional[int]:

    for clause in formula:
        if len(clause) == 1:
            return clause[0]
    return None


# 4. 規則 
def find_pure_literal(formula: CNFFormula) -> Optional[int]:

    literals = set()
    # 收集目前公式中所有出現過的文字
    for clause in formula:
        for lit in clause:
            literals.add(lit)

    # 檢查是否有文字的相反項不存在於集合中
    for lit in literals:
        if -lit not in literals:
            return lit
    return None

#(遞迴與回溯)
def dpll(formula: CNFFormula, assignment: Assignment) -> Optional[Assignment]:
    """
    DPLL (Davis-Putnam-Logemann-Loveland) 演算法主體：
    結合剪枝規則與深度優先搜尋（DFS）回溯法。
    """
    # 終止條件：若公式變為空列表，代表所有子句皆已被滿足，找到合法解！
    if not formula:
        return assignment


    unit_lit = find_unit_literal(formula)
    if unit_lit is not None:
        var = abs(unit_lit)
        # 若文字為正整數則設 True，負整數則設 False
        assignment[var] = (unit_lit > 0)
        
        # 根據此單一文字簡化公式
        simplified_f = simplify(formula, unit_lit)
        if simplified_f is None:
            return None  # 簡化過程中產生空子句，此路不通，回溯
        
        return dpll(simplified_f, assignment)

    # --------------------------------------------------
    # 步驟 2：Pure Literal Elimination (純文字消除)
    # --------------------------------------------------
    pure_lit = find_pure_literal(formula)
    if pure_lit is not None:
        var = abs(pure_lit)
        assignment[var] = (pure_lit > 0)
        
        simplified_f = simplify(formula, pure_lit)
        if simplified_f is None:
            return None
        
        return dpll(simplified_f, assignment)

    # --------------------------------------------------
    # 步驟 3：Splitting / Branching (分支與回溯)
    # 當沒有 Unit Clause 也沒有 Pure Literal 時，挑選一個變數猜測真假
    # --------------------------------------------------
    chosen_lit = formula[0][0]  # 簡單策略：挑選當前第一個子句的第一個文字
    var = abs(chosen_lit)

    # 分支嘗試 A：假設 chosen_lit 為 True
    branch_1_f = simplify(formula, chosen_lit)
    if branch_1_f is not None:
        result = dpll(branch_1_f, {**assignment, var: (chosen_lit > 0)})
        if result is not None:
            return result  # 猜測成功，向上回傳解

    # 分支嘗試 B：若嘗試 A 失敗，回溯並嘗試相反情況（即 chosen_lit 為 False）
    branch_2_f = simplify(formula, -chosen_lit)
    if branch_2_f is not None:
        return dpll(branch_2_f, {**assignment, var: (chosen_lit < 0)})

    # 兩個分支都宣告矛盾，代表當前路徑不可滿足
    return None

#輸出函式
def solve_sat(formula: CNFFormula) -> None:
    """
    封裝執行流程、補齊未指派的自由變數，並格式化印出結果。
    """
    # 取得公式中所有曾出現過的變數編號集合（例如 {1, 2, 3}）
    all_vars: Set[int] = {abs(lit) for clause in formula for lit in clause}
    
    # 啟動 DPLL，初始賦值字典為空
    solution = dpll(formula, {})
    
    if solution is not None:
        print("狀態: SATISFIABLE (可滿足)")
        # 自由變數補齊：部分變數即使不設值公式也已成立，預設補上 True 即可
        for var in all_vars:
            if var not in solution:
                solution[var] = True
        
        # 轉換為容易閱讀的格式：將整數鍵轉為 'x1', 'x2' 並按順序排序
        sorted_solution = {f"x{k}": v for k, v in sorted(solution.items())}
        print(f"變數賦值解: {sorted_solution}")
    else:
        print("狀態: UNSATISFIABLE (不可滿足)")


#測試
if __name__ == "__main__":
    # 測試 1：基本可滿足公式
    print("--- 測試 1：(x1 or x2) and (not x1 or x3) [預期：可滿足 SAT] ---")
    formula1 = [
        [1, 2],
        [-1, 3]
    ]
    solve_sat(formula1)

    # 測試 2：直接矛盾無解式
    print("\n--- 測試 2：(x1) and (not x1) [預期：互斥矛盾 UNSAT] ---")
    formula2 = [
        [1],
        [-1]
    ]
    solve_sat(formula2)

    # 測試 3：維基百科經典例題 (Unit Propagation 傳播測試)
    print("\n--- 測試 3：(x1 or not x2) and (not x1 or x2 or x3) and (not x1) [預期：可滿足 SAT] ---")
    formula3 = [
        [1, -2],
        [-1, 2, 3],
        [-1]
    ]
    solve_sat(formula3)

    # 測試 4：3-SAT 複合子句
    print("\n--- 測試 4：(x1 or not x2 or x3) and (not x1 or x2 or x4) and (not x3 or not x4) [預期：可滿足 SAT] ---")
    formula4 = [
        [1, -2, 3],
        [-1, 2, 4],
        [-3, -4]
    ]
    solve_sat(formula4)