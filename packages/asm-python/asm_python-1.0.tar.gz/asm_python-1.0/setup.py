from setuptools import setup, Extension

# Đọc nội dung của README.md làm long description
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# Định nghĩa module
module = Extension('asm_python', sources=['main.c'])

setup(
    name='asm_python',
    version='1.0',
    description='A module that executes assembly code.',
    long_description=long_description,  # Thêm long description
    long_description_content_type='text/markdown',  # Định dạng là markdown
    author='Bobby',
    ext_modules=[module],
    # Nếu bạn muốn thêm thông tin về các yêu cầu phụ thuộc, có thể thêm:
    # install_requires=[
    #     'some_dependency',
    # ],
)
