const express = require('express');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const path = require('path');

const app = express();
const port = 3000;

// Cấu hình EJS và thư mục file tĩnh (public)
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));

// Cấu hình Multer để xử lý upload file trong bộ nhớ
const upload = multer({ storage: multer.memoryStorage() });

// === CÁC ROUTE ĐÃ CẬP NHẬT ===

/**
 * ROUTE 1: Trang chủ (dấu /), bây giờ sẽ là trang DASHBOARD.
 * - Nó sẽ tự động gọi API /stats của Python để lấy dữ liệu từ file stats.json.
 * - Sau đó, nó render file `dashboard.ejs` và truyền dữ liệu thống kê vào.
 */
app.get('/', async (req, res) => {
    try {
        console.log("Đang lấy dữ liệu thống kê cho Dashboard...");
        // Gọi đến API Flask (đang chạy ở cổng 5000) để lấy dữ liệu từ stats.json
        const response = await axios.get('http://127.0.0.1:5000/stats');
        
        // Render trang dashboard.ejs và truyền biến 'stats' chứa dữ liệu JSON vào
        res.render('dashboard', { 
            stats: response.data, 
            error: null 
        });

    } catch (error) {
        console.error('Lỗi khi lấy dữ liệu thống kê cho Dashboard:', error.message);
        const errorMessage = 'Không thể kết nối đến server AI để lấy dữ liệu tổng quan. Vui lòng đảm bảo server Python đang chạy.';
        // Render trang dashboard với thông báo lỗi
        res.render('dashboard', { 
            stats: null, 
            error: errorMessage 
        });
    }
});

/**
 * ROUTE 2: Trang Phân tích File (/analyze)
 * - Khi người dùng nhấn vào link "Phân tích File" trên menu.
 * - Nó chỉ đơn giản là render trang `analyze.ejs` với các biến rỗng.
 */
app.get('/analyze', (req, res) => {
    res.render('analyze', { 
        results: null, 
        error: null 
    });
});

/**
 * ROUTE 3: Xử lý việc upload file (POST đến /analyze)
 * - Khi người dùng submit form trên trang Phân tích.
 * - Logic này giữ nguyên như cũ, nhưng cuối cùng nó sẽ render lại trang `analyze.ejs` với kết quả.
 */
app.post('/analyze', upload.single('csvfile'), async (req, res) => {
    if (!req.file) {
        return res.render('analyze', { results: null, error: 'Vui lòng chọn một file để upload.' });
    }
    try {
        const formData = new FormData();
        formData.append('file', req.file.buffer, {
            filename: req.file.originalname,
            contentType: req.file.mimetype,
        });

        const response = await axios.post('http://127.0.0.1:5000/predict', formData, {
            headers: { ...formData.getHeaders() },
            timeout: 60000 // Tăng thời gian chờ
        });
        
        // Render lại trang `analyze.ejs` với dữ liệu kết quả
        res.render('analyze', { results: response.data, error: null });

    } catch (error) {
        console.error('Lỗi khi gọi API dự đoán:', error.message);
        let errorMessage = 'Đã xảy ra lỗi khi phân tích file.';
        if (error.response && error.response.data && error.response.data.error) {
            errorMessage = `Lỗi từ server AI: ${error.response.data.error}`;
        }
        res.render('analyze', { results: null, error: errorMessage });
    }
});

// Khởi động server
app.listen(port, () => {
    console.log(`Server chính đang chạy tại http://localhost:${port}`);
});