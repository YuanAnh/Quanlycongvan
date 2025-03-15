import sys
import MySQLdb as mdb
from PyQt6 import QtWidgets, uic
from dscvden import DanhSachCVDen
from PyQt6.QtWidgets import QMessageBox

class DKCVDen(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(DKCVDen, self).__init__()
        uic.loadUi('ui/dkycvden.ui', self)  # Đảm bảo file .ui nằm đúng vị trí
        self.parent = parent
        
        # Kết nối đến DB
        self.db = None
        self.cursor = None
        self.connect_db()
        
        # Nút "Ghi dữ liệu"
        self.btnghidulieu.clicked.connect(self.ghi_du_lieu)
        # Nút "Hủy" nếu cần
        self.btnhuy.clicked.connect(self.dong)
        
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

    def ghi_du_lieu(self):
        try:
            congvandenid = self.txtcvid.text().strip()
            socongvan = self.txtsocongvan.text().strip()
            ngaynhan = self.datengaynhan.date().toString("yyyy-MM-dd")
            noigui = self.cbnoigui.currentText().strip()
            noidung = self.txtnoidung.toPlainText().strip()
            trangthai = self.cbtrangthai.currentText().strip()
            phongbanphutrach = self.cbphongban.currentText().strip()
            linkdinhkem = self.txtfiledinhkem.text().strip()


            if not all([congvandenid, socongvan, ngaynhan, noigui, noidung, trangthai, phongbanphutrach, linkdinhkem]):
                QMessageBox.warning(self, "Lỗi", "Các trường Nội dung trích yếu và Nơi nhận không được để trống!")
                return

            sql = """
            INSERT INTO congvanden (congvandenid, socongvan, ngaynhan, noigui, noidung, trangthai, phongbanphutrach, linkdinhkem)
            VALUES (%s ,%s, %s, %s, %s, %s, %s, %s)
            """
            values = (congvandenid, socongvan, ngaynhan, noigui, noidung, trangthai, phongbanphutrach, linkdinhkem)
            self.cursor.execute(sql, values)
            self.db.commit()

            QMessageBox.information(self, "Thành công", "Đã thêm công văn đến thành công!")
            self.clear_form()
            self.hide()
            self.danhsachcvden = DanhSachCVDen(self)
            self.danhsachcvden.show()

        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm công văn!\n{e}")


    def load_data(self):
        pass

    def clear_form(self):
        """Xoá dữ liệu trên form sau khi ghi."""
        self.txtcvid.clear()
        self.txtsocongvan.clear()
        self.cbnoigui.setCurrentIndex(0)
        self.txtnoidung.clear()
        self.cbphongban.setCurrentIndex(0)
        self.txtfiledinhkem.clear()
        self.datengaynhan.setDate(self.datengaynhan.minimumDate())
        self.cbtrangthai.setCurrentIndex(0)

    def dong(self):
        self.close() 
        if self.parent: 
            self.parent.show() 



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DKCVDen()
    sys.exit(app.exec())