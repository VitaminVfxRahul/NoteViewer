from PySide2 import  QtCore, QtGui
from PySide2.QtSvg import QSvgRenderer


def colorize_svg(svg_path, color):
    """Load an SVG and apply a solid color to it."""
    renderer = QSvgRenderer(svg_path)
    pixmap = QtGui.QPixmap(32, 32)  # Set icon size
    pixmap.fill(QtCore.Qt.transparent)  # Transparent background

    painter = QtGui.QPainter(pixmap)
    renderer.render(painter)  # Draw original SVG

    # Apply color overlay
    painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceAtop)
    painter.fillRect(pixmap.rect(), color)
    
    painter.end()
    return QtGui.QIcon(pixmap)
