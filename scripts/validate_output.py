import ast
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

VERIFY_PATH = os.path.join(os.path.dirname(__file__), '../verify.py')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../output')

class Assertion:
    def __init__(self, json_file, key_chain, expected_value, line):
        self.json_file = json_file
        self.key_chain = key_chain
        self.expected_value = expected_value
        self.line = line
        self.passed = None
        self.actual_value = None
        self.error = None

def extract_assertions_from_verify():
    with open(VERIFY_PATH, 'r') as f:
        tree = ast.parse(f.read(), filename=VERIFY_PATH)

    json_file_vars = {}
    assertions = []
    for node in ast.walk(tree):
        # Track assignments like: foo = json.load(file)
        if isinstance(node, ast.With):
            for item in node.items:
                if (
                    isinstance(item.context_expr, ast.Call)
                    and isinstance(item.context_expr.func, ast.Name)
                    and item.context_expr.func.id == 'open'
                ):
                    # Get the file name string
                    if len(item.context_expr.args) > 0 and isinstance(item.context_expr.args[0], ast.Constant):
                        file_path = item.context_expr.args[0].value
                        # Find the variable assigned to json.load(file)
                        for n in ast.walk(node):
                            if (
                                isinstance(n, ast.Assign)
                                and isinstance(n.value, ast.Call)
                                and getattr(n.value.func, 'attr', None) == 'load'
                            ):
                                var_name = n.targets[0].id
                                json_file_vars[var_name] = os.path.basename(file_path)
        # Find assert statements
        if isinstance(node, ast.Assert):
            # Only handle simple asserts like: assert foo["bar"] == 123
            if (
                isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Subscript)
                and isinstance(node.test.comparators[0], (ast.Constant, ast.Num))
            ):
                # Get the variable and key chain
                sub = node.test.left
                key_chain = []
                while isinstance(sub, ast.Subscript):
                    if isinstance(sub.slice, ast.Constant):
                        key_chain.insert(0, sub.slice.value)
                    elif isinstance(sub.slice, ast.Index) and isinstance(sub.slice.value, ast.Constant):
                        key_chain.insert(0, sub.slice.value.value)
                    sub = sub.value
                if isinstance(sub, ast.Name):
                    var_name = sub.id
                    json_file = json_file_vars.get(var_name)
                    if json_file:
                        expected_value = node.test.comparators[0].value
                        assertions.append(Assertion(json_file, key_chain, expected_value, node.lineno))
            # Handle dict-of-dict: assert foo["bar"]["baz"] == 123
            elif (
                isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Subscript)
                and isinstance(node.test.left.value, ast.Subscript)
                and isinstance(node.test.comparators[0], (ast.Constant, ast.Num))
            ):
                sub = node.test.left
                key_chain = []
                for _ in range(2):
                    if isinstance(sub.slice, ast.Constant):
                        key_chain.insert(0, sub.slice.value)
                    elif isinstance(sub.slice, ast.Index) and isinstance(sub.slice.value, ast.Constant):
                        key_chain.insert(0, sub.slice.value.value)
                    sub = sub.value
                if isinstance(sub, ast.Name):
                    var_name = sub.id
                    json_file = json_file_vars.get(var_name)
                    if json_file:
                        expected_value = node.test.comparators[0].value
                        assertions.append(Assertion(json_file, key_chain, expected_value, node.lineno))
    return assertions

def check_assertions(assertions):
    # Load all JSON files only once
    json_cache = {}
    for assertion in assertions:
        json_path = os.path.join(OUTPUT_DIR, assertion.json_file)
        if assertion.json_file not in json_cache:
            try:
                with open(json_path, 'r') as f:
                    json_cache[assertion.json_file] = json.load(f)
            except Exception as e:
                assertion.error = f"Failed to load {json_path}: {e}"
                assertion.passed = False
                continue
        
        data_to_check = json_cache[assertion.json_file]
        # If the file is status_total.json, navigate into the 'status' sub-dictionary
        if assertion.json_file == "status_total.json" and "status" in data_to_check:
            data_to_check = data_to_check["status"]
            
        try:
            value = data_to_check
            for key in assertion.key_chain:
                value = value[key]
            assertion.actual_value = value
            assertion.passed = (value == assertion.expected_value)
        except KeyError as e:
            keys_in_dict = list(value.keys()) if isinstance(value, dict) else "N/A (not a dict)"
            assertion.error = f"Key error accessing '{e.args[0]}'. Available keys: {keys_in_dict}"
            assertion.passed = False
        except Exception as e:
            assertion.error = f"Error accessing data: {e}"
            assertion.passed = False

def main():
    assertions = extract_assertions_from_verify()
    check_assertions(assertions)
    
    passed_assertions = [a for a in assertions if a.passed]
    failed_assertions = [a for a in assertions if not a.passed]

    logger.info("\n--- PASSED Assertions ---")
    if passed_assertions:
        for a in passed_assertions:
            logger.info(f"[PASS] {a.json_file} {a.key_chain} == {a.expected_value} (actual: {a.actual_value}) at line {a.line}")
    else:
        logger.info("No assertions passed.")

    logger.info("\n--- FAILED Assertions ---")
    if failed_assertions:
        for a in failed_assertions:
            logger.info(f"[FAIL] {a.json_file} {a.key_chain} == {a.expected_value} (actual: {a.actual_value}) at line {a.line}")
            if a.error:
                logger.error(f"    Error: {a.error}")
    else:
        logger.info("No assertions failed.")

    total_passed = len(passed_assertions)
    total_failed = len(failed_assertions)
    logger.info(f"\nSummary: {total_passed} passed, {total_failed} failed, {len(assertions)} total.")

if __name__ == "__main__":
    main()
