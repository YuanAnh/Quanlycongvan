import sys
import MySQLdb as mdb
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QInputDialog, QComboBox
from PyQt6.QtCore import QDate

class DanhSachCVDen(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(DanhSachCVDen, self).__init__()
        uic.loadUi('ui/danhsachcvden.ui', self)
        self.parent = parent
        self.show()

        self.db = None
        self.cursor = None
        self.connect_db()
        self.load_data()
        
        self.btnxoa.clicked.connect(self.Xoa)
        self.btnpheduyet.clicked.connect(self.PheDuyet)
        self.btnluutru.clicked.connect(self.LuuTru)
        self.btnchitiet.clicked.connect(self.ChiTiet)
        self.btnback.clicked.connect(self.QuayLai)
        self.btnLamMoi.clicked.connect(self.load_data)
        self.btnTimKiem.clicked.connect(self.TimKiemCongVan)

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

    def load_data(self):
        if not self.db:
            QMessageBox.critical(self, "Lỗi", "Chưa kết nối database!")
            return

        try:
            query = "SELECT congvandenid, socongvan, ngaynhan, noigui, noidung, trangthai, phongbanphutrach, linkdinhkem, createdat FROM congvanden"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            self.tableCongVan.setRowCount(0)
            for row_number, row_data in enumerate(rows):
                self.tableCongVan.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableCongVan.setItem(row_number, column_number, QTableWidgetItem(str(data) if data else "N/A"))
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tải dữ liệu!\n{e}")

    def Xoa(self):
        selected = self.tableCongVan.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một công văn để xóa!")
            return

        congvandenid = self.tableCongVan.item(selected, 0).text()
        confirm = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa công văn ID {congvandenid}?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                       QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.cursor.execute("DELETE FROM congvanden WHERE congvandenid = %s", (congvandenid,))
                self.db.commit()
                self.tableCongVan.removeRow(selected)
                QMessageBox.information(self, "Thành công", "Đã xóa công văn thành công!")
            except mdb.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa công văn!\n{e}")

    def TimKiemCongVan(self):
        timkiem = self.txtTimKiem.text().strip()
        if not timkiem:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return

        try:
            sql = """
            SELECT congvandenid, socongvan, ngaynhan, noigui, noidung, trangthai, phongbanphutrach, linkdinhkem, createdat 
            FROM congvanden 
            WHERE congvandenid LIKE %s OR socongvan LIKE %s OR noigui LIKE %s OR trangthai LIKE %s
            """
            self.cursor.execute(sql, ('%' + timkiem + '%', '%' + timkiem + '%', '%' + timkiem + '%', '%' + timkiem + '%'))
            rows = self.cursor.fetchall()

            self.tableCongVan.setRowCount(0)
            for row_number, row_data in enumerate(rows):
                self.tableCongVan.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableCongVan.setItem(row_number, column_number, QTableWidgetItem(str(data) if data else "N/A")) 

            if not rows:
                QMessageBox.information(self, "Thông báo", "Không tìm thấy công văn!")
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tìm kiếm công văn!\n{e}")

    def PheDuyet(self):
        selected = self.tableCongVan.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một công văn để phê duyệt!")
            return

        congvandenid = self.tableCongVan.item(selected, 0).text()
        loaicongvan = "Công văn đến"

        current_user = getattr(self.parent, 'current_role', "admin")

        dialog = PheDuyetDialog(self, congvandenid, loaicongvan, current_user)
        dialog.exec()


    def LuuTru(self):
        selected = self.tableCongVan.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một công văn để lưu trữ!")
            return

        congvandenid = self.tableCongVan.item(selected, 0).text()
        socongvan = self.tableCongVan.item(selected, 1).text()
        noidung = self.tableCongVan.item(selected, 4).text()
        linkdinhkem = self.tableCongVan.item(selected, 7).text()
        phongbanphutrach = self.tableCongVan.item(selected, 6).text()

        # Nhập ID lưu trữ thủ công
        luutruid, ok1 = QInputDialog.getText(self, "Nhập ID lưu trữ", "Nhập mã lưu trữ:")
        if not ok1 or not luutruid.strip():
            QMessageBox.warning(self, "Lỗi", "Bạn phải nhập ID lưu trữ!")
            return

        # Nhập tiêu đề thủ công
        tieude, ok2 = QInputDialog.getText(self, "Nhập Tiêu Đề", "Nhập tiêu đề lưu trữ:")
        if not ok2 or not tieude.strip():
            QMessageBox.warning(self, "Lỗi", "Bạn phải nhập tiêu đề!")
            return

        confirm = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn lưu trữ công văn ID {congvandenid}?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Chèn vào bảng luutrucongvan
                insert_query = """
                INSERT INTO luutrucongvan (luutruid, socongvan, tieude, noidung, linkdinhkem, phongbanphutrach, createdat)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """
                self.cursor.execute(insert_query, (luutruid, socongvan, tieude, noidung, linkdinhkem, phongbanphutrach))
                self.db.commit()

                # Xóa công văn khỏi bảng congvanden
                self.cursor.execute("DELETE FROM congvanden WHERE congvandenid = %s", (congvandenid,))
                self.db.commit()

                # Cập nhật lại bảng hiển thị
                self.tableCongVan.removeRow(selected)
                QMessageBox.information(self, "Thành công", "Công văn đã được lưu trữ thành công!")

            except mdb.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu trữ công văn!\n{e}")

    def ChiTiet(self):
        pass

    def QuayLai(self):
        self.close() 
        if self.parent: 
            self.parent.show() 

class PheDuyetDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, id_cv=None, loaicongvan="", current_user=""):
        super(PheDuyetDialog, self).__init__(parent)
        self.setWindowTitle(f"Phê duyệt Công Văn ID {id_cv}")
        self.setGeometry(200, 200, 400, 500)
        self.id_cv = id_cv
        self.parent = parent

        layout = QtWidgets.QVBoxLayout(self)

        # Trường phê duyệt ID
        self.labelPheDuyetID = QtWidgets.QLabel("Phê duyệt ID:", self)
        self.inputPheDuyetID = QtWidgets.QLineEdit(self)

        # Trường công văn ID (chỉ đọc)
        self.labelCongVanID = QtWidgets.QLabel("Công văn ID:", self)
        self.inputCongVanID = QtWidgets.QLineEdit(self)
        self.inputCongVanID.setText(str(id_cv))
        self.inputCongVanID.setReadOnly(True)

        # Trường loại công văn (combobox)
        self.labelLoaiCongVan = QtWidgets.QLabel("Loại công văn:", self)
        self.comboLoaiCongVan = QComboBox(self)
        self.comboLoaiCongVan.addItems(["Công văn đi", "Công văn đến", "Công văn nội bộ"])
        self.comboLoaiCongVan.setCurrentText(loaicongvan)

        # Trường người phê duyệt (hiển thị tài khoản đăng nhập, chỉ đọc)
        self.labelNguoiPheDuyet = QtWidgets.QLabel("Người phê duyệt:", self)
        self.inputNguoiPheDuyet = QtWidgets.QLineEdit(self)
        self.inputNguoiPheDuyet.setText(current_user)
        self.inputNguoiPheDuyet.setReadOnly(True)

        # Trường trạng thái (combobox)
        self.labelTrangThai = QtWidgets.QLabel("Trạng thái:", self)
        self.comboTrangThai = QComboBox(self)
        self.comboTrangThai.addItems(["Đã duyệt", "Yêu cầu chỉnh sửa", "Từ chối"])
        self.comboTrangThai.setCurrentText("Đã phê duyệt")

        # Trường ghi chú
        self.labelGhiChu = QtWidgets.QLabel("Ghi chú:", self)
        self.textEditGhiChu = QtWidgets.QTextEdit(self)

        # Trường ngày phê duyệt (approvedat)
        self.labelApprovedAt = QtWidgets.QLabel("Ngày phê duyệt:", self)
        self.dateEditApprovedAt = QtWidgets.QDateEdit(self)
        self.dateEditApprovedAt.setCalendarPopup(True)
        self.dateEditApprovedAt.setDate(QDate.currentDate())

        # Nút lưu và hủy
        self.saveButton = QtWidgets.QPushButton("Lưu", self)
        self.saveButton.clicked.connect(self.save_changes)

        self.cancelButton = QtWidgets.QPushButton("Hủy", self)
        self.cancelButton.clicked.connect(self.close)

        # Thêm widget vào layout
        layout.addWidget(self.labelPheDuyetID)
        layout.addWidget(self.inputPheDuyetID)
        layout.addWidget(self.labelCongVanID)
        layout.addWidget(self.inputCongVanID)
        layout.addWidget(self.labelLoaiCongVan)
        layout.addWidget(self.comboLoaiCongVan)
        layout.addWidget(self.labelNguoiPheDuyet)
        layout.addWidget(self.inputNguoiPheDuyet)
        layout.addWidget(self.labelTrangThai)
        layout.addWidget(self.comboTrangThai)
        layout.addWidget(self.labelGhiChu)
        layout.addWidget(self.textEditGhiChu)
        layout.addWidget(self.labelApprovedAt)
        layout.addWidget(self.dateEditApprovedAt)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.cancelButton)

    def save_changes(self):
        pheduyet_id = self.inputPheDuyetID.text().strip()
        loaicongvan = self.comboLoaiCongVan.currentText()
        nguoipheduyet = self.inputNguoiPheDuyet.text()
        trangthai = self.comboTrangThai.currentText()
        ghichu = self.textEditGhiChu.toPlainText()
        approvedat = self.dateEditApprovedAt.date().toString("yyyy-MM-dd")

        if not pheduyet_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Phê duyệt ID!")
            return

        try:
            # Chèn bản ghi mới vào bảng pheduyetcongvan
            insert_query = """
            INSERT INTO pheduyetcongvan (pheduyetid, congvanid, loaicongvan, nguoipheduyet, trangthai, ghichu, approvedat)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.parent.cursor.execute(insert_query, (pheduyet_id, self.id_cv, loaicongvan, nguoipheduyet, trangthai, ghichu, approvedat))
            self.parent.db.commit()
            QMessageBox.information(self, "Thành công", "Phê duyệt công văn thành công!")
            self.parent.load_data()  # Cập nhật lại bảng congvanden
            self.close()
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi phê duyệt công văn!\n{e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DanhSachCVDen()
    sys.exit(app.exec())