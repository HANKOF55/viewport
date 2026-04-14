# Linux Spacedesk Clone - Complete Documentation

## Overview

Linux Spacedesk Clone is an open-source implementation of spacedesk for Linux systems. It allows you to use mobile devices (Android, iOS) as secondary monitors for your Linux desktop over local network or Wi-Fi connections.

## Features

- **Cross-Platform Compatibility**: Works with X11 and experimental Wayland support
- **Network Streaming**: Low-latency video streaming over UDP
- **Input Support**: Touch, keyboard, and mouse input from mobile devices
- **Virtual Display**: Creates virtual monitors for seamless desktop extension
- **GUI Interface**: User-friendly graphical interface for server control
- **Command-Line Interface**: Terminal-based operation for advanced users

## System Requirements

### Hardware Requirements
- Linux-based operating system
- At least 2GB RAM (4GB recommended)
- Network interface (Ethernet or Wi-Fi)
- GPU with hardware encoding support (optional, improves performance)

### Software Requirements
- Python 3.6 or higher
- X11 display server (for X11 mode)
- Required Python packages (see Installation)

### Supported Display Servers
- **X11**: Full support with virtual display creation
- **Wayland**: Experimental support (limited virtual display functionality)

## Installation

### 1. Install Python Dependencies

```bash
# Install system packages (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip x11-utils xrandr

# Install Python packages
pip install -r requirements.txt
```

### 2. Configure Virtual Display (X11)

For X11 systems, you may need to configure virtual display support:

```bash
# Load dummy display kernel module (if available)
sudo modprobe dummy

# Or add to /etc/modules
echo "dummy" | sudo tee -a /etc/modules
```

### 3. Firewall Configuration

Ensure UDP ports 5900-5901 are open for network communication:

```bash
# UFW (Ubuntu)
sudo ufw allow 5900/udp
sudo ufw allow 5901/udp

# Or iptables
sudo iptables -A INPUT -p udp --dport 5900 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 5901 -j ACCEPT
```

## Usage

### Graphical Interface (Recommended)

Launch the GUI application:

```bash
python gui.py
```

#### GUI Features
- **Server Control**: Start/stop the server with one click
- **Configuration**: Set display mode, resolution, port, FPS, and quality
- **Client Monitoring**: View connected mobile devices
- **Real-time Logging**: Monitor server activity and errors

#### GUI Workflow
1. Select display server (X11/Wayland)
2. Set desired resolution (e.g., 1920x1080)
3. Choose network port (default: 5900)
4. Click "Start Server"
5. Connect mobile devices using compatible client apps

### Command-Line Interface

For advanced users or headless operation:

```bash
python main.py [options]
```

#### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | IP address to bind to | 0.0.0.0 |
| `--port` | UDP port for connections | 5900 |
| `--display` | Display server (X11/Wayland) | X11 |
| `--width` | Virtual display width | 1920 |
| `--height` | Virtual display height | 1080 |
| `--fps` | Frames per second (10-60) | 30 |
| `--quality` | Video quality (0-100) | 90 |
| `--help` | Show help message | - |

#### Examples

```bash
# Start with default settings
python main.py

# Custom configuration
python main.py --display X11 --width 2560 --height 1440 --port 5901

# Wayland mode (experimental)
python main.py --display Wayland
```

## Mobile Client Setup

### Android Devices
1. Install a compatible VNC or remote desktop client
2. Connect to your Linux machine's IP address and port 5900
3. Configure for touch input and display streaming

### iOS Devices
1. Use compatible remote desktop apps from App Store
2. Connect using your Linux machine's IP address
3. Enable touch gestures and keyboard input

### Recommended Client Apps
- **Android**: RealVNC Viewer, Microsoft Remote Desktop
- **iOS**: Microsoft Remote Desktop, RealVNC Viewer
- **Web-based**: Any HTML5 VNC client

## Network Configuration

### Local Network Setup
1. Ensure devices are on the same network
2. Find your Linux machine's IP address:
   ```bash
   ip addr show
   ```
3. Connect clients using the IP address and port 5900

### Wi-Fi Direct (Advanced)
For direct device-to-device connection:
1. Enable Wi-Fi Direct on both devices
2. Pair devices in system settings
3. Use the direct IP address for connection

### Port Forwarding (Remote Access)
For access over internet (not recommended for security):
```bash
# Forward ports on router
# External port 5900 -> Internal IP:5900 (UDP)
```

## Technical Architecture

### Server Components

#### 1. Virtual Display Creation
- **X11**: Uses RandR extension to create virtual outputs
- **Wayland**: Requires custom protocol extensions (limited)

#### 2. Screen Capture
- Captures framebuffer content using:
  - X11: Xlib/XCB libraries
  - Wayland: wlroots or custom capture methods

#### 3. Video Encoding
- H.264/AVC encoding for compression
- Hardware acceleration when available (VAAPI, VDPAU)
- Adaptive bitrate based on network conditions

#### 4. Network Transport
- **Video Stream**: UDP unicast/multicast on port 5900
- **Input Stream**: UDP on port 5901
- Custom protocol for low-latency transmission

#### 5. Input Processing
- Receives touch/keyboard/mouse events from clients
- Translates to system input using uinput/evdev
- Supports multi-touch gestures

### Protocol Details

#### Video Stream Protocol
```
Frame Header (12 bytes):
- Magic: 0x53504453 ('SPDS')
- Frame ID: uint32
- Timestamp: uint32
- Width: uint16
- Height: uint16
- Format: uint8 (0=JPEG, 1=H.264)

Frame Data: Variable length encoded data
```

#### Input Protocol
```
Input Header (8 bytes):
- Type: uint8 (0=mouse, 1=keyboard, 2=touch)
- Action: uint8 (0=down, 1=up, 2=move)
- X/Y coordinates: uint16 each
- Additional data: variable
```

## Troubleshooting

### Common Issues

#### Virtual Display Not Created
**Symptoms**: Server starts but no virtual monitor appears
**Solutions**:
- Ensure X11 is running: `echo $DISPLAY`
- Check xrandr availability: `xrandr --version`
- Load dummy kernel module: `sudo modprobe dummy`
- Restart X server after configuration changes

#### Network Connection Failed
**Symptoms**: Clients cannot connect to server
**Solutions**:
- Verify IP address: `ip addr show`
- Check firewall: `sudo ufw status`
- Test connectivity: `nc -u -z <IP> 5900`
- Ensure same network subnet

#### High Latency/Stuttering
**Symptoms**: Video stream is laggy or choppy
**Solutions**:
- Reduce resolution: `--width 1280 --height 720`
- Lower frame rate in code (modify fps variable)
- Use wired Ethernet instead of Wi-Fi
- Enable hardware encoding if available

#### Input Not Working
**Symptoms**: Touch/keyboard input not registering
**Solutions**:
- Check uinput permissions: `ls -l /dev/uinput`
- Run with sudo for input access
- Verify client app input settings

### Log Analysis

Server logs are available in:
- GUI: Server Log panel
- Terminal: Console output
- File: Redirect output to file for analysis

Common log messages:
- `Created virtual display VIRTUAL1`: Success
- `Failed to create virtual display`: Configuration issue
- `Client connected: 192.168.1.100:54321`: New connection
- `Screen capture failed`: Display access issue

### Performance Tuning

#### CPU Optimization
- Use hardware-accelerated encoding
- Reduce color depth if needed
- Limit frame rate for slower systems
- Adjust quality settings (lower for better performance)

#### Network Optimization
- Use 5GHz Wi-Fi for better bandwidth
- Reduce distance between devices
- Avoid network congestion
- Lower FPS for high-latency connections

#### Memory Usage
- Monitor with `top` or `htop`
- Adjust buffer sizes in code
- Close unused applications
- Lower resolution reduces memory usage

## Development

### Project Structure
```
linux-spacedesk/
├── main.py              # Command-line server
├── gui.py               # GUI application
├── requirements.txt     # Python dependencies
├── README.md           # Basic documentation
├── DOCS.md             # This file
└── .github/
    └── copilot-instructions.md
```

### Extending the Code

#### Adding New Features
1. Modify `LinuxSpacedeskServer` class in `main.py`
2. Update GUI in `gui.py` if needed
3. Add command-line options
4. Update documentation

#### Custom Display Integration
For custom display server support:
1. Implement `create_virtual_display()` method
2. Add screen capture logic
3. Update input handling

#### Protocol Extensions
To modify network protocol:
1. Update protocol definitions
2. Modify encoding/decoding functions
3. Ensure backward compatibility

### Building from Source

```bash
# Clone repository
git clone <repository-url>
cd linux-spacedesk

# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest

# Build distribution
python setup.py sdist bdist_wheel
```

## Security Considerations

### Network Security
- Only use on trusted local networks
- Avoid internet exposure
- Use VPN for remote access if needed

### Input Security
- Be aware of input injection risks
- Monitor connected clients
- Use authentication for production deployments

### Data Privacy
- Video stream contains screen content
- Ensure compliance with local privacy laws
- Use encryption for sensitive data

## License

This project is released under the MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure cross-platform compatibility

## Support

### Getting Help
- Check the troubleshooting section
- Review server logs for errors
- Test with minimal configuration

### Reporting Issues
When reporting bugs, include:
- Linux distribution and version
- Display server (X11/Wayland)
- Python version
- Full error logs
- Steps to reproduce

### Feature Requests
Feature requests should include:
- Use case description
- Technical requirements
- Implementation suggestions

## Changelog

### Version 1.0.0
- Initial release
- X11 virtual display support
- Basic UDP streaming
- Touch input handling
- GUI interface
- Command-line interface

## Roadmap

### Planned Features
- Full Wayland support
- Hardware acceleration optimization
- Advanced compression algorithms
- Multi-client support
- Audio streaming
- Security enhancements
- Mobile client applications

### Known Limitations
- Wayland virtual display creation
- High-resolution performance on low-end hardware
- Multi-monitor configurations
- Advanced input gestures

---

For more information, visit the project repository or contact the maintainers.