import pandas as pd
import os

# --- CÁC THAM SỐ CÓ THỂ TÙY CHỈNH ---
SOURCE_FILE = 'cicids2017_cleaned.csv' # Tên file dữ liệu nguồn
NUM_SAMPLES = 100                      # Số lượng dòng muốn lấy cho các file test
OUTPUT_FOLDER = 'test_data'            # Tên thư mục để lưu các file test

# Link tải file dữ liệu nếu không tìm thấy
DOWNLOAD_LINK = "https://drive.google.com/file/d/1vIKT7tz8x_KJ8dxrhxM42EIbiebrJrmt/view?usp=sharing"

# ----------------------------------------

def create_test_files():
    """
    Hàm chính để đọc file dữ liệu lớn và tạo ra các file test nhỏ hơn.
    """
    # Tạo thư mục output nếu chưa tồn tại
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Đã tạo thư mục '{OUTPUT_FOLDER}' để chứa các file test.")

    print(f"Đang đọc file nguồn '{SOURCE_FILE}'... Vui lòng chờ.")
    try:
        df = pd.read_csv(SOURCE_FILE)
        print(f"Đọc file thành công! Tổng cộng có {len(df)} dòng.")
    except FileNotFoundError:
        print(f"\nLỖI: Không tìm thấy file '{SOURCE_FILE}'.")
        print("Hãy đảm bảo file này nằm cùng thư mục với script.")
        print(f"Bạn có thể tải file tại đây: {DOWNLOAD_LINK}\n")
        return

    # --- 1. Tạo File Test chỉ có 'Normal Traffic' ---
    print("\n[1/8] Đang tạo file 'test_normal_traffic.csv'...")
    try:
        normal_df = df[df['Attack Type'] == 'Normal Traffic'].sample(n=NUM_SAMPLES, random_state=42)
        normal_df.to_csv(os.path.join(OUTPUT_FOLDER, 'test_normal_traffic.csv'), index=False)
        print(f"-> Đã tạo thành công với {len(normal_df)} dòng.")
    except ValueError:
        print("-> Lỗi: Không đủ mẫu 'Normal Traffic'.")

    # --- 2. Tạo File Test chứa dữ liệu hỗn hợp ---
    print("\n[2/8] Đang tạo file 'test_mixed_traffic.csv'...")
    try:
        num_normal = NUM_SAMPLES // 2
        num_attack = NUM_SAMPLES - num_normal
        mixed_normal_df = df[df['Attack Type'] == 'Normal Traffic'].sample(n=num_normal, random_state=42)
        mixed_attack_df = df[df['Attack Type'] != 'Normal Traffic'].sample(n=num_attack, random_state=42)
        mixed_df = pd.concat([mixed_normal_df, mixed_attack_df]).sample(frac=1).reset_index(drop=True)
        mixed_df.to_csv(os.path.join(OUTPUT_FOLDER, 'test_mixed_traffic.csv'), index=False)
        print(f"-> Đã tạo thành công với {len(mixed_df)} dòng.")
    except ValueError:
        print("-> Lỗi: Không đủ mẫu để tạo file dữ liệu hỗn hợp.")

    # --- 3-8. Tạo các file chỉ chứa 1 loại tấn công cụ thể ---
    attack_types_to_create = [
        'Bot',
        'DDoS',
        'DoS',
        'Port Scanning',
        'Brute Force',
        'Web Attacks'
    ]

    for i, attack_type in enumerate(attack_types_to_create):
        filename = f'test_{attack_type.lower().replace(" ", "_")}_only.csv'
        print(f"\n[{i+3}/8] Đang tạo file '{filename}'...")
        
        attack_df = df[df['Attack Type'] == attack_type]
        
        if not attack_df.empty:
            # Lấy tối đa NUM_SAMPLES dòng, nếu không đủ thì lấy hết
            sample_size = min(NUM_SAMPLES, len(attack_df))
            attack_sample_df = attack_df.sample(n=sample_size, random_state=42)
            
            attack_sample_df.to_csv(os.path.join(OUTPUT_FOLDER, filename), index=False)
            print(f"-> Đã tạo thành công với {len(attack_sample_df)} dòng.")
        else:
            print(f"-> Không tìm thấy dòng nào có nhãn '{attack_type}'. Bỏ qua.")

    print(f"\nHoàn thành! Tất cả các file test đã được lưu trong thư mục '{OUTPUT_FOLDER}'.")

if __name__ == '__main__':
    create_test_files()