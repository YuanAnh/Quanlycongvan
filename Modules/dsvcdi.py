
import sys
import MySQLdb as mdb
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QComboBox, QInputDialog
from PyQt6.QtCore import QDate

class SuaNoiDungDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, id_cv=None, noi_dung="", so_vb="", noi_nhan="", phong_ban= "", trang_thai=""):
        super(SuaNoiDungDialog, self).__init__(parent)
        self.setWindowTitle(f"Sửa Công Văn ID {id_cv}")
        self.setGeometry(200, 200, 600, 400)
        self.id_cv = id_cv
        self.parent = parent
        layout = QtWidgets.QVBoxLayout(self)
        self.labelSoVB = QtWidgets.QLabel("Số công văn:", self)
        self.inputSoVB = QtWidgets.QLineEdit(self)
        self.inputSoVB.setText(so_vb)
        self.labelNoiDung = QtWidgets.QLabel("Nội dung:", self)
        self.textEditNoiDung = QtWidgets.QTextEdit(self)
        self.textEditNoiDung.setText(noi_dung)
        self.labelNoiNhan = QtWidgets.QLabel("Nơi nhận:", self)
        self.textEditNoiNhan = QtWidgets.QTextEdit(self)
        self.textEditNoiNhan.setText(noi_nhan)
        self.labelPhongBan = QtWidgets.QLabel("Phòng ban phụ trách:", self)
        self.textEditPhongBan = QtWidgets.QTextEdit(self)
        self.textEditPhongBan.setText(phong_ban)
        self.labelTrangThai = QtWidgets.QLabel("Trạng thái:", self)
        self.comboTrangThai = QComboBox(self)
        self.comboTrangThai.addItems(["Chưa gửi", "Đã gửi", "Đang chờ duyệt"])
        self.comboTrangThai.setCurrentText(trang_thai)
        self.saveButton = QtWidgets.QPushButton("Lưu", self)
        self.saveButton.clicked.connect(self.save_changes)
        self.cancelButton = QtWidgets.QPushButton("Hủy", self)
        self.cancelButton.clicked.connect(self.close)

        layout.addWidget(self.labelSoVB)
        layout.addWidget(self.inputSoVB)
        layout.addWidget(self.labelNoiDung)
        layout.addWidget(self.textEditNoiDung)
        layout.addWidget(self.labelNoiNhan)
        layout.addWidget(self.textEditNoiNhan)
        layout.addWidget(self.labelPhongBan)
        layout.addWidget(self.textEditPhongBan)
        layout.addWidget(self.labelTrangThai)
        layout.addWidget(self.comboTrangThai)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.cancelButton)

    def save_changes(self):
        new_so_vb = self.inputSoVB.text()
        new_noi_dung = self.textEditNoiDung.toPlainText()
        new_noi_nhan = self.textEditNoiNhan.toPlainText()
        new_phong_ban = self.textEditPhongBan.toPlainText()
        new_trang_thai = self.comboTrangThai.currentText()
        try:
            self.parent.cursor.execute(
                """
                UPDATE congvandi 
                SET socongvan = %s, noidung = %s, noinhan = %s, phongbanphutrach= %s, trangthai = %s 
                WHERE congvandiid = %s
                """, (new_so_vb, new_noi_dung, new_noi_nhan, new_phong_ban, new_trang_thai, self.id_cv))
            self.parent.db.commit()
            QMessageBox.information(self, "Thành công", "Cập nhật văn bản thành công!")
            self.parent.load_data()
            self.close()
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi cập nhật văn bản!\n{e}")

class XemNoiDungDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, id_cv=None, noi_dung=""):
        super(XemNoiDungDialog, self).__init__(parent)
        self.setWindowTitle(f"Nội dung công văn ID {id_cv}")
        self.setGeometry(200, 200, 600, 400)
        layout = QtWidgets.QVBoxLayout(self)
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setText(noi_dung)
        self.textEdit.setReadOnly(True)
        closeButton = QtWidgets.QPushButton("Đóng", self)
        closeButton.clicked.connect(self.close)
        layout.addWidget(self.textEdit)
        layout.addWidget(closeButton)

class DanhSachCVDi(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(DanhSachCVDi, self).__init__()
        uic.loadUi('ui/danhsachcvdi.ui', self)
        self.parent = parent
        self.show()
        self.db = None
        self.cursor = None
        self.connect_db()
        self.load_data()

        self.btnlammoi.clicked.connect(self.load_data)
        self.btntimkiem.clicked.connect(self.TimKiem)
        self.btnluutru.clicked.connect(self.LuuTru)
        self.btnpheduyet.clicked.connect(self.PheDuyet)
        self.btnsua.clicked.connect(self.Sua)
        self.btnxoa.clicked.connect(self.Xoa)
        self.btnxem.clicked.connect(self.Xemnoidung)
        self.btnQuaylai.clicked.connect(self.QuayLai)

        self.show()

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
            query = "SELECT congvandiid, socongvan, noidung, nguoiky, ngayphathanh, noinhan, phongbanphutrach, loaicongvan, trangthai, linkdinhkem, createdby, createdat FROM congvandi"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            self.tableCongVanDi.setRowCount(0)
            for row_number, row_data in enumerate(rows):
                self.tableCongVanDi.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableCongVanDi.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tải dữ liệu!\n{e}")

    def TimKiem(self):
        timkiem = self.txttimkiem.text().strip()
        if not timkiem:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return
        try:
            sql = """
            SELECT congvandiid, socongvan, noidung, nguoiky, ngayphathanh, noinhan, phongbanphutrach, loaicongvan, trangthai, linkdinhkem, createdby, createdat 
            FROM congvandi
            WHERE congvandiid LIKE %s OR socongvan LIKE %s OR noinhan LIKE %s OR trangthai LIKE %s OR loaicongvan LIKE %s OR phongbanphutrach LIKE %s
            """
            self.cursor.execute(sql, ('%' + timkiem + '%', '%' + timkiem + '%', '%' + timkiem + '%', '%' + timkiem + '%', '%' + timkiem + '%' , '%' + timkiem + '%'))
            rows = self.cursor.fetchall()
            self.tableCongVanDi.setRowCount(0)
            for row_number, row_data in enumerate(rows): 
                self.tableCongVanDi.insertRow(row_number) 
                for column_number, data in enumerate(row_data): 
                    self.tableCongVanDi.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            if not rows:
                QMessageBox.information(self, "Thông báo", "Không tìm thấy công văn!")
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tìm kiếm công văn!\n{e}")

    def Sua(self):
        selected = self.tableCongVanDi.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một công văn để sửa!")
            return
        
        congvandiid = self.tableCongVanDi.item(selected, 0).text()
        so_vb = self.tableCongVanDi.item(selected, 1).text()
        noi_dung = self.tableCongVanDi.item(selected, 2).text()
        noinhan = self.tableCongVanDi.item(selected, 5).text()
        phongbanphutrach = self.tableCongVanDi.item(selected, 6).text()
        trang_thai = self.tableCongVanDi.item(selected, 7).text()
        
        dialog = SuaNoiDungDialog(self, congvandiid, noi_dung, so_vb, noinhan, phongbanphutrach, trang_thai) 
        dialog.exec()


    def Xoa(self):
        """Xóa văn bản được chọn"""
        selected = self.tableCongVanDi.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một công văn để xóa!")
            return

        congvandiid = self.tableCongVanDi.item(selected, 0).text()
        confirm = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa công văn ID {congvandiid}?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                       QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                query = "DELETE FROM congvandi WHERE congvandiid = %s"
                self.cursor.execute(query, (congvandiid,))
                self.db.commit()
                self.tableCongVanDi.removeRow(selected)
                QMessageBox.information(self, "Thành công", "Đã xóa công văn thành công!")
            except mdb.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa công văn!\n{e}")

    def Xemnoidung(self):
        selected = self.tableCongVanDi.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một công văn để xem!")
            return

        congvandiid = self.tableCongVanDi.item(selected, 0).text()

        try:
            query = "SELECT noidung FROM congvandi WHERE congvandiid = %s"
            self.cursor.execute(query, (congvandiid,))
            result = self.cursor.fetchone()
            
            if result:
                noidung = result[0] 
                dialog = XemNoiDungDialog(self, congvandiid, noidung)
                dialog.exec()
            else:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy nội dung văn bản!")
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải nội dung!\n{e}")

    def LuuTru(self):
        selected = self.tableCongVanDi.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một công văn để lưu trữ!")
            return

        congvandenid = self.tableCongVanDi.item(selected, 0).text()
        socongvan = self.tableCongVanDi.item(selected, 1).text()
        noidung = self.tableCongVanDi.item(selected, 2).text()
        linkdinhkem = self.tableCongVanDi.item(selected, 9).text()
        phongbanphutrach = self.tableCongVanDi.item(selected, 6).text()

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
                self.cursor.execute("DELETE FROM congvandi WHERE congvandiid = %s", (congvandenid,))
                self.db.commit()

                # Cập nhật lại bảng hiển thị
                self.tableCongVanDi.removeRow(selected)
                QMessageBox.information(self, "Thành công", "Công văn đã được lưu trữ thành công!")

            except mdb.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu trữ công văn!\n{e}")

    def PheDuyet(self):
        selected = self.tableCongVanDi.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một công văn để phê duyệt!")
            return

        congvandenid = self.tableCongVanDi.item(selected, 0).text()
        loaicongvan = "Công văn đi"

        current_user = getattr(self.parent, 'current_role', "admin")

        dialog = PheDuyetDialog(self, congvandenid, loaicongvan, current_user)
        dialog.exec()

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
    window = DanhSachCVDi()
    sys.exit(app.exec())
