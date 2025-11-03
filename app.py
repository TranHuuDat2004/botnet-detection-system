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
    model = scaler = label_encoder = None

# --- API ENDPOINT ĐỂ DỰ ĐOÁN ---
@app.route('/predict', methods=['POST'])
def predict():
    if not all([model, scaler, label_encoder]):
         return jsonify({'error': 'Model hoặc các file hỗ trợ chưa được load thành công. Vui lòng kiểm tra console.'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'Không có file nào được gửi lên'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'File không có tên'}), 400

    try:
        input_df = pd.read_csv(file)
        original_df = input_df.copy()

        required_features = scaler.get_feature_names_out()
        
        if not all(feature in input_df.columns for feature in required_features):
            missing_features = [f for f in required_features if f not in input_df.columns]
            return jsonify({'error': f'File CSV thiếu các cột cần thiết: {", ".join(missing_features)}'}), 400
        
        features_df = input_df[required_features]

        features_scaled = scaler.transform(features_df)
        predictions_encoded = model.predict(features_scaled)
        predictions_text = label_encoder.inverse_transform(predictions_encoded)
        original_df['Attack_Prediction'] = predictions_text

        result = original_df.to_dict(orient='records')
        
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'Đã xảy ra lỗi trong quá trình xử lý: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)