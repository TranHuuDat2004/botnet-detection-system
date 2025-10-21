# Hệ thống Dashboard Phát hiện Botnet

Đây là dự án cho Đồ án CNTT "Ứng dụng Học máy để phát hiện Botnet". Hệ thống bao gồm một dịch vụ AI (Python/Flask) và một giao diện web (Node.js/EJS) để người dùng có thể upload file log mạng và nhận kết quả phân tích.

## Hướng dẫn Cài đặt và Chạy

### **Bước 0: Chuẩn bị Dữ liệu (Bắt buộc)**

Do file dữ liệu quá lớn để lưu trữ trên GitHub, bạn cần tải nó về theo cách thủ công.

1.  **Tải file `cicids2017_cleaned.csv`** từ link Google Drive sau đây:
    [**>> TẢI DỮ LIỆU TẠI ĐÂY <<**](https://drive.google.com/file/d/1vIKT7tz8x_KJ8dxrhxM42EIbiebrJrmt/view?usp=sharing)

2.  **Đặt file vừa tải về vào thư mục gốc của dự án.** Cấu trúc thư mục của bạn sau bước này phải trông giống như sau:
    ```
    /DuAnCNTT
    ├── app.py
    ├── cicids2017_cleaned.csv  <-- FILE BẠN VỪA TẢI VỀ
    ├── create_test_files.py
    ├── server.js
    └── ... (các file khác)
    ```

### **Bước 1: Tạo các file Test (Tùy chọn)**

Nếu bạn muốn tạo ra các file CSV nhỏ để kiểm tra, hãy chạy script sau. Script này sẽ đọc file lớn và tạo ra một thư mục `test_data` chứa 8 file test nhỏ.

```bash
python create_test_files.py
```

### **Bước 2: Khởi động Backend AI (Python/Flask)**

1.  Mở một cửa sổ Terminal, di chuyển đến thư mục gốc của dự án.
2.  (Khuyến khích) Tạo và kích hoạt môi trường ảo.
3.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```
4.  Khởi động server AI:
    ```bash
    python app.py
    ```
5.  Server sẽ chạy tại `http://127.0.0.1:5000`. **Hãy giữ cho cửa sổ terminal này luôn mở.**

### **Bước 3: Khởi động Frontend Web (Node.js)**

1.  Mở một **cửa sổ Terminal thứ hai**, di chuyển đến thư mục gốc của dự án.
2.  Cài đặt các thư viện cần thiết:
    ```bash
    npm install
    ```
3.  Khởi động server web:
    ```bash
    npm start
    ```
4.  Server sẽ chạy tại `http://localhost:3000`.

### **Bước 4: Truy cập Ứng dụng**

Mở trình duyệt web và truy cập vào địa chỉ: [http://localhost:3000](http://localhost:3000). Bây giờ bạn đã có thể sử dụng ứng dụng.


---

## Lộ trình Phát triển Tiếp theo

Sản phẩm hiện tại đã hoàn thành phần lõi (Proof of Concept). Các bước tiếp theo sẽ tập trung vào việc nâng cấp sản phẩm thành một ứng dụng hoàn chỉnh và thân thiện với người dùng.

### 1. (Ưu tiên cao) Trực quan hóa Dữ liệu

-   **Mục tiêu:** Tóm tắt kết quả phân tích bằng biểu đồ để người dùng nắm bắt thông tin nhanh chóng.
-   **Công việc cần làm:**
    -   Tích hợp thư viện **Chart.js** vào dự án Frontend (`index.ejs`).
    -   Viết thêm logic JavaScript để xử lý dữ liệu JSON trả về từ backend.
    -   Đếm số lượng của từng loại `Attack_Prediction` (Normal, Bot, DDoS...).
    -   Vẽ một **biểu đồ tròn (Pie Chart)** để hiển thị tỷ lệ phần trăm giữa lưu lượng sạch và các loại tấn công.

### 2. (Ưu tiên cao) Cải thiện Trải nghiệm Người dùng (UX)

-   **Mục tiêu:** Giúp người dùng hiểu rõ trạng thái của hệ thống và tương tác dễ dàng hơn.
-   **Công việc cần làm:**
    -   **Thêm Trạng thái Loading:**
        -   Khi người dùng bấm nút "Phân tích", hãy vô hiệu hóa nút bấm.
        -   Hiển thị một biểu tượng loading (spinner) hoặc dòng chữ "Đang phân tích, vui lòng chờ...".
        -   Sau khi nhận được kết quả (hoặc lỗi), hãy ẩn loading và kích hoạt lại nút bấm.
    -   **Cải thiện Giao diện:**
        -   Sử dụng CSS để làm đẹp và sắp xếp lại layout cho chuyên nghiệp hơn. File để làm việc là `public/css/style.css`.

### 3. (Nên làm) Cải thiện Bảng Kết quả

-   **Mục tiêu:** Giúp người dùng thao tác hiệu quả hơn với lượng dữ liệu lớn.
-   **Công việc cần làm:**
    -   **Phân trang (Pagination):** Nếu kết quả trả về có nhiều hơn 50 dòng, hãy chia nhỏ ra thành nhiều trang. Thêm các nút "Trang trước", "Trang sau".
    -   **Tìm kiếm & Bộ lọc:** Thêm một ô `<input type="text">` phía trên bảng. Viết code JavaScript để khi người dùng gõ vào, bảng sẽ tự động lọc và chỉ hiển thị các dòng có chứa từ khóa đó.

### 4. (Nâng cao) Các hướng phát triển khác

-   **Giám sát Thư mục:** Xây dựng một script riêng để tự động phân tích các file log mới được thêm vào một thư mục được chỉ định.
-   **Hoàn thiện Báo cáo:** Dành thời gian cuối kỳ để viết báo cáo chi tiết, giải thích toàn bộ quy trình và phân tích các kết quả đạt được.

---

## Phân công Nhiệm vụ

-   **Frontend (UI/UX, Chart.js, Loading State...):** Dương Thị Thùy Linh.
-   **Backend & Tích hợp:** Trần Hữu Đạt.
-   Cả nhóm cùng thảo luận ý tưởng và viết báo cáo.