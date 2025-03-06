from pathlib import Path
from PySide2 import QtWidgets
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, QSize


class ImageDialog(QtWidgets.QDialog):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.pixmap = QPixmap(self.image_path) if Path(self.image_path).exists() else QPixmap()
        self.last_size = QSize(0, 0)   

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.image_label)
        self.update_image_size()  
        self.resize(600, 400)

    def update_image_size(self):
        if not self.pixmap.isNull():
            scaled_pixmap = self.pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        if self.size() != self.last_size:   
            self.last_size = self.size()
            self.update_image_size()
        super().resizeEvent(event)   


# Run the application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    image_path = "C:/Users/rahul.mishra/.note_viewer/11134/annot_version_13309.131.png"
    window = ImageDialog(image_path)
    window.resize(600, 400)  # Initial window size
    window.show()

    sys.exit(app.exec_())
