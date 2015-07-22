# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui

class ExpandableBox(QtGui.QWidget):
    def __init__(self, content_widget, title='', hide=False):
        super(ExpandableBox, self).__init__()

        self._vertical_layout = QtGui.QVBoxLayout()
        self._vertical_layout.setContentsMargins(0, 0, 0, 0)
        self._vertical_layout.setSpacing(0)

        self.create_head_widget(title)
        self.create_content_widget(content_widget)
        self.set_custom_stylesheet()

        self._vertical_layout.addWidget(self.head_widget)
        self._vertical_layout.addWidget(self.content_widget)
        self.setLayout(self._vertical_layout)

        self.minimize_btn.clicked.connect(self.change_visible_state)

        self.minimized = False

        if hide:
            self.change_visible_state()

    def create_head_widget(self, title):
        self._head_layout = QtGui.QHBoxLayout()
        self._head_layout.setContentsMargins(10, 8, 15, 3)
        self._head_layout.setSpacing(0)

        self.minimize_btn = QtGui.QPushButton("-")
        self.minimize_btn.setFixedHeight(20)
        self.minimize_btn.setFixedWidth(20)
        self.minimize_btn.setObjectName("minimize_btn")

        self.title_lbl = QtGui.QLabel(title)
        self.title_lbl.setStyleSheet("font: italic 15px;")

        self._head_layout.addWidget(self.minimize_btn)
        self._head_layout.addSpacing(10)
        self._head_layout.addWidget(self.title_lbl)

        self.head_widget = QtGui.QWidget()
        self.head_widget.setLayout(self._head_layout)
        self.head_widget.setObjectName("head_widget")


    def create_content_widget(self, content_widget):

        self._content_widget = content_widget

        self.content_widget = QtGui.QWidget()
        self.content_layout = QtGui.QVBoxLayout()
        self.content_layout.setContentsMargins(8,8,8,8)
        self.content_layout.setSpacing(0)
        self.content_layout.addWidget(self._content_widget)
        self.content_widget.setLayout(self.content_layout)

        self.content_widget.setObjectName("content_widget")

    def set_custom_stylesheet(self):
        self.setStyleSheet(
            """
            QLabel, #head_widget{
                background: #303030;
            }
            #head_widget{
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border: 2px solid #666;
                border-bottom: 1px solid #666;
            }
            """
        )
        self.content_widget.setStyleSheet(
            """
            QLabel, QGroupBox, #content_widget{
                background: #3B3B3B;
            }
            #content_widget{
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                border: 2px solid #666;
                border-top: None;
            }
            """
        )
        self.head_widget.setStyleSheet(
            """
            #minimize_btn{
                border-radius:0px;
                padding: 0px;
                margin: 0px;
                margin-bottom: 2px;
                margin-left: 2px;
                border-top-left-radius: 5px;
            }
            """
        )

    def change_visible_state(self):
        if self.minimized:
            self.content_widget.show()
            self.minimized = False
            self.minimize_btn.setText("-")
        else:
            self.content_widget.hide()
            self.minimized = True
            self.minimize_btn.setText("+")