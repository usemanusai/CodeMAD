#!/usr/bin/env python3
"""
Test script for Phase C (Synthesis Layer) components.
Validates integration and functionality of all agent synthesis systems.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'architecture', 'ase'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'architecture', 'ase', 'validators'))

from agent_synthesis_engine import AgentSynthesisEngine, AgentBlueprint
from asset_generator import AssetGenerator
from agent_integration_system import AgentIntegrationSystem
from agent_validator import AgentValidator
from gap_analyzer import AgentGap

def test_agent_synthesis_engine():
    """Test Agent Synthesis Engine functionality."""
    print("=" * 60)
    print("TESTING AGENT SYNTHESIS ENGINE")
    print("=" * 60)
    
    try:
        engine = AgentSynthesisEngine()
        print("✅ Agent Synthesis Engine initialized successfully")
        
        # Create mock gap data
        mock_gap = AgentGap(
            occupation_title="Quantum Computing Specialist",
            domain="Quantum Technology",
            priority_score=0.85,
            market_demand_score=0.80,
            strategic_value_score=0.90,
            similarity_to_existing=0.15,
            gap_rationale="No existing agent covers quantum computing expertise",
            required_capabilities=["Quantum Algorithms", "Quantum Hardware", "Quantum Software", "Research"],
            estimated_effort="Medium effort",
            business_impact="High impact",
            sources=["Gap Analysis System"],
            related_existing_agents=[]
        )
        
        print(f"🔄 Testing agent synthesis for: {mock_gap.occupation_title}")
        
        # Synthesize agent
        blueprint = engine.synthesize_agent(mock_gap)
        
        if blueprint:
            print(f"✅ Agent synthesis successful: {blueprint.agent_id}")
            print(f"   Title: {blueprint.title}")
            print(f"   Name: {blueprint.name}")
            print(f"   Domain: {blueprint.domain}")
            print(f"   Quality Score: {blueprint.quality_score:.3f}")
            print(f"   Specializations: {len(blueprint.specializations)}")
            print(f"   Tasks: {len(blueprint.tasks)}")
            print(f"   Templates: {len(blueprint.templates)}")
            return blueprint
        else:
            print("❌ Agent synthesis failed")
            return None
            
    except Exception as e:
        print(f"❌ Error testing Agent Synthesis Engine: {e}")
        return None

def test_agent_validator():
    """Test Agent Validator functionality."""
    print("\n" + "=" * 60)
    print("TESTING AGENT VALIDATOR")
    print("=" * 60)
    
    try:
        validator = AgentValidator()
        print("✅ Agent Validator initialized successfully")
        
        # Create mock blueprint
        mock_blueprint = AgentBlueprint(
            agent_id="test_validator_agent",
            title="Test Validator Specialist",
            name="Validator Agent",
            description="Agent for testing validation system with comprehensive capabilities",
            domain="Testing & Validation",
            specializations=["Validation", "Testing", "Quality Assurance", "Compliance"],
            key_responsibilities=[
                "Validate system components",
                "Ensure quality standards",
                "Conduct comprehensive testing",
                "Maintain compliance requirements"
            ],
            required_skills=["Testing", "Validation", "Analysis", "Documentation", "Quality Control"],
            persona_content="# Test Validator Specialist\n\n" + "A" * 600,
            tasks=[
                {"name": "System Validation", "description": "Validate system functionality", "type": "validation"},
                {"name": "Quality Testing", "description": "Test quality standards", "type": "testing"}
            ],
            templates=[{"name": "Validation Report Template", "description": "Template for validation reports"}],
            checklists=[{"name": "Validation Checklist", "description": "Checklist for validation processes"}],
            memory_structure={
                "knowledge_graph": {"domain": "Testing"},
                "episodic_memory": {"creation": "test"},
                "working_memory": {}
            },
            quality_score=0.0,  # Will be calculated
            creation_rationale="Created for testing validation system"
        )
        
        print(f"🔄 Testing validation for: {mock_blueprint.agent_id}")
        
        # Validate blueprint
        validation_result = validator.validate_blueprint(mock_blueprint)
        
        print(f"✅ Validation completed")
        print(f"   Valid: {validation_result['is_valid']}")
        print(f"   Quality Score: {validation_result['quality_score']:.3f}")
        print(f"   Errors: {len(validation_result['errors'])}")
        print(f"   Warnings: {len(validation_result['warnings'])}")
        
        if validation_result['errors']:
            print("   Errors found:")
            for error in validation_result['errors'][:3]:
                print(f"     - {error}")
        
        return validation_result['is_valid']
        
    except Exception as e:
        print(f"❌ Error testing Agent Validator: {e}")
        return False

def test_asset_generator():
    """Test Asset Generator functionality."""
    print("\n" + "=" * 60)
    print("TESTING ASSET GENERATOR")
    print("=" * 60)
    
    try:
        generator = AssetGenerator()
        print("✅ Asset Generator initialized successfully")
        
        # Create mock blueprint
        mock_blueprint = AgentBlueprint(
            agent_id="test_asset_agent",
            title="Asset Generation Specialist",
            name="Asset Agent",
            description="Agent for testing asset generation system",
            domain="Asset Management",
            specializations=["Asset Generation", "File Management", "Documentation"],
            key_responsibilities=["Generate assets", "Manage files", "Create documentation"],
            required_skills=["Asset Management", "Documentation", "Organization"],
            persona_content="# Asset Generation Specialist\n\nSpecialist in generating and managing assets.",
            tasks=[{"name": "Generate Assets", "description": "Create required assets", "type": "generation"}],
            templates=[{"name": "Asset Template", "description": "Template for assets"}],
            checklists=[{"name": "Asset Checklist", "description": "Checklist for assets"}],
            memory_structure={
                "knowledge_graph": {"domain": "Assets"},
                "episodic_memory": {"creation": "test"},
                "working_memory": {}
            },
            quality_score=0.85,
            creation_rationale="Created for testing asset generation"
        )
        
        print(f"🔄 Testing asset generation for: {mock_blueprint.agent_id}")
        
        # Generate assets
        generation_result = generator.generate_agent_assets(mock_blueprint)
        
        print(f"✅ Asset generation completed")
        print(f"   Success: {generation_result['success']}")
        print(f"   Generated assets: {len(generation_result['generated_assets'])}")
        
        for asset_type, asset_result in generation_result['generated_assets'].items():
            if isinstance(asset_result, dict) and asset_result.get('success'):
                print(f"   ✅ {asset_type}: Generated successfully")
            else:
                print(f"   ❌ {asset_type}: Generation failed")
        
        return generation_result['success']
        
    except Exception as e:
        print(f"❌ Error testing Asset Generator: {e}")
        return False

def test_agent_integration_system():
    """Test Agent Integration System functionality."""
    print("\n" + "=" * 60)
    print("TESTING AGENT INTEGRATION SYSTEM")
    print("=" * 60)
    
    try:
        integration_system = AgentIntegrationSystem()
        print("✅ Agent Integration System initialized successfully")
        
        # Create mock blueprint
        mock_blueprint = AgentBlueprint(
            agent_id="test_integration_agent_2",
            title="Integration Test Specialist v2",
            name="Integration Agent v2",
            description="Agent for testing integration system version 2",
            domain="Integration Testing",
            specializations=["Integration", "Testing", "Validation", "System Integration"],
            key_responsibilities=["Test integrations", "Validate systems", "Ensure compatibility"],
            required_skills=["Integration Testing", "System Validation", "Quality Assurance", "Documentation"],
            persona_content="# Integration Test Specialist v2\n\n" + "A" * 600,
            tasks=[
                {"name": "Integration Testing", "description": "Test system integrations", "type": "testing"},
                {"name": "System Validation", "description": "Validate integrated systems", "type": "validation"}
            ],
            templates=[{"name": "Integration Report Template", "description": "Template for integration reports"}],
            checklists=[{"name": "Integration Checklist", "description": "Checklist for integration processes"}],
            memory_structure={
                "knowledge_graph": {"domain": "Integration"},
                "episodic_memory": {"creation": "test"},
                "working_memory": {}
            },
            quality_score=0.88,
            creation_rationale="Created for testing integration system v2"
        )
        
        print(f"🔄 Testing integration for: {mock_blueprint.agent_id}")
        
        # Integrate agent
        integration_result = integration_system.integrate_agent(mock_blueprint)
        
        print(f"✅ Integration completed")
        print(f"   Success: {integration_result['success']}")
        print(f"   Agent ID: {integration_result['agent_id']}")
        print(f"   Integration steps: {len(integration_result['integration_steps'])}")
        
        for step_name, step_result in integration_result['integration_steps'].items():
            status = "✅" if step_result.get('success', False) else "❌"
            print(f"   {status} {step_name}: {'Passed' if step_result.get('success', False) else 'Failed'}")
        
        return integration_result['success']
        
    except Exception as e:
        print(f"❌ Error testing Agent Integration System: {e}")
        return False

def test_end_to_end_synthesis():
    """Test end-to-end agent synthesis workflow."""
    print("\n" + "=" * 60)
    print("TESTING END-TO-END SYNTHESIS WORKFLOW")
    print("=" * 60)
    
    try:
        # Step 1: Create gap data (from Phase B)
        print("🔄 Step 1: Gap Analysis Input")
        gap_data = AgentGap(
            occupation_title="Sustainable Energy Analyst",
            domain="Renewable Energy",
            priority_score=0.88,
            market_demand_score=0.85,
            strategic_value_score=0.90,
            similarity_to_existing=0.20,
            gap_rationale="Growing demand for sustainable energy analysis expertise",
            required_capabilities=["Energy Analysis", "Sustainability", "Data Analysis", "Policy Knowledge"],
            estimated_effort="Medium effort",
            business_impact="High impact",
            sources=["Gap Analysis System"],
            related_existing_agents=[]
        )
        print(f"   ✅ Gap identified: {gap_data.occupation_title}")
        
        # Step 2: Agent synthesis
        print("🔄 Step 2: Agent Synthesis")
        engine = AgentSynthesisEngine()
        blueprint = engine.synthesize_agent(gap_data)
        
        if not blueprint:
            print("   ❌ Agent synthesis failed")
            return False
        
        print(f"   ✅ Agent synthesized: {blueprint.agent_id} (Quality: {blueprint.quality_score:.3f})")
        
        # Step 3: Asset generation
        print("🔄 Step 3: Asset Generation")
        generator = AssetGenerator()
        asset_result = generator.generate_agent_assets(blueprint)
        
        if not asset_result['success']:
            print("   ❌ Asset generation failed")
            return False
        
        print(f"   ✅ Assets generated: {len(asset_result['generated_assets'])} types")
        
        # Step 4: Integration
        print("🔄 Step 4: System Integration")
        integration_system = AgentIntegrationSystem()
        integration_result = integration_system.integrate_agent(blueprint)
        
        if not integration_result['success']:
            print("   ❌ Integration failed")
            return False
        
        print(f"   ✅ Agent integrated successfully: {integration_result['agent_id']}")
        
        print("\n✅ End-to-end synthesis workflow completed successfully!")
        print(f"🎉 New agent created: {blueprint.title}")
        print(f"📊 Final Quality Score: {blueprint.quality_score:.3f}")
        print(f"🏆 Integration Status: Active")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in end-to-end synthesis: {e}")
        return False

def main():
    """Run all Phase C tests."""
    print("🚀 STARTING PHASE C (SYNTHESIS LAYER) TESTING")
    print("=" * 80)
    
    results = {
        'agent_synthesis_engine': False,
        'agent_validator': False,
        'asset_generator': False,
        'agent_integration_system': False,
        'end_to_end_synthesis': False
    }
    
    # Test individual components
    blueprint = test_agent_synthesis_engine()
    results['agent_synthesis_engine'] = blueprint is not None
    
    results['agent_validator'] = test_agent_validator()
    results['asset_generator'] = test_asset_generator()
    results['agent_integration_system'] = test_agent_integration_system()
    results['end_to_end_synthesis'] = test_end_to_end_synthesis()
    
    # Summary
    print("\n" + "=" * 80)
    print("PHASE C TESTING SUMMARY")
    print("=" * 80)
    
    passed = sum(results.values())
    total = len(results)
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component.replace('_', ' ').title()}: {'PASSED' if status else 'FAILED'}")
    
    print(f"\n📊 Overall Result: {passed}/{total} components passed")
    
    if passed == total:
        print("🎉 Phase C (Synthesis Layer) implementation is SUCCESSFUL!")
        print("🚀 Ready to proceed to Phase D (Orchestration Layer)")
    else:
        print("⚠️  Some components need attention before proceeding")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
