# 🔧 AI Hedge Fund Web Interface - Troubleshooting Guide

## 🎯 Quick Test Links

If you're seeing blank pages, try these test links first:

### Primary Flask Server (Port 5000)
- **Test Page**: `http://172.30.0.2:5000/testpage`
- **API Test**: `http://172.30.0.2:5000/test`
- **Main Interface**: `http://172.30.0.2:5000/`

### Backup Simple Server (Port 8000)
- **Test Page**: `http://172.30.0.2:8000/`

## 🚨 Common Issues & Solutions

### Issue 1: Blank White Pages
**Symptoms**: Browser shows blank/white pages when accessing the links
**Solutions**:
1. **Clear Browser Cache**: Press `Ctrl+F5` (Windows/Linux) or `Cmd+Shift+R` (Mac)
2. **Try Incognito/Private Mode**: Open the link in a private browsing window
3. **Disable Browser Extensions**: Some ad blockers or extensions can block content
4. **Try Different Browser**: Test with Chrome, Firefox, or Safari

### Issue 2: "Site Can't Be Reached" Error
**Symptoms**: `ERR_CONNECTION_ABORTED` or similar network errors
**Solutions**:
1. **Check Server Status**: Visit `http://172.30.0.2:5000/test` for a simple JSON response
2. **Try Alternative URLs**:
   - `http://127.0.0.1:5000/`
   - `http://localhost:5000/`
3. **Restart the Server**: Run `./start_web.sh` or `poetry run python app.py`

### Issue 3: API Key Issues
**Symptoms**: Server starts but AI functionality doesn't work
**Solutions**:
1. **Add Your OpenAI API Key** to the `.env` file:
   ```bash
   # Edit .env file
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   ```
2. **Restart the Server** after updating the API key

## 🧪 Testing Steps

### Step 1: Basic Connectivity Test
```bash
curl http://172.30.0.2:5000/test
```
**Expected Response**: JSON with status "success"

### Step 2: HTML Content Test
```bash
curl http://172.30.0.2:5000/testpage | head -5
```
**Expected Response**: HTML with DOCTYPE declaration

### Step 3: Browser Test
1. Open: `http://172.30.0.2:5000/testpage`
2. **Expected**: Colorful test page with "AI Hedge Fund" title
3. **If working**: Click "Main Interface" to access the full app

## 🔄 Server Management

### Start the Flask Server
```bash
# Method 1: Using startup script
./start_web.sh

# Method 2: Direct command
poetry run python app.py
```

### Start the Backup Server
```bash
python3 simple_server.py
```

### Stop All Servers
```bash
pkill -f "python app.py"
pkill -f "simple_server.py"
```

### Check Running Servers
```bash
# Check if processes are running
ps aux | grep python | grep -E "(app.py|simple_server.py)"

# Test connectivity
curl http://172.30.0.2:5000/test
curl http://172.30.0.2:8000/
```

## 🌐 Network Configuration

### Available Interfaces
The servers bind to `0.0.0.0:5000` and `0.0.0.0:8000`, making them accessible via:
- `http://172.30.0.2:5000/` (External IP)
- `http://127.0.0.1:5000/` (Localhost)
- `http://localhost:5000/` (Localhost alias)

### Firewall/Network Issues
If you can curl but browser doesn't work:
1. Check if there's a firewall blocking the browser
2. Try accessing from the same machine as the server
3. Check if your network has proxy settings that might interfere

## 📋 Verification Checklist

- [ ] Server is running (check with `curl http://172.30.0.2:5000/test`)
- [ ] Test page loads (`http://172.30.0.2:5000/testpage`)
- [ ] Browser cache is cleared
- [ ] Tried incognito/private mode
- [ ] OpenAI API key is set in `.env` file
- [ ] Dependencies are installed (`poetry install`)

## 🆘 If Nothing Works

### Emergency Backup: Command Line Interface
```bash
# Run the hedge fund analysis directly
poetry run python src/main.py --ticker AAPL,MSFT,NVDA

# Run backtesting
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

### Get Help
1. **Check Server Logs**: Look at the terminal where you started the server
2. **Browser Developer Tools**: Press F12 and check Console/Network tabs for errors
3. **Network Test**: Try `ping 172.30.0.2` to verify network connectivity

## 🔧 Advanced Debugging

### Check Server Logs
```bash
# Start server with verbose logging
export FLASK_DEBUG=1
poetry run python app.py
```

### Browser Developer Tools
1. Press `F12` to open developer tools
2. Go to **Console** tab - look for JavaScript errors
3. Go to **Network** tab - check if requests are being made
4. Check if there are any failed resource loads

### Alternative Port
If port 5000 is blocked, edit `app.py` and change:
```python
app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
```

## ✅ Success Indicators

**Working Correctly When**:
- `http://172.30.0.2:5000/test` returns JSON
- `http://172.30.0.2:5000/testpage` shows a colorful page
- `http://172.30.0.2:5000/` shows the full AI Hedge Fund interface
- Analysis and backtesting functions work through the web interface