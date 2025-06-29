# Create API Documentation Task

## Purpose

To create comprehensive, user-friendly API documentation that enables developers to effectively understand, integrate with, and use the API services.

## Inputs

- API Specifications (OpenAPI/Swagger, RAML, etc.)
- System Architecture Document
- API Design Guidelines and Standards
- User Stories and Use Cases
- Authentication and Authorization Requirements

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with creating the API documentation? We can work:
A. **Incrementally (Default & Recommended):** We'll document each API section step-by-step, getting your feedback.
B. **"YOLO" Mode:** I can create comprehensive API documentation for you to review."

### 2. API Documentation Planning

- **Audience Analysis:** Identify target audiences (internal developers, external partners, public developers)
- **Documentation Scope:** Define which APIs and endpoints to document
- **Documentation Standards:** Establish documentation standards and style guidelines
- **Tool Selection:** Choose appropriate documentation tools and platforms
- **Information Architecture:** Plan documentation structure and navigation
- **Maintenance Strategy:** Plan for ongoing documentation maintenance and updates

### 3. API Reference Documentation

- **Endpoint Documentation:** Document all API endpoints with methods, parameters, and responses
- **Request/Response Examples:** Provide comprehensive examples for all API operations
- **Error Documentation:** Document all error codes, messages, and resolution guidance
- **Data Models:** Document all data models, schemas, and field descriptions
- **Authentication Guide:** Document authentication methods and implementation details
- **Rate Limiting:** Document rate limits, quotas, and throttling policies

### 4. Getting Started Guide

- **Quick Start Tutorial:** Create step-by-step quick start guide for new users
- **Authentication Setup:** Guide users through authentication setup and configuration
- **First API Call:** Walk through making the first successful API call
- **Common Use Cases:** Document common integration patterns and use cases
- **SDK and Libraries:** Document available SDKs, libraries, and code samples
- **Environment Setup:** Guide for setting up development and testing environments

### 5. Advanced Documentation

- **Integration Guides:** Create detailed integration guides for complex scenarios
- **Best Practices:** Document API usage best practices and recommendations
- **Performance Optimization:** Guide for optimizing API performance and efficiency
- **Troubleshooting Guide:** Common issues and their solutions
- **Migration Guides:** Documentation for API version migrations and updates
- **Webhook Documentation:** Document webhook implementation and handling

### 6. Interactive Documentation

- **API Explorer:** Implement interactive API testing and exploration tools
- **Code Samples:** Provide code samples in multiple programming languages
- **Try It Out:** Enable users to test API calls directly from documentation
- **Response Visualization:** Show formatted responses and data structures
- **Postman Collections:** Create and maintain Postman collections for API testing
- **Sandbox Environment:** Provide sandbox environment for safe testing

### 7. Documentation Quality and Maintenance

- **Review Process:** Establish documentation review and approval process
- **Accuracy Validation:** Validate documentation accuracy against actual API behavior
- **User Feedback:** Implement feedback collection and incorporation process
- **Analytics and Usage:** Track documentation usage and identify improvement areas
- **Version Management:** Manage documentation versions aligned with API versions
- **Continuous Updates:** Establish process for keeping documentation current

## Output Deliverables

- **API Documentation Website** (comprehensive, searchable documentation)
- **Getting Started Guide** (`docs/api-getting-started.md`)
- **API Reference** (`docs/api-reference.md`)
- **Integration Examples** (code samples and tutorials)

## Key Resources

- **Template:** `templates#api-documentation-tmpl`
- **Validation:** `checklists#api-documentation-checklist`
- **User Preferences:** `data#technical-preferences`
