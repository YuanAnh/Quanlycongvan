import sys
import MySQLdb as mdb
from trangchu import TrangChuCongVan
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.uic import loadUi
from dangki import DangkyApp
from quenmatkhau import QuenMatKhauApp

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("ui/login.ui", self)
        self.db = None
        self.cursor = None
        self.connect_db()
        self.btn_login.clicked.connect(self.handle_login)
        self.btn_forgot.clicked.connect(self.handle_forgot)
        self.btn_register.clicked.connect(self.handle_register)

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
            print("✅ Kết nối MySQL thành công!")
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể kết nối DB!\n{e}")

    def handle_login(self):
        if not self.db:
            QMessageBox.critical(self, "Lỗi", "Chưa kết nối database!")
            return 
        username = self.txt_username.text()
        password = self.txt_password.text()
        try:
            query = "SELECT * FROM user WHERE username=%s AND passwordhash=%s"
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()
            if user:
                QMessageBox.information(self, "Thành công", "Đăng nhập thành công!")
                self.hide()
                # Lấy userid từ kết quả truy vấn (giả sử userid là cột đầu tiên)
                role = user[8] # Lấy role từ cột thứ 9
                fullname = user[3] # Lấy fullname từ cột thứ 4
                self.main_window = TrangChuCongVan(login_window=self, current_user=username, current_role=role, current_fullname=fullname)
                self.main_window.show()
            else:
                QMessageBox.warning(self, "Lỗi", "Sai tài khoản hoặc mật khẩu!")
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi truy vấn DB: {e}")

    def handle_forgot(self):
        self.hide()
        self.forget_windown = QuenMatKhauApp(self)
        self.forget_windown.show()
    
    def handle_register(self):
        self.hide()
        self.register_window = DangkyApp(self)
        self.register_window.show()

    def closeEvent(self, event):
        if self.db:
            self.cursor.close()
            self.db.close()
            print("🔴 Đã đóng kết nối DB")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec())
