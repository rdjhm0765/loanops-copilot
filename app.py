import sys
from PyQt5.QtWidgets import QApplication
from modules.dashboard import Dashboard

def main():
    app = QApplication(sys.argv)

    # 🔥 LOAD QSS HERE
    with open("ui/styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = Dashboard()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
