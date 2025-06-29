# Generate Test Cases Task

## Purpose

To create comprehensive test cases based on user stories, acceptance criteria, and system requirements, ensuring thorough coverage of functional and non-functional scenarios.

## Inputs

- User Stories with Acceptance Criteria
- System Requirements and Specifications
- UI/UX Mockups or Prototypes
- API Documentation
- Risk Assessment and Priority Matrix

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with generating test cases? We can work:
A. **Incrementally (Default & Recommended):** We'll go through each feature/story step-by-step, creating test cases and getting your feedback.
B. **"YOLO" Mode:** I can generate a comprehensive test case suite for you to review."

### 2. Analyze Requirements for Testing

- Review user stories and break down acceptance criteria into testable scenarios
- Identify positive, negative, and edge case scenarios
- Analyze business rules and validation requirements
- Consider integration points and data flow scenarios
- Identify security and performance testing requirements

### 3. Design Test Case Structure

- **Test Case Organization:** Group test cases by feature, user story, or system component
- **Test Case Format:** Use consistent format including:
  - Test Case ID and Title
  - Preconditions and Test Data Requirements
  - Step-by-step Test Procedures
  - Expected Results and Acceptance Criteria
  - Priority and Risk Level
- **Traceability Matrix:** Link test cases back to requirements and user stories

### 4. Create Functional Test Cases

- **Happy Path Scenarios:** Test normal user workflows and expected behaviors
- **Boundary Value Testing:** Test limits, minimums, maximums, and edge cases
- **Negative Testing:** Test error handling, invalid inputs, and failure scenarios
- **Business Rule Validation:** Test complex business logic and validation rules
- **User Interface Testing:** Test UI elements, navigation, and user interactions

### 5. Design Non-Functional Test Cases

- **Performance Test Cases:** Load, stress, and scalability testing scenarios
- **Security Test Cases:** Authentication, authorization, and data protection testing
- **Usability Test Cases:** User experience and accessibility testing
- **Compatibility Test Cases:** Cross-browser, cross-platform, and device testing
- **Data Integrity Test Cases:** Data validation, backup, and recovery testing

### 6. Create API and Integration Test Cases

- **API Endpoint Testing:** Test all API endpoints with various input combinations
- **Data Format Validation:** Test request/response data formats and schemas
- **Error Response Testing:** Test API error handling and status codes
- **Integration Flow Testing:** Test end-to-end data flow between systems
- **Third-Party Integration Testing:** Test external service integrations

### 7. Develop Automation Test Scripts

- **Automated Test Case Selection:** Identify test cases suitable for automation
- **Test Script Development:** Create automated test scripts using selected frameworks
- **Test Data Management:** Implement test data setup and cleanup procedures
- **Continuous Integration:** Integrate automated tests into CI/CD pipeline
- **Maintenance Strategy:** Plan for test script maintenance and updates

## Output Deliverables

- **Test Case Repository** (organized by feature/component)
- **Automated Test Scripts** (for selected test cases)
- **Test Data Sets** (for various testing scenarios)
- **Traceability Matrix** (linking tests to requirements)

## Key Resources

- **Template:** `templates#test-plan-tmpl`
- **Validation:** `checklists#test-coverage-checklist`
- **User Preferences:** `data#technical-preferences`
