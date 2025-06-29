# Code Security Review Checklist

[[LLM: This checklist ensures comprehensive security review of code changes. Check off each item as it's completed and verified.]]

## Input Validation and Sanitization
- [ ] All user inputs are validated and sanitized
- [ ] Input validation is performed on both client and server side
- [ ] Whitelist validation is used where possible
- [ ] Input length limits are enforced
- [ ] Special characters are properly handled
- [ ] File upload validation includes type and size checks
- [ ] SQL injection prevention measures are implemented
- [ ] Command injection prevention is implemented

## Authentication and Session Management
- [ ] Strong authentication mechanisms are implemented
- [ ] Password policies meet security standards
- [ ] Multi-factor authentication is available for sensitive operations
- [ ] Session tokens are securely generated and managed
- [ ] Session timeout is properly configured
- [ ] Session invalidation is implemented on logout
- [ ] Concurrent session limits are enforced where appropriate
- [ ] Account lockout mechanisms are implemented

## Authorization and Access Control
- [ ] Role-based access control is properly implemented
- [ ] Principle of least privilege is enforced
- [ ] Authorization checks are performed at all access points
- [ ] Direct object references are protected
- [ ] Privilege escalation protections are in place
- [ ] Administrative functions require additional authorization
- [ ] API endpoints have proper authorization controls
- [ ] File and directory access controls are implemented

## Data Protection and Encryption
- [ ] Sensitive data is encrypted at rest
- [ ] Data is encrypted in transit using TLS/SSL
- [ ] Cryptographic keys are properly managed
- [ ] Strong encryption algorithms are used
- [ ] Passwords are properly hashed with salt
- [ ] Personal data handling complies with privacy regulations
- [ ] Data masking is used in non-production environments
- [ ] Secure deletion of sensitive data is implemented

## Error Handling and Logging
- [ ] Error messages don't expose sensitive information
- [ ] Generic error messages are returned to users
- [ ] Detailed errors are logged securely for debugging
- [ ] Security events are properly logged
- [ ] Log data is protected from tampering
- [ ] Sensitive data is not logged
- [ ] Log retention policies are implemented
- [ ] Monitoring and alerting for security events is configured

## Cross-Site Scripting (XSS) Prevention
- [ ] Output encoding is implemented for all dynamic content
- [ ] Content Security Policy (CSP) headers are configured
- [ ] Input validation prevents script injection
- [ ] DOM manipulation is done securely
- [ ] User-generated content is properly sanitized
- [ ] Rich text editors have security controls
- [ ] File upload content is validated and sanitized
- [ ] Reflected XSS prevention is implemented

## Cross-Site Request Forgery (CSRF) Prevention
- [ ] CSRF tokens are implemented for state-changing operations
- [ ] SameSite cookie attributes are properly configured
- [ ] Referer header validation is implemented where appropriate
- [ ] Double-submit cookie pattern is used if applicable
- [ ] Custom headers are required for AJAX requests
- [ ] GET requests don't perform state changes
- [ ] Critical operations require re-authentication
- [ ] CORS policies are properly configured

## Secure Configuration
- [ ] Default passwords and accounts are changed or disabled
- [ ] Unnecessary services and features are disabled
- [ ] Security headers are properly configured
- [ ] Database connections use least privilege accounts
- [ ] File permissions are properly set
- [ ] Debug information is disabled in production
- [ ] Error pages don't reveal system information
- [ ] Security configurations are documented

## Third-Party Components and Dependencies
- [ ] Third-party libraries are kept up to date
- [ ] Known vulnerabilities in dependencies are addressed
- [ ] Dependency scanning is performed regularly
- [ ] License compliance is verified
- [ ] Third-party code is reviewed for security issues
- [ ] Vendor security practices are evaluated
- [ ] Supply chain security is considered
- [ ] Component inventory is maintained

## API Security
- [ ] API authentication is properly implemented
- [ ] API rate limiting is configured
- [ ] API input validation is comprehensive
- [ ] API responses don't expose sensitive data
- [ ] API versioning is handled securely
- [ ] API documentation doesn't reveal security details
- [ ] API endpoints are properly secured
- [ ] API monitoring and logging are implemented

## Mobile and Web Application Security
- [ ] Client-side security controls are implemented
- [ ] Sensitive operations are performed server-side
- [ ] Client-side data storage is minimized and secured
- [ ] Communication with backend is secured
- [ ] Certificate pinning is implemented where appropriate
- [ ] Jailbreak/root detection is implemented if needed
- [ ] Code obfuscation is applied where necessary
- [ ] Runtime application self-protection is considered

## Security Testing Integration
- [ ] Static application security testing (SAST) is performed
- [ ] Dynamic application security testing (DAST) is performed
- [ ] Interactive application security testing (IAST) is considered
- [ ] Security unit tests are implemented
- [ ] Penetration testing recommendations are addressed
- [ ] Security regression testing is performed
- [ ] Vulnerability scanning is automated
- [ ] Security testing is integrated into CI/CD pipeline

## Notes and Comments
[[LLM: Space for additional notes, security issues identified, or recommendations]]

**Completed By:** _____________________ **Date:** _____________________

**Reviewed By:** _____________________ **Date:** _____________________

**Approved By:** _____________________ **Date:** _____________________
