# 🍎 Mac Setup Guide for Telecom KPI Dashboard

This guide provides comprehensive macOS-specific instructions for setting up the Telecom KPI Dashboard with proper security configuration.

## 📋 Prerequisites

### **Required Software**
- **Python 3.8+** - Install via Homebrew or [python.org](https://python.org)
- **Git** - Pre-installed on macOS or via Xcode Command Line Tools
- **OpenRouter API Key** - Get from [openrouter.ai](https://openrouter.ai)

### **Install Xcode Command Line Tools**
```bash
xcode-select --install
```

### **Install Homebrew (Recommended)**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### **Install Python via Homebrew**
```bash
brew install python@3.11
brew install git
```

## 🚀 Installation

### **1. Clone Repository**

```bash
git clone <repository-url>
cd telecomdashboard
```

### **2. Python Virtual Environment**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show (venv) prefix)
which python
```

### **3. Install Dependencies**

```bash
# Install core dependencies
pip install -r requirements.txt

# Install security dependencies (recommended)
pip install -r requirements-security.txt

# Upgrade pip if needed
pip install --upgrade pip
```

### **4. Database Setup**

```bash
# Load data warehouse
python load_csv_data.py

# Verify database creation
ls -la data/telecom_db.sqlite
```

## 🔒 Security Configuration

### **Option A: Automated Setup (Recommended)**

```bash
python setup_secure_environment.py
```

This will:
- Create `.env` file with proper API key management
- Set up security logging with proper permissions
- Configure file permissions (600/700)
- Create security checklist

### **Option B: Manual Setup**

#### **Environment Variables**

**Method 1: Session Variables (Temporary)**
```bash
export LLM_API_KEY="your-openrouter-api-key"
export SECURE_MODE=true
export DEBUG=false
```

**Method 2: Shell Profile (Permanent)**

For **Zsh** (default on macOS Catalina+):
```bash
echo 'export LLM_API_KEY="your-api-key"' >> ~/.zshrc
echo 'export SECURE_MODE=true' >> ~/.zshrc
echo 'export DEBUG=false' >> ~/.zshrc
source ~/.zshrc
```

For **Bash**:
```bash
echo 'export LLM_API_KEY="your-api-key"' >> ~/.bash_profile
echo 'export SECURE_MODE=true' >> ~/.bash_profile
echo 'export DEBUG=false' >> ~/.bash_profile
source ~/.bash_profile
```

**Method 3: Environment File**
```bash
# Create .env file
cat > .env << EOF
LLM_API_KEY=your-openrouter-api-key
SECURE_MODE=true
DEBUG=false
EOF

# Secure the file
chmod 600 .env
```

#### **File Permissions (Security)**

```bash
# Create logs directory with secure permissions
mkdir -p logs
chmod 700 logs

# Set restrictive permissions on sensitive files
chmod 600 config.secrets.yaml
chmod 600 .env
chmod 600 data/telecom_db.sqlite

# Verify permissions
ls -la config.secrets.yaml .env data/telecom_db.sqlite logs/
```

#### **Advanced Security (Optional)**

```bash
# Set extended attributes for additional protection
xattr -w com.apple.metadata:_kMDItemUserTags "Secure" config.secrets.yaml
xattr -w com.apple.metadata:_kMDItemUserTags "Secure" .env

# Use FileVault for full disk encryption (System Preferences)
# Enable Firewall (System Preferences → Security & Privacy → Firewall)

# Restrict network access to localhost only
sudo pfctl -f /etc/pf.conf  # Configure if needed
```

## 🏃‍♂️ Running the Application

### **Development Mode**

```bash
# Activate virtual environment
source venv/bin/activate

# Set API key (if not in environment)
export LLM_API_KEY="your-api-key"

# Run application
streamlit run app.py
```

### **Production Mode**

```bash
# Set production environment
export LLM_API_KEY="your-production-key"
export SECURE_MODE=true
export DEBUG=false

# Run with security options
streamlit run app.py \
  --server.enableCORS false \
  --server.enableXsrfProtection true \
  --server.maxUploadSize 10 \
  --server.maxMessageSize 50 \
  --server.address 127.0.0.1 \
  --server.port 8501
```

### **Background Service (Production)**

**Using launchd (macOS Service Manager):**

Create service file:
```bash
sudo tee /Library/LaunchDaemons/com.telecom.dashboard.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.telecom.dashboard</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/streamlit</string>
        <string>run</string>
        <string>/path/to/telecomdashboard/app.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/telecomdashboard</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>LLM_API_KEY</key>
        <string>your-api-key</string>
        <key>SECURE_MODE</key>
        <string>true</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load and start service
sudo launchctl load /Library/LaunchDaemons/com.telecom.dashboard.plist
sudo launchctl start com.telecom.dashboard
```

## 🔍 Security Validation

### **Run Security Checks**

```bash
# Activate virtual environment
source venv/bin/activate

# Run security linter
bandit -r . -x ./venv

# Check for vulnerabilities
safety check  # or safety scan

# Verify no hardcoded keys
grep -r "sk-or-v1" . --exclude-dir=venv --exclude=".env"

# Check file permissions
ls -la config.secrets.yaml .env data/telecom_db.sqlite
stat -f "%Sp %N" config.secrets.yaml .env data/telecom_db.sqlite
```

### **Network Security**

```bash
# Check listening ports
lsof -i :8501

# Monitor network connections
netstat -an | grep 8501

# Check firewall status
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```

## 🐳 Docker Setup (Alternative)

### **Install Docker Desktop**
Download from [docker.com](https://docker.com) or via Homebrew:
```bash
brew install --cask docker
```

### **Build and Run**

```bash
# Create .env file with API key
echo "LLM_API_KEY=your-api-key" > .env

# Build Docker image
docker build -t telecom-dashboard .

# Run container
docker run -p 8501:8501 --env-file .env telecom-dashboard
```

### **Docker Compose**

```bash
# Set environment variable
export LLM_API_KEY="your-api-key"

# Run with compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

## 🛠️ Troubleshooting

### **Common Issues**

#### **Python Version Conflicts**
```bash
# Check Python versions
python3 --version
which python3

# Use specific Python version
python3.11 -m venv venv

# Update PATH if needed
export PATH="/usr/local/bin:$PATH"
```

#### **Permission Denied Errors**
```bash
# Fix ownership
sudo chown -R $(whoami) .

# Fix permissions
chmod 755 .
chmod 600 config.secrets.yaml .env
chmod 644 *.py *.md *.txt
```

#### **Port Already in Use**
```bash
# Find process using port 8501
lsof -i :8501

# Kill process (replace PID with actual process ID)
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

#### **SSL Certificate Issues**
```bash
# Update certificates
/Applications/Python\ 3.x/Install\ Certificates.command

# Or install certificates via pip
pip install --upgrade certifi
```

### **Environment Variable Issues**

```bash
# Check environment variables
echo $LLM_API_KEY
env | grep LLM

# Debug shell profile loading
echo $SHELL
source ~/.zshrc  # or ~/.bash_profile
```

### **Homebrew Issues**

```bash
# Update Homebrew
brew update && brew upgrade

# Fix permissions
sudo chown -R $(whoami) $(brew --prefix)/*

# Reinstall Python if needed
brew reinstall python@3.11
```

## 📚 macOS-Specific Tools

### **Development Tools**
```bash
# Install via Homebrew
brew install --cask visual-studio-code
brew install --cask pycharm-ce
brew install --cask docker
brew install tree htop
```

### **Security Tools**
```bash
# Install security tools
brew install nmap
brew install wireshark
brew install gpg

# System security
# Enable FileVault: System Preferences → Security & Privacy → FileVault
# Enable Firewall: System Preferences → Security & Privacy → Firewall
# Enable Gatekeeper: System Preferences → Security & Privacy → General
```

### **Terminal Enhancements**
```bash
# Install iTerm2
brew install --cask iterm2

# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install useful terminal tools
brew install zsh-autosuggestions
brew install zsh-syntax-highlighting
```

## 🚀 Production Deployment

### **Using nginx (Reverse Proxy)**

Install nginx:
```bash
brew install nginx
```

Configure nginx:
```bash
sudo tee /usr/local/etc/nginx/sites-available/telecom-dashboard << EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /usr/local/etc/nginx/sites-available/telecom-dashboard /usr/local/etc/nginx/sites-enabled/

# Start nginx
sudo brew services start nginx
```

### **SSL/TLS with Let's Encrypt**
```bash
# Install certbot
brew install certbot

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renew
echo "0 12 * * * /usr/local/bin/certbot renew --quiet" | sudo crontab -
```

### **Process Management**
```bash
# Using pm2 (Node.js process manager)
npm install -g pm2

# Create ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'telecom-dashboard',
    script: 'streamlit',
    args: 'run app.py --server.port 8501',
    cwd: '/path/to/telecomdashboard',
    env: {
      LLM_API_KEY: 'your-api-key',
      SECURE_MODE: 'true'
    }
  }]
}
EOF

# Start with pm2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 🔐 Advanced Security

### **Code Signing (for distribution)**
```bash
# Create developer certificate in Keychain Access
# Sign the application
codesign --force --verify --verbose --sign "Developer ID Application: Your Name" app.py

# Verify signature
codesign --verify --deep --strict --verbose=2 app.py
```

### **Sandboxing**
```bash
# Run in sandbox (limited permissions)
sandbox-exec -f /usr/share/sandbox/generic.sb streamlit run app.py
```

### **System Integrity Protection (SIP)**
```bash
# Check SIP status
csrutil status

# SIP provides protection against system modification
# Keep enabled in production environments
```

---

*For additional support, refer to the main README.md or SECURITY.md documentation.*
