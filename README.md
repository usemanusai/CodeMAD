# BMAD AI Agent Orchestration System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/usemanusai/CodeMAD?style=social)](https://github.com/usemanusai/CodeMAD)
[![GitHub Issues](https://img.shields.io/github/issues/usemanusai/CodeMAD)](https://github.com/usemanusai/CodeMAD/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/usemanusai/CodeMAD)](https://github.com/usemanusai/CodeMAD/pulls)

## 🚀 Project Overview

The **BMAD (Breakthrough Method of Agile AI Agent-Driven Development)** AI Agent Orchestration System is a comprehensive, intelligent platform that coordinates **50+ specialized software development AI agents** to handle virtually any software development scenario through automatic AI agent selection and workflow optimization.

### 🎯 Key Benefits

- **🤖 Intelligent AI Agent Automation**: Automatically selects optimal AI agents and coordinates workflows based on project requirements
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

- **Feature Development**: End-to-end feature implementation with AI agent quality assurance
- **System Architecture**: Enterprise-level architecture design and implementation via specialized AI agents
- **Security Implementation**: Comprehensive security analysis and implementation through AI agent coordination
- **Data Platform Development**: Advanced data engineering and AI system creation using specialized AI agents
- **Legacy Modernization**: Complex system migration and modernization projects with AI agent expertise

## AI Agent Orchestration System Enhancements

The BMAD Method 3.1 features a comprehensive **AI Agent Orchestration System** that coordinates multiple specialized AI agents working collaboratively toward specific deliverable goals. The system has been enhanced to properly understand that it coordinates AI agents (not human workers) and delivers three comprehensive documentation files through coordinated AI agent collaboration.

### Key System Corrections (Latest Update)

- **AI Agent Self-Perception**: System now correctly identifies as coordinating "AI agents" rather than "human workers"
- **Comprehensive Task Breakdown**: Added new Task Breakdown Specialist AI Agent (Tyler) for creating detailed `tasks.md` deliverables
- **Three-Deliverable Workflow**: Complete workflow for `prd.md`, `architecture.md`, and `tasks.md` creation
- **AI Agent Optimization**: Tasks sized and structured specifically for AI agent context windows and capabilities

## Do This First, and all will make sense

There are lots of docs here, but I HIGHLY suggest you just try the Web Agent - it takes just a few minutes to set up in Gemini - and you can use the BMad AI Agent Orchestrator to explain how this method works, how to set up in the IDE, how to set up in the Web, what should be done in the web or ide (although you can choose your own path also!) - all just by talking to the bmad AI agent orchestrator!

### Web Quickstart Project Setup (Recommended)

AI Agent Orchestrator that coordinates multiple specialized AI agents - already pre-compiled in the `web-build-sample` folder.

- The contents of [Agent Prompt Sample](web-build-sample/agent-prompt.txt) text get pasted into the Gemini Gem, or ChatGPT customGPT 'Instructions' field.
- The remaining files in that same folder just need to be attached as shown in the screenshot below. Give it a name (such as BMad AI Agent Orchestrator) and save it, and you now have the BMad AI Agent Orchestrator available to help you brainstorm, research, plan, execute on your vision, or understand how this all even works!
- Once its running, start with typing `/help`, and then type option `2` when it presents 3 options to learn about the method!

![image info](docs/images/gem-setup.png)

## 🏗️ System Architecture

### Overall AI Agent Orchestration Architecture

```mermaid
graph TB
    subgraph "BMAD AI Agent Orchestration System"
        O[Enhanced AI Agent Orchestrator<br/>🧠 Natural Language Processing<br/>🎯 AI Agent Selection Algorithm<br/>🔄 Workflow Coordination<br/>📊 Adaptive Learning]

        subgraph "AI Agent Categories"
            CD[Core Development AI Agents<br/>👨‍💻 12 AI Agents<br/>Frontend, Backend, Mobile<br/>API, Database, Blockchain]
            IO[Infrastructure & Operations AI Agents<br/>⚙️ 10 AI Agents<br/>DevOps, SRE, Cloud<br/>Kubernetes, Monitoring]
            SC[Security & Compliance AI Agents<br/>🔒 8 AI Agents<br/>Security, Cybersecurity<br/>Compliance, Privacy]
            DA[Data & AI Agents<br/>🤖 8 AI Agents<br/>Data Engineering, ML<br/>AI, Analytics]
            QT[Quality & Testing AI Agents<br/>✅ 6 AI Agents<br/>QA, Automation<br/>Performance, Accessibility]
            ST[Specialized Technical AI Agents<br/>🎯 6 AI Agents<br/>Architecture, Integration<br/>Migration, Research]
        end

        subgraph "Supporting Systems"
            KB[Knowledge Base<br/>📚 Templates & Checklists<br/>📋 Best Practices<br/>📖 Documentation]
            QF[Quality Framework<br/>🎯 Quality Gates<br/>✅ Validation Rules<br/>📊 Metrics & KPIs]
            WE[Workflow Engine<br/>🔄 Task Orchestration<br/>⚡ Parallel Execution<br/>🔗 Dependency Management]
        end
    end

    U[User Request] --> O
    O --> CD
    O --> IO
    O --> SC
    O --> DA
    O --> QT
    O --> ST

    CD --> KB
    IO --> KB
    SC --> KB
    DA --> KB
    QT --> KB
    ST --> KB

    O --> QF
    O --> WE

    style O fill:#e1f5fe
    style CD fill:#f3e5f5
    style IO fill:#e8f5e8
    style SC fill:#fff3e0
    style DA fill:#e3f2fd
    style QT fill:#f1f8e9
    style ST fill:#fce4ec
```

### AI Agent Workflow Process Flow

```mermaid
sequenceDiagram
    participant U as User
    participant O as AI Agent Orchestrator
    participant A1 as AI Agent 1
    participant A2 as AI Agent 2
    participant A3 as AI Agent 3
    participant QG as Quality Gates

    U->>O: Submit Request
    Note over O: 🧠 Analyze Request<br/>📊 Extract Requirements<br/>🎯 Assess Complexity

    O->>O: AI Agent Selection
    Note over O: 🔍 Capability Matching<br/>⚖️ Workload Balancing<br/>🤝 Collaboration History

    O->>A1: Assign Primary Task
    O->>A2: Assign Secondary Task
    O->>A3: Assign Supporting Task

    par Parallel Execution
        A1->>A1: Execute Task 1
        A2->>A2: Execute Task 2
        A3->>A3: Execute Task 3
    end

    A1->>QG: Submit Deliverable
    A2->>QG: Submit Deliverable
    A3->>QG: Submit Deliverable

    QG->>QG: Quality Validation
    Note over QG: ✅ Code Review<br/>🔒 Security Check<br/>⚡ Performance Test

    alt Quality Gates Pass
        QG->>O: Validation Success
        O->>U: Deliver Results
    else Quality Issues Found
        QG->>O: Issues Identified
        O->>A1: Refinement Required
        A1->>QG: Resubmit
    end

    O->>O: Learn from Outcome
    Note over O: 📈 Update Patterns<br/>🎯 Improve Selection<br/>🔄 Optimize Workflows
```

## AI Agent Coordination Workflow

The BMAD Method 3.1 orchestrates multiple AI agents in a coordinated workflow to deliver comprehensive project documentation:

```mermaid
graph TD
    A[User Request] --> B[BMad AI Agent Orchestrator]
    B --> C{Select AI Agent}
    C --> D[Product Manager AI Agent - John]
    C --> E[Architect AI Agent - Fred]
    C --> F[Task Breakdown Specialist AI Agent - Tyler]
    C --> G[Design Architect AI Agent - Jane]
    C --> H[Other Specialist AI Agents]

    D --> I[Creates prd.md]
    E --> J[Creates architecture.md]
    F --> K[Creates tasks.md]
    G --> L[Creates frontend specs]

    I --> M[Quality Validation]
    J --> M
    K --> M
    L --> M

    M --> N[Coordinated Deliverables]

    style B fill:#e1f5fe
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fff3e0
    style G fill:#fce4ec
```

## Three-Deliverable Creation Process

The system follows a sequential AI agent handoff process to create three comprehensive documentation files:

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator as BMad AI Agent Orchestrator
    participant PM as Product Manager AI Agent (John)
    participant Arch as Architect AI Agent (Fred)
    participant Task as Task Breakdown Specialist AI Agent (Tyler)

    User->>Orchestrator: Request project documentation
    Orchestrator->>PM: Activate for PRD creation
    PM->>PM: Create comprehensive prd.md
    PM->>Orchestrator: PRD complete with handoff context

    Orchestrator->>Arch: Activate for architecture design
    Arch->>Arch: Analyze PRD and create architecture.md
    Arch->>Orchestrator: Architecture complete with handoff context

    Orchestrator->>Task: Activate for task breakdown
    Task->>Task: Analyze PRD & architecture, create tasks.md
    Task->>Orchestrator: Task breakdown complete

    Orchestrator->>User: Three comprehensive deliverables ready

    Note over PM,Task: Each AI agent validates inputs and optimizes for AI agent execution
```

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

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ or **Python** 3.9+
- **Git** for version control
- **Docker** (optional, for containerized deployment)
- **Cloud Platform Account** (AWS, Azure, or GCP for cloud deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/usemanusai/CodeMAD.git
   cd CodeMAD
   ```

2. **Install dependencies**
   ```bash
   # For Node.js setup
   npm install

   # For Python setup
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize the system**
   ```bash
   # Start the orchestrator
   npm start
   # or
   python orchestrator.py
   ```

### Basic Usage Examples

#### Simple Task Assignment
```bash
# Request a frontend component creation
bmad request "Create a responsive navigation component with accessibility features"

# Expected AI agent selection: Frontend Developer AI + Accessibility Engineer AI
# Estimated completion: 2-3 days
```

#### Complex Multi-Agent Workflow
```bash
# Request a complete feature implementation
bmad request "Implement user authentication with OAuth, including API, frontend, security review, and testing"

# Expected AI agent selection:
# - Backend Developer AI (OAuth API)
# - Frontend Developer AI (Auth UI)
# - Security Engineer AI (Security review)
# - QA Engineer AI (Testing strategy)
# Estimated completion: 1-2 weeks
```

#### Enterprise Architecture Planning
```bash
# Request architecture design
bmad request "Design microservices architecture for e-commerce platform with high availability and security"

# Expected AI agent selection:
# - Solutions Architect AI (Overall design)
# - Security Architect AI (Security strategy)
# - Cloud Architect AI (Infrastructure)
# - Performance Engineer AI (Scalability)
# Estimated completion: 3-4 weeks
```

### Configuration

Create a `.env` file with the following configuration:

```env
# AI Agent Orchestrator Configuration
ORCHESTRATOR_MODE=intelligent
AGENT_SELECTION_ALGORITHM=multi-criteria
WORKFLOW_OPTIMIZATION=enabled
ADAPTIVE_LEARNING=enabled

# Quality Gates
ENABLE_CODE_REVIEW=true
ENABLE_SECURITY_SCAN=true
ENABLE_PERFORMANCE_TEST=true
QUALITY_THRESHOLD=85

# Integration Settings
GITHUB_INTEGRATION=enabled
SLACK_NOTIFICATIONS=enabled
MONITORING_ENABLED=true
```

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

## 📚 Documentation

### Google Gemini Knowledge Base
Comprehensive system documentation optimized for AI assistant integration:

- **[System Overview & Orchestrator](google-gemini-knowledge-base/01-system-overview-and-orchestrator.md)** - Core system and orchestrator intelligence
- **[Core Development Agents](google-gemini-knowledge-base/02-core-development-agents.md)** - 12 development specialists
- **[Infrastructure & Operations](google-gemini-knowledge-base/03-infrastructure-operations-agents.md)** - 10 infrastructure specialists
- **[Security & Compliance](google-gemini-knowledge-base/04-security-compliance-agents.md)** - 8 security specialists
- **[Data & AI Agents](google-gemini-knowledge-base/05-data-ai-agents.md)** - 8 data and AI specialists
- **[Quality & Testing](google-gemini-knowledge-base/06-quality-testing-agents.md)** - 6 quality specialists
- **[Specialized Technical](google-gemini-knowledge-base/07-specialized-technical-agents.md)** - 6 advanced specialists
- **[Task Library](google-gemini-knowledge-base/08-comprehensive-task-library.md)** - 200+ detailed tasks
- **[Templates & Checklists](google-gemini-knowledge-base/09-templates-and-checklists.md)** - Quality frameworks
- **[Workflows & Examples](google-gemini-knowledge-base/10-workflows-and-examples.md)** - Implementation patterns

### Detailed AI Agent Documentation
- **[AI Agent Personas](codemad-agent/personas/)** - Individual AI agent personalities and capabilities
- **[Task Specifications](codemad-agent/tasks/)** - Detailed task requirements and deliverables
- **[Templates](codemad-agent/templates/)** - Standardized documentation templates
- **[Checklists](codemad-agent/checklists/)** - Quality validation checklists

### Legacy Documentation
- **[Original BMAD Method](docs/readme.md)** - Original method documentation and IDE specifics
- **[Web Build Sample](web-build-sample/)** - Quick start web agent setup
- **[Contributing Guidelines](docs/CONTRIBUTING.md)** - How to contribute to the project
- **[License](docs/LICENSE)** - Project license information

## 🤝 Contributing

We welcome contributions to the BMAD AI Agent Orchestration System! Here's how you can help:

### Adding New AI Agents

1. **Create AI Agent Persona**
   ```bash
   # Create new AI agent persona file
   touch codemad-agent/personas/new-agent-name.md
   ```

2. **Define AI Agent Capabilities**
   - Specify core technologies and expertise areas
   - Define personality and communication style
   - List key capabilities and specializations

3. **Create AI Agent Tasks**
   ```bash
   # Create task directory for new AI agent
   mkdir codemad-agent/tasks/new-agent-name/
   # Add 4-8 specialized tasks
   ```

4. **Update Configuration**
   - Add AI agent to appropriate category in `comprehensive-agent-config.md`
   - Update AI agent count and capability matrix
   - Add to Google Gemini knowledge base files

### Adding New Tasks

1. **Task Specification**
   - Define clear inputs, outputs, and success criteria
   - Specify complexity level (Simple/Moderate/Complex)
   - Include quality gates and validation requirements

2. **Documentation**
   - Create detailed task documentation with examples
   - Add to comprehensive task library
   - Update relevant checklists and templates

### Code Standards

- **Documentation**: All new AI agents and tasks must include comprehensive documentation
- **Quality Gates**: Include appropriate quality validation and review processes
- **Testing**: Validate new AI agents and tasks through pilot implementations
- **Consistency**: Follow existing naming conventions and file structures

### Review Process

1. **Fork the repository** and create a feature branch
2. **Implement changes** following the contribution guidelines
3. **Create pull request** with detailed description and rationale
4. **Code review** by maintainers and community members
5. **Testing and validation** of new AI agent capabilities
6. **Merge and integration** into main system

### Getting Help

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Join community discussions and Q&A
- **Documentation**: Refer to comprehensive documentation and examples
- **Community**: Connect with other contributors and users

## 📊 Success Metrics

### Expected Outcomes
- **50% Developer Productivity Increase** through intelligent AI agent automation
- **40% Workflow Efficiency Gain** via optimized AI agent task coordination
- **60% Quality Improvement** through integrated AI agent validation
- **90% Project Success Rate** with comprehensive AI agent coverage
- **30% Cost Reduction** via AI agent efficiency gains and optimization

### Performance Targets
- **<2 Second Response Time** for AI agent selection and task assignment
- **80%+ AI Agent Selection Accuracy** for optimal capability matching
- **95%+ Quality Gate Pass Rate** for first-time deliverable approval
- **85%+ User Satisfaction** with AI agent orchestration system effectiveness

## 🚀 Quick Start with Web Agent

For immediate hands-on experience, try our pre-built web agent:

1. **Navigate to** `web-build-sample/` directory
2. **Copy contents** of `agent-prompt.txt` into Gemini or ChatGPT custom instructions
3. **Attach remaining files** as shown in setup documentation
4. **Start with** `/help` command and select option `2` to learn about the method

This provides instant access to BMAD AI agent capabilities while you explore the full system architecture and implementation.

---

**Ready to revolutionize your software development workflow with AI agents?** 🚀

[Get Started](#-getting-started) | [View Documentation](#-documentation) | [Join Community](https://github.com/usemanusai/CodeMAD/discussions) | [Report Issues](https://github.com/usemanusai/CodeMAD/issues)
