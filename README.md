# Hướng Dẫn Cài Đặt và Chạy Chương Trình

## 1. Yêu Cầu Hệ Thống
- Python 3.x
- MySQL Server
- Visual Studio Code (hoặc bất kỳ IDE nào hỗ trợ Python)
- Các thư viện Python cần thiết (xem phần Cài Đặt)

## 2. Cấu Trúc Thư Mục
```
Source/
│── 📁Database/
│   ├── qlcv2.sql
│
│── 📁Modules/
│   ├── dangki.py
│   ├── danhsachphongban.py
│   ├── dklcvden.py
│   ├── dklcvdi.py
│   ├── dscvden.py
│   ├── dsvcdi.py
│   ├── luutru.py
│   ├── main.py
│   ├── pheduyet.py
│   ├── quenmatkhau.py
│   ├── tk.py
│   ├── trangchu.py
│
│── 📁ui/
│   ├── dangki.ui
│   ├── danhsachcden.ui
│   ├── danhsachcvdi.ui
│   ├── dklcvdi.ui
│   ├── dkycvden.ui
│   ├── dsphongban.ui
│   ├── login.ui
│   ├── luutru.ui
│   ├── pheduyet.ui
│   ├── quenmatkhau.ui
│   ├── tk.ui
│   ├── trangchu.ui
│
│── README.md
│── Requirements.txt
```

## 3. Cài Đặt
### 3.1 Cài Đặt Python và Thư Viện Phụ Thuộc

1. **Cài đặt Python**: Tải và cài đặt Python từ [python.org](https://www.python.org/downloads/).
2. **Cài đặt các thư viện cần thiết**:
   ```sh
   pip install -r Requirements.txt
   ```

### 3.2 Cấu Hình Cơ Sở Dữ Liệu
1. **Tạo database**:
   - Mở MySQL và tạo database mới:
     ```sql
     CREATE DATABASE qlcv2 CHARACTER SET utf8 COLLATE utf8_general_ci;
     ```
   - Chạy file `qlcv2.sql` trong thư mục `Database` để nhập dữ liệu mẫu.
2. **Cập nhật thông tin kết nối trong các file Python**:
   - Mở file có phần kết nối MySQL (`Modules/main.py`, `Modules/trangchu.py`, v.v.)
   - Sửa thông tin user, password, host nếu cần.

## 4. Chạy Chương Trình
1. Mở **Visual Studio Code** hoặc terminal.
2. Điều hướng đến thư mục `Source/`:
   ```sh
   cd path/to/Source
   ```
3. Chạy chương trình bằng lệnh:
   ```sh
   python Modules/main.py
   ```

## 5. Lưu Ý
- Đảm bảo MySQL đang chạy trước khi khởi động chương trình.
- Nếu gặp lỗi module không tìm thấy, kiểm tra lại cài đặt thư viện bằng `pip list`.
- Nếu chương trình không kết nối được với MySQL, kiểm tra lại thông tin user/password trong file Python.

---

**Chúc bạn thành công!** 🚀

