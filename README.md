# Linux Spacedesk Clone

A clone of spacedesk that allows Linux systems to use mobile devices as secondary monitors over local network or Wi-Fi.

## Features

- Compatible with X11 display server (Wayland support limited)
- Low-latency video streaming using H.264 encoding
- Touch and keyboard input from mobile devices
- Local network and Wi-Fi support
- Virtual display creation for seamless desktop extension

## Requirements

- Linux with X11 (recommended) or Wayland
- Python 3.6+
- Required Python packages (install with `pip install -r requirements.txt`)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Server (Linux)

Run the server on your Linux machine:

```bash
python main.py --host 0.0.0.0 --port 5900 --display X11 --width 1920 --height 1080
```

### Client (Mobile Device)

For mobile clients, you would need a companion app that connects to the server. This implementation provides the server-side functionality. For a complete spacedesk clone, you would need to develop or use compatible mobile apps.

The server listens on UDP port 5900 for video streaming and 5901 for input.

## Configuration

- `--host`: IP address to bind to (0.0.0.0 for all interfaces)
- `--port`: Base port for connections
- `--display`: Display server type (X11 or Wayland)
- `--width/--height`: Resolution of the virtual display

## How It Works

1. **Virtual Display Creation**: Creates a virtual monitor using X11 RandR extension
2. **Screen Capture**: Captures the content of the virtual display
3. **Video Encoding**: Compresses frames using H.264 for efficient transmission
4. **Network Streaming**: Sends encoded video over UDP to connected clients
5. **Input Handling**: Receives touch/keyboard input from clients and injects into the system

## Limitations

- Wayland support is experimental and may require additional setup
- Virtual display creation requires proper X11 configuration
- Mobile client apps need to be developed separately or use compatible existing apps
- Performance depends on hardware encoding capabilities

## Troubleshooting

- Ensure X11 is running and xrandr is available
- Check firewall settings for UDP ports 5900-5901
- For virtual display issues, you may need to load kernel modules like `dummy` or `vboxvideo`
- On Wayland, consider switching to X11 session or using wlroots-based solutions

## License

This project is a proof-of-concept implementation. Check individual library licenses for usage restrictions.