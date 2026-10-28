import numpy as np
import random

N = 200 # Số mẫu mỗi bit

def nrz_l(bits):
    levels = [0 if b == 1 else 1 for b in bits]
    return np.repeat(levels, N)

def nrzi(bits, start_level=0):
    levels = []
    current = start_level
    for b in bits:
        if b == 1: current = 1 - current
        levels.append(current)
    return np.repeat(levels, N)

def ami(bits):
    levels = []
    last = 1
    for b in bits:
        if b == 1:
            levels.append(last)
            last = -last
        else:
            levels.append(0)
    return np.repeat(levels, N)

def pseudoternary(bits):
    levels = []
    last = 1
    for b in bits:
        if b == 0:
            levels.append(last)
            last = -last
        else:
            levels.append(0)
    return np.repeat(levels, N)

def manchester(bits):
    levels = []
    for b in bits:
        if b == 0:
            levels.extend([1, -1]) # Nửa đầu cao, nửa sau thấp
        else:
            levels.extend([-1, 1]) # Nửa đầu thấp, nửa sau cao
    return np.repeat(levels, N // 2)

def diff_manchester(bits):
    levels = []
    current = 1
    for b in bits:
        if b == 0:
            current = -current
        levels.append(current)
        current = -current
        levels.append(current)
    return np.repeat(levels, N // 2)

# Các hàm giải mã: lấy mẫu ở giữa nửa đầu (giữa ô bit) và giữa nửa sau (nếu cần)

def nrz_l_decode(x):
    bits = []
    for i in range(0, len(x), N):
        sample = x[i + N//2] # Mẫu giữa ô bit
        bits.append(0 if sample == 1 else 1)
    return bits

def nrzi_decode(x):
    bits = []
    last_level = x[0] # Mức khởi đầu
    for i in range(0, len(x), N):
        current_level = x[i + N//2]
        if current_level != last_level:
            bits.append(1) # Đảo mức -> 1
        else:
            bits.append(0) # Giữ nguyên -> 0
        last_level = current_level
    return bits

def ami_decode(x):
    bits = []
    for i in range(0, len(x), N):
        sample = x[i + N//2]
        if sample == 0:
            bits.append(0)
        else:
            bits.append(1)
    return bits

def pseudoternary_decode(x):
    bits = []
    for i in range(0, len(x), N):
        sample = x[i + N//2]
        if sample == 0:
            bits.append(1)
        else:
            bits.append(0)
    return bits

def manchester_decode(x):
    bits = []
    half = N // 2
    for i in range(0, len(x), N):
        first_half = x[i + half//2] # Giữa nửa đầu
        second_half = x[i + half + half//2] # Giữa nửa sau
        if first_half == 1 and second_half == -1:
            bits.append(0)
        elif first_half == -1 and second_half == 1:
            bits.append(1)
        else:
            bits.append(None) # Lỗi
    return bits

def diff_manchester_decode(x):
    bits = []
    half = N // 2
    # Mẫu ở cuối nửa sau của bit trước
    last_second_half = x[half//2 + half] if len(x) > half else 1 
    
    for i in range(0, len(x), N):
        first_half = x[i + half//2] # Giữa nửa đầu
        second_half = x[i + half + half//2] # Giữa nửa sau
        
        # Kiểm tra xem có đảo mức ở đầu bit không
        if first_half == last_second_half:
            bits.append(1) # Giữ nguyên đầu bit -> 1
        else:
            bits.append(0) # Đảo mức đầu bit -> 0
            
        last_second_half = second_half
    return bits

# Các hàm kiểm tra

def test_decoders():
    # Danh sách các bộ mã: (Tên, Hàm mã hóa, Hàm giải mã)
    codecs = [
        ("NRZ-L", nrz_l, nrz_l_decode),
        ("NRZI", nrzi, nrzi_decode),
        ("Bipolar-AMI", ami, ami_decode),
        ("Pseudoternary", pseudoternary, pseudoternary_decode),
        ("Manchester", manchester, manchester_decode),
        ("Differential Manchester", diff_manchester, diff_manchester_decode)
    ]
    
    results = {}
    errors = {}
    
    for name, encode_func, decode_func in codecs:
        correct = 0
        total = 0
        first_error_seq = None
        
        # 1. Kiểm thử với 500 chuỗi ngẫu nhiên
        for _ in range(500):
            length = random.randint(8, 60)
            bits = [random.randint(0, 1) for _ in range(length)]
            encoded = encode_func(bits)
            decoded = decode_func(encoded)
            
            total += 1
            if bits == decoded:
                correct += 1
            elif first_error_seq is None:
                first_error_seq = bits
                
        # 2. Kiểm thử trường hợp biên: Toàn 0, toàn 1
        for bits in [[0]*10, [1]*10]:
            encoded = encode_func(bits)
            decoded = decode_func(encoded)
            total += 1
            if bits == decoded:
                correct += 1
            elif first_error_seq is None:
                first_error_seq = bits
                
        # 3. Kiểm thử trường hợp k bit 0 liên tiếp (k từ 0 đến 20)
        for k in range(21):
            # Tạo chuỗi có đúng k bit 0 ở giữa, bao quanh là bit 1
            bits = [1] * 5 + [0] * k + [1] * 5
            encoded = encode_func(bits)
            decoded = decode_func(encoded)
            total += 1
            if bits == decoded:
                correct += 1
            elif first_error_seq is None:
                first_error_seq = bits
                
        results[name] = (correct, total)
        errors[name] = first_error_seq

    # In báo cáo
    print("--- BẢNG KẾT QUẢ KIỂM THỬ ---")
    for name, (correct, total) in results.items():
        print(f"{name:25}: {correct} / {total} trường hợp đúng")
        if correct < total:
            print(f"   -> Chuỗi gây lỗi đầu tiên: {errors[name]}")
            
test_decoders()