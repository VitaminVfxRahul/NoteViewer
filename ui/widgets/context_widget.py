from PySide2 import QtWidgets, QtCore
from .context_combo import ContextCombo


class ContextWidget(QtWidgets.QWidget):
    on_show_changed = QtCore.Signal((object,), ())
    on_seq_changed = QtCore.Signal((object,), ())
    on_shot_changed = QtCore.Signal((object,), ())

    def __init__(self, sg_util,  parent=None):
        super().__init__(parent=parent)
        self.sg_util = sg_util
        self.all_projects = self.sg_util.get_all_projects()
        self.current_show = None 
        self.current_seq = None 
        self.current_shot = None 
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)

        # show widget
        self.show_combo = ContextCombo('Show', 'Select show')
        self.show_combo.add_items(self.all_projects)
        self.main_layout.addWidget(self.show_combo)
        

        # seq widget
        self.seq_combo = ContextCombo('Sequence', 'Select sequence')
        self.main_layout.addWidget(self.seq_combo)
        
        # shot widget
        self.shot_combo = ContextCombo('Shot', 'Select shot')
        self.main_layout.addWidget(self.shot_combo)


        # connections
        self.show_combo.on_selection_changed.connect(self.show_changed)
        self.seq_combo.on_selection_changed.connect(self.seq_changed)
        self.shot_combo.on_selection_changed.connect(self.shot_changed)

    def show_changed(self, item):
        if not item:
            self.current_show = None
            self.seq_combo.clear_items()
        else:
            self.current_show = item
            if self.current_show:
                seqs = self.sg_util.get_all_sequences(item)
                self.seq_combo.add_items(seqs)
        
        result = {'show': self.current_show}
        self.on_show_changed.emit(result)

    def seq_changed(self, item):
        if not any([item, self.current_show]):
            self.current_seq = None
            self.seq_combo.clear_items()
        else:
            self.current_seq = item
            if self.current_seq:
                seqs = self.sg_util.get_all_shots(self.current_show, self.current_seq)
                self.shot_combo.add_items(seqs)
        
        result = {'show': self.current_show, 'seq': self.current_seq}
        self.on_seq_changed.emit(result)

    def shot_changed(self, item):
        if not any([item, self.current_show, self.current_seq]):
            self.current_shot = None
            self.shot_combo.clear_items()
        else:
            self.current_shot = item
        
        result = {
            'show': self.current_show,
            'seq': self.current_seq,
            'shot':self.current_shot
            }
        
        self.on_shot_changed.emit(result)

    def set_default_show(self, show):
        self.show_combo.set_default(show)

    def set_default_seq(self, seq):
        self.seq_combo.set_default(seq)
    
    def set_default_shot(self, shot):
        self.shot_combo.set_default(shot)


if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    w = ContextWidget()
    w.show()
    app.exec_()