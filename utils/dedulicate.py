import re
from typing import List
class Deduplicate:
    def __init__():
            pass
    
    # ------------- PYTHON -------------
    def deduplicate_python_imports(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'^(import\s+\w+|from\s+\w+\s+import\s+\w+)', code, re.MULTILINE))
        missing = [imp for imp in required if imp not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    # ------------- C / C++ / C# -------------
    def deduplicate_c_includes(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'#include\s*<[^>]+>', code))
        missing = [inc for inc in required if inc not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    def deduplicate_csharp_usings(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'using\s+[\w\.]+;', code))
        missing = [u for u in required if u not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    # ------------- Java -------------
    def deduplicate_java_imports(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'import\s+[\w\.]+;', code))
        missing = [imp for imp in required if imp not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    # ------------- JavaScript / TypeScript -------------
    def deduplicate_js_imports(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'import\s+.*?from\s+["\'].*?["\'];', code))
        missing = [imp for imp in required if imp not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    # ------------- Go -------------
    def deduplicate_go_imports(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'import\s+\(?\s*\"[^\"]+\"', code))
        missing = [imp for imp in required if imp not in existing]
        return "\n".join(["import \"" + m + "\"" for m in missing]) + "\n" + code if missing else code

    # ------------- Ruby -------------
    def deduplicate_ruby_requires(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'require\s+[\'"].+?[\'"]', code))
        missing = [req for req in required if req not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    # ------------- Swift -------------
    def deduplicate_swift_imports(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'import\s+\w+', code))
        missing = [imp for imp in required if imp not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    # ------------- Kotlin -------------
    def deduplicate_kotlin_imports(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'import\s+[\w\.]+', code))
        missing = [imp for imp in required if imp not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    # ------------- Scala -------------
    def deduplicate_scala_imports(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'import\s+[\w\.]+', code))
        missing = [imp for imp in required if imp not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    # ------------- Rust -------------
    def deduplicate_rust_use_statements(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'use\s+[\w\:]+;', code))
        missing = [imp for imp in required if imp not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    # ------------- PHP -------------
    def deduplicate_php_uses(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'use\s+[\w\\]+;', code))
        missing = [imp for imp in required if imp not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

    # ------------- Bash -------------
    def deduplicate_bash_sources(code: str, required: List[str]) -> str:
        existing = set(re.findall(r'(source|\. )\s+[\w\/\.]+', code))
        missing = [imp for imp in required if imp not in existing]
        return "\n".join(missing) + "\n" + code if missing else code

# ------------- Dispatcher -------------

deduplication_map = {
    "python":Deduplicate. deduplicate_python_imports(),
    "cpp":Deduplicate. deduplicate_c_includes(),
    "c":Deduplicate. deduplicate_c_includes(),
    "csharp":Deduplicate. deduplicate_csharp_usings(),
    "java":Deduplicate. deduplicate_java_imports(),
    "javascript":Deduplicate. deduplicate_js_imports(),
    "typescript":Deduplicate. deduplicate_js_imports(),
    "go":Deduplicate. deduplicate_go_imports(),
    "ruby":Deduplicate. deduplicate_ruby_requires(),
    "swift":Deduplicate. deduplicate_swift_imports(),
    "kotlin":Deduplicate. deduplicate_kotlin_imports(),
    "scala":Deduplicate. deduplicate_scala_imports(),
    "rust":Deduplicate. deduplicate_rust_use_statements(),
    "php":Deduplicate. deduplicate_php_uses(),
    "bash":Deduplicate. deduplicate_bash_sources(),
}

def deduplicate_imports(language: str, code: str, required_imports: List[str]) -> str:
    func = deduplication_map.get(language.lower())
    if func:
        return func(code, required_imports)
    return code 
