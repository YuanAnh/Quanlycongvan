import sys
import MySQLdb as mdb
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic

class QuenMatKhauApp(QMainWindow):
    def __init__(self, login_window=None):
        super().__init__()
        uic.loadUi('ui/quenmatkhau.ui', self)
        self.setWindowTitle("Quên Mật Khẩu")
        self.login_window = login_window
        self.db = None
        self.cursor = None
        self.connect_db()
        
        # Kết nối sự kiện cho các nút
        self.btn_xacnhan.clicked.connect(self.handle_reset_password)
        self.btn_thoat.clicked.connect(self.handle_exit)
        
    def connect_db(self):
        try:
            self.db = mdb.connect(
                host="localhost",
                user="root",
                passwd="",
                db="qlcv2",
                charset="utf8"
            )
            self.cursor = self.db.cursor()
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể kết nối DB!\n{e}")
            
    def handle_reset_password(self):
        if not self.db:
            QMessageBox.critical(self, "Lỗi", "Chưa kết nối database!")
            return
        
        name = self.txt_hoten.text()
        username = self.txt_tdn.text()
        new_password = self.txt_matkhaumoi.text()
        confirm_password = self.txt_xacnhanmk.text()
        cau_hoi1 = self.txt_cauhoi1.text().strip()
        cau_hoi2 = self.txt_cauhoi2.text().strip()
        cau_hoi3 = self.txt_cauhoi3.text().strip()
        
        # Kiểm tra các trường bắt buộc
        if not all([name, username, new_password, confirm_password]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
            
        # Kiểm tra mật khẩu xác nhận
        if new_password != confirm_password:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return
            
        try:
            # Kiểm tra tài khoản và email có tồn tại không
            check_query = "SELECT * FROM user WHERE fullname=%s AND username=%s"
            self.cursor.execute(check_query, (name, username))
            user = self.cursor.fetchone()
            
            if not user:
                QMessageBox.warning(self, "Lỗi", "Họ và tên hoặc tên đang nhập không chính xác!")
                return
            
            check_question = "SELECT * FROM user WHERE cauhoi1=%s AND cauhoi2=%s AND cauhoi3=%s"
            self.cursor.execute(check_question, (cau_hoi1, cau_hoi2, cau_hoi3))
            question = self.cursor.fetchone()

            if not question:
                QMessageBox.warning(self,"Lỗi", "Câu hỏi bảo mật không chính xác!")
                return
                
            # Cập nhật mật khẩu mới
            update_query = "UPDATE user SET passwordhash=%s WHERE fullname=%s AND username=%s"
            self.cursor.execute(update_query, (new_password, name, username))
            self.db.commit()
            
            QMessageBox.information(self, "Thành công", "Thay đổi mật khẩu thành công!")
            self.close()
            if self.login_window:
                self.login_window.show()
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi truy vấn DB: {e}")
            
    def handle_exit(self):
        self.close()
        if self.login_window:
            self.login_window.show()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuenMatKhauApp()
    window.show()
    sys.exit(app.exec())