# Configuration Examples

This directory contains example configuration files for SemOps2. These files demonstrate the configuration-driven architecture and can be used as starting points for customization.

## Configuration Loading Hierarchy

SemOps2 uses a layered configuration loading system:

1. **Built-in defaults** - Embedded in the tool itself
2. **Project overrides** - `.semops/` directory at repository root
3. **Explicit config path** - `--config-path` command line argument

## Configuration Files

### Core Configuration
- `entity_types.yaml` - Defines all entity types with namespaces, template bundles, and relationship types
- `expert_types.yaml` - AI expert configurations and capabilities
- `source_types.yaml` - Knowledge source definitions with Haystack-compatible chunking strategies
- `storage_backends.yaml` - Vector stores, graph databases, and storage configurations

### Processing Configuration
- `pipeline_configurations.yaml` - Source ingestion pipeline definitions
- `rag_workflows.yaml` - Retrieval-Augmented Generation workflow configurations

### Complete Examples
- `complete_knowledge_config.yaml` - Production-ready cloud security domain example

## Usage

### Basic Setup
```bash
# Copy example configs to your project
mkdir -p .semops/config
cp examples/config/entity_types.yaml .semops/config/
cp examples/config/source_types.yaml .semops/config/

# Customize for your domain
$EDITOR .semops/config/entity_types.yaml
```

### Override Specific Config
```bash
# Use explicit config path
semops --config-path ./my-custom-config/ domain list

# Or set environment variable
export SEMOPS_CONFIG_PATH=./my-custom-config/
semops domain list
```

### Production Deployment
```bash
# Use complete configuration as base
cp examples/config/complete_knowledge_config.yaml .semops/config/domain_config.yaml

# Customize domains, sources, and expert preferences
$EDITOR .semops/config/domain_config.yaml
```

## Configuration Validation

All configuration files use YAML schemas and are validated at load time:

```bash
# Validate configuration
semops config validate

# Generate JSON schema from protobuf
semops config schema --output-format json
```

## Extending Configuration

### Adding New Entity Types
1. Edit `entity_types.yaml` to add your new type
2. Create corresponding template in `.semops/templates/`
3. CLI commands are auto-generated

### Adding New Source Types
1. Edit `source_types.yaml` to define processing pipeline
2. Configure chunking strategy (token, semantic, code, etc.)
3. Source ingestion works automatically

### Adding New Experts
1. Edit `expert_types.yaml` to define expert capabilities
2. Configure prompts and workflows
3. Analysis commands become available

For detailed documentation, see:
- [docs/ENTITY_CONFIGURATION.md](../../docs/ENTITY_CONFIGURATION.md) - BDD scenarios and configuration schema
- [ARCHITECTURE.md](../../ARCHITECTURE.md) - System architecture and design principles
- [docs/KNOWLEDGE_REPOSITORY_ARCHITECTURE.md](../../docs/KNOWLEDGE_REPOSITORY_ARCHITECTURE.md) - Source ingestion details
