from modules.highlight_detector import detect_highlights
from modules.video_editor import edit_video
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Video Highlighter')
        self.setGeometry(100, 100, 400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel('동영상 파일을 선택하세요')
        self.btn_select = QPushButton('동영상 선택')
        self.btn_select.clicked.connect(self.open_file)
        self.btn_process = QPushButton('하이라이트 추출 및 편집')
        self.btn_process.clicked.connect(self.process_video)
        self.btn_process.setEnabled(False)
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.btn_process)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.video_path = None

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '동영상 파일 선택', '', 'Video Files (*.mp4 *.avi *.mov)')
        if file_path:
            self.video_path = file_path
            self.label.setText(f'선택된 파일: {file_path}')
            self.btn_process.setEnabled(True)

    def process_video(self):
        if self.video_path:
            self.label.setText('하이라이트 추출 중...')
            highlights = detect_highlights(self.video_path)
            output_path = edit_video(self.video_path, highlights)
            self.label.setText(f'완료! 결과 파일: {output_path}')

def main():
    # Qt 플러그인 경로 환경 변수 설정 (PyQt5>=5.15.4에서 Qt5/plugins 경로 사용)
    qt_plugins_path = os.path.join(os.path.dirname(sys.modules['PyQt5'].__file__), 'Qt5', 'plugins')
    if os.path.exists(qt_plugins_path):
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugins_path

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
