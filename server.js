const express = require('express');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const path = require('path');

const app = express();
const port = 3000;

// Cấu hình EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Thiết lập middleware để phục vụ các file tĩnh từ thư mục 'public'
app.use(express.static(path.join(__dirname, 'public')));

// Cấu hình Multer
const upload = multer({ storage: multer.memoryStorage() });

// Route để hiển thị trang chủ
app.get('/', (req, res) => {
    res.render('index', { results: null, error: null });
});

// Route để xử lý upload
app.post('/analyze', upload.single('csvfile'), async (req, res) => {
    if (!req.file) {
        return res.render('index', { results: null, error: 'Vui lòng chọn một file để upload.' });
    }

    try {
        const formData = new FormData();
        formData.append('file', req.file.buffer, {
            filename: req.file.originalname,
            contentType: req.file.mimetype,
        });

        console.log('Đang chuyển tiếp file đến Flask API...');

        const response = await axios.post('http://127.0.0.1:5000/predict', formData, {
            headers: {
                ...formData.getHeaders()
            },
            timeout: 60000 // 60 giây
        });

        console.log('Đã nhận kết quả từ Flask API.');

        res.render('index', { results: response.data, error: null });

    } catch (error) {
        console.error('Lỗi khi gọi Flask API:', error.message);
        let errorMessage = 'Đã xảy ra lỗi khi phân tích file.';
        if (error.response && error.response.data && error.response.data.error) {
            errorMessage = `Lỗi từ server AI: ${error.response.data.error}`;
        }
        res.render('index', { results: null, error: errorMessage });
    }
});

// Khởi động server
app.listen(port, () => {
    console.log(`Dashboard đang chạy tại http://localhost:${port}`);
});