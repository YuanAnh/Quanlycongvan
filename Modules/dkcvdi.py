import sys
import MySQLdb as mdb
from PyQt6 import QtWidgets, uic
from dsvcdi import DanhSachCVDi
from PyQt6.QtWidgets import QMessageBox, QFileDialog

class DKCVDI(QtWidgets.QMainWindow):
    def __init__(self, parent=None, current_user=None, current_role=None):
        super(DKCVDI, self).__init__()
        uic.loadUi('ui/dkicvdi.ui', self)
        self.parent = parent
        self.current_user = current_user
        self.current_role = current_role

        self.db = None
        self.cursor = None
        self.connect_db()
        
        self.btnGhiDuLieu.clicked.connect(self.GhiDuLieu)
        self.btnHuy.clicked.connect(self.HuyBo)
        self.btnChonFile.clicked.connect(self.chon_file_dinhkem)
        
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

    def GhiDuLieu(self):
        try:
            congvanid = self.txtcongvanid.text().strip()
            socongvan = self.txtsocongvan.text().strip()
            noidung = self.txtnoidung.toPlainText().strip() 
            nguoiky = self.txtnguoiky.text().strip()
            ngayphat = self.datengayphat.date().toString("yyyy-MM-dd") 
            noinhan = self.cbnoinhan.currentText().strip()
            phongbanphutrach = self.cbphongban.currentText().strip()
            loaicongvan = self.cbloaicongvan.currentText().strip() 
            trangthai = self.cbtrangthai.currentText().strip()
            linkdinhkem = self.txtfiledinhkem.text().strip()
            createdby = self.current_role  # Lấy userid từ biến global

            if not all([congvanid, socongvan, noidung, nguoiky, ngayphat, noinhan, phongbanphutrach, loaicongvan, trangthai]):
                QMessageBox.warning(self, "Lỗi", "Các trường Nội dung trích yếu và Nơi nhận không được để trống!")
                return

            # Tạo câu lệnh INSERT. Nếu cột id được tự động tăng, không cần truyền id_val
            sql = """
            INSERT INTO congvandi (congvandiid, socongvan, noidung, nguoiky, ngayphathanh, noinhan, phongbanphutrach, loaicongvan, trangthai, linkdinhkem, createdby)
            VALUES (%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (congvanid, socongvan, noidung, nguoiky, ngayphat, noinhan, phongbanphutrach, loaicongvan, trangthai, linkdinhkem, createdby)

            print("Values:", values)  # Debug
            self.cursor.execute(sql, values)
            self.db.commit()
            
            QMessageBox.information(self, "Thành công", "Đã thêm công văn thành công!")
            self.clear_form()

            self.hide()  # ẩn cửa sổ đăng ký
            self.danhsachcvdi = DanhSachCVDi(self)
            self.danhsachcvdi.show()

        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm công văn!\n{e}")

    def chon_file_dinhkem(self):
        """Mở hộp thoại chọn file và hiển thị đường dẫn vào txtfiledinhkem."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Chọn tệp đính kèm", "", "All Files (*);;PDF Files (*.pdf);;Word Files (*.docx);;Excel Files (*.xlsx)")
        
        if file_path:  # Nếu người dùng chọn file
            self.txtfiledinhkem.setText(file_path)

    def load_data(self):
        pass

    def clear_form(self):
        self.txtcongvanid.clear()
        self.txtsocongvan.clear()
        self.txtnoidung.clear()
        self.txtnguoiky.clear()
        self.cbphongban.setCurrentIndex
        self.cbnoinhan.setCurrentIndex(0)
        self.cbloaicongvan.setCurrentIndex(0)
        self.txtfiledinhkem.clear()
        self.datengayphat.setDate(self.datengayphat.minimumDate())
        self.cbtrangthai.setCurrentIndex(0)

    def HuyBo(self):
        self.close() 
        if self.parent: 
            self.parent.show() 

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DKCVDI()
    sys.exit(app.exec())
