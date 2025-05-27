import os
import json
import logging
from aiohttp import web
from github import Github
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize GitHub client
github_token = os.getenv('GITHUB_TOKEN')
logger.debug(f"Raw token from env: {github_token}")

if not github_token:
    raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in .env file")

# Create Github instance
try:
    g = Github("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")
    # Test connection
    user = g.get_user()
    logger.info(f"Successfully authenticated as {user.login}")
except Exception as e:
    logger.error(f"Failed to authenticate with GitHub: {str(e)}")
    raise

async def verify_token(request):
    try:
        user = g.get_user()
        return web.json_response({
            'valid': True,
            'user': {
                'login': user.login,
                'name': user.name,
                'email': user.email,
                'avatar_url': user.avatar_url,
                'public_repos': user.public_repos
            }
        })
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        return web.json_response({
            'valid': False,
            'error': str(e)
        }, status=401)

async def handle_context_search(request):
    try:
        data = await request.json()
        query = data.get('query', '')
        logger.debug(f"Searching for: {query}")
        
        # Search GitHub repositories
        results = []
        repositories = g.search_repositories(query)
        
        for repo in repositories[:5]:  # Limit to top 5 results
            results.append({
                'id': str(repo.id),
                'title': repo.full_name,
                'url': repo.html_url,
                'description': repo.description,
                'stars': repo.stargazers_count
            })
        
        logger.debug(f"Found {len(results)} results")
        return web.json_response({
            'items': results
        })
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        return web.json_response({'error': str(e)}, status=500)

async def handle_context_details(request):
    try:
        data = await request.json()
        context_id = data.get('contextId', '')
        logger.debug(f"Getting details for repo ID: {context_id}")
        
        # Get repository details
        repo = g.get_repo(int(context_id))
        
        return web.json_response({
            'id': str(repo.id),
            'title': repo.full_name,
            'url': repo.html_url,
            'description': repo.description,
            'language': repo.language,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'topics': repo.get_topics()
        })
    except Exception as e:
        logger.error(f"Get details failed: {str(e)}")
        return web.json_response({'error': str(e)}, status=500)

app = web.Application()
app.router.add_get('/verify-token', verify_token)
app.router.add_post('/context/search', handle_context_search)
app.router.add_post('/context/details', handle_context_details)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    web.run_app(app, port=port)
