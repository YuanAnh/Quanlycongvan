import sys
import uuid 
import MySQLdb as mdb
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow
from PyQt6 import uic

class DangkyApp(QMainWindow):
    def __init__(self, login_window=None):
        super(DangkyApp, self).__init__()
        uic.loadUi('Source/ui/dangki.ui', self)
        self.db = None
        self.cursor = None
        self.login_window = login_window
        self.connect_db()
        self.btndangki.clicked.connect(self.handle_register)
        self.btnquaylai.clicked.connect(self.handle_back)

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

    def handle_register(self):
        if not self.db:
            QMessageBox.critical(self, "Lỗi", "Chưa kết nối database!")
            return
        userid = self.txtid.text().strip()
        username = self.txtusername.text().strip()
        password = self.txtmk.text().strip()
        confirmpassword = self.txtxnmk.text().strip()
        hoten = self.txthoten.text().strip()
        email = self.txtemail.text().strip()
        sodienthoai = self.txtsdt.text().strip()
        vaitro = self.cbrole.currentText().strip()
        ngaysinh = self.dateEdit.date().toString("yyyy-MM-dd")
        gioitinh = self.cbgioitinh.currentText().strip()
        cauhoi1 = self.txtcau1.text().strip()
        cauhoi2 = self.txtcau2.text().strip()
        cauhoi3 = self.txtcau3.text().strip()

        if not all([userid, username, password, confirmpassword, hoten, email, sodienthoai, vaitro, ngaysinh, gioitinh, cauhoi1, cauhoi2, cauhoi3]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        if password != confirmpassword:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        try:
            # Kiểm tra userid đã tồn tại chưa
            check_userid_query = "SELECT userid FROM user WHERE userid=%s"
            self.cursor.execute(check_userid_query, (userid,))
            if self.cursor.fetchone():
                QMessageBox.warning(self, "Lỗi", "UserID đã tồn tại! Vui lòng nhập userID khác.")
                return

            # Kiểm tra username đã tồn tại chưa
            check_query = "SELECT username FROM user WHERE username=%s"
            self.cursor.execute(check_query, (username,))
            if self.cursor.fetchone():
                QMessageBox.warning(self, "Lỗi", "Tên đăng nhập đã tồn tại!")
                return

            # Thực hiện chèn vào DB
            query = """INSERT INTO user (userid, username, passwordhash, fullname, ngaysinh, gioitinh, email, phone, role, cauhoi1, cauhoi2, cauhoi3) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(query, (userid, username, password, hoten, ngaysinh, gioitinh, email, sodienthoai, vaitro, cauhoi1, cauhoi2, cauhoi3))
            self.db.commit()

            QMessageBox.information(self, "Thành công", "Đăng ký thành công!")
            self.close()
            if self.login_window:
                self.login_window.show()
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi truy vấn DB: {e}")

    def handle_back(self):
        self.close() 
        if self.login_window: 
            self.login_window.show() 

if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    window = DangkyApp() 
    window.show()
    sys.exit(app.exec())
