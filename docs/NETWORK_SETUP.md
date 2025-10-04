# Network Setup Guide

This guide explains how to access your Military Hierarchy System from other devices on your local WiFi network.

## Your Network Configuration

- **Local IP Address**: `10.3.35.27`
- **Network Access**: All services are now configured to accept connections from any device on your local network

## Services and Ports

| Service | Local Access | Network Access | Port |
|---------|-------------|----------------|------|
| Backend API | http://localhost:8000 | http://10.3.35.27:8000 | 8000 |
| Main Dashboard | http://localhost:3000 | http://10.3.35.27:3000 | 3000 |
| Reports UI | http://localhost:3001 | http://10.3.35.27:3001 | 3001 |

## How to Access from Other Devices

### From Mobile Devices (Phone/Tablet)
1. Connect your device to the same WiFi network
2. Open a web browser
3. Navigate to one of these URLs:
   - **Main Dashboard**: http://10.3.35.27:3000
   - **Reports UI**: http://10.3.35.27:3001
   - **API Documentation**: http://10.3.35.27:8000/docs

### From Other Computers
1. Connect to the same WiFi network
2. Open a web browser
3. Use the same URLs as above

## Starting the System

### Option 1: Use the Batch Script (Recommended)
```bash
start_all.bat
```

This will start all services and display the network URLs.

### Option 2: Manual Start
1. **Start Backend**:
   ```bash
   python backend.py
   ```

2. **Start Main Dashboard**:
   ```bash
   cd mil_dashboard
   npm run dev
   ```

3. **Start Reports UI**:
   ```bash
   cd ui-for-reports/frontend
   npm run dev
   ```

## Testing Network Access

Run the network test script to verify all services are accessible:

```bash
python test_network_access.py
```

This will test all services and report their accessibility status.

## Troubleshooting

### Services Not Accessible from Other Devices

1. **Check Windows Firewall**:
   - Open Windows Defender Firewall
   - Allow Python and Node.js through the firewall
   - Or temporarily disable firewall for testing

2. **Verify IP Address**:
   - Run `ipconfig` to confirm your IP address
   - Update the IP in `test_network_access.py` if it changed

3. **Check Network Connection**:
   - Ensure all devices are on the same WiFi network
   - Try pinging the host machine: `ping 10.3.35.27`

4. **Port Conflicts**:
   - Make sure no other applications are using ports 3000, 3001, or 8000
   - Check with: `netstat -an | findstr "3000\|3001\|8000"`

### Services Not Starting

1. **Backend Issues**:
   - Check if Python virtual environment is activated
   - Verify database exists: `python database_setup.py`

2. **Frontend Issues**:
   - Install dependencies: `npm install` in each frontend directory
   - Check Node.js version compatibility

## Security Notes

⚠️ **Important**: This setup exposes your services to your local network. 

- Only use this configuration on trusted networks
- For production use, implement proper authentication and HTTPS
- Consider using a reverse proxy (nginx) for better security

## API Endpoints

The backend API is accessible at `http://10.3.35.27:8000` with these main endpoints:

- `GET /` - System status
- `GET /units` - List all military units
- `GET /soldiers` - List all soldiers
- `GET /hierarchy` - Complete military hierarchy
- `GET /reports` - List all reports
- `GET /docs` - Interactive API documentation

## Next Steps

1. Start the system using `start_all.bat`
2. Test network access with `python test_network_access.py`
3. Access the dashboard from your mobile device
4. Share the network URLs with team members on the same WiFi

---

**Need Help?** Check the console output when starting services for any error messages.
