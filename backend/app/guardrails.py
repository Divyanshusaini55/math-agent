# guardrails.py
import re
from sympy.parsing.sympy_parser import parse_expr
from sympy import simplify

MATH_KEYWORDS = [r"\d", r"\+", r"-", r"\*", r"/", r"=", "integral", "derivative", "limit", "sum"]

def looks_like_math(text: str) -> bool:
    low = text.lower()
    if any(k in low for k in ["derivative", "integral", "limit", "solve", "differentiate", "integrate", "root", "equation"]):
        return True
    if re.search(r"[0-9].*[\+\-\*/\^=]", text):
        return True
    if "$" in text or "\\" in text:
        return True
    return False

def validate_output_answer(answer_text: str):
    try:
        lines = [l.strip() for l in answer_text.strip().splitlines() if l.strip()]
        candidate = lines[-1]
        expr = parse_expr(candidate, evaluate=True)
        _ = simplify(expr)
        return True, None
    except Exception as e:
        return False, str(e)
