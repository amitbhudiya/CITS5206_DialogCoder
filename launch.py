import os
import sys
import subprocess
import pathlib

def run_app():
    # Get script directory
    current_dir = pathlib.Path(__file__).parent.absolute()
    
    # Set working directory
    os.chdir(current_dir)
    
    # Ensure app directory is in Python path
    sys.path.append(str(current_dir))
    
    # Set Streamlit configuration
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = 'localhost'
    
    try:
        # Launch Streamlit application
        subprocess.run([
            'streamlit',
            'run',
            os.path.join('app', 'Home.py'),
            '--server.headless', 'false',
            '--server.runOnSave', 'false'
        ], check=True)
    except Exception as e:
        print(f"Error occurred while starting the application: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    run_app() 
