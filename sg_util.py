import sys
import getpass
from constants import SG_CONNECTOR
from pathlib import Path

sys.path.append(SG_CONNECTOR)

from connector import get_sg_instance, get_sg_user_name


class SG_Utils:
    def __init__(self):
        self.sg = get_sg_instance()
        self.active_shows = []

    def get_all_projects(self):
        if not self.active_shows:
            self.active_shows = self.sg.find("Project", [["sg_status", "is", "Active"]], ["id", "name", "code"])
        return self.active_shows

    def get_all_sequences(self, project):
        return self.sg.find("Sequence", [["project", "is", project], ["sg_status_list", "is_not", "omt"]], ["id", "code"])

    def get_all_shots(self, project, seq):
        return self.sg.find("Shot", [["project", "is", project],
                                ["sg_sequence", "is", seq],
                                ["sg_status_list", "is_not", "omt"]
                            ],
                            ["id", "code", 'sg_status_list'])

    def get_all_tasks(self, shot):
        return self.sg.find("Task",
                            [["entity", "is", shot]],
                            ["id", "content", 'name'])

    def get_all_notes(self, shot):
        return self.sg.find("Note",
                            [["note_links", "in", shot]],
                            [
                                "id",
                                "subject",
                                "content",
                                "user",
                                "created_at",
                                "note_type",
                                "tasks",
                                "note_links",
                                "attachments"
                            ]
                            )

    def get_all_versions(self, shot):
        return self.sg.find("Version", [["entity", "is", shot]], ["id", "code"])

    def download_attachment(self, id, filepath):
        self.sg.download_attachment(id, filepath)

    def create_note(self, data, attachments):
        #         note_data = {
        #     "project": {"type": "Project", "id": 123},  # Replace with actual project ID
        #     "content": "This is a new note created via API.",
        #     "subject": "New Note Example",
        #     "note_links": [{"type": "Shot", "id": 456}],  # Replace with entity ID (Shot, Asset, etc.)
        #     "created_by": {"type": "HumanUser", "id": 789},  # Replace with the user ID
        # }

        # Send the request
        new_note = self.sg.create("Note", data)
        uploaded_files = []
        for fullpath in attachments:
            uploaded_file = self.sg.upload("Note", new_note.get("id"), fullpath, field_name="attachments")
            new_at ={"id": uploaded_file, "name": Path(fullpath).name, 'type': 'Attachment' }
            uploaded_files.append(new_at)
        return new_note, uploaded_files

    def get_user(self):
        return get_sg_user_name(self.sg, getpass.getuser())



if __name__ == '__main__':
    sgu = SG_Utils()
    print(sgu.get_all_projects())


{'id': 7149,
  'project': {'id': 155, 'name': 'pipeline_dev', 'type': 'Project'},
    'content': 'test note result', 
    'subject': 'test_shot_002_roto_v004.mov',
      'note_links': [{'id': 2068, 'name': 'test_shot_002', 'type': 'Shot'}, 
                     {'id': 9200, 'name': 'test_shot_002_roto_v004.mov', 'type': 'Version'}], 
                     'created_by': None, 'type': 'Note'}
# [15731]