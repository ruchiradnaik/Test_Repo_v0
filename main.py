"""
Main entry point for the application.
"""
from api import app
from database import db_manager
import sys

def main():
    """Initialize and run the application."""
    try:
        print("Starting application...")
        print("Database initialized:", db_manager.engine.url)
        print("Starting Flask server on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
        db_manager.close()
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        db_manager.close()
        sys.exit(1)

if __name__ == '__main__':
    main()
