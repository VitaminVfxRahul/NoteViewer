from PySide2 import QtWidgets, QtCore
from .context_combo import ContextCombo


class FilterWidget(QtWidgets.QWidget):
    on_task_changed = QtCore.Signal((list,), ())
    on_version_changed = QtCore.Signal((list,), ())
  

    def __init__(self, tasks=None, versions=None, parent=None):
        super().__init__(parent=parent)
        self.tasks = tasks or []
        self.versions = versions or [] 

        self.current_task = None 
        self.current_version = None 
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)


        # task widget
        self.task_combo = ContextCombo('Task', 'Select Task')
        self.task_combo.add_items(self.tasks)
        self.main_layout.addWidget(self.task_combo)

        # version widget
        self.version_combo = ContextCombo('Version', 'Select Version')
        self.version_combo.add_items(self.versions)
        self.main_layout.addWidget(self.version_combo)
      
        # connections
        self.task_combo.on_selection_changed.connect(self.task_changed)
        self.version_combo.on_selection_changed.connect(self.version_changed)

    def task_changed(self, item):
        self.current_task = item
        result = [] 

        if self.current_task:
            result.append(self.current_task)
        if self.current_version:
            result.append(self.current_version)

        self.on_task_changed.emit(result)

    def version_changed(self, item):
        self.current_version = item
        result = [] 

        if self.current_task:
            result.append(self.current_task)
        if self.current_version:
            result.append(self.current_version)

        self.on_version_changed.emit(result)




if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    w = FilterWidget()
    w.show()
    app.exec_()