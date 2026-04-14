#!/usr/bin/env python3
"""
Linux Spacedesk Clone - Server
Allows mobile devices to act as secondary monitors over local network/Wi-Fi.
Compatible with X11 (primary), Wayland support limited.
"""

import platform

# Import macOS support if on macOS
if platform.system() == 'Darwin':
    try:
        import macos_support
        print("macOS support loaded")
    except ImportError:
        print("macOS support module not found")

class LinuxSpacedeskServer:
    def __init__(self, host='0.0.0.0', port=5900, display_mode='X11', fps=30, quality=90):
        self.host = host
        self.port = port
        self.display_mode = display_mode  # 'X11' or 'Wayland'
        self.running = False
        self.clients = []
        self.virtual_display = None
        
        # Video settings
        self.width = 1920
        self.height = 1080
        self.fps = fps
        self.quality = quality  # JPEG quality 0-100
        
        # Encoder settings
        self.codec = 'libx264'
        self.bitrate = '5M'
        
    def create_virtual_display(self):
        """Create virtual display for secondary monitor"""
        if self.display_mode == 'X11':
            try:
                # Check if xrandr available
                result = subprocess.run(['xrandr', '--version'], capture_output=True, text=True)
                if result.returncode != 0:
                    print("xrandr not available. Ensure X11 is running.")
                    return False
                
                # Add virtual output (requires kernel module and config)
                # This is simplified; real implementation needs proper setup
                subprocess.run(['xrandr', '--addmode', 'VIRTUAL1', f'{self.width}x{self.height}'])
                subprocess.run(['xrandr', '--output', 'VIRTUAL1', '--mode', f'{self.width}x{self.height}', '--right-of', 'eDP1'])
                
                self.virtual_display = 'VIRTUAL1'
                print(f"Created virtual display {self.virtual_display}")
                return True
                
            except Exception as e:
                print(f"Failed to create virtual display: {e}")
                return False
                
        elif self.display_mode == 'Wayland':
            print("Wayland virtual display creation is complex and requires custom protocol extensions.")
            print("For Wayland, consider using wlroots-based compositors or custom solutions.")
            return False
            
        return False
    
    def capture_screen(self):
        """Capture screen content"""
        try:
            # For virtual display, capture specific region
            if self.virtual_display:
                # Get position of virtual display
                result = subprocess.run(['xrandr'], capture_output=True, text=True)
                # Parse output to find VIRTUAL1 position
                # Simplified: assume it's at (1920, 0) if primary is 1920x1080
                x, y = 1920, 0
                screenshot = pyautogui.screenshot(region=(x, y, self.width, self.height))
            else:
                # Capture entire screen
                screenshot = ImageGrab.grab()
                
            return screenshot
            
        except Exception as e:
            print(f"Screen capture failed: {e}")
            return None
    
    def encode_frame(self, frame):
        """Encode frame using OpenCV/FFmpeg"""
        try:
            # Convert PIL to numpy
            np_frame = np.array(frame)
            
            # Convert RGB to BGR for OpenCV
            bgr_frame = cv2.cvtColor(np_frame, cv2.COLOR_RGB2BGR)
            
            # Encode to H.264
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
            _, encoded_img = cv2.imencode('.jpg', bgr_frame, encode_param)
            
            return encoded_img.tobytes()
            
        except Exception as e:
            print(f"Frame encoding failed: {e}")
            return None
    
    def start_server(self):
        """Main server loop"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        self.running = True
        
        print(f"Server started on {self.host}:{self.port}")
        print("Waiting for clients to connect...")
        
        while self.running:
            try:
                frame = self.capture_screen()
                if frame:
                    encoded = self.encode_frame(frame)
                    if encoded:
                        # Send to all connected clients
                        for client in self.clients:
                            try:
                                sock.sendto(encoded, client)
                            except:
                                # Remove disconnected client
                                self.clients.remove(client)
                
                time.sleep(1 / self.fps)
                
            except KeyboardInterrupt:
                break
                
        sock.close()
    
    def handle_input(self, data, addr):
        """Process input from client (mouse, keyboard)"""
        try:
            # Parse input data (simplified protocol)
            # Format: "type,x,y,button" for mouse
            # "key,code,pressed" for keyboard
            
            parts = data.decode().split(',')
            input_type = parts[0]
            
            if input_type == 'mouse':
                x, y, button = int(parts[1]), int(parts[2]), parts[3]
                if button == 'move':
                    pyautogui.moveTo(x, y)
                elif button == 'click':
                    pyautogui.click(x, y)
                    
            elif input_type == 'keyboard':
                key, pressed = parts[1], parts[2] == '1'
                if pressed:
                    pyautogui.press(key)
                    
        except Exception as e:
            print(f"Input handling failed: {e}")
    
    def input_listener(self):
        """Listen for client input"""
        input_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        input_sock.bind((self.host, self.port + 1))  # Different port for input
        
        while self.running:
            try:
                data, addr = input_sock.recvfrom(1024)
                if addr not in self.clients:
                    self.clients.append(addr)
                    print(f"New client connected: {addr}")
                    
                self.handle_input(data, addr)
                
            except:
                pass
                
        input_sock.close()
    
    def run(self):
        """Start the server"""
        if not self.create_virtual_display():
            print("Warning: Virtual display creation failed. Using primary display.")
        
        # Start input listener thread
        input_thread = threading.Thread(target=self.input_listener, daemon=True)
        input_thread.start()
        
        # Start main server
        self.start_server()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Linux Spacedesk Clone Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5900, help='Port to bind to')
    parser.add_argument('--display', choices=['X11', 'Wayland'], default='X11', help='Display server type')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second (10-60)')
    parser.add_argument('--quality', type=int, default=90, help='Video quality (0-100)')
    
    args = parser.parse_args()
    
    server = LinuxSpacedeskServer(
        host=args.host,
        port=args.port,
        display_mode=args.display,
        fps=args.fps,
        quality=args.quality
    )
    server.width = args.width
    server.height = args.height
    
    try:
        server.run()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.running = False

if __name__ == "__main__":
    main()