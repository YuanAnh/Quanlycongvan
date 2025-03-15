import sys
import MySQLdb as mdb
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt

class ThongKe(QWidget):
    def __init__(self, parent=None):
        super(ThongKe, self).__init__()
        uic.loadUi('ui/tk.ui', self)
        self.parent = parent
        self.show()
        self.btnback.clicked.connect(self.go_back)
        self.load_data()

    def connect_db(self):
        try:
            conn = mdb.connect(
                host="localhost",
                user="root",
                passwd="",
                db="qlcv2",
                charset="utf8"
            )
            return conn
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể kết nối DB!\n{e}")
            return None

    def load_data(self):
        conn = self.connect_db()
        if conn is None:
            return
        try:
            cursor = conn.cursor()

            query_congvandi = """
                SELECT trangthai, COUNT(*) AS SoLuong
                FROM congvandi
                WHERE trangthai IN ('Đã gửi', 'Chưa gửi', 'Đang chờ duyệt')
                GROUP BY trangthai
            """
            cursor.execute(query_congvandi)
            data_congvandi = cursor.fetchall()
            self.fill_tabletk(data_congvandi)
            
            query_congvanden = """
                SELECT trangthai, COUNT(*) AS SoLuong
                FROM congvanden
                WHERE trangthai IN ('Đã xử lý', 'Đang xử lý', 'Chưa xử lý')
                GROUP BY trangthai
            """
            cursor.execute(query_congvanden)
            data_congvanden = cursor.fetchall()
            self.fill_tabletk1(data_congvanden)

            query_tong = """
                SELECT 
                    (SELECT COUNT(*) FROM congvandi) + (SELECT COUNT(*) FROM congvanden) AS TongSoLuong
            """
            cursor.execute(query_tong)
            data_lichsu = cursor.fetchall()
            self.fill_tabletk2(data_lichsu)

        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu!\n{e}")
        finally:
            cursor.close()
            conn.close()

    def fill_tabletk(self, data):
        self.tabletk.setRowCount(len(data))
        self.tabletk.setColumnCount(2)
        self.tabletk.setHorizontalHeaderLabels(["Trạng thái", "Số lượng"])
        for row_idx, (trangthai, soluong) in enumerate(data):
            self.tabletk.setItem(row_idx, 0, QTableWidgetItem(trangthai))
            self.tabletk.setItem(row_idx, 1, QTableWidgetItem(str(soluong)))
        self.tabletk.resizeColumnsToContents()

    def fill_tabletk1(self, data):
        self.tabletk1.setRowCount(len(data))
        self.tabletk1.setColumnCount(2)
        self.tabletk1.setHorizontalHeaderLabels(["Trạng thái", "Số lượng"])
        for row_idx, (trangthai, soluong) in enumerate(data):
            self.tabletk1.setItem(row_idx, 0, QTableWidgetItem(trangthai))
            self.tabletk1.setItem(row_idx, 1, QTableWidgetItem(str(soluong)))
        self.tabletk1.resizeColumnsToContents()

    def fill_tabletk2(self, data):
        self.tabletk2.setRowCount(len(data))
        self.tabletk2.setColumnCount(1)
        self.tabletk2.setHorizontalHeaderLabels(["Tổng số lượng công văn"])
        for row_idx, (tongsoluong,) in enumerate(data):
            self.tabletk2.setItem(row_idx, 0, QTableWidgetItem(str(tongsoluong)))

        self.tabletk2.resizeColumnsToContents()

    def go_back(self):
        self.close()
        if self.parent:
            self.parent.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThongKe()
    window.show()
    sys.exit(app.exec())
