import sys
import MySQLdb as mdb
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem


class DanhSachPhongBan(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(DanhSachPhongBan, self).__init__()
        uic.loadUi('ui/dsphongban.ui', self)
        self.parent = parent
        self.show()

        # Kết nối database
        self.db = None
        self.cursor = None
        self.connect_db()
        self.load_data()

        self.btnthem.clicked.connect(self.themphongban)
        self.btnxoa.clicked.connect(self.xoaphongban)
        self.btnquaylai.clicked.connect(self.quaylai)

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
        try:
            # Load danh sách phòng ban bên ngoài
            self.cursor.execute("SELECT id, tenphongban FROM phongbanngoai")
            rows = self.cursor.fetchall()
            self.tablebenngoai.setRowCount(len(rows))
            for row_idx, (id_, tenphongban) in enumerate(rows):
                self.tablebenngoai.setItem(row_idx, 0, QTableWidgetItem(str(id_)))
                self.tablebenngoai.setItem(row_idx, 1, QTableWidgetItem(tenphongban))
            
            # Load danh sách phòng ban nội bộ
            self.cursor.execute("SELECT id, tenphongban FROM phongbannoi")
            rows = self.cursor.fetchall() 
            self.tablenoibo.setRowCount(len(rows)) 
            for row_idx, (id_, tenphongban) in enumerate(rows): 
                self.tablenoibo.setItem(row_idx, 0, QTableWidgetItem(str(id_))) 
                self.tablenoibo.setItem(row_idx, 1, QTableWidgetItem(tenphongban)) 
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu!\n{e}")

    def themphongban(self):
        dialog = ThemPhongBanDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            id_phongban, ten_phongban, loai_phongban = dialog.get_data()

            if not ten_phongban:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập tên phòng ban!")
                return

            try:
                if loai_phongban == "Phòng ban bên ngoài":
                    self.cursor.execute("INSERT INTO phongbanngoai (id, tenphongban) VALUES (%s, %s)", (id_phongban, ten_phongban))
                else:
                    self.cursor.execute("INSERT INTO phongbannoi (id, tenphongban) VALUES (%s, %s)", (id_phongban, ten_phongban))

                self.db.commit()
                QMessageBox.information(self, "Thành công", "Phòng ban đã được thêm!")
                self.load_data()  # Cập nhật lại danh sách phòng ban
            except mdb.Error as e:
                self.db.rollback()
                QMessageBox.critical(self, "Lỗi", f"Không thể thêm phòng ban!\n{e}")


    def xoaphongban(self):
        selected_items_benngoai = self.tablebenngoai.selectedItems()
        selected_items_noibo = self.tablenoibo.selectedItems()
        
        # Nếu không có dòng nào được chọn
        if not selected_items_benngoai and not selected_items_noibo:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn phòng ban cần xóa!")
            return
        
        # Hỏi xác nhận trước khi xóa
        confirm = QMessageBox.question(self, "Xác nhận", 
                                    "Bạn có chắc chắn muốn xóa phòng ban này không?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Xóa phòng ban bên ngoài nếu được chọn
                if selected_items_benngoai:
                    selected_row = self.tablebenngoai.currentRow()
                    id_to_delete = self.tablebenngoai.item(selected_row, 0).text()
                    
                    # Thực hiện câu lệnh xóa
                    self.cursor.execute("DELETE FROM phongbanngoai WHERE id = %s", (id_to_delete,))
                    self.db.commit()
                    
                    self.tablebenngoai.removeRow(selected_row)
                    QMessageBox.information(self, "Thông báo", "Đã xóa phòng ban bên ngoài thành công!")
                
                if selected_items_noibo:
                    selected_row = self.tablenoibo.currentRow()
                    id_to_delete = self.tablenoibo.item(selected_row, 0).text()
                    
                    self.cursor.execute("DELETE FROM phongbannoi WHERE id = %s", (id_to_delete,))
                    self.db.commit()
                    
                    self.tablenoibo.removeRow(selected_row)
                    QMessageBox.information(self, "Thông báo", "Đã xóa phòng ban nội bộ thành công!")
                
            except mdb.Error as e:
                self.db.rollback()
                QMessageBox.critical(self, "Lỗi", f"Không thể xóa phòng ban!\n{e}")
                
            # Tải lại dữ liệu sau khi xóa
            self.load_data()

    def quaylai(self):
        self.close() 
        if self.parent: 
            self.parent.show() 

class ThemPhongBanDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ThemPhongBanDialog, self).__init__(parent)
        self.setWindowTitle("Thêm Phòng Ban")
        self.setFixedSize(300, 200)

        layout = QtWidgets.QVBoxLayout()

        # Nhập ID phòng ban
        self.txtIDPhongBan = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Nhập ID phòng ban:"))
        layout.addWidget(self.txtIDPhongBan)

        # Nhập tên phòng ban
        self.txtTenPhongBan = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Nhập tên phòng ban:"))
        layout.addWidget(self.txtTenPhongBan)

        # Chọn loại phòng ban
        self.cmbLoaiPhongBan = QtWidgets.QComboBox()
        self.cmbLoaiPhongBan.addItems(["Phòng ban bên ngoài", "Phòng ban nội bộ"])
        layout.addWidget(QtWidgets.QLabel("Chọn loại phòng ban:"))
        layout.addWidget(self.cmbLoaiPhongBan)

        # Nút Thêm và Hủy
        button_layout = QtWidgets.QHBoxLayout()
        self.btnThem = QtWidgets.QPushButton("Thêm")
        self.btnHuy = QtWidgets.QPushButton("Hủy")
        button_layout.addWidget(self.btnThem)
        button_layout.addWidget(self.btnHuy)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Kết nối sự kiện
        self.btnThem.clicked.connect(self.accept)
        self.btnHuy.clicked.connect(self.reject)

    def get_data(self):
        return (self.txtIDPhongBan.text().strip(), 
                self.txtTenPhongBan.text().strip(), 
                self.cmbLoaiPhongBan.currentText())



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DanhSachPhongBan()
    sys.exit(app.exec())