#!/usr/bin/env python3
"""
Test query script for testing RAG queries
"""

import asyncio
import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from services.query_service import QueryService


async def test_query(query: str, top_k: int = 5):
    """
    Test a query
    """
    try:
        query_service = QueryService()
        result = await query_service.query(query, top_k)
        
        print(f"Query: {result['query']}")
        print(f"\nAnswer:\n{result['answer']}")
        print(f"\nSources ({len(result['sources'])}):")
        for i, source in enumerate(result['sources'], 1):
            print(f"\n  {i}. {source.filename}")
            if source.page:
                print(f"     Page: {source.page}")
            print(f"     Score: {source.similarity_score:.4f}")
            print(f"     Content: {source.content[:200]}...")
    except Exception as e:
        print(f"Error querying: {e}")
        import traceback
        traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(description='Test a RAG query')
    parser.add_argument('query', help='Query to test')
    parser.add_argument('--top-k', type=int, default=5, help='Number of results to retrieve')
    
    args = parser.parse_args()
    
    asyncio.run(test_query(args.query, args.top_k))


if __name__ == "__main__":
    main()

