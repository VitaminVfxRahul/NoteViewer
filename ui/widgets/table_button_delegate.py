from PySide2 import QtWidgets, QtCore, QtGui


class ButtonDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, icon_path, color, action=None, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.color = color 
        self.__action = action

    def paint(self, painter, option, index):
        if not index.isValid():
            return

       
        pixmap = QtGui.QPixmap(self.icon_path)
        if pixmap.isNull():
            return  
        
        colored_pixmap = self.colorize_pixmap(pixmap, self.color)

        icon_size = QtCore.QSize(25, 25)
        icon_rect = QtCore.QRect(option.rect.center() - QtCore.QPoint(12, 12), icon_size)

        painter.drawPixmap(icon_rect, colored_pixmap)

    def colorize_pixmap(self, pixmap, color):
        colored_pixmap = QtGui.QPixmap(pixmap.size())
        colored_pixmap.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(colored_pixmap)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)

        painter.drawPixmap(0, 0, pixmap)

        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.fillRect(colored_pixmap.rect(), QtGui.QColor(color))

        painter.end()
        return colored_pixmap

    def editorEvent(self, event, model, option, index):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            self.__action(index)
            # if index.column() == 1:
            #     self.view_row(index)
            # elif index.column() == 2:
            #     self.delete_row(index)
            return True
        return False

    # def view_row(self, index):
    #     print("View", index.row())
    #     QtWidgets.QMessageBox.information(None, "View Row", f"Viewing row {index.row()}")

    # def delete_row(self, index):
    #     print("Delete", index.row())
    #     model = index.model()
    #     model.removeRow(index.row())
