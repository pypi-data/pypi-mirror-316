from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
import subprocess
import os
import sys
import shutil

class BuildSwiftExtension(build_ext):
    def run(self):
        # Kiểm tra Swift có được cài đặt không
        if not shutil.which("swift"):
            print("Swift compiler (swift) is not found. Please install Swift.")
            sys.exit(1)

        # Đường dẫn tệp Swift và thư viện chia sẻ .so
        swift_code_file = 'swiftonpython/main.swift'
        output_file = 'swiftonpython/swiftonpython.so'

        # Kiểm tra xem tệp Swift có tồn tại không
        if not os.path.exists(swift_code_file):
            print(f"Swift code file {swift_code_file} not found!")
            sys.exit(1)

        # Lệnh biên dịch Swift thành thư viện chia sẻ .so
        swift_compile_command = [
            'swiftc', '-emit-library', '-o', output_file, swift_code_file
        ]

        try:
            # Biên dịch mã Swift thành thư viện .so
            print(f"Compiling Swift code into shared library ({output_file})...")
            subprocess.check_call(swift_compile_command)
            print(f"Library {output_file} has been created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error compiling Swift code: {e}")
            sys.exit(1)

        # Tiến hành xây dựng phần còn lại của gói Python
        super().run()

# Đọc nội dung từ README.md
def read_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# Thiết lập gói Python và phần mở rộng
setup(
    name='swiftonpython',
    version='0.6',
    description='A Python library to run Swift code',
    author='Bobby',
    url='https://github.com/hqmdokkai/swiftonpython.git',
    packages=find_packages(),
    cmdclass={'build_ext': BuildSwiftExtension},
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    package_data={
        'swiftonpython': ['swift.py', 'main.swift', '__init__.py'],
    },
    include_package_data=True,  # Đảm bảo bao gồm tệp từ package_data
    # Không cài đặt yêu cầu phụ thuộc
)
