import ctypes
import os
import subprocess
import sys
import shutil

# Đường dẫn đến tệp thư viện Swift
lib_path = os.path.join(os.path.dirname(__file__), 'swiftonpython.so')

# Kiểm tra xem thư viện đã tồn tại hay chưa
if not os.path.exists(lib_path):
    # Nếu thư viện không tồn tại, biên dịch mã Swift thành thư viện .so
    swift_code_file = os.path.join(os.path.dirname(__file__), 'main.swift')
    output_file = lib_path  # Đặt tên thư viện xuất ra là swiftonpython.so

    # Kiểm tra xem Swift có được cài đặt không
    if not shutil.which("swift"):
        print("Swift compiler (swift) is not found. Please install Swift.")
        sys.exit(1)

    # Kiểm tra xem tệp Swift có tồn tại không
    if not os.path.exists(swift_code_file):
        print(f"Swift code file {swift_code_file} not found!")
        sys.exit(1)

    # Lệnh biên dịch Swift thành thư viện .so
    swift_compile_command = [
        'swiftc', '-emit-library', '-o', output_file, swift_code_file
    ]

    try:
        print(f"Compiling Swift code from {swift_code_file} into shared library ({output_file})...")
        subprocess.check_call(swift_compile_command)
        print(f"Library {output_file} has been created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling Swift code: {e}")
        sys.exit(1)

# Tải thư viện Swift đã biên dịch
swiftpython = ctypes.CDLL(lib_path)

# Khai báo hàm từ thư viện Swift
swiftpython.swiftonpython.argtypes = [ctypes.c_char_p]  # Đối số là chuỗi ký tự
swiftpython.swiftonpython.restype = None  # Hàm không trả về giá trị

def swift(code):
    """
    Gọi hàm Swift từ thư viện để thực thi mã Swift.

    Parameters:
    - code: Mã Swift cần thực thi, dưới dạng chuỗi ký tự.
    """
    # Mã hóa chuỗi thành UTF-8 và gọi hàm Swift
    swift_code = code.encode('utf-8')
    swiftpython.swiftonpython(swift_code)
