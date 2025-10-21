from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# --- LOAD CÁC FILE .pkl KHI SERVER KHỞI ĐỘNG ---
try:
    model = joblib.load('botnet_model.pkl')
    scaler = joblib.load('scaler.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    print("* Đã load thành công model, scaler, và label encoder.")
except Exception as e:
    print(f"* Lỗi khi load file .pkl: {e}")

# --- API ENDPOINT ĐỂ DỰ ĐOÁN ---
@app.route('/predict', methods=['POST'])
def predict():
    # Kiểm tra xem có file được gửi lên không
    if 'file' not in request.files:
        return jsonify({'error': 'Không có file nào được gửi lên'}), 400
    
    file = request.files['file']
    
    # Kiểm tra xem file có tên không
    if file.filename == '':
        return jsonify({'error': 'File không có tên'}), 400

    try:
        # Đọc file CSV người dùng upload
        input_df = pd.read_csv(file)
        
        # Giữ lại một bản copy của dữ liệu gốc để trả về
        original_df = input_df.copy()

        # --- QUY TRÌNH TIỀN XỬ LÝ (GIỐNG HỆT LÚC TRAIN) ---
        # 1. Chọn đúng các cột đặc trưng mà mô hình cần
        # (Lấy danh sách các cột từ scaler hoặc model)
        required_features = scaler.get_feature_names_out()
        
        # Kiểm tra xem file upload có đủ các cột cần thiết không
        if not all(feature in input_df.columns for feature in required_features):
            return jsonify({'error': 'File CSV thiếu các cột cần thiết cho việc dự đoán'}), 400
        
        # Chỉ giữ lại các cột cần thiết
        features_df = input_df[required_features]

        # 2. Áp dụng Scaling
        features_scaled = scaler.transform(features_df)

        # --- THỰC HIỆN DỰ ĐOÁN ---
        predictions_encoded = model.predict(features_scaled)
        
        # --- CHUYỂN KẾT QUẢ TỪ SỐ VỀ CHỮ ---
        predictions_text = label_encoder.inverse_transform(predictions_encoded)

        # Thêm cột kết quả dự đoán vào dữ liệu gốc
        original_df['Attack_Prediction'] = predictions_text

        # Chuyển DataFrame kết quả thành JSON để gửi về
        result = original_df.to_dict(orient='records')
        
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'Đã xảy ra lỗi trong quá trình xử lý: {str(e)}'}), 500

# Chạy server
if __name__ == '__main__':
    app.run(port=5000, debug=True)