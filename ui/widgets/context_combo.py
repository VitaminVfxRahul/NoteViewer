from PySide2 import QtWidgets, QtCore


class ContextCombo(QtWidgets.QWidget):
    on_selection_changed = QtCore.Signal(object)

    def __init__(self,label, placeholder, items=None,  parent=None):
        super().__init__(parent=parent)

        self.items = items or []
        self.placeholder = placeholder

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setMargin(0)
        self.item_label = QtWidgets.QLabel(label)
        self.item_label.setFixedWidth(100)
        self.item_combo = QtWidgets.QComboBox()

        self.main_layout.addWidget(self.item_label)
        self.main_layout.addWidget(self.item_combo)

        self.item_combo.currentIndexChanged.connect(self.on_item_changed)

    def add_items(self, items):
        self.clear_items()
        self.item_combo.addItem(self.placeholder)
        for i, item in enumerate(items):
            title = item.get("name") or item.get("code") or item.get("content")
            self.item_combo.addItem(title, item)

    def on_item_changed(self, index):
        if index > -1:
            item_data = self.item_combo.itemData(index, QtCore.Qt.UserRole)
            self.on_selection_changed.emit(item_data)

    def clear_items(self):
        self.item_combo.clear()

    def set_default(self, name):
        index = self.item_combo.findText(name)
        if index > -1:
            self.item_combo.setCurrentIndex(index)