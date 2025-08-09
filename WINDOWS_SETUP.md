# 🪟 Windows Setup Guide for Telecom KPI Dashboard

This guide provides comprehensive Windows-specific instructions for setting up the Telecom KPI Dashboard with proper security configuration.

## 📋 Prerequisites

### **Required Software**
- **Python 3.8+** - Download from [python.org](https://python.org)
- **Git** - Download from [git-scm.com](https://git-scm.com)
- **OpenRouter API Key** - Get from [openrouter.ai](https://openrouter.ai)

### **Optional (Recommended)**
- **Windows Terminal** - Modern terminal with better PowerShell support
- **VS Code** - Code editor with Python support
- **Docker Desktop** - For containerized deployment

## 🚀 Installation

### **1. Clone Repository**

**Command Prompt:**
```cmd
git clone <repository-url>
cd telecomdashboard
```

**PowerShell:**
```powershell
git clone <repository-url>
Set-Location telecomdashboard
```

### **2. Python Virtual Environment**

**Command Prompt:**
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (should show (venv) prefix)
echo %VIRTUAL_ENV%
```

**PowerShell:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# If execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verify activation
$env:VIRTUAL_ENV
```

### **3. Install Dependencies**

```cmd
# Install core dependencies
pip install -r requirements.txt

# Install security dependencies (recommended)
pip install -r requirements-security.txt

# Upgrade pip if needed
python -m pip install --upgrade pip
```

### **4. Database Setup**

```cmd
# Load data warehouse
python load_csv_data.py

# Verify database creation
dir data\telecom_db.sqlite
```

## 🔒 Security Configuration

### **Option A: Automated Setup (Recommended)**

```cmd
python setup_secure_environment.py
```

This will:
- Create `.env` file with proper API key management
- Set up security logging
- Configure file permissions (where possible)
- Create security checklist

### **Option B: Manual Setup**

#### **Environment Variables**

**Method 1: PowerShell Session (Temporary)**
```powershell
$env:LLM_API_KEY = "your-openrouter-api-key"
$env:SECURE_MODE = "true"
$env:DEBUG = "false"
```

**Method 2: System Environment Variables (Permanent)**
```powershell
# Run as Administrator
[Environment]::SetEnvironmentVariable("LLM_API_KEY", "your-api-key", "Machine")
[Environment]::SetEnvironmentVariable("SECURE_MODE", "true", "Machine")
[Environment]::SetEnvironmentVariable("DEBUG", "false", "Machine")

# Restart PowerShell after setting system variables
```

**Method 3: User Environment Variables**
```powershell
[Environment]::SetEnvironmentVariable("LLM_API_KEY", "your-api-key", "User")
[Environment]::SetEnvironmentVariable("SECURE_MODE", "true", "User")
```

**Method 4: GUI Method**
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Click "Environment Variables"
3. Under "User variables" or "System variables", click "New"
4. Add: `LLM_API_KEY` = `your-openrouter-api-key`

#### **File Permissions (Security)**

**PowerShell (Run as Administrator):**
```powershell
# Create logs directory
New-Item -ItemType Directory -Path logs -Force

# Set restrictive permissions on sensitive files
# Note: Windows permissions are more complex than Unix
# Use GUI for precise control

# Remove inheritance and set explicit permissions
$acl = Get-Acl "config.secrets.yaml"
$acl.SetAccessRuleProtection($true, $false)
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("$env:USERNAME", "FullControl", "Allow")
$acl.SetAccessRule($accessRule)
Set-Acl "config.secrets.yaml" $acl
```

**GUI Method (Recommended):**
1. Right-click `config.secrets.yaml` → Properties → Security → Advanced
2. Click "Disable inheritance" → "Remove all inherited permissions"
3. Click "Add" → "Select a principal" → Type your username → OK
4. Select "Full control" → OK
5. Repeat for `.env` and `data\telecom_db.sqlite`

## 🏃‍♂️ Running the Application

### **Development Mode**

**Command Prompt:**
```cmd
# Activate virtual environment
venv\Scripts\activate

# Set API key (if not in environment)
set LLM_API_KEY=your-api-key

# Run application
streamlit run app.py
```

**PowerShell:**
```powershell
# Activate virtual environment
venv\Scripts\Activate.ps1

# Set API key (if not in environment)
$env:LLM_API_KEY = "your-api-key"

# Run application
streamlit run app.py
```

### **Production Mode**

```powershell
# Set production environment
$env:LLM_API_KEY = "your-production-key"
$env:SECURE_MODE = "true"
$env:DEBUG = "false"

# Run with security options
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection true --server.maxUploadSize 10 --server.maxMessageSize 50
```

## 🔍 Security Validation

### **Run Security Checks**

```cmd
# Activate virtual environment
venv\Scripts\activate

# Run security linter
bandit -r . -x ./venv

# Check for vulnerabilities
safety check

# Verify no hardcoded keys
findstr /s /i "sk-or-v1" *.py *.yaml *.md
```

### **File Permission Verification**

```powershell
# Check file permissions
Get-Acl config.secrets.yaml | Format-List
Get-Acl .env | Format-List
Get-Acl data\telecom_db.sqlite | Format-List
```

## 🐳 Docker Setup (Alternative)

### **Prerequisites**
- Docker Desktop for Windows
- WSL2 (recommended)

### **Build and Run**

```cmd
# Create .env file with API key
echo LLM_API_KEY=your-api-key > .env

# Build Docker image
docker build -t telecom-dashboard .

# Run container
docker run -p 8501:8501 --env-file .env telecom-dashboard
```

### **Docker Compose**

```cmd
# Set environment variable
set LLM_API_KEY=your-api-key

# Run with compose
docker-compose up -d
```

## 🛠️ Troubleshooting

### **Common Issues**

#### **PowerShell Execution Policy**
```powershell
# If you get execution policy errors:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or temporarily bypass:
PowerShell -ExecutionPolicy Bypass -File script.ps1
```

#### **Python Not Found**
```cmd
# Check if Python is in PATH
python --version

# If not found, add Python to PATH:
# Control Panel → System → Advanced → Environment Variables
# Add Python installation directory to PATH
```

#### **Permission Denied Errors**
```powershell
# Run PowerShell as Administrator
Start-Process PowerShell -Verb RunAs

# Or use UAC bypass for specific operations
```

#### **Port Already in Use**
```cmd
# Find process using port 8501
netstat -ano | findstr :8501

# Kill process (replace PID with actual process ID)
taskkill /PID <process_id> /F

# Or use different port
streamlit run app.py --server.port 8502
```

### **Environment Variable Issues**

```powershell
# Check if environment variables are set
$env:LLM_API_KEY
Get-ChildItem Env: | Where-Object {$_.Name -like "*LLM*"}

# Refresh environment variables without restart
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
```

## 📚 Additional Resources

### **Windows-Specific Tools**
- **Windows Subsystem for Linux (WSL)** - For Unix-like environment
- **Windows Terminal** - Modern terminal with tabs and themes
- **PowerShell 7** - Cross-platform PowerShell
- **Chocolatey** - Package manager for Windows

### **Security Tools**
- **Windows Defender** - Built-in antivirus (whitelist project directory)
- **Windows Firewall** - Configure for Streamlit port
- **BitLocker** - Full disk encryption for laptops

### **Development Tools**
- **VS Code** - Code editor with Python extension
- **PyCharm** - Full-featured Python IDE
- **Git for Windows** - Git with Bash shell
- **Docker Desktop** - Container platform

## 🚀 Production Deployment on Windows Server

### **IIS Integration**
```xml
<!-- web.config for IIS -->
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="FastCgiModule" scriptProcessor="C:\Python\python.exe|C:\path\to\app.py" resourceType="Unspecified" />
    </handlers>
  </system.webServer>
</configuration>
```

### **Windows Service**
```powershell
# Install as Windows service using NSSM
nssm install TelecomDashboard "C:\Python\Scripts\streamlit.exe"
nssm set TelecomDashboard Parameters "run C:\path\to\app.py"
nssm set TelecomDashboard Start SERVICE_AUTO_START
nssm start TelecomDashboard
```

---

*For additional support, refer to the main README.md or SECURITY.md documentation.*
