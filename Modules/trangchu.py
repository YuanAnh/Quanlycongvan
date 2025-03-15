import sys
import MySQLdb as mdb
from qtpy import QtWidgets, uic
from dsvcdi import DanhSachCVDi
from dscvden import DanhSachCVDen
from dkcvdi import DKCVDI
from dkcvden import DKCVDen
from danhsachphongban import DanhSachPhongBan
from luutru import LuuTruCongVan
from pheduyet import PheDuyetCongVan
from tk import ThongKe
from PyQt6.QtWidgets import QMessageBox

class TrangChuCongVan(QtWidgets.QMainWindow):
    def __init__(self, login_window=None, current_user=None, current_role=None, current_fullname=None):
        super(TrangChuCongVan, self).__init__()
        uic.loadUi('ui/trangchu.ui', self)
        self.login_window = login_window
        self.current_user = current_user  # Lưu username của người đăng nhập
        self.current_role = current_role
        self.current_fullname = current_fullname
        # Khởi tạo database (dùng chung từ login)
        self.db = None
        self.cursor = None
        
        # Kết nối database
        self.connect_db()
        
        # Kết nối các nút với chức năng
        self.btncongvanden.clicked.connect(self.CongVanDen)
        self.btncongvandi.clicked.connect(self.CongVanDi)
        self.btndangkyden.clicked.connect(self.DangKyDen)
        self.btndangkydi.clicked.connect(self.DangKyDi)
        self.btnquanlyphongban.clicked.connect(self.QuanLyPhongBan)
        self.btnluutru.clicked.connect(self.LuuTruCongVan)
        self.btnpheduyet.clicked.connect(self.PheDuyetCongVan)
        self.btnthongke.clicked.connect(self.ThongKeBaoCao)
        self.btndangxuat.clicked.connect(self.XuLyDangXuat)
        self.btnthoat.clicked.connect(self.DongChuongTrinh)
        
        self.show()
        self.load_data()

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

    def close_db(self):
        if self.db:
            self.cursor.close()
            self.db.close()
            self.db = None
            self.cursor = None
            print("🔴 Đã đóng kết nối DB")

    def CongVanDi(self):
        self.hide()
        self.congvandi_window = DanhSachCVDi(self)
        self.congvandi_window.show()

    def CongVanDen(self):
        self.hide()
        self.congvanden_window = DanhSachCVDen(self)
        self.congvanden_window.show()

    def DangKyDi(self):
        self.hide()
        self.dangkidi_window = DKCVDI(self, self.current_user, self.current_role)
        self.dangkidi_window.show()

    def DangKyDen(self):
        self.hide()
        self.dangkiden_window = DKCVDen(self)
        self.dangkiden_window.show()

    def QuanLyPhongBan(self):
        self.hide()
        self.quanli_window = DanhSachPhongBan(self)
        self.quanli_window.show()

    def LuuTruCongVan(self):
        self.hide()
        self.luutru_window = LuuTruCongVan(self)
        self.luutru_window.show()


    def PheDuyetCongVan(self):
        self.hide()
        self.pheduyet_window = PheDuyetCongVan(self)
        self.pheduyet_window.show()
        
    def ThongKeBaoCao(self):
        self.hide()
        self.thongke_window = ThongKe(self)
        self.thongke_window.show()

    def XuLyDangXuat(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Bạn có chắc chắn muốn đăng xuất?")
        msg.setWindowTitle("Xác nhận đăng xuất")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.button(QMessageBox.Yes).setText("Có")
        msg.button(QMessageBox.No).setText("Không")

        ret = msg.exec()

        if ret == QMessageBox.Yes:
            self.close_db() 
            self.close()


            if not self.login_window:
                from login import LoginApp 
                self.login_window = LoginApp()
            
                self.login_window.txt_username.clear()
                self.login_window.txt_password.clear()
                self.login_window.show()

            self.deleteLater()
    def load_data(self):    
        pass

    def DongChuongTrinh(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Bạn có chắc chắn muốn đóng chương trình?")
        msg.setWindowTitle("Xác nhận thoát")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.button(QMessageBox.Yes).setText("Có")
        msg.button(QMessageBox.No).setText("Không")
        
        ret = msg.exec()
        
        if ret == QMessageBox.Yes:
            self.close_db()  # Đóng database trước khi thoát
            QtWidgets.QApplication.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrangChuCongVan()
    sys.exit(app.exec())
