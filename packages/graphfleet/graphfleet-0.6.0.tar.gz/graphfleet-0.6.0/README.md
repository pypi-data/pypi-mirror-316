# GraphFleet

A Python library for building and querying knowledge graphs using GraphRAG.

## Installation

```bash
pip install graphfleet
```

## Features

- Document indexing with customizable chunking
- Knowledge graph construction using GraphRAG
- Natural language querying
- Azure OpenAI integration
- FastAPI-based API endpoints

## Quick Start

```python
import asyncio
from pathlib import Path
from graphfleet.core import GraphFleet

async def main():
    # Initialize GraphFleet
    gf = GraphFleet(project_dir=Path("./data"))
    
    # Add a document
    doc_path = Path("example.txt")
    await gf.add_document(doc_path)
    
    # Search the knowledge base
    results = await gf.search("What are the main challenges in AI?")
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

Set the following environment variables in your `.env` file:

```bash
GRAPHRAG_API_KEY=your_api_key
GRAPHRAG_API_BASE=your_api_base
GRAPHRAG_API_VERSION=your_api_version
GRAPHRAG_DEPLOYMENT_NAME=your_deployment_name
GRAPHRAG_EMBEDDING_KEY=your_embedding_key
GRAPHRAG_EMBEDDING_ENDPOINT=your_embedding_endpoint
GRAPHRAG_EMBEDDING_DEPLOYMENT_NAME=your_embedding_deployment_name
```

## Documentation

For more examples and detailed documentation, see the `examples` directory.

## License

MIT License
