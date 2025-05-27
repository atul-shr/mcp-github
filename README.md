# MCP GitHub Integration Server

This is a Model Context Protocol (MCP) server that integrates with GitHub, allowing you to search and retrieve GitHub repository information.

## Setup

1. Create a virtual environment (already done):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install aiohttp pygithub python-dotenv
```

3. Create a GitHub Personal Access Token:
   - Go to GitHub Settings > Developer Settings > Personal Access Tokens
   - Create a new token with `repo` and `read:user` scopes
   - Copy the token

4. Configure environment variables:
   - Copy the `.env.example` file to `.env`
   - Replace `your_github_token_here` with your actual GitHub token

## Running the Server

To start the server:

```bash
python mcp_server.py
```

The server will start on port 3000 by default (can be changed in .env file).

## API Endpoints

### Search Context
- **Endpoint**: POST `/context/search`
- **Request Body**:
```json
{
    "query": "search term"
}
```

### Get Context Details
- **Endpoint**: POST `/context/details`
- **Request Body**:
```json
{
    "contextId": "repository_id"
}
```

## Response Format

The server follows the Model Context Protocol format for responses:

### Search Response
```json
{
    "items": [
        {
            "id": "repo_id",
            "title": "owner/repo",
            "url": "https://github.com/owner/repo",
            "description": "Repository description",
            "stars": 1234
        }
    ]
}
```

### Details Response
```json
{
    "id": "repo_id",
    "title": "owner/repo",
    "url": "https://github.com/owner/repo",
    "description": "Repository description",
    "language": "Python",
    "stars": 1234,
    "forks": 567,
    "topics": ["topic1", "topic2"]
}

curl -s "https://api.github.com/repos/atul-shr/portfolio" | jq '.id'

