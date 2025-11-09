# Scripts

Utility scripts for testing and development.

## ingest_local.py

Test script for ingesting local files.

```bash
python scripts/ingest_local.py path/to/document.pdf --file-id optional-file-id --s3-bucket ragledger-documents-dev
```

## test_query.py

Test script for querying the RAG system.

```bash
python scripts/test_query.py "What is the customer's credit limit?" --top-k 5
```

## Requirements

- Python 3.11+
- AWS credentials configured
- Environment variables set (see .env.example)

