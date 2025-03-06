
from pathlib import Path 

SG_CONNECTOR = "P:/utils/python/vitamin_sg"

etc_dir_path = Path(__file__).parent / 'etc'
css_file_path = etc_dir_path / "ui.css"
theme_file_path = etc_dir_path / "ui_theme_new.xml"
icon_dir_path = etc_dir_path / "icons"

CSS_FILE = css_file_path.as_posix()
THEME_FILE = theme_file_path.as_posix()
ICON_DIR = icon_dir_path.as_posix()
