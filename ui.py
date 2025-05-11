from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QMainWindow
from PyQt5.QtGui import QColor, QFont, QPainterPath, QPainter, QBrush
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect
import sys
from BP import P

class RoundedWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("roundedWidget")
        # 设置背景色为白色
        self.setStyleSheet("#roundedWidget { background-color: white; }")
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
    def paintEvent(self, event):
        # 绘制圆角矩形
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 12, 12)
        
        painter.fillPath(path, QBrush(QColor("white")))

class VideoDownloaderUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置窗口属性
        self.setWindowTitle('B站视频下载器')
        self.setFixedSize(450, 350)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # 创建圆角容器
        self.container = RoundedWidget()
        container_layout = QVBoxLayout(self.container)
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel('B站视频下载器')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 18))
        title.setStyleSheet("""
            color: #333;
            font-weight: 500;
            margin-bottom: 10px;
        """)
        
        # 输入框
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('请输入视频链接')
        self.url_input.setStyleSheet("""
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 12px 15px;
            font-size: 14px;
        """)
        self.url_input.setFixedHeight(45)
        
        # 下载按钮
        self.download_btn = QPushButton('下载视频')
        self.download_btn.setStyleSheet("""
            background-color: #eb52d6;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 14px;
        """)
        self.download_btn.setFixedHeight(45)
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.clicked.connect(self.on_download_clicked)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                height: 4px;
                background: #e0e0e0;
                border-radius: 2px;
                border: none;
            }
            QProgressBar::chunk {
                background: #eb52d6;
                border-radius: 2px;
            }
        """)
        self.progress.setFixedHeight(4)
        self.progress.hide()
        
        # 添加控件到容器布局
        container_layout.addWidget(title)
        container_layout.addWidget(self.url_input)
        container_layout.addWidget(self.download_btn)
        container_layout.addWidget(self.progress)
        
        # 添加容器到主布局
        main_layout.addWidget(self.container)
        
        # 添加淡入动画
        self.fade_in_animation()
        
    def fade_in_animation(self):
        # 创建透明度效果
        self.opacity_effect = QGraphicsOpacityEffect(self.container)
        self.container.setGraphicsEffect(self.opacity_effect)
        
        # 创建动画
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()
        
    def on_download_clicked(self):
        url = self.url_input.text()
        if not url:
            return
            
        # 显示进度条
        self.progress.show()
        self.progress.setValue(0)
        
        # 禁用按钮和输入框
        self.download_btn.setEnabled(False)
        self.url_input.setEnabled(False)
        
        # 模拟下载进度
        self.progress_value = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)
        
        # 实际下载逻辑
        try:
            self.downloader = P(url)
            self.downloader.py()
            # 下载完成后会自动调用update_progress更新进度到100%
        except Exception as e:
            print(f"下载出错: {e}")
            self.timer.stop()
            self.progress.setValue(0)
            self.download_btn.setEnabled(True)
            self.url_input.setEnabled(True)
        
    def update_progress(self):
        self.progress_value += 5
        if self.progress_value >= 100:
            self.progress_value = 100
            self.timer.stop()
            
            # 下载完成后的操作
            self.download_btn.setEnabled(True)
            self.url_input.setEnabled(True)
            
            # 延迟隐藏进度条
            QTimer.singleShot(1000, lambda: self.progress.hide())
            
        self.progress.setValue(self.progress_value)

def main():
    app = QApplication(sys.argv)
    window = VideoDownloaderUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()