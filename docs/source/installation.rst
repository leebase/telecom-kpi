============
Installation
============

This guide covers the installation and setup of the Telecom KPI Dashboard for different environments and platforms.

System Requirements
===================

**Minimum Requirements:**

* Python 3.8 or higher
* 4GB RAM
* 2GB free disk space
* Internet connection (for AI insights)

**Recommended Requirements:**

* Python 3.10 or higher
* 8GB RAM
* 10GB free disk space
* SSD storage for better performance

**Supported Platforms:**

* macOS 10.14+
* Windows 10/11
* Linux (Ubuntu 18.04+, CentOS 7+, RHEL 8+)

Quick Installation
==================

**1. Clone the Repository**

.. code-block:: bash

   git clone https://github.com/yourorg/telecom-dashboard.git
   cd telecom-dashboard

**2. Create Virtual Environment**

.. code-block:: bash

   # Using venv (recommended)
   python -m venv venv
   
   # Activate on macOS/Linux
   source venv/bin/activate
   
   # Activate on Windows
   venv\Scripts\activate

**3. Install Dependencies**

.. code-block:: bash

   # Install core dependencies
   pip install -r requirements.txt
   
   # Install security dependencies
   pip install -r requirements-security.txt
   
   # Install development dependencies (optional)
   pip install -r requirements-dev.txt

**4. Set Up Environment**

.. code-block:: bash

   # Set your LLM API key
   export LLM_API_KEY="your-openrouter-api-key"
   
   # Or create a .env file
   echo "LLM_API_KEY=your-openrouter-api-key" > .env

**5. Run the Application**

.. code-block:: bash

   streamlit run app.py

**6. Access the Dashboard**

Open your browser and navigate to:

* Local: http://localhost:8501
* Network: http://your-ip:8501

Detailed Platform Setup
=======================

macOS Installation
------------------

**Prerequisites:**

.. code-block:: bash

   # Install Homebrew (if not already installed)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python
   brew install python@3.10
   
   # Install Git
   brew install git

**Complete Setup:**

.. code-block:: bash

   # Clone repository
   git clone https://github.com/yourorg/telecom-dashboard.git
   cd telecom-dashboard
   
   # Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Upgrade pip
   pip install --upgrade pip
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-security.txt
   
   # Set secure file permissions
   chmod 600 config.secrets.yaml
   chmod 755 setup_secure_environment.py
   
   # Run security setup
   python setup_secure_environment.py
   
   # Start the application
   export LLM_API_KEY="your-api-key"
   streamlit run app.py

Windows Installation
--------------------

**Prerequisites:**

1. Download Python 3.10+ from `python.org <https://www.python.org/downloads/>`_
2. Install Git from `git-scm.com <https://git-scm.com/download/win>`_
3. Install Visual Studio Build Tools (for some dependencies)

**PowerShell Setup:**

.. code-block:: powershell

   # Clone repository
   git clone https://github.com/yourorg/telecom-dashboard.git
   cd telecom-dashboard
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   .\venv\Scripts\Activate.ps1
   
   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -r requirements-security.txt
   
   # Set environment variable
   $env:LLM_API_KEY="your-api-key"
   
   # Run application
   streamlit run app.py

**Command Prompt Setup:**

.. code-block:: cmd

   REM Clone repository
   git clone https://github.com/yourorg/telecom-dashboard.git
   cd telecom-dashboard
   
   REM Create virtual environment
   python -m venv venv
   
   REM Activate virtual environment
   venv\Scripts\activate.bat
   
   REM Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -r requirements-security.txt
   
   REM Set environment variable
   set LLM_API_KEY=your-api-key
   
   REM Run application
   streamlit run app.py

Linux Installation
------------------

**Ubuntu/Debian:**

.. code-block:: bash

   # Update package lists
   sudo apt update
   
   # Install Python and dependencies
   sudo apt install python3.10 python3.10-venv python3-pip git
   
   # Clone repository
   git clone https://github.com/yourorg/telecom-dashboard.git
   cd telecom-dashboard
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -r requirements-security.txt
   
   # Set permissions
   chmod 600 config.secrets.yaml
   chmod +x setup_secure_environment.py
   
   # Run setup
   python setup_secure_environment.py
   
   # Set environment variable
   export LLM_API_KEY="your-api-key"
   
   # Run application
   streamlit run app.py

**CentOS/RHEL:**

.. code-block:: bash

   # Enable EPEL repository
   sudo yum install epel-release
   
   # Install Python and Git
   sudo yum install python3 python3-pip git
   
   # Continue with standard Linux setup...

Docker Installation
===================

**Using Docker Compose:**

.. code-block:: yaml

   # docker-compose.yml
   version: '3.8'
   
   services:
     telecom-dashboard:
       build: .
       ports:
         - "8501:8501"
       environment:
         - LLM_API_KEY=${LLM_API_KEY}
       volumes:
         - ./data:/app/data
         - ./config:/app/config
         - ./logs:/app/logs

**Build and Run:**

.. code-block:: bash

   # Build container
   docker-compose build
   
   # Run with environment file
   echo "LLM_API_KEY=your-api-key" > .env
   docker-compose up -d

**Direct Docker:**

.. code-block:: bash

   # Build image
   docker build -t telecom-dashboard .
   
   # Run container
   docker run -d \
     -p 8501:8501 \
     -e LLM_API_KEY="your-api-key" \
     -v $(pwd)/data:/app/data \
     telecom-dashboard

Database Setup
==============

**Automatic Setup:**

The application automatically creates and populates the SQLite database on first run.

**Manual Database Creation:**

.. code-block:: bash

   # Run database setup script
   python setup_database.py
   
   # Load sample data
   python load_data.py
   
   # Generate test data (optional)
   python generate_comprehensive_data.py

**Database Location:**

* Default: ``data/telecom_db.sqlite``
* Configurable via ``config.yaml``

Configuration
=============

**Environment Variables:**

.. code-block:: bash

   # Required
   export LLM_API_KEY="your-openrouter-api-key"
   
   # Optional
   export DATABASE_PATH="data/custom_db.sqlite"
   export LOG_LEVEL="INFO"
   export SECURITY_LOG_FILE="logs/security.log"

**Configuration Files:**

Create ``config/config.yaml`` for custom settings:

.. code-block:: yaml

   database:
     path: "data/telecom_db.sqlite"
     cache_size: 64
     connection_timeout: 30000
   
   ui:
     default_theme: "verizon"
     page_title: "Custom Dashboard"
     show_debug_info: false
   
   security:
     enable_rate_limiting: true
     max_requests_per_minute: 120
     
   ai:
     model: "openai/gpt-5-nano"
     temperature: 0.1
     max_tokens: 2000

Security Setup
==============

**Automated Security Setup:**

.. code-block:: bash

   # Run the security setup script
   python setup_secure_environment.py

This script will:

* Prompt for your API key
* Create/update ``.env`` file
* Set secure file permissions  
* Install security dependencies
* Generate security checklist

**Manual Security Configuration:**

.. code-block:: bash

   # Set file permissions
   chmod 600 .env
   chmod 600 config.secrets.yaml
   chmod 755 *.py
   
   # Create logs directory
   mkdir -p logs
   chmod 755 logs
   
   # Install security tools
   pip install bandit safety

**Security Validation:**

.. code-block:: bash

   # Run security scans
   bandit -r . -f json -o security_report.json
   safety check --json --output safety_report.json

Development Setup
=================

**Additional Dependencies:**

.. code-block:: bash

   # Install development dependencies
   pip install -r requirements-dev.txt
   
   # Install pre-commit hooks
   pre-commit install

**Testing Setup:**

.. code-block:: bash

   # Install test dependencies
   pip install pytest pytest-cov pytest-xdist
   
   # Run tests
   pytest tests/ -v --cov=src --cov-report=html

**Documentation Setup:**

.. code-block:: bash

   # Install documentation dependencies
   pip install sphinx sphinx-rtd-theme myst-parser
   
   # Build documentation
   cd docs
   make html

Troubleshooting
===============

**Common Issues:**

**1. Python Not Found**

.. code-block:: bash

   # Try alternative Python commands
   python3 --version
   py --version  # Windows

**2. Permission Denied (macOS/Linux)**

.. code-block:: bash

   # Fix permissions
   chmod +x setup_secure_environment.py
   sudo chown -R $USER:$USER .

**3. Module Import Errors**

.. code-block:: bash

   # Ensure virtual environment is activated
   which python  # Should show venv path
   
   # Reinstall dependencies
   pip install --force-reinstall -r requirements.txt

**4. Streamlit Port Already in Use**

.. code-block:: bash

   # Use different port
   streamlit run app.py --server.port 8502

**5. Database Connection Issues**

.. code-block:: bash

   # Check database file exists and is readable
   ls -la data/telecom_db.sqlite
   
   # Regenerate database
   python setup_database.py

**Getting Help:**

* Check the :doc:`troubleshooting` section
* Review log files in ``logs/`` directory
* Create an issue on GitHub
* Check the FAQ section

Next Steps
==========

After installation:

1. :doc:`configuration` - Customize your setup
2. :doc:`usage` - Learn how to use the dashboard
3. :doc:`themes` - Set up corporate branding
4. :doc:`ai_insights` - Configure AI features
5. :doc:`security` - Review security settings


