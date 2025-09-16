# Migration Plan: SemOps v1 → SemOps v2

## Overview

This document outlines the strategy for migrating from the current entity-specific service architecture to the new generic, configuration-driven architecture.

## Migration Phases

### Phase 1: Foundation & Configuration System
**Goal**: Build core configuration and model infrastructure

#### Tasks
- [ ] Create entity type configuration system
- [ ] Implement `EntityType` and `EntityConfig` models
- [ ] Build configuration loader and validator
- [ ] Create JSON schema validation for entity types
- [ ] Set up template engine foundation (Jinja2)

#### Deliverables
- `config/entity_types.yaml` with current entity definitions
- `src/models/entity_type.py` - Entity type model
- `src/core/config_manager.py` - Configuration management
- Validation schemas for entity type definitions
- Unit tests for configuration system

#### Success Criteria
- Load and validate existing entity types from configuration
- Configuration validation catches invalid definitions
- Template engine can process basic Jinja2 templates

### Phase 2: Generic Entity Service
**Goal**: Replace entity-specific services with generic EntityService

#### Tasks
- [ ] Implement generic `EntityService` class
- [ ] Port context detection from v1 `ContextDetector`
- [ ] Build template processing and document generation
- [ ] Implement file system utilities and frontmatter handling
- [ ] Create entity CRUD operations (list, get, create, analyze)

#### Deliverables
- `src/core/entity_service.py` - Generic entity operations
- `src/core/template_engine.py` - Template processing
- `src/core/context_detector.py` - Context detection
- `src/utils/` - File utilities and frontmatter handling
- Integration tests with real templates and data

#### Success Criteria
- EntityService can perform all operations for domain/problem/persona/product
- Context detection works equivalently to v1
- Template processing generates valid documents with frontmatter

### Phase 3: Dynamic CLI System
**Goal**: Replace hardcoded CLI commands with auto-generated commands

#### Tasks
- [ ] Implement dynamic command generation from configuration
- [ ] Create context-aware parameter resolution
- [ ] Build output formatters for different entity types
- [ ] Port error handling with helpful hints
- [ ] Add comprehensive CLI testing framework

#### Deliverables
- `src/cli/dynamic_commands.py` - Command generation
- `src/cli/formatters.py` - Output formatting
- Auto-generated CLI commands for all entity types
- Comprehensive error handling and hints
- CLI integration tests

#### Success Criteria
- CLI commands work identically to v1 for existing entity types
- New entity types automatically get full CLI support
- Error messages and hints match v1 quality
- All output formats (table, JSON, YAML) work correctly

### Phase 4: Template Migration & Extension
**Goal**: Migrate existing templates and add new entity types

#### Tasks
- [ ] Convert existing templates to Jinja2 format
- [ ] Migrate domain/problem/persona/product templates
- [ ] Add solution and feature entity types as examples
- [ ] Validate template compatibility and variable mapping
- [ ] Update guidance and suggestion templates

#### Deliverables
- `config/templates/` with migrated Jinja2 templates
- Solution and feature entity type definitions
- Template validation and testing framework
- Updated guidance templates for all entity types

#### Success Criteria
- All existing templates work with new system
- Generated documents are identical to v1 output
- New entity types (solution, feature) work end-to-end
- Template validation catches errors early

### Phase 5: Data Migration & Testing
**Goal**: Ensure existing data works with new system

#### Tasks
- [ ] Create data migration utilities
- [ ] Test with existing domain/problem/persona data
- [ ] Performance testing with large entity sets
- [ ] Comprehensive integration testing
- [ ] Documentation and user guides

#### Deliverables
- Data migration scripts and utilities
- Performance benchmarks and optimization
- Full integration test suite
- Updated user documentation and migration guide
- Compatibility verification with existing data

#### Success Criteria
- All existing SemOps v1 data works with v2
- Performance is equivalent or better than v1
- No data loss or corruption during migration
- Complete test coverage for all functionality

## Backward Compatibility Strategy

### Configuration Compatibility
- **Entity IDs**: Preserve existing ID formats (DOM-, PROB-, PERS-, PROD-)
- **File Structures**: Maintain existing directory layouts and filenames
- **Templates**: Ensure generated documents match v1 output exactly
- **CLI Interface**: Keep same command patterns and parameter names

### Data Compatibility
- **YAML Frontmatter**: Preserve all existing metadata fields
- **File Locations**: Keep files in same directories
- **Cross-References**: Maintain all entity relationship links
- **Source References**: Preserve source citations and links

### API Compatibility
- **MCP Server**: Maintain same tool definitions and responses
- **REST API**: Keep same endpoint structures and data formats
- **Service Interfaces**: Preserve public method signatures where possible

## Risk Mitigation

### Technical Risks
- **Template Complexity**: Start with simple templates, gradually add complexity
- **Performance Regression**: Benchmark early and optimize proactively
- **Configuration Errors**: Comprehensive validation and clear error messages
- **Data Loss**: Extensive testing with backup/restore procedures

### User Experience Risks
- **Learning Curve**: Maintain familiar CLI patterns and commands
- **Feature Parity**: Ensure v2 has all v1 functionality before migration
- **Documentation Gap**: Update docs alongside implementation
- **Migration Friction**: Provide automated migration tools

## Migration Testing Strategy

### Unit Testing
- Test each component in isolation
- Mock file system and configuration dependencies
- Validate configuration loading and validation
- Test template processing with various inputs

### Integration Testing
- Test complete workflows end-to-end
- Use real templates and entity data
- Validate CLI command generation and execution
- Test context detection with real directory structures

### Compatibility Testing
- Compare v1 and v2 outputs for identical inputs
- Test with existing domain/problem/persona data
- Verify all CLI commands produce equivalent results
- Validate MCP server tool compatibility

### Performance Testing
- Benchmark entity operations against v1 baseline
- Test with large numbers of entities and templates
- Memory and CPU usage profiling
- CLI response time measurements

## Rollback Strategy

### Development Environment
- **Feature Flags**: Allow switching between v1 and v2 services
- **Parallel Development**: Maintain v1 codebase during v2 development
- **Configuration Toggle**: Runtime switching between architectures

### Production Migration
- **Blue-Green Deployment**: Run v1 and v2 in parallel
- **Data Backup**: Complete backup before any migration
- **Incremental Migration**: Migrate entity types one at a time
- **Rollback Triggers**: Clear criteria for reverting to v1

## Success Metrics

### Functional Success
- [ ] All v1 functionality available in v2
- [ ] New entity types (solution, feature) work end-to-end
- [ ] CLI commands generate identical output to v1
- [ ] All existing data migrates successfully

### Technical Success
- [ ] Single EntityService handles all entity types
- [ ] Configuration-driven entity type definitions
- [ ] Auto-generated CLI commands from configuration
- [ ] Template-based document generation

### User Experience Success
- [ ] No change to user workflow or commands
- [ ] Better error messages and hints
- [ ] Faster response times for common operations
- [ ] Easy addition of custom entity types

## Timeline

### Phase 1 - Foundation (Weeks 1-2)
- Configuration system and models
- Template engine foundation
- Basic validation framework

### Phase 2 - Core Services (Weeks 3-4)
- Generic EntityService implementation
- Context detection and file operations
- Template processing and document generation

### Phase 3 - CLI System (Weeks 5-6)
- Dynamic command generation
- Output formatting and error handling
- CLI integration testing

### Phase 4 - Template Migration (Weeks 7-8)
- Convert existing templates
- Add new entity types
- Template validation and testing

### Phase 5 - Integration & Testing (Weeks 9-10)
- Data migration utilities
- Performance testing and optimization
- Documentation and user guides

## Post-Migration Benefits

### For Developers
- **Reduced Codebase**: Single service instead of multiple entity services
- **Easier Maintenance**: Configuration changes instead of code changes
- **Consistent Patterns**: Same operations across all entity types
- **Better Testing**: Generic tests work for all entity types

### For Users
- **More Entity Types**: Easy addition of solutions, features, etc.
- **Consistent CLI**: Same patterns work for all entities
- **Better Performance**: Optimized generic operations
- **Enhanced Flexibility**: Custom entity types without code changes

### For System Evolution
- **Rapid Prototyping**: Quick experimentation with new entity structures
- **Simplified Architecture**: Fewer components and dependencies
- **Configuration Management**: Centralized entity type definitions
- **Future-Proof Design**: Extensible without architectural changes