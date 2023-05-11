import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class WebcamWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('webcam2.ui', self)  # UI 파일 로드
        self.webcam = cv2.VideoCapture(0)
        self.timer = self.startTimer(5)  # 타이머 설정

        # 버튼 클릭 이벤트 설정
        self.switch_button.clicked.connect(self.switch_webcam)
        self.set_resolution_button.clicked.connect(self.set_resolution)

    def switch_webcam(self):
        if self.webcam.get(cv2.CAP_PROP_CAMERA_MODE) == 0:
            self.webcam.release()
            self.webcam = cv2.VideoCapture(1)
        else:
            self.webcam.release()
            self.webcam = cv2.VideoCapture(0)

    def set_resolution(self):
        width = int(self.width_edit.text())
        height = int(self.height_edit.text())
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def timerEvent(self, event):
        ret, image = self.webcam.read()
        if ret:
            # 이미지 변환
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, ch = image.shape
            bytes_per_line = ch * w
            # QImage 생성
            q_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            # QLabel에 이미지 출력
            self.image_label.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        self.webcam.release()  # 웹캠 종료


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebcamWindow()
    window.show()
    sys.exit(app.exec_())