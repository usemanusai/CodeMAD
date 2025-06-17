# Checklist Mappings Documentation

This document describes the mapping between checklists and their required documentation files for the BMAD agent system.

## Architect Checklist
- **Checklist File:** `docs/checklists/architect-checklist.md`
- **Required Documents:**
  - `architecture.md`
- **Default Locations:**
  - `docs/architecture.md`

## Platform Engineer Checklist
- **Checklist File:** `docs/checklists/infrastructure-checklist.md`
- **Required Documents:**
  - `platform-architecture.md`
- **Default Locations:**
  - `docs/platform-architecture.md`

## Frontend Architecture Checklist
- **Checklist File:** `docs/checklists/frontend-architecture-checklist.md`
- **Required Documents:**
  - `frontend-architecture.md`
- **Default Locations:**
  - `docs/frontend-architecture.md`
  - `docs/fe-architecture.md`

## Project Manager Checklist
- **Checklist File:** `docs/checklists/pm-checklist.md`
- **Required Documents:**
  - `prd.md`
- **Default Locations:**
  - `docs/prd.md`

## Product Owner Master Checklist
- **Checklist File:** `docs/checklists/po-master-checklist.md`
- **Required Documents:**
  - `prd.md`
  - `architecture.md`
- **Optional Documents:**
  - `frontend-architecture.md`
- **Default Locations:**
  - `docs/prd.md`
  - `docs/frontend-architecture.md`
  - `docs/architecture.md`

## Story Draft Checklist
- **Checklist File:** `docs/checklists/story-draft-checklist.md`
- **Required Documents:**
  - `story.md`
- **Default Locations:**
  - `docs/stories/*.md`

## Story Definition of Done Checklist
- **Checklist File:** `docs/checklists/story-dod-checklist.md`
- **Required Documents:**
  - `story.md`
- **Default Locations:**
  - `docs/stories/*.md`

## Usage Notes

This mapping system helps ensure that the appropriate documentation is available when running specific checklists. Each checklist may require certain documents to be present and will look for them in the specified default locations.

### File Path Conventions
- All checklist files are stored in `docs/checklists/`
- Documentation files are typically stored in `docs/`
- Story files are organized in `docs/stories/`
- Architecture documents follow the pattern `*-architecture.md`
