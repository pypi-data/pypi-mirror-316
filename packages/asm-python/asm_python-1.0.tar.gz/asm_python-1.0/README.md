# asm_python

`asm_python` is a Python module that allows you to execute assembly code directly from Python using inline assembly in C.

## Installation and Usage

```bash
pip install asm_python
```
```python
import asm_python
asm_code = """
#your code assembly here (i am use clang to compile assembly code.)
"""
result = asm_python.asm(asm_code)
print("Result:", result)
```