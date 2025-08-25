from PyQt6.QtWidgets import (QApplication, QWidget, QGroupBox, QTextEdit, QComboBox, QLabel,
                             QSpinBox, QLineEdit, QPushButton, QVBoxLayout, QGridLayout)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt
from sys import argv, exit
from m import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Визуализация интегральных уравнений второго рода')

        layout = QVBoxLayout(self)

        canvas_box = QGroupBox('Визуализация')
        canvas_box.setContentsMargins(0, 5, 0, 0)
        canvas_layout = QVBoxLayout()

        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)

        self.ax.set_title(' ')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.figure.tight_layout()

        self.canvas = FigureCanvasQTAgg(self.figure)

        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        canvas_layout.addWidget(self.toolbar)
        canvas_layout.addWidget(self.canvas)
        canvas_box.setLayout(canvas_layout)

        layout.addWidget(canvas_box)

        out_box = QGroupBox('Вывод')
        out_layout = QVBoxLayout()

        self.out_edit = QTextEdit()
        self.out_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.out_edit.setStyleSheet('QTextEdit {background-color: white;}')

        out_layout.addWidget(self.out_edit)
        out_box.setLayout(out_layout)
        out_box.setContentsMargins(0, 10, 0, 0)

        layout.addWidget(out_box)

        intake_box = QGroupBox('Вводные')
        intake_layout = QGridLayout()

        self.combo_box = QComboBox()
        self.combo_box.addItem('Уравнение Фредгольма второго рода')
        self.combo_box.addItem('Уравнение Вольтерра второго рода')
        self.combo_box.currentTextChanged.connect(self.box_change)
        intake_layout.addWidget(self.combo_box, 0, 0, 1, 4)

        a_l = QLabel('a :')
        intake_layout.addWidget(a_l, 0, 5)

        self.spin_a = QSpinBox()
        self.spin_a.setMinimum(-100)
        self.spin_a.setMaximum(100)
        self.spin_a.textChanged.connect(self.check_input_fields)
        intake_layout.addWidget(self.spin_a, 0, 6)
        intake_layout.setColumnStretch(6, 1)

        b_l = QLabel('b :')
        intake_layout.addWidget(b_l, 0, 7)

        self.spin_b = QSpinBox()
        self.spin_b.setMinimum(-100)
        self.spin_b.setMaximum(100)
        self.spin_b.textChanged.connect(self.check_input_fields)
        intake_layout.addWidget(self.spin_b, 0, 8)
        intake_layout.setColumnStretch(8, 1)

        n_l = QLabel('n :')
        intake_layout.addWidget(n_l, 0, 9)

        self.spin_n = QSpinBox()
        self.spin_n.setMinimum(2)
        self.spin_n.setMaximum(20)
        self.spin_n.setSingleStep(2)
        self.spin_n.textChanged.connect(self.check_input_fields)
        intake_layout.addWidget(self.spin_n, 0, 10)
        intake_layout.setColumnStretch(10, 1)

        l_l = QLabel('l :')
        intake_layout.addWidget(l_l, 0, 11)

        self.spin_l = QSpinBox()
        self.spin_l.setMinimum(-100)
        self.spin_l.setMaximum(100)
        self.spin_l.textChanged.connect(self.check_input_fields)
        intake_layout.addWidget(self.spin_l, 0, 12)
        intake_layout.setColumnStretch(12, 1)

        self.k_l = QLabel('K(x,s) :')
        intake_layout.addWidget(self.k_l, 1, 0)

        self.k_edit = QLineEdit()
        self.k_edit.textChanged.connect(self.check_input_fields)
        intake_layout.addWidget(self.k_edit, 1, 1)

        self.f_l = QLabel('f(x) :')
        intake_layout.addWidget(self.f_l, 1, 2)

        self.f_edit = QLineEdit()
        self.f_edit.textChanged.connect(self.check_input_fields)
        intake_layout.addWidget(self.f_edit, 1, 3)

        self.button = QPushButton('Применить')
        self.button.clicked.connect(self.plot_graph)
        self.button.setEnabled(False)
        intake_layout.addWidget(self.button, 1, 4, 1, 9)

        intake_box.setLayout(intake_layout)
        intake_box.setContentsMargins(0, 10, 0, 0)

        layout.addWidget(intake_box)

    def check_input_fields(self):
        if (self.spin_a.text() and self.spin_b.text() and self.spin_n.text() and self.spin_l.text() and
                self.k_edit.text() and self.f_edit.text()):
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

    def box_change(self):
        if self.combo_box.currentText() == 'Уравнение Фредгольма второго рода':
            self.spin_n.setMaximum(8)
        elif self.combo_box.currentText() == 'Уравнение Вольтерра второго рода':
            self.spin_n.setMaximum(14)

    def plot_graph(self):
        try:
            f, y, o = 0, 0, 0
            self.ax.clear()
            if self.combo_box.currentText() == 'Уравнение Фредгольма второго рода':
                self.ax.set_title('Уравнение Фредгольма второго рода')
                s1, s2, p1, p2, f, y, o = fredholm_f(int(self.spin_a.text()), int(self.spin_b.text()),
                                                     int(self.spin_n.text()), int(self.spin_l.text()),
                                                     self.k_edit.text(), self.f_edit.text())
                self.ax.scatter(s1, s2)
                self.ax.plot(p1, p2)
            elif self.combo_box.currentText() == 'Уравнение Вольтерра второго рода':
                self.ax.set_title('Уравнение Вольтерра второго рода')
                s1, s2, p1, p2, f, y, o = volterre_f(int(self.spin_a.text()), int(self.spin_b.text()),
                                                     int(self.spin_n.text()), int(self.spin_l.text()),
                                                     self.k_edit.text(), self.f_edit.text())
                self.ax.scatter(s1, s2)
                self.ax.plot(p1, p2)
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y(x)')
            self.ax.grid(True)

            self.figure.tight_layout()
            self.canvas.draw()
            if o != '':
                o = ' ' * int((len(o.split('\n')[0])//2) * 0.8) + o.split('\n')[0] + '\n' + o.split('\n')[1]
            self.out_edit.setText(f'{f}\n\n{y}\n\n{o}')
        except Exception as e:
            self.out_edit.setText(str(e))


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    exit(app.exec())
