# Claude Files API - Python Client

Python client for uploading and managing files with the Anthropic Files API.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As a Library

```python
from claude_files_api import ClaudeFilesAPI

# Initialize client (API key from environment or pass directly)
client = ClaudeFilesAPI()  # Uses ANTHROPIC_API_KEY env var
# or
client = ClaudeFilesAPI(api_key="your-api-key")

# Upload a file
result = client.upload_file("/path/to/document.pdf")
file_id = result['id']

# List all files
files = client.list_files()

# Get file metadata
metadata = client.get_file(file_id)

# Download file content
content = client.get_file_content(file_id)

# Delete a file
client.delete_file(file_id)
```

### As a CLI Tool

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-api-key"

# Upload a file
python claude_files_api.py upload --file /path/to/document.pdf

# List all files
python claude_files_api.py list

# Get file metadata
python claude_files_api.py get --file-id file-xxx

# Download a file
python claude_files_api.py download --file-id file-xxx --output downloaded.pdf

# Delete a file
python claude_files_api.py delete --file-id file-xxx
```

## Supported File Types

- PDF documents
- Text files
- JSON files
- CSV files
- Markdown files
- HTML/XML files
- Images (JPEG, PNG, GIF, WebP)

## Security

**NEVER** hardcode API keys in your code. Always use environment variables or secure secret management.

```bash
export ANTHROPIC_API_KEY="your-api-key"
```
