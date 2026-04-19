from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import json
import sys

import os
import PyQt5

# Находим папку с плагинами Qt внутри установленного PyQt5
pyqt_path = os.path.dirname(PyQt5.__file__)
candidates = [
    os.path.join(pyqt_path, "Qt5", "plugins"),
    os.path.join(pyqt_path, "Qt", "plugins"),
]
for plugins_dir in candidates:
    if os.path.exists(os.path.join(plugins_dir, "platforms")):
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugins_dir
        print(f"[OK] Плагины Qt найдены: {plugins_dir}")
        break
else:
    print("[ERROR] Папка 'platforms' не найдена. Переустановите PyQt5.")

app = QApplication([])
main_win = QWidget()
main_win.show()
main_win.setWindowTitle('Вход')
main_win.resize(300, 100)

with open('base.json', 'r', encoding="utf-8") as file:
    Base = json.load(file)

login = QLabel('Логин')
passw = QLabel('Пароль')
writeline_login = QLineEdit()
writeline_passw = QLineEdit()
PB_enter = QPushButton('Войти')
PB_regist = QPushButton('Зарегестрироваться')
PB_asGuest = QPushButton('Войти как Гость')

lV = QVBoxLayout()
regist_guest = QHBoxLayout()

main_win.setLayout(lV)

regist_guest.addWidget(PB_regist)
regist_guest.addWidget(PB_asGuest)

lV.addWidget(login)
lV.addWidget(writeline_login)
lV.addWidget(passw)
lV.addWidget(writeline_passw)
lV.addWidget(PB_enter)
lV.addLayout(regist_guest)


def regist():
    lgn, result = QInputDialog.getText(
        main_win, 'Логин', 'Придумайте Логин:'
    )
    password, result = QInputDialog.getText(
        main_win, "Пароль", 'Придумайте пароль:'
    )
    if result and lgn != "":
        if result and password != "":
            Base[lgn] = password

    with open('base.json', 'w', encoding="utf-8") as file:
        json.dump(Base, file, ensure_ascii = False)


def ent():
    login_text = writeline_login.text()
    password_text = writeline_passw.text()

    if login_text in Base:
        if password_text == Base[login_text]:
            sys.exit(app.exec())   # успешный вход
        else:
            QMessageBox.warning(main_win, "Ошибка", "Неверный пароль.")
    else:
        QMessageBox.warning(main_win, "Ошибка", "Пользователь с таким логином не найден.")


def ent_asGuest():
    sys.exit(app.exec())

PB_regist.clicked.connect(regist)
PB_enter.clicked.connect(ent)
PB_asGuest.clicked.connect(ent_asGuest)


app.exec()