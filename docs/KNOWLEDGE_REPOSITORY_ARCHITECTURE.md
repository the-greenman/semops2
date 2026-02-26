# Knowledge Repository Architecture - Generic RAG Framework

## Overview

SemOps2's knowledge repository provides a generic, extensible framework for managing diverse knowledge sources and retrieval methods. Instead of the current hardcoded external/internal source types and single ChromaDB vector store, the new system supports unlimited source types, multiple storage backends (vector, graph, hybrid), and configurable processing pipelines.

Persistence invariant (ADR-0001): canonical operational records remain markdown + frontmatter documents. Knowledge graph, entity graph, and vector stores are derived projections for retrieval and traversal, maintained synchronously or via durable queued reconciliation.

### Runtime Baseline (Haystack)

SemOps2 standardizes on **Haystack** as the primary RAG pipeline orchestration layer. Source ingestion, chunking, retrieval, and ranking pipelines are implemented through SemOps adapters that wrap Haystack components.

Design constraints:
- Haystack usage stays behind SemOps interfaces (`KnowledgeService`, `RAGPipelineExecutor`, and adapter boundaries).
- Pipeline behavior remains configuration-driven via `.semops/config/*` files.
- Vector backend choice remains environment-specific (e.g., Chroma for local development, Qdrant for production) without changing domain-level behavior.

## Current RAG System Problems

### Hardcoded Source Types
```python
# Current rigid categorization
source_types = ["external", "internal"]  # Only 2 types supported
processing = {
    "external": web_download_pipeline,
    "internal": file_scan_pipeline    # Very limited
}
```

### Single Storage Backend
```python
# Only ChromaDB + sentence-transformers
vector_store = ChromaDB(embedding_model="sentence-transformers/all-MiniLM-L6-v2")
# No graph relationships, no multi-modal, no hybrid approaches
```

### Fixed Processing Pipeline
```python
# Rigid pipeline: URL → Download → Text → Chunk → Embed → Store
# No support for: APIs, structured data, images, code, real-time feeds, etc.
```

### Limited Retrieval Methods
- Only semantic similarity search
- No graph traversal
- No hybrid vector+graph retrieval
- No multi-modal search
- No context-aware retrieval

## SemOps2 Generic Knowledge Repository

### Source Type Configuration System

```yaml
# .semops/config/source_types.yaml
source_types:
  # Web Content Sources
  web_content:
    name: "Web Content"
    description: "HTML pages, articles, documentation sites"
    icon: "🌐"

    # Processing Pipeline
    pipeline:
      - extractor: "web_html_extractor"
      - processor: "markdown_converter"
      - chunker: "semantic_chunker"
      - enricher: "metadata_enricher"

    # Storage Configuration
    storage:
      primary: "vector_store"
      secondary: ["graph_store"]  # Optional graph relationships

    # Supported Protocols
    protocols: ["http", "https"]
    mime_types: ["text/html", "application/xhtml+xml"]

    # Processing Options
    options:
      chunk_size: 1000
      overlap: 100
      extract_links: true
      preserve_structure: true

  # Document Sources
  documents:
    name: "Documents"
    description: "PDFs, Word docs, presentations"
    icon: "📄"

    pipeline:
      - extractor: "document_extractor"  # Handles PDF, DOCX, PPTX
      - processor: "text_processor"
      - chunker: "document_aware_chunker"
      - enricher: ["metadata_enricher", "document_structure_enricher"]

    storage:
      primary: "vector_store"
      secondary: ["document_graph"]

    protocols: ["file", "http", "https"]
    mime_types:
      - "application/pdf"
      - "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      - "application/vnd.ms-powerpoint"

  # API Data Sources (NEW)
  api_feeds:
    name: "API Data Feeds"
    description: "REST APIs, GraphQL endpoints, real-time data"
    icon: "🔌"

    pipeline:
      - extractor: "api_extractor"
      - processor: "json_processor"
      - structurer: "schema_mapper"
      - chunker: "data_chunker"

    storage:
      primary: "graph_store"  # APIs often have structured relationships
      secondary: ["vector_store"]

    protocols: ["rest", "graphql", "websocket"]
    authentication: ["bearer", "api_key", "oauth2"]

    options:
      poll_interval: 3600  # seconds
      schema_validation: true
      rate_limiting: true

  # Code Repositories (NEW)
  code_repos:
    name: "Code Repositories"
    description: "GitHub repos, code documentation, examples"
    icon: "💻"

    pipeline:
      - extractor: "git_extractor"
      - processor: "code_processor"
      - chunker: "function_aware_chunker"
      - enricher: ["ast_enricher", "dependency_enricher"]

    storage:
      primary: "graph_store"  # Code has rich relationships
      secondary: ["vector_store"]

    protocols: ["git", "github", "gitlab"]
    languages: ["python", "javascript", "typescript", "go", "rust"]

  # Knowledge Graphs (NEW)
  knowledge_graphs:
    name: "Knowledge Graphs"
    description: "Structured knowledge bases, ontologies"
    icon: "🕸️"

    pipeline:
      - extractor: "rdf_extractor"
      - processor: "graph_processor"
      - mapper: "ontology_mapper"

    storage:
      primary: "graph_store"
      secondary: []  # Pure graph storage

    protocols: ["sparql", "rdf", "owl"]
    formats: ["turtle", "json-ld", "rdf-xml"]

  # Media Sources (NEW)
  media_content:
    name: "Media Content"
    description: "Images, videos, audio with AI analysis"
    icon: "🎬"

    pipeline:
      - extractor: "media_extractor"
      - processor: "multimodal_processor"  # Vision/audio AI models
      - chunker: "temporal_chunker"
      - enricher: "media_metadata_enricher"

    storage:
      primary: "multimodal_store"
      secondary: ["vector_store"]  # Text descriptions go to vector

    protocols: ["http", "file"]
    mime_types:
      - "image/*"
      - "video/*"
      - "audio/*"

  # Internal Sources (Enhanced)
  internal_knowledge:
    name: "Internal Knowledge"
    description: "Meeting notes, decisions, organizational knowledge"
    icon: "🏢"

    pipeline:
      - extractor: "file_extractor"
      - processor: "internal_processor"
      - chunker: "topic_aware_chunker"
      - enricher: ["people_enricher", "decision_enricher"]

    storage:
      primary: "vector_store"
      secondary: ["organizational_graph"]  # People, decisions, relationships

    protocols: ["file", "sharepoint", "confluence", "notion"]

  # Real-time Feeds (NEW)
  realtime_feeds:
    name: "Real-time Data Feeds"
    description: "RSS, news feeds, social media, monitoring"
    icon: "📡"

    pipeline:
      - extractor: "feed_extractor"
      - processor: "stream_processor"
      - chunker: "temporal_chunker"
      - enricher: "trend_enricher"

    storage:
      primary: "time_series_store"
      secondary: ["vector_store"]

    protocols: ["rss", "atom", "websocket", "sse"]

    options:
      retention_policy: "30d"
      real_time: true
      trend_detection: true
```

### Storage Backend Configuration

```yaml
# config/storage_backends.yaml
storage_backends:
  # Vector Stores
  chromadb:
    type: "vector"
    name: "ChromaDB"
    description: "Local persistent vector database"
    embedding_models:
      - "sentence-transformers/all-MiniLM-L6-v2"
      - "sentence-transformers/all-mpnet-base-v2"
      - "text-embedding-ada-002"  # OpenAI
    configuration:
      persist_directory: "{domain_path}/knowledge/.chromadb"
      collection_prefix: "{domain_name}"
    capabilities: ["similarity_search", "metadata_filtering"]

  pinecone:
    type: "vector"
    name: "Pinecone"
    description: "Managed vector database service"
    embedding_models:
      - "text-embedding-ada-002"
      - "text-embedding-3-small"
    configuration:
      api_key_env: "PINECONE_API_KEY"
      environment: "gcp-starter"
    capabilities: ["similarity_search", "metadata_filtering", "namespaces"]

  weaviate:
    type: "vector"
    name: "Weaviate"
    description: "Multi-modal vector database"
    embedding_models:
      - "text2vec-openai"
      - "multi2vec-clip"  # Multi-modal
    configuration:
      url: "http://localhost:8080"
      api_key_env: "WEAVIATE_API_KEY"
    capabilities: ["similarity_search", "hybrid_search", "multimodal"]

  # Graph Stores
  neo4j:
    type: "graph"
    name: "Neo4j"
    description: "Property graph database"
    configuration:
      url: "bolt://localhost:7687"
      auth_env: ["NEO4J_USERNAME", "NEO4J_PASSWORD"]
    capabilities: ["graph_traversal", "pattern_matching", "centrality_analysis"]

  networkx:
    type: "graph"
    name: "NetworkX"
    description: "In-memory graph for development"
    configuration:
      persist_directory: "{domain_path}/knowledge/.graphs"
    capabilities: ["graph_traversal", "local_analysis"]

  # Hybrid Stores
  elasticsearch:
    type: "hybrid"
    name: "Elasticsearch"
    description: "Full-text search with vector capabilities"
    configuration:
      url: "http://localhost:9200"
      index_prefix: "{domain_name}"
    capabilities: ["full_text_search", "vector_search", "hybrid_ranking"]

  # Multimodal Stores
  multimodal_chroma:
    type: "multimodal"
    name: "Multimodal ChromaDB"
    description: "ChromaDB with CLIP embeddings for images"
    embedding_models:
      - "sentence-transformers/clip-ViT-B-32"
    capabilities: ["text_search", "image_search", "cross_modal_search"]

  # Time Series
  influxdb:
    type: "timeseries"
    name: "InfluxDB"
    description: "Time series database for real-time data"
    configuration:
      url: "http://localhost:8086"
      token_env: "INFLUXDB_TOKEN"
    capabilities: ["temporal_queries", "aggregation", "trend_analysis"]

# Default Storage Strategy per Source Type
default_storage_strategy:
  web_content: ["chromadb"]
  documents: ["chromadb", "neo4j"]
  api_feeds: ["neo4j", "chromadb"]
  code_repos: ["neo4j", "elasticsearch"]
  knowledge_graphs: ["neo4j"]
  media_content: ["multimodal_chroma"]
  internal_knowledge: ["chromadb", "neo4j"]
  realtime_feeds: ["influxdb", "chromadb"]
```

### Processing Pipeline Configuration

```yaml
# config/processing_pipelines.yaml
processing_components:
  # Extractors
  extractors:
    web_html_extractor:
      component: "extractors.WebHTMLExtractor"
      configuration:
        remove_navigation: true
        extract_main_content: true
        preserve_links: true

    document_extractor:
      component: "extractors.DocumentExtractor"
      configuration:
        extract_text: true
        extract_images: true
        preserve_structure: true

    api_extractor:
      component: "extractors.APIExtractor"
      configuration:
        rate_limit: 10  # requests per second
        timeout: 30
        retry_policy: "exponential_backoff"

  # Processors
  processors:
    markdown_converter:
      component: "processors.MarkdownConverter"
      configuration:
        preserve_formatting: true
        extract_headings: true

    code_processor:
      component: "processors.CodeProcessor"
      configuration:
        syntax_highlighting: false
        extract_functions: true
        extract_comments: true

  # Chunkers
  chunkers:
    semantic_chunker:
      component: "chunkers.SemanticChunker"
      configuration:
        chunk_size: 1000
        overlap: 100
        respect_boundaries: ["sentence", "paragraph"]

    function_aware_chunker:
      component: "chunkers.CodeAwareChunker"
      configuration:
        chunk_by: "function"
        include_context: true

  # Enrichers
  enrichers:
    metadata_enricher:
      component: "enrichers.MetadataEnricher"
      configuration:
        extract_timestamps: true
        extract_authors: true
        extract_keywords: true

    ast_enricher:
      component: "enrichers.ASTEnricher"
      configuration:
        extract_dependencies: true
        extract_function_signatures: true

# Pipeline Definitions
pipelines:
  standard_web:
    components:
      - extractor: "web_html_extractor"
      - processor: "markdown_converter"
      - chunker: "semantic_chunker"
      - enricher: "metadata_enricher"

  code_analysis:
    components:
      - extractor: "git_extractor"
      - processor: "code_processor"
      - chunker: "function_aware_chunker"
      - enricher: ["ast_enricher", "dependency_enricher"]
```

## Generic Knowledge Repository Service

### KnowledgeRepository Architecture

```python
class KnowledgeRepository:
    """Generic knowledge repository supporting multiple source types and storage backends."""

    def __init__(self, config_manager: ConfigManager, domain_path: Path):
        self.config = config_manager
        self.domain_path = domain_path
        self.source_types = config_manager.get_source_types()
        self.storage_backends = config_manager.get_storage_backends()
        self.pipelines = config_manager.get_processing_pipelines()

        # Initialize storage backends
        self.stores = {}
        for backend_name, backend_config in self.storage_backends.items():
            self.stores[backend_name] = self._initialize_store(backend_config)

    def add_source(self, source_type: str, source_config: Dict) -> str:
        """Add a new knowledge source and process it."""
        source_type_config = self.source_types[source_type]
        pipeline = self.pipelines[source_type_config.pipeline]

        # Process through pipeline
        processed_data = self._execute_pipeline(pipeline, source_config)

        # Store in configured backends
        source_id = self._store_knowledge(processed_data, source_type_config.storage)

        return source_id

    def search(self, query: str, search_type: str = "hybrid",
               source_types: List[str] = None, limit: int = 10) -> List[KnowledgeResult]:
        """Search across knowledge repository."""

        if search_type == "vector":
            return self._vector_search(query, source_types, limit)
        elif search_type == "graph":
            return self._graph_search(query, source_types, limit)
        elif search_type == "hybrid":
            return self._hybrid_search(query, source_types, limit)
        elif search_type == "multimodal":
            return self._multimodal_search(query, source_types, limit)

    def _hybrid_search(self, query: str, source_types: List[str], limit: int) -> List[KnowledgeResult]:
        """Combine vector similarity with graph traversal."""
        # Get vector similarity results
        vector_results = self._vector_search(query, source_types, limit * 2)

        # Expand with graph relationships
        graph_results = []
        for result in vector_results:
            related = self._get_related_entities(result.entity_id, max_depth=2)
            graph_results.extend(related)

        # Combine and rank results
        return self._rank_hybrid_results(vector_results, graph_results, limit)
```

### Multi-Modal RAG Support

```python
class MultiModalKnowledgeRepository(KnowledgeRepository):
    """Extended repository supporting images, video, audio content."""

    def add_media_source(self, media_path: Path, metadata: Dict) -> str:
        """Process and store media content with AI analysis."""

        # Extract content based on media type
        if media_path.suffix in ['.jpg', '.png', '.gif']:
            content = self._analyze_image(media_path)
        elif media_path.suffix in ['.mp4', '.avi', '.mov']:
            content = self._analyze_video(media_path)
        elif media_path.suffix in ['.mp3', '.wav', '.m4a']:
            content = self._analyze_audio(media_path)

        # Store in multimodal backend
        return self._store_multimodal(content, metadata)

    def search_multimodal(self, query: Union[str, Path],
                         modalities: List[str] = ["text", "image"]) -> List[MultiModalResult]:
        """Search across text and media content."""

        results = []

        if "text" in modalities:
            text_results = self._vector_search(query)
            results.extend(text_results)

        if "image" in modalities and isinstance(query, (str, Path)):
            if isinstance(query, str):
                # Text to image search
                image_results = self._clip_search(query)
            else:
                # Image to image search
                image_results = self._image_similarity_search(query)
            results.extend(image_results)

        return self._rank_multimodal_results(results)
```

### Graph-Enhanced Retrieval

```python
class GraphEnhancedRetrieval:
    """Retrieval system that leverages entity relationships."""

    def __init__(self, graph_store: GraphStore, vector_store: VectorStore):
        self.graph_store = graph_store
        self.vector_store = vector_store

    def retrieve_with_context(self, query: str, context_depth: int = 2) -> List[ContextualResult]:
        """Retrieve knowledge with relationship context."""

        # Initial vector search
        initial_results = self.vector_store.search(query, limit=20)

        # Expand with graph context
        contextual_results = []
        for result in initial_results:
            # Get entity relationships
            related_entities = self.graph_store.get_related(
                result.entity_id,
                max_depth=context_depth,
                relationship_types=["references", "relates_to", "part_of"]
            )

            # Build contextual result
            contextual_results.append(ContextualResult(
                primary_content=result,
                related_entities=related_entities,
                relationship_graph=self._build_subgraph(result.entity_id, related_entities)
            ))

        return self._rank_contextual_results(contextual_results)

    def retrieve_by_expertise_path(self, start_entity: str, target_expertise: str) -> List[ExpertisePathResult]:
        """Find knowledge through expertise relationship paths."""

        # Find shortest paths through expertise relationships
        paths = self.graph_store.find_expertise_paths(
            start_entity,
            target_expertise,
            relationship_types=["created_by", "reviewed_by", "expertise_in"]
        )

        # Score paths by expertise relevance
        return self._score_expertise_paths(paths)
```

## Benefits of Generic Knowledge Repository

### **Unlimited Source Types**
- Web content, documents, APIs, code repos, media, real-time feeds
- Custom source types through configuration
- Flexible processing pipelines per source type

### **Multi-Backend Storage**
- Vector stores: ChromaDB, Pinecone, Weaviate
- Graph databases: Neo4j, NetworkX
- Hybrid: Elasticsearch with vector+text search
- Multi-modal: CLIP embeddings for images/text
- Time series: InfluxDB for real-time data

### **Advanced Retrieval Methods**
- **Hybrid Search**: Vector similarity + graph traversal
- **Multi-modal**: Text, image, video content search
- **Contextual Retrieval**: Entity relationships and context
- **Expertise-based**: Find knowledge through expert connections
- **Temporal**: Time-aware retrieval for evolving knowledge

### **Extensible Processing**
- Pluggable extractors, processors, chunkers, enrichers
- Custom pipelines for different content types
- AI-powered content analysis (vision, NLP, code analysis)
- Real-time processing for streaming sources

This generic knowledge repository eliminates the hardcoded external/internal source limitation and single ChromaDB constraint, providing unlimited extensibility for any knowledge source type and storage backend while maintaining the same user interface.
