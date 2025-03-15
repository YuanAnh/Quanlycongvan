from PyQt6 import QtWidgets, uic
import MySQLdb as mdb
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

class LuuTruCongVan(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(LuuTruCongVan, self).__init__()
        uic.loadUi('ui/luutru.ui', self)
        self.parent = parent
        self.show()

        # Kết nối database
        self.db = None
        self.cursor = None
        self.connect_db()
        self.load_data()
        
        self.btntailai.clicked.connect(self.load_data)
        self.btntimkiem.clicked.connect(self.search_data)
        self.btnxoa.clicked.connect(self.delete_selected_row)
        self.btnquaylai.clicked.connect(self.QuayLai)

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
            self.cursor.execute("SELECT luutruid, socongvan, tieude, noidung, linkdinhkem, phongbanphutrach, createdat FROM luutrucongvan")
            records = self.cursor.fetchall()

            self.tableLuuTru.setRowCount(len(records))
            for row_idx, row_data in enumerate(records):
                for col_idx, col_data in enumerate(row_data):
                    self.tableLuuTru.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tải dữ liệu!\n{e}")

    def search_data(self):
        keyword = self.txttimkiem.text().strip()
        if not keyword:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return

        try:
            query = """
                SELECT luutruid, socongvan, tieude, noidung, linkdinhkem, phongbanphutrach, createdat 
                FROM luutrucongvan 
                WHERE socongvan LIKE %s OR tieude LIKE %s OR luutruid LIKE %s OR phongbanphutrach LIKE %s
            """
            self.cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%" , f"%{keyword}%"))
            records = self.cursor.fetchall()

            self.tableLuuTru.setRowCount(len(records))
            for row_idx, row_data in enumerate(records):
                for col_idx, col_data in enumerate(row_data):
                    self.tableLuuTru.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            if not records:
                QMessageBox.information(self, "Thông báo", "Không tìm thấy công văn!")
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tìm kiếm!\n{e}")

    def delete_selected_row(self):
        selected_row = self.tableLuuTru.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một hàng để xóa!")
            return

        luutruid = self.tableLuuTru.item(selected_row, 0).text()

        confirm = QMessageBox.question(
            self, "Xác nhận", f"Bạn có chắc muốn xóa công văn ID {luutruid}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.cursor.execute("DELETE FROM luutrucongvan WHERE luutruid = %s", (luutruid,))
                self.db.commit()
                self.tableLuuTru.removeRow(selected_row)
                QMessageBox.information(self, "Thành công", "Đã xóa công văn thành công!")
            except mdb.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa công văn!\n{e}")

    def QuayLai(self):
        self.close() 
        if self.parent: 
            self.parent.show() 

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LuuTruCongVan()
    window.show()
    sys.exit(app.exec())
