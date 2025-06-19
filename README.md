# BMAD AI Agent Orchestration System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/usemanusai/CodeMAD?style=social)](https://github.com/usemanusai/CodeMAD)
[![GitHub Issues](https://img.shields.io/github/issues/usemanusai/CodeMAD)](https://github.com/usemanusai/CodeMAD/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/usemanusai/CodeMAD)](https://github.com/usemanusai/CodeMAD/pulls)

## 🚀 Project Overview

The **BMAD (Breakthrough Method of Agile AI Agent-Driven Development)** AI Agent Orchestration System is a comprehensive, intelligent platform that coordinates **50+ specialized software development AI agents** to handle virtually any software development scenario. The system now features **mandatory mode selection** to ensure users get exactly what they need: either comprehensive documentation for developer handoff or complete application development within the chat session.

### 🎯 Key Benefits

- **🎯 Mandatory Mode Selection**: Forces explicit choice between Documentation Mode (handoff documents) and Full Development Mode (complete implementation)
- **📋 Documentation Mode**: Generates exactly 3 complete, standalone documents (prd.md, architecture.md, checklist.md) ready for developer handoff
- **🚀 Full Development Mode**: Complete application development with intelligent AI agent coordination and workflow optimization
- **🤖 Intelligent AI Agent Automation**: Automatically selects optimal AI agents and coordinates workflows based on project requirements and selected mode
- **⚡ 50% Productivity Increase**: Streamlines development processes through specialized AI agent expertise and parallel execution
- **🛡️ Quality Assurance**: Integrated quality gates and validation throughout all AI agent workflows
- **📈 Scalable Architecture**: Enterprise-ready system that scales from startup MVPs to complex enterprise projects
- **🔄 Adaptive Learning**: Continuously improves AI agent workflow efficiency based on outcomes and feedback

### 👥 Target Audience

- **Software Development Teams** seeking intelligent AI agent workflow automation
- **Engineering Managers** looking to optimize team productivity through AI agent coordination
- **Enterprise Organizations** requiring comprehensive development process orchestration via AI agents
- **Startups** needing rapid, high-quality software development capabilities through AI agent collaboration
- **DevOps Teams** implementing advanced CI/CD and automation strategies with AI agent support

### 🎯 Use Cases

**Documentation Mode (Perfect for Client/Team Handoffs):**
- **Project Specification**: Generate comprehensive documentation for external development teams
- **Client Deliverables**: Create professional handoff documents for VS Code developers
- **Requirement Documentation**: Complete PRD, architecture, and implementation checklists
- **Vendor Coordination**: Provide detailed specifications for outsourced development

**Full Development Mode (Complete Implementation):**
- **Feature Development**: End-to-end feature implementation with AI agent quality assurance
- **System Architecture**: Enterprise-level architecture design and implementation via specialized AI agents
- **Security Implementation**: Comprehensive security analysis and implementation through AI agent coordination
- **Data Platform Development**: Advanced data engineering and AI system creation using specialized AI agents
- **Legacy Modernization**: Complex system migration and modernization projects with AI agent expertise

## 🎯 Mandatory Mode Selection System

The BMAD Method 3.1 features a **mandatory mode selection system** that ensures users get exactly what they need. Before any AI agent operations begin, users must explicitly choose between two distinct workflows:

### 📋 Documentation Mode (Mode 1) - Default & Recommended
**Perfect for:** Sending specifications to developers working in VS Code Insiders

**Generates exactly 3 complete, final documents:**
- **`prd.md`** - Product Requirements Document (complete final product specifications)
- **`architecture.md`** - Technical architecture document (system design & implementation approach)
- **`checklist.md`** - Development checklist (acceptance criteria & implementation steps)

**Key Features:**
- ✅ Standalone documents requiring no additional clarification
- ✅ Comprehensive enough for independent development
- ✅ Professional quality ready for client/team handoff
- ✅ No actual development or coding included

### 🚀 Full Development Mode (Mode 2)
**Perfect for:** Complete application development within the chat session

**Features:**
- 🤖 Complete AI agent orchestration and coordination
- 🔄 Interactive development workflow with specialized AI agents
- 🛠️ Full implementation, testing, and deployment
- 📊 Real-time collaboration between 50+ specialized AI agents

### Key System Enhancements (Latest Update)

- **Mandatory Mode Selection**: Users must explicitly choose their workflow before proceeding
- **Documentation Mode Workflow**: Complete system for generating handoff-ready documents
- **AI Agent Self-Perception**: System correctly identifies as coordinating "AI agents" rather than "human workers"
- **Comprehensive Task Breakdown**: Enhanced Task Breakdown Specialist AI Agent (Tyler) for detailed deliverables
- **Mode-Based Routing**: Intelligent workflow routing based on user selection
- **AI Agent Optimization**: Tasks sized and structured specifically for AI agent context windows and capabilities

## 🚀 Quick Start - Try the Mode Selection System

The fastest way to understand the BMAD system is to experience the new mode selection workflow! Set up takes just a few minutes in Gemini or ChatGPT.

### Web Quickstart Project Setup (Recommended)

AI Agent Orchestrator with **mandatory mode selection** - already pre-compiled in the `web-build-sample` folder.

**Setup Steps:**
1. **Copy** the contents of [Agent Prompt Sample](web-build-sample/agent-prompt.txt)
2. **Paste** into Gemini Gem or ChatGPT Custom GPT 'Instructions' field
3. **Attach** the remaining files from `web-build-sample/` folder as knowledge base
4. **Save** with a name like "BMAD AI Agent Orchestrator"

**First Experience:**
- The system will **immediately present the mode selection menu**
- Choose **Mode 1 (Documentation)** to generate handoff documents
- Choose **Mode 2 (Development)** for full application development
- Start with `/help` to explore all capabilities

![image info](docs/images/gem-setup.png)

### Mode Selection Menu Preview

When you first interact with the system, you'll see:

```
🎯 **BMAD AI Agent System - Mode Selection Required**

Please choose your workflow mode:

**1. Documentation Mode (Default & Recommended)**
   📋 Generate exactly 3 complete, final documents ready for developer handoff:
   • prd.md - Product Requirements Document
   • architecture.md - Technical architecture document
   • checklist.md - Development checklist

**2. Full Development Mode**
   🚀 Build the entire project within this chat session

**Please type "1" for Documentation Mode or "2" for Full Development Mode to continue.**
```

## 🏗️ System Architecture

### Mode Selection System Architecture

```mermaid
graph TB
    subgraph "BMAD AI Agent Orchestration System with Mode Selection"
        U[User Request] --> MS[Mandatory Mode Selection Menu]

        MS --> DM[Documentation Mode Selected]
        MS --> FM[Full Development Mode Selected]

        subgraph "Documentation Mode Workflow"
            DM --> DW[Documentation Workflow Engine]
            DW --> PM[Product Manager AI - John]
            DW --> AR[Architect AI - Fred]
            DW --> TB[Task Breakdown AI - Tyler]

            PM --> PRD[prd.md<br/>Complete Product Requirements]
            AR --> ARCH[architecture.md<br/>Technical Architecture]
            TB --> TASKS[checklist.md<br/>Development Checklist]

            PRD --> DD[Documentation Deliverables]
            ARCH --> DD
            TASKS --> DD
        end

        subgraph "Full Development Mode Workflow"
            FM --> O[Enhanced AI Agent Orchestrator<br/>🧠 Natural Language Processing<br/>🎯 AI Agent Selection Algorithm<br/>🔄 Workflow Coordination<br/>📊 Adaptive Learning]

            subgraph "AI Agent Categories"
                CD[Core Development AI Agents<br/>👨‍💻 12 AI Agents<br/>Frontend, Backend, Mobile<br/>API, Database, Blockchain]
                IO[Infrastructure & Operations AI Agents<br/>⚙️ 10 AI Agents<br/>DevOps, SRE, Cloud<br/>Kubernetes, Monitoring]
                SC[Security & Compliance AI Agents<br/>🔒 8 AI Agents<br/>Security, Cybersecurity<br/>Compliance, Privacy]
                DA[Data & AI Agents<br/>🤖 8 AI Agents<br/>Data Engineering, ML<br/>AI, Analytics]
                QT[Quality & Testing AI Agents<br/>✅ 6 AI Agents<br/>QA, Automation<br/>Performance, Accessibility]
                ST[Specialized Technical AI Agents<br/>🎯 6 AI Agents<br/>Architecture, Integration<br/>Migration, Research]
            end

            O --> CD
            O --> IO
            O --> SC
            O --> DA
            O --> QT
            O --> ST

            CD --> FD[Full Development Deliverables]
            IO --> FD
            SC --> FD
            DA --> FD
            QT --> FD
            ST --> FD
        end

        subgraph "Supporting Systems"
            KB[Knowledge Base<br/>📚 Templates & Checklists<br/>📋 Best Practices<br/>📖 Documentation]
            QF[Quality Framework<br/>🎯 Quality Gates<br/>✅ Validation Rules<br/>📊 Metrics & KPIs]
            WE[Workflow Engine<br/>🔄 Task Orchestration<br/>⚡ Parallel Execution<br/>🔗 Dependency Management]
        end

        DW --> KB
        O --> KB
        DW --> QF
        O --> QF
        DW --> WE
        O --> WE
    end

    style MS fill:#ff9800
    style DM fill:#4caf50
    style FM fill:#2196f3
    style DD fill:#8bc34a
    style FD fill:#03a9f4
    style O fill:#e1f5fe
    style CD fill:#f3e5f5
    style IO fill:#e8f5e8
    style SC fill:#fff3e0
    style DA fill:#e3f2fd
    style QT fill:#f1f8e9
    style ST fill:#fce4ec
```

### Mode Selection Workflow Process

```mermaid
sequenceDiagram
    participant U as User
    participant MS as Mode Selection System
    participant DW as Documentation Workflow
    participant PM as Product Manager AI
    participant AR as Architect AI
    participant TB as Task Breakdown AI
    participant O as AI Agent Orchestrator
    participant AG as AI Agent Team
    participant QG as Quality Gates

    U->>MS: Initial Request
    MS->>MS: Present Mode Selection Menu
    Note over MS: 🎯 Mandatory Choice Required<br/>📋 Mode 1: Documentation<br/>🚀 Mode 2: Full Development

    alt Documentation Mode Selected
        U->>MS: Select Mode 1 (Documentation)
        MS->>DW: Activate Documentation Workflow

        DW->>PM: Generate PRD
        PM->>PM: Create prd.md
        PM->>DW: Complete Product Requirements

        DW->>AR: Generate Architecture
        AR->>AR: Create architecture.md
        AR->>DW: Complete Technical Architecture

        DW->>TB: Generate Checklist
        TB->>TB: Create checklist.md
        TB->>DW: Complete Development Checklist

        DW->>QG: Validate Documentation
        QG->>QG: Quality Check
        Note over QG: ✅ Completeness Check<br/>📋 Consistency Validation<br/>🎯 Handoff Readiness

        QG->>U: Deliver 3 Complete Documents
        Note over U: 📄 prd.md<br/>🏗️ architecture.md<br/>✅ checklist.md

    else Full Development Mode Selected
        U->>MS: Select Mode 2 (Full Development)
        MS->>O: Activate AI Agent Orchestrator

        O->>O: AI Agent Selection & Coordination
        Note over O: 🧠 Analyze Request<br/>🎯 Select Optimal AI Agents<br/>🔄 Coordinate Workflows

        O->>AG: Deploy AI Agent Team
        AG->>AG: Parallel Development Execution

        AG->>QG: Submit Development Deliverables
        QG->>QG: Comprehensive Quality Validation
        Note over QG: ✅ Code Review<br/>🔒 Security Check<br/>⚡ Performance Test

        QG->>U: Deliver Complete Application
        Note over U: 🚀 Full Implementation<br/>🧪 Tested & Validated<br/>📦 Ready for Deployment
    end

    Note over MS,U: 🎯 Mode Selection Ensures<br/>Appropriate Output for User Needs
```

## Mode-Based AI Agent Coordination

The BMAD Method 3.1 features two distinct AI agent coordination workflows based on mandatory mode selection:

### Documentation Mode Workflow

```mermaid
graph TD
    A[User Request] --> MS[Mandatory Mode Selection]
    MS --> DM[Documentation Mode Selected]

    DM --> B[BMad AI Agent Orchestrator]
    B --> DW[Documentation Workflow Engine]

    DW --> PM[Product Manager AI - John<br/>📋 PRD Specialist]
    DW --> AR[Architect AI - Fred<br/>🏗️ Technical Design]
    DW --> TB[Task Breakdown AI - Tyler<br/>✅ Implementation Planning]

    PM --> PRD[prd.md<br/>Complete Product Requirements<br/>• User Stories & Acceptance Criteria<br/>• Technical Constraints<br/>• Success Metrics]

    AR --> ARCH[architecture.md<br/>Technical Architecture<br/>• System Design & Components<br/>• Technology Stack<br/>• Security & Deployment]

    TB --> CHECK[checklist.md<br/>Development Checklist<br/>• Phase-based Implementation<br/>• Quality Gates<br/>• Testing & Deployment]

    PRD --> QV[Quality Validation<br/>📊 Completeness Check<br/>🔗 Cross-Reference Validation<br/>🎯 Handoff Readiness]
    ARCH --> QV
    CHECK --> QV

    QV --> DD[Documentation Deliverables<br/>Ready for Developer Handoff]

    style MS fill:#ff9800
    style DM fill:#4caf50
    style B fill:#e1f5fe
    style PM fill:#f3e5f5
    style AR fill:#e8f5e8
    style TB fill:#fff3e0
    style DD fill:#8bc34a
```

### Full Development Mode Workflow

```mermaid
graph TD
    A[User Request] --> MS[Mandatory Mode Selection]
    MS --> FM[Full Development Mode Selected]

    FM --> B[BMad AI Agent Orchestrator]
    B --> C{Select AI Agent Team}

    C --> D[Product Manager AI - John]
    C --> E[Architect AI - Fred]
    C --> F[Task Breakdown AI - Tyler]
    C --> G[Design Architect AI - Jane]
    C --> H[Development AI Agents]
    C --> I[QA & Security AI Agents]

    D --> J[Creates prd.md]
    E --> K[Creates architecture.md]
    F --> L[Creates tasks.md]
    G --> M[Creates frontend specs]
    H --> N[Implements Features]
    I --> O[Tests & Validates]

    J --> P[Quality Validation & Integration]
    K --> P
    L --> P
    M --> P
    N --> P
    O --> P

    P --> Q[Complete Application<br/>🚀 Fully Implemented<br/>🧪 Tested & Validated<br/>📦 Ready for Deployment]

    style MS fill:#ff9800
    style FM fill:#2196f3
    style B fill:#e1f5fe
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fff3e0
    style G fill:#fce4ec
    style Q fill:#03a9f4
```

## Documentation Mode: Three-Document Creation Process

When Documentation Mode is selected, the system follows a sequential AI agent handoff process to create three comprehensive, standalone documents ready for developer handoff:

```mermaid
sequenceDiagram
    participant User
    participant MS as Mode Selection System
    participant Orchestrator as BMad AI Agent Orchestrator
    participant PM as Product Manager AI (John)
    participant Arch as Architect AI (Fred)
    participant Task as Task Breakdown AI (Tyler)
    participant QV as Quality Validation

    User->>MS: Request project documentation
    MS->>MS: Present Mode Selection Menu
    User->>MS: Select Mode 1 (Documentation)

    MS->>Orchestrator: Activate Documentation Workflow

    Orchestrator->>PM: Activate for PRD creation
    Note over PM: 📋 Gather requirements<br/>👥 Define user personas<br/>🎯 Set success criteria
    PM->>PM: Create comprehensive prd.md
    PM->>Orchestrator: PRD complete with handoff context

    Orchestrator->>Arch: Activate for architecture design
    Note over Arch: 🏗️ Analyze PRD requirements<br/>⚙️ Design system architecture<br/>🔧 Select technology stack
    Arch->>Arch: Create detailed architecture.md
    Arch->>Orchestrator: Architecture complete with handoff context

    Orchestrator->>Task: Activate for checklist creation
    Note over Task: ✅ Analyze PRD & architecture<br/>📋 Create implementation phases<br/>🎯 Define acceptance criteria
    Task->>Task: Create comprehensive checklist.md
    Task->>Orchestrator: Development checklist complete

    Orchestrator->>QV: Validate all documents
    Note over QV: 🔍 Cross-reference validation<br/>📊 Completeness check<br/>🎯 Handoff readiness
    QV->>QV: Quality assurance review

    QV->>User: Three comprehensive deliverables ready
    Note over User: 📄 prd.md - Complete specifications<br/>🏗️ architecture.md - Technical design<br/>✅ checklist.md - Implementation guide

    Note over PM,Task: Each document is standalone and<br/>comprehensive for independent development
```

### Documentation Mode Output Examples

**📄 prd.md - Product Requirements Document**
- Executive summary and project vision
- Detailed user personas and use cases
- Complete functional requirements with user stories
- Non-functional requirements (performance, security, scalability)
- Technical constraints and success criteria
- Timeline and acceptance criteria

**🏗️ architecture.md - Technical Architecture Document**
- System overview and design patterns
- Complete technology stack with specific versions
- Component architecture and data models
- API design and security architecture
- Infrastructure and deployment strategy
- Development guidelines and coding standards

**✅ checklist.md - Development Checklist**
- Pre-development setup and environment configuration
- Phase-based implementation guide (6 phases from setup to post-launch)
- Specific, actionable tasks for each development stage
- Quality gates and testing requirements
- Deployment preparation and launch procedures
- Post-launch monitoring and maintenance guidelines

### Multi-Agent Collaboration Patterns

```mermaid
graph LR
    subgraph "Sequential Handoff Pattern"
        S1[AI Agent 1<br/>Requirements] --> S2[AI Agent 2<br/>Design]
        S2 --> S3[AI Agent 3<br/>Implementation]
        S3 --> S4[AI Agent 4<br/>Testing]
        S4 --> S5[AI Agent 5<br/>Deployment]
    end

    subgraph "Parallel Execution Pattern"
        P0[Task Distribution] --> P1[Frontend Dev AI]
        P0 --> P2[Backend Dev AI]
        P0 --> P3[Database Dev AI]
        P1 --> PI[Integration Point]
        P2 --> PI
        P3 --> PI
    end

    subgraph "Collaborative Team Pattern"
        C1[Solutions Architect AI] <--> C2[Security Engineer AI]
        C2 <--> C3[Performance Engineer AI]
        C3 <--> C1
        C1 --> CR[Collaborative Result]
        C2 --> CR
        C3 --> CR
    end

    subgraph "Review Chain Pattern"
        R1[Implementation AI] --> R2[Code Review AI]
        R2 --> R3[Security Review AI]
        R3 --> R4[Performance Review AI]
        R4 --> R5[Final Approval AI]
    end

    style S1 fill:#e3f2fd
    style P1 fill:#e8f5e8
    style C1 fill:#fff3e0
    style R1 fill:#f3e5f5
```

## AI Agent Interaction Patterns

The updated system features enhanced AI agent coordination with clear specialization and handoff protocols:

```mermaid
graph LR
    subgraph "AI Agent Orchestration Layer"
        O[BMad AI Agent Orchestrator]
    end

    subgraph "Specialist AI Agents"
        PM[Product Manager AI<br/>John - PRD Creation]
        AR[Architect AI<br/>Fred - Technical Design]
        TB[Task Breakdown Specialist AI<br/>Tyler - Task Analysis]
        DA[Design Architect AI<br/>Jane - Frontend Design]
        AN[Analyst AI<br/>Mary - Research & Analysis]
        PO[Product Owner AI<br/>Sarah - Validation]
    end

    subgraph "Deliverables"
        PRD[prd.md<br/>Product Requirements]
        ARCH[architecture.md<br/>Technical Architecture]
        TASKS[tasks.md<br/>Comprehensive Task Breakdown]
        FRONTEND[Frontend Specifications]
    end

    O --> PM
    O --> AR
    O --> TB
    O --> DA
    O --> AN
    O --> PO

    PM --> PRD
    AR --> ARCH
    TB --> TASKS
    DA --> FRONTEND

    PRD -.-> AR
    ARCH -.-> TB

    style O fill:#e1f5fe
    style PM fill:#f3e5f5
    style AR fill:#e8f5e8
    style TB fill:#fff3e0
    style DA fill:#fce4ec
```

## Available AI Agents

The system includes the following specialized AI agents:

| AI Agent | Name | Specialization | Primary Deliverable |
|----------|------|----------------|-------------------|
| **Product Manager** | John | PRD creation, user needs analysis | `prd.md` |
| **Architect** | Fred | Technical architecture, system design | `architecture.md` |
| **Task Breakdown Specialist** | Tyler | Comprehensive task analysis & breakdown | `tasks.md` |
| **Design Architect** | Jane | UI/UX specifications, frontend architecture | Frontend specs |
| **Analyst** | Mary | Research, brainstorming, requirements gathering | Project briefs |
| **Product Owner** | Sarah | Validation, quality assurance, change management | Quality validation |

## 🚀 Getting Started with Mode Selection System

### Quick Setup (Recommended)

The BMAD AI Agent Orchestration System is designed to work with AI assistants like ChatGPT or Google Gemini. No traditional software installation required!

#### Web Agent Setup (5 minutes)

1. **Navigate to** the `web-build-sample/` directory in this repository
2. **Copy the contents** of `agent-prompt.txt`
3. **Paste into your AI assistant** (ChatGPT Custom GPT or Google Gemini Gem instructions field)
4. **Attach the remaining files** from the `web-build-sample/` folder as knowledge base files
5. **Save your AI agent** with a name like "BMAD AI Agent Orchestrator"
6. **Experience the mode selection** - the system will immediately present the mode selection menu

#### Mode Selection Experience

Once your AI agent orchestrator is set up, every interaction begins with mode selection:

**For Documentation Handoff (Recommended for most users):**
```
Request: "I need complete project documentation for a new e-commerce platform"

System Response: [Mode Selection Menu]
Your Choice: "1" (Documentation Mode)

AI Agent Orchestrator will:
1. Activate Product Manager AI (John) → Creates prd.md
2. Activate Architect AI (Fred) → Creates architecture.md
3. Activate Task Breakdown AI (Tyler) → Creates checklist.md

Result: 3 complete, standalone documents ready for developer handoff
```

**For Full Development (Complete implementation):**
```
Request: "I want to build a complete e-commerce platform"

System Response: [Mode Selection Menu]
Your Choice: "2" (Full Development Mode)

AI Agent Orchestrator will:
1. Coordinate 50+ specialized AI agents
2. Implement complete application with testing
3. Provide fully functional, deployment-ready solution

Result: Complete application with full implementation
```

#### Mode Selection Commands

After setup, you can also use direct commands:

```
/help - View all available commands and mode options
/agent-list - See all 50+ available AI agents (Full Development Mode)
1 or "Documentation Mode" - Generate handoff documents
2 or "Full Development Mode" - Build complete application
```

### AI Agent Coordination Configuration

The system uses configuration files to define AI agent capabilities and workflows:

- **`agent-config.txt`** - Defines all available AI agents and their specializations
- **`personas.txt`** - Contains detailed AI agent personality and capability definitions
- **`tasks.txt`** - Comprehensive task library for AI agent execution
- **`templates.txt`** - Standardized templates for deliverable creation
- **`checklists.txt`** - Quality validation checklists for AI agent workflows

## 🤖 AI Agent Categories Overview

### 🔧 Core Development (12 AI Agents)
Comprehensive application development coverage including frontend, backend, full-stack, mobile, web, API, database, microservices, game, embedded, desktop, and blockchain development AI specialists.

### ⚙️ Infrastructure & Operations (10 AI Agents)
Complete operational excellence with DevOps, SRE, platform, cloud, infrastructure, Kubernetes, network, systems administration, monitoring, and deployment AI specialists.

### 🔒 Security & Compliance (8 AI Agents)
Full security and regulatory coverage including security engineers, cybersecurity analysts, penetration testers, compliance officers, privacy engineers, identity engineers, cryptography engineers, and security architect AI specialists.

### 🤖 Data & AI (8 AI Agents)
Modern data and AI capabilities with data engineers, data scientists, ML engineers, AI engineers, data analysts, database administrators, big data engineers, and MLOps engineer AI specialists.

### ✅ Quality & Testing (6 AI Agents)
Comprehensive quality assurance including QA engineers, test automation engineers, performance engineers, accessibility engineers, usability engineers, and QA manager AI specialists.

### 🎯 Specialized Technical (6 AI Agents)
Advanced technical expertise with solutions architects, technical leads, integration engineers, migration engineers, optimization engineers, and research engineer AI specialists.

**Total System Capacity:**
- **50+ Specialized AI Agents** across all domains
- **200+ Granular Tasks** with detailed specifications
- **Intelligent AI Agent Orchestration** with adaptive learning
- **Enterprise-Ready** scalability and reliability

[More Documentation, Explanations, and IDE Specifics](docs/readme.md) available here!

## ✨ Key Features

### 🧠 Intelligent AI Agent Selection
- **Multi-Criteria Algorithm**: 40% expertise match, 20% secondary skills, 15% experience level
- **Workload Balancing**: Considers AI agent availability and capacity
- **Collaboration History**: Leverages past successful AI agent team combinations
- **Context Awareness**: Adapts selection based on project requirements and constraints

### 🔄 AI Agent Workflow Orchestration
- **Dynamic Task Sequencing**: Optimizes task order for efficiency and dependencies
- **Parallel Execution**: Maximizes throughput through intelligent AI agent parallelization
- **Quality Gate Integration**: Embedded validation checkpoints throughout AI agent workflows
- **Adaptive Learning**: Continuously improves based on AI agent outcome analysis

### 🛡️ Quality Assurance Integration
- **Built-in Quality Gates**: Code review, security scan, performance testing
- **Comprehensive Validation**: Multi-layer validation with specialized AI agents
- **Metrics and KPIs**: Quality metrics tracking and continuous improvement
- **Risk Mitigation**: Proactive risk identification and mitigation strategies

### 📈 Enterprise Readiness
- **Scalable Architecture**: Handles projects from MVP to enterprise scale
- **Security First**: Comprehensive security integration throughout all AI agent workflows
- **Compliance Support**: Built-in compliance validation and audit trails
- **Integration Capabilities**: Seamless integration with existing development tools

## 📚 AI Agent Orchestration Documentation

### Core AI Agent System Files
Essential files for understanding and configuring the AI agent orchestration system:

- **[AI Agent Configuration](web-build-sample/agent-config.txt)** - Complete AI agent roster and capabilities
- **[AI Agent Personas](web-build-sample/personas.txt)** - Detailed AI agent personality definitions
- **[Task Library](web-build-sample/tasks.txt)** - Comprehensive task specifications for AI agents
- **[Templates](web-build-sample/templates.txt)** - Standardized templates for deliverable creation
- **[Quality Checklists](web-build-sample/checklists.txt)** - Validation frameworks for AI agent workflows

### AI Agent Orchestration Guides
- **[Comprehensive Deliverable Workflow](codemad-agent/comprehensive-deliverable-workflow.md)** - Complete guide to three-deliverable creation process
- **[AI Agent Orchestration Correction Summary](AI_AGENT_ORCHESTRATION_CORRECTION_SUMMARY.md)** - Details of system corrections and enhancements

### Individual AI Agent Documentation
- **[AI Agent Personas](codemad-agent/personas/)** - Individual AI agent personalities and capabilities
- **[Task Specifications](codemad-agent/tasks/)** - Detailed task requirements and deliverables
- **[Templates](codemad-agent/templates/)** - Standardized documentation templates
- **[Checklists](codemad-agent/checklists/)** - Quality validation checklists

### Setup and Configuration
- **[Web Build Sample](web-build-sample/)** - Complete AI agent orchestrator setup files
- **[Original BMAD Method](docs/readme.md)** - Original method documentation and IDE specifics
- **[Contributing Guidelines](docs/CONTRIBUTING.md)** - How to contribute to the AI agent system

## 🤝 Contributing to AI Agent Orchestration

We welcome contributions to the BMAD AI Agent Orchestration System! Here's how you can help enhance our AI agent capabilities:

### Adding New AI Agents

1. **Create AI Agent Persona**
   - Define AI agent personality, expertise, and communication style
   - Add to `codemad-agent/personas/new-agent-name.md`
   - Include specialization areas and confidence levels

2. **Define AI Agent Capabilities**
   - Specify core technologies and expertise domains
   - Define collaboration patterns with other AI agents
   - List primary deliverables and output formats

3. **Create AI Agent Tasks**
   - Develop 4-8 specialized tasks for the AI agent
   - Add to `codemad-agent/tasks/` directory
   - Ensure tasks are optimized for AI agent context windows

4. **Update Configuration Files**
   - Add AI agent to `web-build-sample/agent-config.txt`
   - Update `web-build-sample/personas.txt` with full persona definition
   - Add tasks to `web-build-sample/tasks.txt`

### Enhancing AI Agent Workflows

1. **Task Optimization**
   - Improve task specifications for better AI agent execution
   - Add quality gates and validation checkpoints
   - Optimize for AI agent context window limitations

2. **Template Development**
   - Create standardized templates for new deliverable types
   - Add to `web-build-sample/templates.txt`
   - Ensure templates support AI agent workflow patterns

3. **Quality Assurance**
   - Develop comprehensive checklists for AI agent validation
   - Add to `web-build-sample/checklists.txt`
   - Include AI agent-specific quality criteria

### AI Agent System Standards

- **Documentation**: All AI agents must include comprehensive persona definitions and task specifications
- **Quality Gates**: Include validation checkpoints optimized for AI agent workflows
- **Testing**: Validate AI agent personas through pilot implementations with real AI assistants
- **Consistency**: Follow established patterns for AI agent coordination and handoffs

### Review Process for AI Agent Enhancements

1. **Fork the repository** and create a feature branch
2. **Implement AI agent enhancements** following the contribution guidelines
3. **Test with AI assistants** (ChatGPT, Gemini) to validate functionality
4. **Create pull request** with detailed description of AI agent capabilities
5. **Community review** of AI agent design and implementation
6. **Integration testing** with existing AI agent orchestration system

### Getting Help with AI Agent Development

- **GitHub Issues**: Report AI agent bugs or request new AI agent capabilities
- **Discussions**: Join community discussions about AI agent design patterns
- **Documentation**: Refer to AI agent orchestration guides and examples
- **Community**: Connect with other AI agent developers and users

## 📊 AI Agent Orchestration Success Metrics

### Expected AI Agent Coordination Outcomes
- **Comprehensive Documentation Delivery** - Complete prd.md, architecture.md, and tasks.md creation
- **AI Agent Workflow Efficiency** - Optimized task handoffs between specialized AI agents
- **Quality Assurance Integration** - Built-in validation throughout AI agent collaboration
- **Context Window Optimization** - Tasks sized appropriately for AI agent capabilities
- **Consistent AI Agent Performance** - Reliable deliverable quality across all AI agent types

### AI Agent System Performance Targets
- **Immediate AI Agent Activation** - Instant persona switching and task assignment
- **100% AI Agent Capability Coverage** - All project requirements addressable by available AI agents
- **Comprehensive Deliverable Quality** - Complete, actionable documentation from AI agent collaboration
- **User Satisfaction with AI Agent Coordination** - Effective orchestration and clear AI agent specialization

## 🚀 Quick Start with Mode Selection System

For immediate hands-on experience with the new mode selection system:

1. **Navigate to** `web-build-sample/` directory
2. **Copy contents** of `agent-prompt.txt` into your AI assistant (Gemini or ChatGPT) custom instructions
3. **Attach remaining files** (`agent-config.txt`, `personas.txt`, `tasks.txt`, `templates.txt`, `checklists.txt`) as knowledge base
4. **Experience mode selection** - the system will immediately present the mandatory mode selection menu
5. **Try Documentation Mode (1)** to generate 3 complete handoff documents (prd.md, architecture.md, checklist.md)
6. **Try Full Development Mode (2)** to access 50+ specialized AI agents for complete application development
7. **Use** `/help` command to explore all capabilities after mode selection

**Key Benefits:**
- **No more automatic development** - you choose what you need
- **Perfect for AI platforms** like Gemini Gems where you want documentation, not code
- **Professional handoff documents** ready for VS Code developers
- **Complete development option** still available when needed

This provides instant access to both documentation generation and full AI agent orchestration capabilities with explicit user control over the workflow.

---

**Ready to experience intelligent AI agent orchestration for your projects?** 🤖

[Get Started with AI Agents](#-getting-started-with-ai-agent-orchestration) | [View AI Agent Documentation](#-ai-agent-orchestration-documentation) | [Join Community](https://github.com/usemanusai/CodeMAD/discussions) | [Report Issues](https://github.com/usemanusai/CodeMAD/issues)
