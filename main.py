from PySide2 import QtWidgets, QtCore
from ui.widgets.context_widget import ContextWidget
from ui.widgets.filter_widget import FilterWidget
from ui.note_item import NewNoteWidget, NoteItem
from sg_util import SG_Utils
from constants import CSS_FILE, THEME_FILE
from qt_material import apply_stylesheet


class NoteViewer(QtWidgets.QWidget):

    def __init__(self, show=None, seq=None, shot=None, parent=None):
        super().__init__(parent=parent)
        self.sg_util = SG_Utils()
        self.notes = []

        self.current_context = {}
        self.current_version = None

        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Left panel container
        self.left_container = QtWidgets.QWidget()   
        self.left_layout = QtWidgets.QVBoxLayout(self.left_container)
        self.left_layout.setContentsMargins(0, 0, 0, 0)  

        self.context_widget = ContextWidget(sg_util=self.sg_util)
        self.left_layout.addWidget(self.context_widget)

        self.filter_widget = FilterWidget()
        self.left_layout.addWidget(self.filter_widget)

        self.add_note_button = QtWidgets.QPushButton("Add Note")
        self.add_note_button.setEnabled(False)

        self.main_layout.addWidget(self.left_container)   

        # Note panel 
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area, 1)   

        self.note_container = QtWidgets.QWidget()   
        self.note_layout = QtWidgets.QVBoxLayout(self.note_container)
        self.note_layout.setAlignment(QtCore.Qt.AlignTop)
        self.note_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.note_container)

        self.main_layout.addWidget(self.add_note_button)
        self.add_note_button.clicked.connect(self.open_add_note)
        self.resize(600, 800)

        # connection 
        self.context_widget.on_show_changed.connect(self.load_filter_widget)
        self.context_widget.on_seq_changed.connect(self.load_filter_widget)
        self.context_widget.on_shot_changed.connect(self.load_filter_widget)
        self.filter_widget.on_task_changed.connect(self.load_fitered_notes)
        self.filter_widget.on_version_changed.connect(self.load_fitered_notes)
        self.context_widget.on_refresh.connect(self.load_fitered_notes)

        # setting defaults 
        if show:
            self.context_widget.set_default_show(show)
        if seq:
            self.context_widget.set_default_seq(seq)
        if shot:
            self.context_widget.set_default_shot(shot)

    def open_add_note(self):
        context = {
            "project": self.current_context.get("show"),
            "note_links": [self.current_context.get("shot"), self.current_version],
            "subject": self.current_version.get("code"),
        }

        self.__open_add_note_dialog(context)


    def load_filter_widget(self, context_data):
        self.current_context = context_data
        shot = context_data.get("shot")

        # get all notes
        if not self.__is_shot_context():
            return

        self.notes = self.sg_util.get_all_notes(shot)

        # update filter widget fields
        tasks = self.sg_util.get_all_tasks(shot)
        self.filter_widget.task_combo.clear_items()
        self.filter_widget.task_combo.add_items(tasks)

        versions = self.sg_util.get_all_versions(shot)
        self.filter_widget.version_combo.clear_items()
        self.filter_widget.version_combo.add_items(versions)

        self.load_fitered_notes()

    def __is_shot_context(self):
        return all([
            self.current_context, 
            self.current_context.get("show"),
            self.current_context.get("seq"),
            self.current_context.get("shot")
        ])
    
    def __enable_add_note_btn(self, filters):
        if not filters or not self.__is_shot_context:
            self.add_note_button.setEnabled(False)
            return
        
        self.current_version = {}
        for f in filters:
            if f.get("type").lower() == 'version':
                self.current_version = f
        
        if self.current_version:
            self.add_note_button.setEnabled(True)
        else:
            self.add_note_button.setEnabled(False)

    def load_fitered_notes(self, filters=None):
        self.clear_items(self.note_layout)
        self.__enable_add_note_btn(filters)
        filtered_notes = self.get_filtered_notes(filters)
       
        for note in filtered_notes:
            self.append_note_item(note)

    def append_note_item(self, note):
        note_item = NoteItem(self.sg_util, new_note=False, note=note)
        note_item.display_thread()
        self.note_layout.addWidget(note_item)
        note_item.onPressOk.connect(self.open_reply_window)

    def get_filtered_notes(self, filters=None):
        if not filters:
            return self.notes

        filtered = []
        for note in self.notes:
            for f in filters:
                matched = False 
                for nl in note.get("note_links", []):
                    if nl.get("type") == f.get("type") and nl.get("name") == f.get("code"):
                        matched = True
                    if nl.get("type") == f.get("type") and nl.get("name") == f.get("content"):
                        matched = True
                for t in note.get("tasks"):
                    if t.get('name') == f.get('content'):
                        matched = True
                if matched:
                    filtered.append(note)
        return filtered

    def open_reply_window(self, data):
        prev_note = data.get('note')
        context = {
            "project": self.current_context.get("show"),
            "note_links": prev_note.get('note_links'),
            "subject": prev_note.get('subject')
        }
        self.__open_add_note_dialog(context)

    def __open_add_note_dialog(self, context):
        ni = NewNoteWidget(sg_util=self.sg_util,  context_data=context)
        result = ni.exec_()
        if result == QtWidgets.QDialog.Accepted:
            if ni.added_note:
                self.notes.append(ni.added_note)
                self.append_note_item(ni.added_note)

    def clear_items(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    w = NoteViewer(show='DID', seq='101', shot='040_010')
    apply_stylesheet( app,  theme=THEME_FILE
                    #  , css_file=CSS_FILE 
                     )
    w.show()
    app.exec_()


# TODO 
# []  note thread.
# []  double check filters

# [x] beautify note shown in the ui
# [x] add refersh button 
# [x] implement task filter.
# [x] Change layout so all the filters are on the top
# [x] Add scroll
# [x] append new note in the ui 
# [x] fix the open image logic
# [x] implement reply. 
# [x] set ui defaults