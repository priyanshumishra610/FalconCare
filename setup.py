#!/usr/bin/env python3
"""
FalconCare Setup Script
Automated setup and training for the FalconCare health assistant bot
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_command(command, description):
    """Run a command and handle errors"""
    logger.info(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8 or higher is required")
        return False
    logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def install_dependencies():
    """Install required dependencies"""
    logger.info("Installing dependencies...")
    return run_command("pip install -r requirements.txt", "Dependency installation")


def train_model():
    """Train the Rasa model"""
    logger.info("Training the Rasa model...")
    return run_command("rasa train", "Model training")


def run_tests():
    """Run the test suite"""
    logger.info("Running tests...")
    
    # Run action tests
    if not run_command("cd actions && python -m pytest test_actions.py -v", "Action tests"):
        return False
    
    # Run Rasa tests
    if not run_command("rasa test nlu", "NLU tests"):
        return False
    
    if not run_command("rasa test stories", "Story tests"):
        return False
    
    return True


def create_directories():
    """Create necessary directories"""
    directories = ["models", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"✅ Created directory: {directory}")


def main():
    """Main setup function"""
    print("🏥 FalconCare Health Assistant Bot Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        logger.error("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Train the model
    if not train_model():
        logger.error("❌ Setup failed at model training")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        logger.error("❌ Setup failed at testing")
        sys.exit(1)
    
    print("\n🎉 FalconCare setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the action server: rasa run actions")
    print("2. Run the bot: python run.py console")
    print("3. Or run in REST API mode: python run.py rest")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
