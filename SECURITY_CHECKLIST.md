
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
