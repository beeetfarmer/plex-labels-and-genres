from plexapi.server import PlexServer
import sys
from . import config

def connect_to_plex():
    """Connect to the Plex server with error handling for missing token."""
    # Check for empty token
    if not config.PLEX_TOKEN:
        print("Error: Plex token is not configured.")
        print("Please edit config.py and add your Plex authentication token.")
        print("You can find your token by following instructions at:")
        print("https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/")
        sys.exit(1)
        
    # Check for server URL
    if not config.PLEX_URL or config.PLEX_URL == 'http://localhost:32400':
        print("Warning: Using default Plex server URL. If your server is at a different location,")
        print("edit the PLEX_URL setting in config.py.")
    
    try:
        print(f"Connecting to Plex server at {config.PLEX_URL}...")
        return PlexServer(config.PLEX_URL, config.PLEX_TOKEN)
    except Exception as e:
        print(f"Error connecting to Plex server: {e}")
        print("\nPossible issues:")
        print("1. Incorrect Plex token")
        print("2. Plex server is not running")
        print("3. Incorrect server URL")
        print("4. Network connectivity issues")
        sys.exit(1)

def get_tv_library(server):
    """Get the TV show library from the Plex server."""
    try:
        print(f"Accessing '{config.LIBRARY_NAME}' library...")
        return server.library.section(config.LIBRARY_NAME)
    except Exception as e:
        print(f"Error finding library '{config.LIBRARY_NAME}': {e}")
        print(f"\nThe library '{config.LIBRARY_NAME}' was not found on your Plex server.")
        print("Available libraries:")
        
        # List available libraries to help user
        try:
            sections = server.library.sections()
            if sections:
                for section in sections:
                    print(f"  - {section.title} (type: {section.type})")
                print(f"\nPlease edit the LIBRARY_NAME setting in config.py to match one of these.")
            else:
                print("  No libraries found on this server.")
        except:
            print("  Could not retrieve library list.")
            
        sys.exit(1)