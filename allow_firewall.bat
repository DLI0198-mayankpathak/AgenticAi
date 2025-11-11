@echo off
echo Adding firewall rule for port 8000...
netsh advfirewall firewall add rule name="Python API Server" dir=in action=allow protocol=TCP localport=8000
echo Done! Port 8000 is now allowed through Windows Firewall.
pause
