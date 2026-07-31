# Start Galaxy Tablet Virtual Monitor
glx() {
    ip -c -br a
    echo "Starting virtual monitor on port 5900..."
    krfb-virtualmonitor --name "GalaxyTablet" --resolution 1280x800 --password "123456" --port 5900 > /dev/null 2>&1 &
    echo "Monitor is running in the background."
}