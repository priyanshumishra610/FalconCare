#!/usr/bin/env python3
"""
FalconCare Rasa Bot Runner
Script to run the FalconCare health assistant bot programmatically
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from rasa.core.agent import Agent
from rasa.core.channels.console import ConsoleInputChannel
from rasa.core.channels.socketio import SocketIOInput
from rasa.core.channels.rest import RestInput
from rasa.core.utils import EndpointConfig
from rasa.utils.endpoints import EndpointConfig as RasaEndpointConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FalconCareBot:
    """FalconCare Health Assistant Bot"""
    
    def __init__(self, model_path: str = "models", endpoints_file: str = "endpoints.yml"):
        """
        Initialize the FalconCare bot
        
        Args:
            model_path: Path to the trained model
            endpoints_file: Path to endpoints configuration
        """
        self.model_path = model_path
        self.endpoints_file = endpoints_file
        self.agent = None
        
    async def load_agent(self):
        """Load the trained Rasa agent"""
        try:
            # Find the latest model
            model_files = list(Path(self.model_path).glob("*.tar.gz"))
            if not model_files:
                logger.error(f"No trained models found in {self.model_path}")
                logger.info("Please train a model first using: rasa train")
                return False
                
            latest_model = max(model_files, key=os.path.getctime)
            logger.info(f"Loading model: {latest_model}")
            
            # Load the agent
            self.agent = Agent.load(
                model_path=str(latest_model),
                action_endpoint=EndpointConfig(url="http://localhost:5055/webhook")
            )
            
            logger.info("FalconCare bot loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load agent: {e}")
            return False
    
    async def run_console(self):
        """Run the bot in console mode"""
        if not self.agent:
            logger.error("Agent not loaded. Cannot start console mode.")
            return
            
        logger.info("Starting FalconCare bot in console mode...")
        logger.info("Type 'quit' or 'exit' to stop the bot")
        logger.info("=" * 50)
        
        try:
            await self.agent.handle_text_async("Hello! I'm FalconCare, your health assistant.")
            await self.agent.handle_text_async("How can I help you with your health concerns today?")
            
            while True:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    logger.info("Goodbye! Take care of your health!")
                    break
                    
                if user_input:
                    response = await self.agent.handle_text_async(user_input)
                    print(f"FalconCare: {response}")
                    
        except KeyboardInterrupt:
            logger.info("\nBot stopped by user")
        except Exception as e:
            logger.error(f"Error in console mode: {e}")
    
    async def run_rest_api(self, host: str = "localhost", port: int = 5005):
        """Run the bot as a REST API server"""
        if not self.agent:
            logger.error("Agent not loaded. Cannot start REST API.")
            return
            
        logger.info(f"Starting FalconCare bot REST API on {host}:{port}")
        
        try:
            from rasa.core import run
            await run.serve_application(
                self.agent,
                channel=RestInput(),
                http_port=port,
                host=host
            )
        except Exception as e:
            logger.error(f"Error starting REST API: {e}")
    
    async def run_socketio(self, host: str = "localhost", port: int = 5005):
        """Run the bot with SocketIO support"""
        if not self.agent:
            logger.error("Agent not loaded. Cannot start SocketIO server.")
            return
            
        logger.info(f"Starting FalconCare bot SocketIO server on {host}:{port}")
        
        try:
            from rasa.core import run
            await run.serve_application(
                self.agent,
                channel=SocketIOInput(
                    user_message_evt="user_uttered",
                    bot_message_evt="bot_uttered",
                    session_persistence=True
                ),
                http_port=port,
                host=host
            )
        except Exception as e:
            logger.error(f"Error starting SocketIO server: {e}")


async def main():
    """Main function to run the FalconCare bot"""
    print("🏥 FalconCare Health Assistant Bot")
    print("=" * 40)
    
    # Initialize the bot
    bot = FalconCareBot()
    
    # Load the agent
    if not await bot.load_agent():
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "console":
            await bot.run_console()
        elif mode == "rest":
            host = sys.argv[2] if len(sys.argv) > 2 else "localhost"
            port = int(sys.argv[3]) if len(sys.argv) > 3 else 5005
            await bot.run_rest_api(host, port)
        elif mode == "socketio":
            host = sys.argv[2] if len(sys.argv) > 2 else "localhost"
            port = int(sys.argv[3]) if len(sys.argv) > 3 else 5005
            await bot.run_socketio(host, port)
        else:
            print("Usage: python run.py [console|rest|socketio] [host] [port]")
            print("  console  - Run in interactive console mode")
            print("  rest     - Run as REST API server")
            print("  socketio - Run with SocketIO support")
            sys.exit(1)
    else:
        # Default to console mode
        await bot.run_console()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
