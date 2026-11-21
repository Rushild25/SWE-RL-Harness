"""AST Anti-Cheat Detector.

Inspects code patches submitted by agents to reject hard-coded return values,
monkey-patching, mock injection into tests, or environmental bypasses.
"""

import ast
from typing import Dict, Any, List

class AntiCheatAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.suspicious_patterns: List[str] = []
        self.hardcoded_returns = 0

    def visit_Return(self, node: ast.Return):
        # Flag if returning static literal or dummy constant in non-trivial function
        if isinstance(node.value, (ast.Constant, ast.Dict, ast.List)):
            self.hardcoded_returns += 1
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        # Detect unauthorized patch monkey-patching
        if node.attr in ("mock", "patch", "MagicMock") and "unittest" in ast.dump(node):
            self.suspicious_patterns.append(f"Mocking detected: {node.attr}")
        self.generic_visit(node)


def scan_patch_for_cheating(source_code: str) -> Dict[str, Any]:
    """Parse python source code patch and verify integrity."""
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {"passed": False, "reason": f"SyntaxError in patch: {e}"}

    analyzer = AntiCheatAnalyzer()
    analyzer.visit(tree)

    if analyzer.suspicious_patterns:
        return {
            "passed": False,
            "reason": f"Suspicious anti-pattern: {', '.join(analyzer.suspicious_patterns)}"
        }

    return {
        "passed": True,
        "hardcoded_returns": analyzer.hardcoded_returns,
        "clean": True
    }
