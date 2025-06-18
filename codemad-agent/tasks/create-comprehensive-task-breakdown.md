# Comprehensive Task Breakdown Creation Task

## Purpose

Transform completed PRD and architecture documents into a comprehensive task breakdown document (`tasks.md`) that provides:
- Epic-level breakdown of all project work
- Detailed user stories with acceptance criteria  
- Frontend and backend development tasks with specific implementation details
- Task dependencies and sequencing
- Effort estimates optimized for AI agent execution
- Definition of Done criteria for each task level

## Instructions

### 1. Review and Validate Inputs

**Required Inputs:**
- Completed PRD document (`prd.md`)
- Technical Architecture document (`architecture.md`) 
- Frontend Architecture document (if applicable)
- Project technical preferences and constraints

**Input Validation:**
- Confirm all required documents are complete and approved
- Verify technical architecture decisions are finalized
- Identify any gaps or ambiguities that need clarification
- Request missing information before proceeding

### 2. Determine Interaction Mode

Confirm with the user their preferred interaction style:

- **Incremental Mode (Recommended):** Work through each section systematically, reviewing epics, then user stories, then detailed tasks with user feedback at each stage
- **YOLO Mode:** Generate complete task breakdown making reasonable assumptions, then review comprehensively with user

### 3. Epic-Level Analysis and Breakdown

**Epic Identification:**
- Analyze PRD features and group into logical epics
- Ensure each epic represents a cohesive set of functionality
- Define clear epic boundaries and scope
- Establish epic priorities and dependencies

**Epic Documentation:**
- Create epic definitions with clear objectives
- Define epic-level acceptance criteria
- Identify cross-epic dependencies
- Estimate epic-level effort and timeline

### 4. User Story Creation and Refinement

**Story Development:**
- Convert epic features into detailed user stories
- Ensure each story follows "As a [user], I want [action], so that [benefit]" format
- Size stories appropriately for AI agent execution (2-4 hour completion target)
- Create vertical slices that deliver complete functionality

**Story Enhancement:**
- Define comprehensive acceptance criteria for each story
- Identify story dependencies and prerequisites
- Add technical context and implementation guidance
- Include UI/UX requirements where applicable

### 5. Detailed Task Breakdown

**Frontend Development Tasks:**
- Component creation and styling tasks
- State management implementation
- API integration tasks
- User interface interaction tasks
- Responsive design implementation
- Accessibility compliance tasks

**Backend Development Tasks:**
- API endpoint creation
- Database schema implementation
- Business logic development
- Authentication and authorization
- Data validation and processing
- Integration with external services

**Cross-Cutting Tasks:**
- Testing strategy implementation
- Documentation creation
- Code review and quality assurance
- Deployment and infrastructure setup
- Performance optimization
- Security implementation

### 6. Dependency Analysis and Sequencing

**Dependency Mapping:**
- Identify all task dependencies (technical and logical)
- Create dependency visualization (Mermaid diagrams)
- Establish critical path through the project
- Identify opportunities for parallel execution

**Sequencing Optimization:**
- Order tasks to minimize AI agent context switching
- Group related tasks for efficient execution
- Plan for incremental delivery and validation
- Account for integration and testing phases

### 7. Effort Estimation and AI Agent Assignment

**Effort Estimation:**
- Provide realistic time estimates for each task
- Consider AI agent capabilities and limitations
- Account for complexity, dependencies, and risk factors
- Include buffer time for integration and testing

**AI Agent Assignment Recommendations:**
- Suggest appropriate AI agent types for each task category
- Consider AI agent specializations and strengths
- Plan for AI agent collaboration and handoffs
- Optimize for AI agent context window efficiency

### 8. Quality Assurance and Validation

**Definition of Done Criteria:**
- Define clear completion criteria for each task level
- Include testing requirements and validation steps
- Specify documentation and review requirements
- Establish quality gates and approval processes

**Risk Assessment:**
- Identify potential bottlenecks and risks
- Plan mitigation strategies for high-risk tasks
- Establish contingency plans for critical path items
- Document assumptions and dependencies

### 9. Document Generation and Review

**Use Template Structure:**
- Follow the `comprehensive-tasks-tmpl` template format
- Ensure all sections are properly completed
- Include visual diagrams and dependency maps
- Maintain clear, actionable language throughout

**Comprehensive Review:**
- Validate completeness against PRD and architecture
- Verify task breakdown supports all requirements
- Confirm effort estimates are realistic
- Ensure AI agent optimization is achieved

### 10. Final Deliverable Preparation

**Document Finalization:**
- Generate complete `tasks.md` document
- Include executive summary and project overview
- Provide clear navigation and cross-references
- Ensure document is ready for AI agent consumption

**Handoff Preparation:**
- Create AI agent assignment matrix
- Prepare task prioritization recommendations
- Document any assumptions or decisions made
- Provide guidance for task breakdown maintenance

### 11. Final Validation and Quality Assurance

**Comprehensive Checklist Review:**
- Run the `task-breakdown-checklist` against completed task breakdown
- Validate all checklist items for completeness and quality
- Address any deficiencies or gaps identified
- Ensure AI agent optimization criteria are met

**Final Quality Gates:**
- Confirm all PRD requirements are covered
- Verify architecture alignment throughout
- Validate AI agent execution readiness
- Ensure comprehensive documentation quality

## Key Resources

- **Template:** `templates#comprehensive-tasks-tmpl`
- **Validation:** `checklists#task-breakdown-checklist`
- **Dependencies:** PRD document, Architecture document
- **User Preferences:** `data#technical-preferences`

## Success Criteria

- Complete task breakdown covering all PRD requirements
- Tasks appropriately sized for AI agent execution
- Clear dependencies and sequencing established
- Realistic effort estimates provided
- Definition of Done criteria defined for all levels
- Document optimized for AI agent collaboration and efficiency
