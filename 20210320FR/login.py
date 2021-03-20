# -*- coding: utf-8 -*-
import sys
import MySQLdb
import face_recognize
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QWidget
from faces_input_frame import Ui_Dialog


# 建立和MySQL数据库的连接
dbconn = MySQLdb.connect(
    host="127.0.0.1",      # 待填写
    port=3306,    # 待填写
    user="root",      # 待填写
    password="123456",  # 待填写
    db="FR",
)

# 获取数据库游标cursor
db_cursor = dbconn.cursor()


class Ui_Form(QWidget):  # 将object改为QWidget，才能弹出消息对话框
    def __init__(self):
        super(Ui_Form, self).__init__()  # 用户添加代码

    def setupUi(self, Form):
        self.form = Form  # 用户添加代码
        Form.setObjectName("Form")
        Form.setMinimumSize(QtCore.QSize(329, 230))
        Form.setMaximumSize(QtCore.QSize(400, 230))
        Form.setStyleSheet("")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_face_pass = QtWidgets.QPushButton(Form)
        self.pushButton_face_pass.setGeometry(QtCore.QRect(100, 100, 150, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_face_pass.setFont(font)
        self.pushButton_face_pass.setObjectName("pushButton_face_pass")
        self.pushButton_face_input = QtWidgets.QPushButton(Form)
        self.pushButton_face_input.setGeometry(QtCore.QRect(100, 31, 150, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_face_input.setFont(font)
        self.pushButton_face_input.setObjectName("pushButton_face_input")

        self.retranslateUi(Form)
        self.pushButton_face_input.clicked.connect(self.faceinput)
        self.pushButton_face_pass.clicked.connect(self.facepass)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "人脸采集识别系统"))
        self.pushButton_face_pass.setText(_translate("Form", "人脸识别登录"))
        self.pushButton_face_input.setText(_translate("Form", "人脸信息录入"))

    def close(self, event):
        self.close()

    def faceinput(self, event):
        self.form.hide()
        Form1 = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Form1, db_cursor)
        Form1.show()
        Form1.exec_()
        self.form.show()  # 子窗口关闭后，主窗口显示
        dbconn.commit()

    def facepass(self, event):
        get_name = face_recognize.recognize_face(db_cursor)  # 返回识别的人名
        if get_name == "unknown":
            reply = QMessageBox.information(self, '提示', '人脸识别失败', QMessageBox.Close)
        else:
            reply = QMessageBox.information(self, '提示', "欢迎您：" + get_name, QMessageBox.Ok)
            print("编写其他程序")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    app.exec_()
    db_cursor.close()
    dbconn.close()
