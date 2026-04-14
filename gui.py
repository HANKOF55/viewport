#!/usr/bin/env python3
"""
Linux Spacedesk Clone - GUI Application
Provides a graphical interface to control the spacedesk server.
"""

import platform

class ServerSignals(QObject):
    """Signals for thread communication"""
    status_update = pyqtSignal(str)
    client_connected = pyqtSignal(str)
    client_disconnected = pyqtSignal(str)

class SpacedeskGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server = None
        self.server_thread = None
        self.signals = ServerSignals()
        self.signals.status_update.connect(self.update_status)
        self.signals.client_connected.connect(self.add_client)
        self.signals.client_disconnected.connect(self.remove_client)
        
        self.init_ui()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.check_server_status)
        self.update_timer.start(1000)  # Check every second
        
    def init_ui(self):
        self.setWindowTitle('Linux Spacedesk Clone')
        self.setGeometry(100, 100, 600, 500)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Server control group
        server_group = QGroupBox("Server Control")
        server_layout = QVBoxLayout()
        
        # Start/Stop buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton('Start Server')
        self.start_btn.clicked.connect(self.start_server)
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px; }")
        
        self.stop_btn = QPushButton('Stop Server')
        self.stop_btn.clicked.connect(self.stop_server)
        self.stop_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 10px; }")
        self.stop_btn.setEnabled(False)
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        server_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel('Server Status: Stopped')
        self.status_label.setStyleSheet("QLabel { font-weight: bold; }")
        server_layout.addWidget(self.status_label)
        
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)
        
        # Configuration group
        config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout()
        
        # Display mode
        display_layout = QHBoxLayout()
        display_layout.addWidget(QLabel('Display Server:'))
        self.display_combo = QComboBox()
        if platform.system() == 'Darwin':
            self.display_combo.addItems(['macOS'])
            self.display_combo.setCurrentText('macOS')
        else:
            self.display_combo.addItems(['X11', 'Wayland'])
            self.display_combo.setCurrentText('X11')
        display_layout.addWidget(self.display_combo)
        display_layout.addStretch()
        config_layout.addLayout(display_layout)
        
        # Resolution
        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel('Resolution:'))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(800, 3840)
        self.width_spin.setValue(1920)
        res_layout.addWidget(self.width_spin)
        res_layout.addWidget(QLabel('x'))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(600, 2160)
        self.height_spin.setValue(1080)
        res_layout.addWidget(self.height_spin)
        res_layout.addStretch()
        config_layout.addLayout(res_layout)
        
        # FPS and Quality
        perf_layout = QHBoxLayout()
        perf_layout.addWidget(QLabel('FPS:'))
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(10, 60)
        self.fps_spin.setValue(30)
        perf_layout.addWidget(self.fps_spin)
        
        perf_layout.addWidget(QLabel('Quality:'))
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(10, 100)
        self.quality_spin.setValue(90)
        perf_layout.addWidget(self.quality_spin)
        perf_layout.addStretch()
        config_layout.addLayout(perf_layout)
        
        # Port
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel('Port:'))
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1024, 65535)
        self.port_spin.setValue(5900)
        port_layout.addWidget(self.port_spin)
        port_layout.addStretch()
        config_layout.addLayout(port_layout)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Clients group
        clients_group = QGroupBox("Connected Clients")
        clients_layout = QVBoxLayout()
        self.clients_text = QTextEdit()
        self.clients_text.setMaximumHeight(100)
        self.clients_text.setReadOnly(True)
        clients_layout.addWidget(self.clients_text)
        clients_group.setLayout(clients_layout)
        layout.addWidget(clients_group)
        
        # Log group
        log_group = QGroupBox("Server Log")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # Set dark theme
        self.set_dark_theme()
        
    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)
        
    def start_server(self):
        if self.server and self.server.running:
            return
            
        # Get configuration
        display_mode = self.display_combo.currentText()
        width = self.width_spin.value()
        height = self.height_spin.value()
        port = self.port_spin.value()
        fps = self.fps_spin.value()
        quality = self.quality_spin.value()
        
        # Create server
        self.server = LinuxSpacedeskServer(
            host='0.0.0.0',
            port=port,
            display_mode=display_mode,
            fps=fps,
            quality=quality
        )
        self.server.width = width
        self.server.height = height
        
        # Start server thread
        self.server_thread = threading.Thread(target=self.server.run, daemon=True)
        self.server_thread.start()
        
        # Update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText('Server Status: Starting...')
        self.log_message(f"Starting server on port {port} with {display_mode} display")
        
        # Disable config while running
        self.fps_spin.setEnabled(False)
        self.quality_spin.setEnabled(False)
        self.display_combo.setEnabled(False)
        self.width_spin.setEnabled(False)
        self.height_spin.setEnabled(False)
        self.port_spin.setEnabled(False)
        
    def stop_server(self):
        if self.server:
            self.server.running = False
            self.server = None
            
        # Update UI
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText('Server Status: Stopped')
        self.log_message("Server stopped")
        
        # Enable config
        self.display_combo.setEnabled(True)
        self.width_spin.setEnabled(True
        self.fps_spin.setEnabled(True)
        self.quality_spin.setEnabled(True))
        self.height_spin.setEnabled(True)
        self.port_spin.setEnabled(True)
        
    def check_server_status(self):
        if self.server and self.server.running:
            self.status_label.setText('Server Status: Running')
        elif self.server and not self.server.running:
            self.status_label.setText('Server Status: Stopped')
            
    def update_status(self, message):
        self.status_label.setText(f'Server Status: {message}')
        
    def add_client(self, client_addr):
        current_text = self.clients_text.toPlainText()
        if client_addr not in current_text:
            self.clients_text.append(f"Connected: {client_addr}")
            self.log_message(f"Client connected: {client_addr}")
            
    def remove_client(self, client_addr):
        current_text = self.clients_text.toPlainText()
        lines = current_text.split('\n')
        new_lines = [line for line in lines if client_addr not in line]
        self.clients_text.setPlainText('\n'.join(new_lines))
        self.log_message(f"Client disconnected: {client_addr}")
        
    def log_message(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.append(f"[{timestamp}] {message}")
        
    def closeEvent(self, event):
        self.stop_server()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    gui = SpacedeskGUI()
    gui.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()