from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QSlider, QStyle
from PyQt5.QtGui import QPixmap, QIcon, QPalette
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PIL.ImageQt import ImageQt


class Monitor(QMainWindow):
    _update_image_signal = pyqtSignal()

    def __init__(
            self,
            file_name: str,
            host_address: str,
            host_port: int,
            rtp_port: int,
            parent=None):
        super(self).__init__(parent)
        self.video_player = QLabel()
        self.play_button = QPushButton()
        self.tear_button = QPushButton()

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.is_playing = False
        self.slider = QSlider(Qt.Horizontal)

        self._update_image_signal.connect(self.update_image)
        self._update_image_timer = QTimer()
        self._update_image_timer.timeout.connect(self._update_image_signal.emit)

        self.image_buffer = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Monitor")
        self.setGeometry(350, 100, 1024, 500)

        # slider #TODO
        self.slider.setRange(0, 0)

        # play Btn
        self.play_button.setEnabled(False)
        self.play_button.setIcon( self.style().standardIcon(QStyle.SP_MediaPlay) )
        self.play_button.clicked.connect(self.handle_play)


        self.tear_button.setEnabled(False)
        self.tear_button.setText('Teardown')
        self.tear_button.clicked.connect(self.handle_teardown)

    
        # slider
        self.slider.setRange(0,0)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)
 
        #set widgets to the hbox layout
        hboxLayout.addWidget(self.play_button)
        hboxLayout.addWidget(self.slider)
        hboxLayout.addWidget(self.tear_button)

        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.video_player)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        central_widget = QVideoWidget(self)
        self.setCentralWidget(central_widget)

        central_widget.setLayout(vboxLayout)

        self.handle_setup()

    def update_image(self):
        if not self.image_buffer: return
        pix = QPixmap.fromImage(ImageQt(self.image_buffer[0]).copy())
        self.video_player.setPixmap(pix)
        self.image_buffer.pop(0)

    def handle_setup(self):
        self._media_client.establish_rtsp_connection()
        self._media_client.send_setup_request()
        self.play_button.setEnabled(True)
        self.tear_button.setEnabled(True)
        self._update_image_timer.start(1000//30)

    def handle_play(self):
        if not self.is_playing: ## play request
            self._media_client.send_play_request()
            self.play_button.setIcon( self.style().standardIcon(QStyle.SP_MediaPause) )
            self.is_playing = True
        else:                   ## pause request
            self._media_client.send_pause_request()
            self.play_button.setIcon( self.style().standardIcon(QStyle.SP_MediaPlay) )
            self.is_playing = False

    def handle_teardown(self):
        self._media_client.send_teardown_request()
        self.play_button.setEnabled(False)
        self._media_client.close_rtsp_connection()
        exit(0)

    def rcv_img(self, frame):
        self.image_buffer.append(frame)