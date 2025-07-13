# 📱 AI Hedge Fund - Mobile Access Guide

## 🚨 Issue: Mobile Links Not Working

**Problem**: The links `http://172.30.0.2:5000/` are not accessible from your mobile device because:
- `172.30.0.2` is a private IP address only accessible within the server's network
- Your mobile device is on a different network (cellular/WiFi)
- Firewall/security groups are blocking external access

## 📱 MOBILE ACCESS SOLUTIONS

### 🔥 SOLUTION 1: Same WiFi Network (Easiest)

**If your mobile device can connect to the same WiFi network as the server:**

1. **Connect your mobile device to the same WiFi network**
2. **Try these mobile-optimized URLs:**
   - `http://172.30.0.2:8080/mobile.html`
   - `http://172.17.0.1:8080/mobile.html`

### 🌐 SOLUTION 2: Tunnel Service (Recommended)

**Use a tunnel service to create a public URL:**

#### Option A: Using ngrok (Most Popular)
```bash
# Install ngrok from https://ngrok.com/
# Then run:
ngrok http 8080
```
This will give you a public URL like: `https://abc123.ngrok.io`

#### Option B: Using localtunnel
```bash
# Install: npm install -g localtunnel
# Then run:
lt --port 8080
```

#### Option C: Using serveo (No installation)
```bash
ssh -R 80:localhost:8080 serveo.net
```

### 📡 SOLUTION 3: Port Forwarding (Advanced)

**If you control the router/network:**

1. **Access your router's admin panel**
2. **Set up port forwarding:**
   - External port: 8080
   - Internal IP: 172.30.0.2
   - Internal port: 8080
3. **Use external IP:** `http://54.201.15.58:8080/mobile.html`

### 🔐 SOLUTION 4: SSH Tunnel (Advanced)

**If you have SSH access:**

```bash
# From your mobile device (using SSH client app):
ssh -L 8080:localhost:8080 user@54.201.15.58

# Then access: http://localhost:8080/mobile.html
```

### 💻 SOLUTION 5: Use Desktop/Laptop

**Access from computer browser:**
- `http://172.30.0.2:5000/` (Full interface)
- `http://172.30.0.2:5000/testpage` (Test page)

## 🎯 IMMEDIATE ACTIONS

### Step 1: Test Mobile-Optimized Server
I've started a mobile-optimized server on port 8080. Try these URLs:

#### If on same network:
- `http://172.30.0.2:8080/mobile.html`
- `http://172.17.0.1:8080/mobile.html`

#### If different network:
- Set up ngrok or tunnel service (see Solution 2)

### Step 2: Verify Server Status
```bash
# Check if mobile server is running
curl http://172.30.0.2:8080/mobile.html | head -5
```

### Step 3: Create Tunnel (Recommended)
```bash
# Install ngrok from https://ngrok.com/
ngrok http 8080

# Or use serveo (no installation):
ssh -R 80:localhost:8080 serveo.net
```

## 📊 Quick Command Line Alternative

**If web interface still doesn't work, use command line:**

```bash
# Run hedge fund analysis
export PATH="/home/ubuntu/.local/bin:$PATH"
poetry run python src/main.py --ticker AAPL,MSFT,NVDA

# Run backtesting
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

## 🔧 Troubleshooting

### Mobile Browser Issues:
1. **Clear browser cache** or use incognito mode
2. **Try different browsers** (Chrome, Firefox, Safari)
3. **Check WiFi connection** - make sure you're on the same network
4. **Disable VPN** if using one

### Network Issues:
1. **Check if server is running:**
   ```bash
   curl http://172.30.0.2:8080/mobile.html
   ```

2. **Restart mobile server:**
   ```bash
   python3 mobile_access.py
   ```

3. **Check firewall/security groups** if on cloud server

## 📞 Support URLs

### Test URLs to Try:
- **Mobile Interface**: `http://172.30.0.2:8080/mobile.html`
- **API Test**: `http://172.30.0.2:5000/test`
- **Main Interface**: `http://172.30.0.2:5000/`

### QR Code Access:
A QR code has been generated in the terminal for easy mobile access. Scan it with your mobile device.

## ⚡ Quick Setup Commands

```bash
# Start mobile-optimized server
python3 mobile_access.py

# Start tunnel (choose one):
ngrok http 8080
# OR
ssh -R 80:localhost:8080 serveo.net

# Test locally
curl http://localhost:8080/mobile.html
```

## 📋 Checklist

- [ ] Mobile device on same WiFi network
- [ ] Mobile server running on port 8080
- [ ] Tunnel service configured (if needed)
- [ ] Browser cache cleared
- [ ] Firewall/security groups allow access
- [ ] API keys configured in .env file

## 🆘 If Nothing Works

**Use the command line interface:**
```bash
# Quick analysis
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --show-reasoning

# Quick backtest
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

---

**The mobile access solutions are now running! Try the URLs above or set up a tunnel service for external access.**