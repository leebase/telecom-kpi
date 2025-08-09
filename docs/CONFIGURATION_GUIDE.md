# 🛠️ Configuration Management Guide: Telecom KPI Dashboard

## 📋 Overview

This document provides comprehensive guidance for configuring and managing the Telecom KPI Dashboard across different environments, including environment validation, feature flag management, and production deployment safety.

## 🏗️ Configuration Architecture

### Configuration System Components
```
Configuration Management:
├── config_manager.py           # Core configuration management and validation
├── config_validator.py         # Standalone CLI utility for operations and validation  
├── config.template.yaml        # Configuration templates with documentation
├── config.secrets.yaml         # Runtime configuration (git-ignored)
├── config/pii_config.yaml      # PII scrubbing configuration
└── Environment Variables       # Runtime overrides and production settings
```

## 🚀 Quick Start

### Prerequisites
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Verify configuration system
python -c "from config_manager import get_config; print('✅ Configuration system ready')"
```

### 🔧 Configuration CLI Tool

**Important Note**: `config_validator.py` is a **standalone command-line utility** designed for operations teams and deployment environments. It is **not integrated** into the main Streamlit application and should be run separately for configuration management tasks.

**Usage**:
```bash
# Standalone operation - not part of main app
python config_validator.py validate
python config_validator.py production-check
python config_validator.py features
```

### Basic Configuration Setup
```bash
# 1. Copy template configuration
cp config.template.yaml config.secrets.yaml

# 2. Edit configuration file
# Set your API keys, database URLs, and feature preferences

# 3. Validate configuration
python config_validator.py validate --verbose

# 4. Check production readiness (if deploying to production)
python config_validator.py production-check
```

## 🔧 Environment Validation

### Validation Levels
The system validates configuration at three levels:

1. **Required Variables** - Critical for any deployment
2. **Production-Required Variables** - Additional requirements for production
3. **Recommended Variables** - Optional but recommended for optimal operation

### Environment Variables by Category

#### Required (All Environments)
```bash
export ENVIRONMENT=development|staging|production
```

#### Production-Required Variables
```bash
export DATABASE_URL=postgresql://user:pass@host:port/db
export LLM_API_KEY=sk-or-v1-...
export LOG_LEVEL=INFO|DEBUG|WARNING|ERROR|CRITICAL
```

#### Recommended Variables
```bash
export CACHE_TTL_SECONDS=300
export FEATURE_STRUCTURED_LOGGING=true
export FEATURE_SECURITY_HEADERS=true
```

### Validation Commands
```bash
# Validate current environment
python config_validator.py validate

# Validate for specific environment
python config_validator.py validate --environment production

# Detailed validation with warnings
python config_validator.py validate --verbose

# Production readiness check
python config_validator.py production-check
```

### Validation Output Example
```
🔍 Environment Validation Report
==================================================
Environment: production
Status: ✅ VALID
Errors: 0
Warnings: 1

⚠️  Warnings:
  - Missing recommended variable: CACHE_TTL_SECONDS

📊 Summary:
  Required vars set: 1/1
  Recommended vars set: 4/5
```

## 🎛️ Feature Flag Management

### Feature Flag Categories

#### 🤖 AI and ML Features
```yaml
features:
  ai_insights: true                    # Enable AI-powered insights generation
  ai_insights_beta: false             # Enable beta AI features
  pii_scrubbing: true                 # Enable PII scrubbing for GDPR compliance
```

#### ⚡ Performance Features
```yaml
features:
  cache_ttl: true                     # Enable TTL-based caching
  circuit_breaker: true               # Enable circuit breaker pattern
  connection_pooling: true            # Enable database connection pooling
```

#### 🏢 Enterprise Features
```yaml
features:
  structured_logging: false           # Enable JSON structured logging (production)
  snowflake_query_tagging: true       # Enable Snowflake query tagging
  health_checks_detailed: true        # Enable detailed health checks
```

#### 🎨 UI and UX Features
```yaml
features:
  theme_switching: true               # Enable dynamic theme switching
  benchmark_management: true          # Enable benchmark management interface
  print_mode: true                   # Enable print-optimized layouts
```

#### 🔒 Security Features
```yaml
features:
  security_headers: true              # Enable security headers
  rate_limiting: true                 # Enable rate limiting
  sql_injection_protection: true     # Enable SQL injection protection
```

#### 🔧 Development Features
```yaml
features:
  debug_mode: false                   # Enable debug features (development only)
  test_mode: false                   # Enable test fixtures and mock data
  performance_monitoring: true        # Enable performance metrics collection
```

### Feature Flag Commands
```bash
# List all feature flags with current values
python config_validator.py features

# Set feature flag via environment variable (current session)
python config_validator.py set-feature structured_logging true

# Export feature flags as environment variables
python config_validator.py export --format env
```

### Environment Variable Overrides
Feature flags can be overridden at runtime using environment variables:

```bash
# Override format: FEATURE_<UPPERCASE_NAME>=true|false
export FEATURE_DEBUG_MODE=true
export FEATURE_STRUCTURED_LOGGING=true
export FEATURE_AI_INSIGHTS_BETA=false

# Verify overrides
python config_validator.py features
```

## 🌍 Environment-Specific Configuration

### Development Environment
```yaml
environments:
  development:
    features:
      debug_mode: true
      structured_logging: false
      detailed_logging: true
      test_mode: true
```

**Characteristics:**
- Debug features enabled
- Simplified logging
- Test mode available
- Validation warnings only (non-blocking)

### Staging Environment
```yaml
environments:
  staging:
    features:
      structured_logging: true
      debug_mode: false
      performance_monitoring: true
      security_headers: true
```

**Characteristics:**
- Production-like configuration
- Structured logging enabled
- Performance monitoring active
- Security features enabled

### Production Environment
```yaml
environments:
  production:
    features:
      structured_logging: true
      debug_mode: false
      detailed_logging: false
      performance_monitoring: true
      security_headers: true
      rate_limiting: true
```

**Characteristics:**
- Maximum security and performance
- All enterprise features enabled
- Debug features disabled
- Strict validation (blocking)

## 🛡️ Production Deployment Safety

### Pre-Deployment Checklist
```bash
# 1. Set production environment
export ENVIRONMENT=production

# 2. Configure required variables
export DATABASE_URL=postgresql://prod-server/telecom_db
export LLM_API_KEY=sk-or-v1-your-production-key
export LOG_LEVEL=INFO

# 3. Run production readiness check
python config_validator.py production-check

# 4. Verify configuration export
python config_validator.py export --format env > production.env
```

### Production Readiness Validation
The production check validates:

1. **Environment Configuration** - All required variables present and valid
2. **Feature Flag Configuration** - Production-appropriate feature settings
3. **Security Configuration** - API keys, database URLs, and security features
4. **Overall Readiness** - Comprehensive deployment safety assessment

### Production Safety Features
- **Fail-Fast Validation** - Stop deployment if critical configuration is missing
- **Environment-Specific Requirements** - Different validation rules per environment
- **Security Validation** - API key format and security feature validation
- **Configuration Drift Detection** - Ensure consistent configuration across deployments

## 📊 Configuration Management CLI

### Command Reference
```bash
# Environment validation
python config_validator.py validate [--environment ENV] [--verbose]

# Feature flag management
python config_validator.py features
python config_validator.py set-feature FEATURE_NAME true|false

# Production readiness
python config_validator.py production-check

# Configuration export
python config_validator.py export [--format json|env]
```

### CLI Output Examples

#### Feature Flag Listing
```
🎛️  Feature Flags Configuration
==================================================

📋 AI and ML Features:
  ai_insights               ✅ ON
  ai_insights_beta          ❌ OFF
  pii_scrubbing             ✅ ON

📋 Performance Features:
  cache_ttl                 ✅ ON
  circuit_breaker           ✅ ON
  connection_pooling        ✅ ON

🔧 Environment Overrides:
  FEATURE_DEBUG_MODE = true
```

#### Production Readiness Check
```
🚀 Production Readiness Check
==================================================
1. Environment Validation...
✅ Environment Configuration

2. Feature Flag Validation...
✅ Feature flags configured for production

3. Security Configuration...
  LLM_API_KEY configured: ✅
  Database URL configured: ✅
  Environment set to production: ✅
  Log level configured: ✅

🎯 Overall Production Readiness: ✅ READY
```

## 🔧 Configuration File Management

### Configuration File Structure
```yaml
# config.secrets.yaml (primary configuration)
llm:
  provider: "openrouter"
  api_key: "your-api-key"
  model: "openai/gpt-5-nano"

database:
  path: "data/telecom_db.sqlite"
  backup_enabled: true

features:
  ai_insights: true
  structured_logging: false
  # ... all feature flags

environments:
  production:
    features:
      structured_logging: true
      security_headers: true

validation:
  required_production_vars:
    - "ENVIRONMENT"
    - "DATABASE_URL"
    - "LLM_API_KEY"
```

### Configuration Best Practices

1. **Use Templates** - Start with `config.template.yaml` and customize
2. **Environment Variables** - Use environment variables for sensitive data
3. **Version Control** - Never commit `config.secrets.yaml` to version control
4. **Validation** - Always validate configuration before deployment
5. **Documentation** - Document custom configuration changes

### Security Considerations

- **API Keys** - Store in environment variables, not configuration files
- **Database URLs** - Use environment variables for production databases
- **Secrets Management** - Consider using dedicated secrets management systems
- **Access Control** - Restrict access to configuration files in production
- **Audit Trails** - Log configuration changes and validation results

## 🚨 Troubleshooting

### Common Configuration Issues

#### Missing Environment Variables
```
Error: Missing required environment variable: DATABASE_URL
Solution: export DATABASE_URL=your-database-url
```

#### Invalid Feature Flag Values
```
Error: Invalid feature flag value for FEATURE_DEBUG_MODE: maybe
Solution: export FEATURE_DEBUG_MODE=true  # or false
```

#### Production Validation Failures
```
Error: Production readiness check failed
Solution: Run 'python config_validator.py production-check' for details
```

### Debug Commands
```bash
# Check current configuration
python -c "from config_manager import get_config; config = get_config(); print('Config loaded successfully')"

# Verify environment variables
python -c "import os; print(f'Environment: {os.getenv(\"ENVIRONMENT\", \"not set\")}')"

# Test feature flag loading
python -c "from config_manager import get_config; print(f'AI insights: {get_config().features.ai_insights}')"
```

### Logging and Monitoring
- Configuration validation results are logged to the application logs
- Environment variable overrides are logged for audit trails
- Production readiness check results should be monitored in CI/CD pipelines
- Feature flag changes should be tracked for operational visibility

## 📈 Integration with Deployment Pipelines

### CI/CD Integration Example
```yaml
# .github/workflows/deploy.yml
- name: Validate Configuration
  run: |
    python config_validator.py validate --environment production
    python config_validator.py production-check

- name: Export Configuration
  run: |
    python config_validator.py export --format env > production.env
```

### Deployment Automation
```bash
#!/bin/bash
# deploy.sh

# Set environment
export ENVIRONMENT=production

# Validate configuration
if python config_validator.py production-check; then
    echo "✅ Configuration validated - proceeding with deployment"
    # Deploy application
else
    echo "❌ Configuration validation failed - aborting deployment"
    exit 1
fi
```

---

**This configuration management system ensures safe, consistent, and reliable deployment of the Telecom KPI Dashboard across all environments with enterprise-grade validation and feature control.**
