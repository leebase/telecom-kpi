#!/usr/bin/env python3
"""
Secure Environment Setup Script
Configures the application for secure production deployment
"""

import os
import sys
import secrets
import subprocess
from pathlib import Path

def generate_secure_api_key():
    """Generate a secure random API key for development"""
    return secrets.token_urlsafe(32)

def setup_environment_file():
    """Create a secure .env file with required environment variables"""
    env_file = Path('.env')
    
    if env_file.exists():
        print("⚠️  .env file already exists. Backup your existing file before proceeding.")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            return False
    
    print("🔧 Setting up secure environment variables...")
    
    # Get API key from user or generate placeholder
    api_key = input("Enter your OpenRouter API key (or press Enter to use placeholder): ").strip()
    if not api_key:
        api_key = "REPLACE_WITH_YOUR_ACTUAL_API_KEY"
        print("⚠️  Using placeholder API key. Replace with your actual key.")
    
    env_content = f"""# Telecom Dashboard Environment Variables
# DO NOT COMMIT THIS FILE TO VERSION CONTROL

# LLM Configuration
LLM_PROVIDER=openrouter
LLM_API_KEY={api_key}
LLM_MODEL=google/gemini-2.5-flash
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
LLM_API_BASE=https://openrouter.ai/api/v1

# Security Configuration
SECURE_MODE=true
LOG_LEVEL=INFO

# Database Configuration
DB_PATH=data/telecom_db.sqlite
DB_TIMEOUT=30000

# Application Configuration
APP_NAME=Telecom KPI Dashboard
APP_VERSION=2.2.0
DEBUG=false
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Environment file created: {env_file}")
    return True

def setup_gitignore():
    """Ensure sensitive files are in .gitignore"""
    gitignore_file = Path('.gitignore')
    
    sensitive_patterns = [
        '.env',
        'config.secrets.yaml',
        '*.log',
        'security.log',
        '__pycache__/',
        '*.pyc',
        '.venv/',
        'venv/',
        '.DS_Store'
    ]
    
    existing_patterns = set()
    if gitignore_file.exists():
        with open(gitignore_file, 'r') as f:
            existing_patterns = set(line.strip() for line in f if line.strip() and not line.startswith('#'))
    
    new_patterns = [pattern for pattern in sensitive_patterns if pattern not in existing_patterns]
    
    if new_patterns:
        with open(gitignore_file, 'a') as f:
            f.write('\n# Security - Sensitive files\n')
            for pattern in new_patterns:
                f.write(f'{pattern}\n')
        
        print(f"✅ Updated .gitignore with {len(new_patterns)} security patterns")
    else:
        print("✅ .gitignore already contains security patterns")

def setup_security_logging():
    """Setup security logging directory"""
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    # Create empty security log file with proper permissions
    security_log = logs_dir / 'security.log'
    security_log.touch()
    
    # Set restrictive permissions (owner read/write only)
    if os.name != 'nt':  # Not Windows
        os.chmod(security_log, 0o600)
    
    print(f"✅ Security logging setup: {security_log}")

def install_security_dependencies():
    """Install additional security dependencies"""
    security_packages = [
        'cryptography>=3.4.8',
        'bcrypt>=3.2.0',
        'python-dotenv>=0.19.0'
    ]
    
    print("📦 Installing security dependencies...")
    
    for package in security_packages:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         check=True, capture_output=True)
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")

def validate_file_permissions():
    """Validate and set secure file permissions"""
    sensitive_files = [
        'config.secrets.yaml',
        '.env',
        'data/telecom_db.sqlite'
    ]
    
    print("🔒 Setting secure file permissions...")
    
    for file_path in sensitive_files:
        path = Path(file_path)
        if path.exists():
            if os.name != 'nt':  # Not Windows
                # Set to owner read/write only
                os.chmod(path, 0o600)
                print(f"✅ Secured {file_path}")
            else:
                print(f"ℹ️  Windows detected - manual permission review recommended for {file_path}")

def create_security_checklist():
    """Create a security checklist for deployment"""
    checklist = """
# 🔒 Security Deployment Checklist

## Pre-deployment Security Checklist

### Environment & Configuration
- [ ] Environment variables configured (not hardcoded)
- [ ] API keys stored securely (not in code)
- [ ] .env file not committed to version control
- [ ] config.secrets.yaml not committed to version control
- [ ] Database file permissions set to 600 (owner only)

### Application Security
- [ ] Input validation enabled on all user inputs
- [ ] SQL injection prevention implemented
- [ ] XSS protection enabled
- [ ] Rate limiting configured
- [ ] Security logging enabled
- [ ] Error messages don't expose sensitive information

### Network Security
- [ ] HTTPS enabled in production
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Database access restricted to application only

### Monitoring & Logging
- [ ] Security events logged
- [ ] Log files secured with proper permissions
- [ ] Monitoring for suspicious activity
- [ ] Regular security log review process

### Data Protection
- [ ] Sensitive data not logged
- [ ] Database backups secured
- [ ] Data retention policies implemented
- [ ] User data properly anonymized where needed

## Production Deployment Commands

```bash
# Set environment variables
export LLM_API_KEY="your-actual-api-key"
export SECURE_MODE=true
export DEBUG=false

# Run with security
python setup_secure_environment.py
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection true
```

## Emergency Response
- Incident response plan documented
- Security contact information available
- API key rotation procedure ready
- Database backup and recovery tested
"""
    
    with open('SECURITY_CHECKLIST.md', 'w') as f:
        f.write(checklist)
    
    print("✅ Security checklist created: SECURITY_CHECKLIST.md")

def main():
    """Main setup function"""
    print("🚀 Starting secure environment setup...")
    
    try:
        setup_environment_file()
        setup_gitignore()
        setup_security_logging()
        install_security_dependencies()
        validate_file_permissions()
        create_security_checklist()
        
        print("\n✅ Secure environment setup completed!")
        print("\n📋 Next steps:")
        print("1. Review and update .env file with your actual API keys")
        print("2. Review SECURITY_CHECKLIST.md before deployment")
        print("3. Test the application in secure mode")
        print("4. Never commit .env or config.secrets.yaml files")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
