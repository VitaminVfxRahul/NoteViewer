from pathlib import Path
import datetime
from PySide2 import QtWidgets, QtCore

from .widgets.table_model import NoteTableModel
from .widgets.table_button_delegate import ButtonDelegate
from .widgets.image_widget import ImageDialog
from constants import ICON_DIR


class TopLabel(QtWidgets.QWidget):
    def __init__(self, title, stretch=None, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QtWidgets.QHBoxLayout(self)

        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold;")
        self.main_layout.addWidget(self.title_label)

        self.text_label = QtWidgets.QLabel()
        if stretch:
            self.text_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        
        self.main_layout.addWidget(self.text_label)

    def set_text(self, text):
        self.text_label.setText(text)

class NoteItem(QtWidgets.QWidget):
    onPressOk = QtCore.Signal(object)

    def __init__(self, sg_util, new_note=None, note=None, parent=None):
        super().__init__(parent=parent)

        self.sg_util = sg_util
        self.new_note = new_note
        self.note = note or {}
        self.reply_messages = []
        self.headers = ["Name", "View"]

        if self.new_note:
            self.headers.append("Delete")

        self.setup_ui()
        self.setFixedHeight(200)

    def setup_ui(self):
        self.frame_layout = QtWidgets.QHBoxLayout(self)
        self.frame_layout.setContentsMargins(0,0,0,0)
        frame = QtWidgets.QFrame()
        frame.setObjectName('noteItemFrame')
        self.frame_layout.addWidget(frame, alignment=QtCore.Qt.AlignTop)
        frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame.setStyleSheet('QFrame#noteItemFrame { background-color: #222222; border: 0px solid; padding: 0px 10px 10px } ')  
        # frame.setFrameShadow(QtWidgets.QFrame.Plain)  

        self.main_layout = QtWidgets.QGridLayout(frame)
        # self.main_layout.setContentsMargins(6,9,6,9)

        self.subject_label = TopLabel('Subject', stretch=True)
        self.subject_label.setMinimumHeight(40)
        self.main_layout.addWidget(self.subject_label, 0, 0, 1, 1)

        self.user_label = TopLabel('User')
        self.main_layout.addWidget(self.user_label, 0, 1, 1, 1)

        self.date_label = TopLabel("Date")
        self.main_layout.addWidget(self.date_label, 0, 2, 1, 1)
        
        # text edit
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.text_edit.setStyleSheet('border: 0px solid')
        self.main_layout.addWidget(self.text_edit, 1, 0, 1, 3)

        # image table
        self.attachment_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.attachment_layout, 1,3,1,1)

        self.table_view = QtWidgets.QTableView()
        self.table_view.setFixedWidth(300)
        self.attachment_layout.addWidget(self.table_view)
       

        self.model = NoteTableModel(self.note.get('attachments', []), self.headers)
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        self.table_view.setColumnWidth(1, 40)
        self.table_view.horizontalHeader().setVisible(False)  
        self.table_view.verticalHeader().setVisible(False)   

        delegate1 = ButtonDelegate(ICON_DIR+"/image.svg", "#4CAF50", action=self.view_item, parent= self.table_view)
        self.table_view.setItemDelegateForColumn(1, delegate1) 

        self.button_layout = QtWidgets.QHBoxLayout()
        self.attachment_layout.addLayout(self.button_layout)

        if self.new_note:
            delegate2 = ButtonDelegate(ICON_DIR+ "/x.svg", "#F44336", action=self.delete_item, parent=self.table_view)
            self.table_view.setItemDelegateForColumn(2, delegate2)
            self.table_view.setColumnWidth(2, 40)
            self.attach_button = QtWidgets.QPushButton('Attach')
            self.attach_button.setStyleSheet('border: 1px solid ')
            self.button_layout.addWidget(self.attach_button)
            self.attach_button.clicked.connect(self.browse_attachment)

        self.ok_button = QtWidgets.QPushButton("Ok" if self.new_note else "Reply")
        self.ok_button.setStyleSheet('border: 1px solid')
        self.button_layout.addWidget(self.ok_button)
        self.ok_button.clicked.connect(self.ok_clicked)

        
    def browse_attachment(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("All Files (*)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                for sf in selected_files:
                    path = Path(sf)
                    item_data = {"name": path.name, "path": path.as_posix()}
                    self.model.insertRow(self.model.rowCount(), item_data)

    def delete_item(self, index):
        self.model.removeRow(index.row())

    def view_item(self,index ):
        item = self.model.data(index, QtCore.Qt.UserRole)
        img_path_str = item.get("path", "")

        if not self.new_note:
            note_id = item.get("id")
            note_image = item.get("name")

            img_path = Path.home() / ".note_viewer" / str(note_id) / note_image
            img_path_str = img_path.as_posix()

            if not img_path.exists():
                img_path.parent.mkdir(parents=True, exist_ok=True)
                self.sg_util.download_attachment(note_id, img_path_str)
    
        if img_path_str:
            id = ImageDialog(img_path_str)
            id.exec_()

    def display_thread(self):
        subject = self.note.get('subject')
        user = self.note.get("user", {}).get("name", "")
        date = self.note.get("created_at").strftime("%b %d, %Y")
        note_content = self.note.get("content")

        self.subject_label.set_text(f'Subject: {subject}')
        self.user_label.set_text(f'User: {user}')
        self.date_label.set_text(f'Date: {date}')
        
        content = f"<p>{note_content}</p>"
        content += "<strong>Entities:</strong>"
        content += "<ul>"

        for each in self.note.get("note_links"):
            if each.get('type', '').lower() == 'shot':
                continue
            content += f"<li>{each.get('type')}: <strong>{each.get('name') or each.get('content')}</strong> </li>"
        content += "</ul>"

        self.text_edit.setHtml(content)

        # content = f"<b>📝️ {subject} - {user} ({date})</b><br>"
        # content += f"<i>{note_content}</i>"

        # for each in self.note.get("note_links"):
        #     msg = f"<br><br><b>{each.get('type')}:- {each.get('name') or each.get('content')} <\b>"
        #     content += msg
        # if self.reply_messages:
        #     content += "<br><hr>"

        # for reply in self.reply_messages:
        #     content += f"<b>↳ {reply['user']} ({reply['date']}):</b><br> {reply['content']}<br><br>"


    def ok_clicked(self):
       data = {
           "note": self.note,
           "new_note": self.new_note,
           "text": self.text_edit.toPlainText(),
           "attachments": self.model._data,
       }
       self.onPressOk.emit(data)
     

class NewNoteWidget(QtWidgets.QDialog):
    def __init__(self, sg_util, context_data, parent=None):
        super().__init__(parent=parent)
        self.added_note = None
        self.context_data = context_data
        self.sg_util = sg_util
        self.main_layout  = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0,0,0)
        self.note_item = NoteItem(sg_util=self.sg_util, new_note=True)
        self.main_layout.addWidget(self.note_item)

        self.note_item.onPressOk.connect(self.add_note)
    
    def add_note(self, note_data):
        user = self.sg_util.get_user()
        new_note = {
            "project": self.context_data.get("project"),
            "content": note_data.get("text"),
            "subject": self.context_data.get("subject"),
            "note_links": self.context_data.get("note_links"),
            "created_by": user
        }

        attachments = [each.get("path") for each in note_data.get("attachments")]
        sg_note, uploaded_files = self.sg_util.create_note(new_note, attachments)

        new_note.update({
            "type": "Note", 
            "id": sg_note.get("id"),
            "user": user or {},
            'attachments':uploaded_files,
            "created_at": sg_note.get("created_at", datetime.datetime.now())
            })
        

        self.added_note = new_note
        self.accept()
        


if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    w = NoteItem() 
    w.show()
    app.exec_()


