# AgentCores Test Documentation

## Quick Start
```python
from agentCores import agentCores

# Default MongoDB connection
core = agentCores()

# Custom MongoDB connection
custom_core = agentCores(connection_uri="mongodb://customhost:27017/")
```

## Custom Database Configuration

### Specifying Custom Database Paths
```python
from agentCores import agentCores

# Custom database configuration
custom_db_paths = {
    "system": {
        "agent_matrix": "my_agent_matrix",
        "documentation": "my_docs",
        "templates": "my_templates",
        "template_files": "my_template_files"
    },
    "agents": {
        "conversation": "my_conversations_{agent_id}",
        "knowledge": "my_knowledge_{agent_id}",
        "designPatterns": "my_patterns_{agent_id}",
        "research_collection": "my_research_{agent_id}",
        "embeddings": "my_embeddings_{agent_id}"
    },
    "shared": {
        "global_knowledge": "my_global_knowledge",
        "models": "my_model_configs", 
        "prompts": "my_prompt_templates"
    }
}

# Initialize with custom paths
core = agentCores(
    connection_uri="mongodb://localhost:27017/",
    custom_db_paths=custom_db_paths
)
```

### Creating an Agent with Custom Collections
```python
# Create agent with custom database config
agent = core.mintAgent(
    agent_id="custom_research_assistant",
    db_config={
        "custom_collection": "my_special_collection",
        "research_data": "my_research_data"
    },
    model_config={
        "largeLanguageModel": {
            "names": ["phi3"],
            "instances": None,
            "model_config_template": {}
        }
    }
)
```

## Testing Guide

### Unit Tests
Create `tests/test_agentCores.py`:
```python
import pytest
from agentCores import agentCores

def test_agent_creation():
    core = agentCores()
    agent = core.mintAgent("test_agent")
    assert agent["agentCore"]["identifyers"]["agent_id"] == "test_agent"
    assert agent["agentCore"]["version"] == 1

def test_custom_database():
    custom_paths = {
        "system": {"agent_matrix": "test_matrix"},
        "agents": {"conversation": "test_conv_{agent_id}"},
        "shared": {"global_knowledge": "test_knowledge"}
    }
    core = agentCores(custom_db_paths=custom_paths)
    assert core.db_paths["system"]["agent_matrix"] == "test_matrix"

def test_template_creation():
    core = agentCores()
    template = {
        "models": {"largeLanguageModel": {"names": ["test_model"]}},
        "prompts": {"userInput": "Test prompt"}
    }
    template_id = core.register_template("test_template", template)
    assert template_id is not None

@pytest.fixture
def test_core():
    return agentCores(connection_uri="mongodb://localhost:27017/test_db")

def test_agent_migration(test_core):
    # Create old format agent
    old_agent = {...}  # Old format
    test_core.storeAgentCore("test_migration", old_agent)
    
    # Run migration
    test_core.migrateAgentCores()
    
    # Verify new format
    migrated = test_core.loadAgentCore("test_migration")
    assert "identifyers" in migrated["agentCore"]
    assert "databases" in migrated["agentCore"]
```

### Integration Tests
Create `tests/test_integration.py`:
```python
import pytest
from agentCores import agentCores
from .researchAssistant import researchAssistant

def test_research_assistant_creation():
    assistant = researchAssistant(agent_id="test_assistant")
    assert assistant.agent["agentCore"]["identifyers"]["agent_id"] == "test_assistant"

def test_search_and_store():
    assistant = researchAssistant()
    results = assistant.search("test query")
    assert len(results) > 0
    
    # Verify storage
    stored = assistant.get_recent_research("test query")
    assert len(stored) > 0

def test_conversation_flow():
    assistant = researchAssistant()
    response = assistant.process_query("What is Python?")
    assert response is not None
    assert len(response) > 0
```

## Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests with coverage
pytest tests/ --cov=agentCores

# Run specific test file
pytest tests/test_agentCores.py

# Run with detailed output
pytest -v tests/
```

## Best Practices

### Database Management
1. Always use unique collection names for each agent
2. Implement proper indexes for frequently queried fields
3. Use the databaseManager for optimizations
4. Implement cleanup strategies for old data

### Template Management
1. Register templates before creating agents
2. Use version control for templates
3. Document template changes
4. Test templates before deployment

### Error Handling
1. Implement proper exception handling
2. Log errors and warnings
3. Provide meaningful error messages
4. Include error recovery strategies

## Common Patterns

### Creating a Custom Agent
```python
def create_specialized_agent(name, model, prompt):
    core = agentCores()
    
    # Create custom template
    template = {
        "models": {
            "largeLanguageModel": {
                "names": [model],
                "instances": None
            }
        },
        "prompts": {
            "userInput": prompt,
            "agent": {
                "llmSystem": "Custom system prompt",
                "llmBooster": "Custom booster"
            }
        }
    }
    
    # Register template
    template_id = core.register_template(f"{name}_template", template)
    
    # Create agent
    return core.mintAgent(name, template=template)
```

### Implementing Custom Collections
```python
def setup_custom_collections(core, agent_id):
    # Create specialized collections
    core.createDatabase(
        f"analytics_{agent_id}",
        indexes=[
            [("timestamp", -1)],
            [("metric", 1)],
            [("value", 1)]
        ]
    )
    
    core.createDatabase(
        f"cache_{agent_id}",
        indexes=[
            [("key", 1)],
            [("expiry", 1)]
        ]
    )
    
    # Link collections to agent
    core.linkDatabase(agent_id, "analytics")
    core.linkDatabase(agent_id, "cache")
```

## Contributing
1. Follow PEP 8 style guide
2. Add tests for new features
3. Update documentation
4. Use type hints
5. Include docstrings
