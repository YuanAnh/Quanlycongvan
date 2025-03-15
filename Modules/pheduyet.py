import sys
import MySQLdb as mdb
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

class PheDuyetCongVan(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(PheDuyetCongVan, self).__init__()
        uic.loadUi('ui/pheduyet.ui', self)
        self.parent = parent
        self.show()

        self.db = None
        self.cursor = None
        self.connect_db()
        self.load_data()

        # Kết nối các nút bấm với hàm tương ứng
        self.btnQuayLai.clicked.connect(self.QuayLai)
        self.btnLamMoi.clicked.connect(self.load_data)
        self.btnxoa.clicked.connect(self.XoaCongVan)
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
            query = """
            SELECT pheduyetid, congvanid, loaicongvan, nguoipheduyet, trangthai, ghichu, approvedat 
            FROM pheduyetcongvan
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            self.tableCongVanPheDuyet.setRowCount(0)
            for row_number, row_data in enumerate(rows):
                self.tableCongVanPheDuyet.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableCongVanPheDuyet.setItem(row_number, column_number, QTableWidgetItem(str(data) if data else "N/A"))
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tải dữ liệu!\n{e}")

    def TimKiemCongVan(self):
        timkiem = self.txtTimKiem.text().strip()
        if not timkiem:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return

        try:
            sql = """
            SELECT pheduyetid, congvanid, loaicongvan, nguoipheduyet, trangthai, ghichu, approvedat
            FROM pheduyetcongvan
            WHERE pheduyetid LIKE %s OR congvanid LIKE %s OR loaicongvan LIKE %s OR nguoipheduyet LIKE %s OR ghichu LIKE %s
            """
            self.cursor.execute(sql, ('%' + timkiem + '%', '%' + timkiem + '%', '%' + timkiem + '%', '%' + timkiem + '%', '%' + timkiem + '%'))
            rows = self.cursor.fetchall()

            self.tableCongVanPheDuyet.setRowCount(0)
            for row_number, row_data in enumerate(rows):
                self.tableCongVanPheDuyet.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableCongVanPheDuyet.setItem(row_number, column_number, QTableWidgetItem(str(data) if data else "N/A"))

            if not rows:
                QMessageBox.information(self, "Thông báo", "Không tìm thấy công văn!")
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tìm kiếm công văn!\n{e}")

    def XoaCongVan(self):
        selected_row = self.tableCongVanPheDuyet.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một hàng để xóa!")
            return

        pheduyetid = self.tableCongVanPheDuyet.item(selected_row, 0).text()

        confirm = QMessageBox.question(
            self, "Xác nhận", f"Bạn có chắc muốn xóa công văn ID {pheduyetid}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.cursor.execute("DELETE FROM pheduyetcongvan WHERE pheduyetid = %s", (pheduyetid,))
                self.db.commit()
                self.tableCongVanPheDuyet.removeRow(selected_row)
                QMessageBox.information(self, "Thành công", "Đã xóa công văn thành công!")
            except mdb.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa công văn!\n{e}")

    def QuayLai(self):
        self.close() 
        if self.parent: 
            self.parent.show() 

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PheDuyetCongVan()
    sys.exit(app.exec())