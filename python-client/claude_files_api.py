#!/usr/bin/env python3
"""
Claude Files API Client
Upload and manage files with the Anthropic Files API
"""

import os
import sys
import requests
from pathlib import Path
from typing import Optional, Dict, Any


class ClaudeFilesAPI:
    """Client for interacting with Anthropic's Files API"""

    BASE_URL = "https://api.anthropic.com/v1"
    API_VERSION = "2023-06-01"
    BETA_HEADER = "files-api-2025-04-14"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Files API client

        Args:
            api_key: Anthropic API key. If not provided, reads from ANTHROPIC_API_KEY env var
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in ANTHROPIC_API_KEY environment variable")

    def _get_headers(self, include_content_type: bool = False) -> Dict[str, str]:
        """Get standard headers for API requests"""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.API_VERSION,
            "anthropic-beta": self.BETA_HEADER
        }
        if include_content_type:
            headers["Content-Type"] = "application/json"
        return headers

    def upload_file(self, file_path: str, purpose: str = "assistants") -> Dict[str, Any]:
        """
        Upload a file to the Files API

        Args:
            file_path: Path to the file to upload
            purpose: Purpose of the file (default: "assistants")

        Returns:
            API response containing file metadata
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'rb') as f:
            files = {
                'file': (file_path.name, f, self._get_mime_type(file_path))
            }
            data = {'purpose': purpose}

            response = requests.post(
                f"{self.BASE_URL}/files",
                headers=self._get_headers(),
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()

    def list_files(self) -> Dict[str, Any]:
        """List all uploaded files"""
        response = requests.get(
            f"{self.BASE_URL}/files",
            headers=self._get_headers(include_content_type=True)
        )
        response.raise_for_status()
        return response.json()

    def get_file(self, file_id: str) -> Dict[str, Any]:
        """
        Get metadata for a specific file

        Args:
            file_id: The ID of the file

        Returns:
            File metadata
        """
        response = requests.get(
            f"{self.BASE_URL}/files/{file_id}",
            headers=self._get_headers(include_content_type=True)
        )
        response.raise_for_status()
        return response.json()

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        """
        Delete a file

        Args:
            file_id: The ID of the file to delete

        Returns:
            Deletion confirmation
        """
        response = requests.delete(
            f"{self.BASE_URL}/files/{file_id}",
            headers=self._get_headers(include_content_type=True)
        )
        response.raise_for_status()
        return response.json()

    def get_file_content(self, file_id: str) -> bytes:
        """
        Download file content

        Args:
            file_id: The ID of the file

        Returns:
            File content as bytes
        """
        response = requests.get(
            f"{self.BASE_URL}/files/{file_id}/content",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.content

    @staticmethod
    def _get_mime_type(file_path: Path) -> str:
        """Determine MIME type based on file extension"""
        mime_types = {
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
            '.json': 'application/json',
            '.csv': 'text/csv',
            '.md': 'text/markdown',
            '.html': 'text/html',
            '.xml': 'application/xml',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        return mime_types.get(file_path.suffix.lower(), 'application/octet-stream')


def main():
    """CLI interface for the Files API client"""
    import argparse

    parser = argparse.ArgumentParser(description="Claude Files API Client")
    parser.add_argument('command', choices=['upload', 'list', 'get', 'delete', 'download'],
                       help='Command to execute')
    parser.add_argument('--file', help='File path (for upload)')
    parser.add_argument('--file-id', help='File ID (for get/delete/download)')
    parser.add_argument('--output', help='Output path (for download)')
    parser.add_argument('--api-key', help='Anthropic API key')

    args = parser.parse_args()

    try:
        client = ClaudeFilesAPI(api_key=args.api_key)

        if args.command == 'upload':
            if not args.file:
                print("Error: --file is required for upload", file=sys.stderr)
                sys.exit(1)
            result = client.upload_file(args.file)
            print(f"File uploaded successfully!")
            print(f"File ID: {result.get('id')}")
            print(f"Full response: {result}")

        elif args.command == 'list':
            result = client.list_files()
            print("Files:")
            for file in result.get('data', []):
                print(f"  - {file.get('id')}: {file.get('filename')} ({file.get('bytes')} bytes)")

        elif args.command == 'get':
            if not args.file_id:
                print("Error: --file-id is required for get", file=sys.stderr)
                sys.exit(1)
            result = client.get_file(args.file_id)
            print(result)

        elif args.command == 'delete':
            if not args.file_id:
                print("Error: --file-id is required for delete", file=sys.stderr)
                sys.exit(1)
            result = client.delete_file(args.file_id)
            print(f"File deleted: {result}")

        elif args.command == 'download':
            if not args.file_id:
                print("Error: --file-id is required for download", file=sys.stderr)
                sys.exit(1)
            content = client.get_file_content(args.file_id)
            output_path = args.output or f"downloaded_{args.file_id}"
            with open(output_path, 'wb') as f:
                f.write(content)
            print(f"File downloaded to: {output_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
