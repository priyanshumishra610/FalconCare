# FalconCare - WhatsApp Business API Integration
# Accessible health chatbot via WhatsApp for rural users

import logging
from typing import Text, Dict, Any, List, Optional
import json
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import UserMessage, OutputChannel
from flask import Blueprint, request, jsonify, Flask

logger = logging.getLogger(__name__)


class WhatsAppOutput(OutputChannel):
    """WhatsApp output channel using Twilio API"""
    
    def __init__(self, account_sid: Text, auth_token: Text, whatsapp_number: Text):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.whatsapp_number = whatsapp_number
        self.client = Client(account_sid, auth_token)
    
    @classmethod
    def name(cls) -> Text:
        return "whatsapp"
    
    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Send text message via WhatsApp"""
        try:
            # Format text for WhatsApp (emoji support, line breaks)
            formatted_text = self._format_for_whatsapp(text)
            
            message = self.client.messages.create(
                body=formatted_text,
                from_=f'whatsapp:{self.whatsapp_number}',
                to=f'whatsapp:{recipient_id}'
            )
            
            logger.info(f"WhatsApp message sent to {recipient_id}: {message.sid}")
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
    
    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        """Send text with buttons (WhatsApp interactive message)"""
        try:
            # WhatsApp Business API supports interactive buttons
            # For demo, we'll send buttons as text options
            
            button_text = "\n\n" + "\n".join([
                f"↪️ {i+1}. {btn['title']}" 
                for i, btn in enumerate(buttons[:3])  # WhatsApp limit: 3 buttons
            ])
            
            full_text = text + button_text + "\n\n💬 कृपया संख्या या टेक्स्ट भेजें"
            
            await self.send_text_message(recipient_id, full_text)
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp buttons: {e}")
    
    async def send_image_url(
        self, recipient_id: Text, image: Text, **kwargs: Any
    ) -> None:
        """Send image via WhatsApp"""
        try:
            message = self.client.messages.create(
                media_url=[image],
                from_=f'whatsapp:{self.whatsapp_number}',
                to=f'whatsapp:{recipient_id}'
            )
            
            logger.info(f"WhatsApp image sent to {recipient_id}: {message.sid}")
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp image: {e}")
    
    def _format_for_whatsapp(self, text: Text) -> Text:
        """Format text for better WhatsApp readability"""
        # Convert markdown-style formatting to WhatsApp
        formatted = text.replace("**", "*")  # Bold formatting
        formatted = formatted.replace("##", "")  # Remove headers
        
        # Ensure proper line breaks
        formatted = formatted.replace("\\n", "\n")
        
        # Truncate if too long (WhatsApp limit: 4096 chars)
        if len(formatted) > 4000:
            formatted = formatted[:3900] + "...\n\n📱 अधिक जानकारी के लिए 'मदद' टाइप करें"
        
        return formatted


class WhatsAppInput(InputChannel):
    """WhatsApp input channel using Twilio webhook"""
    
    def __init__(
        self,
        account_sid: Text,
        auth_token: Text,
        whatsapp_number: Text,
        webhook_url: Optional[Text] = None,
    ):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.whatsapp_number = whatsapp_number
        self.webhook_url = webhook_url
    
    @classmethod
    def name(cls) -> Text:
        return "whatsapp"
    
    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "WhatsAppInput":
        if not credentials:
            cls.raise_missing_credentials_exception()
        
        return cls(
            credentials.get("account_sid"),
            credentials.get("auth_token"),
            credentials.get("whatsapp_number"),
            credentials.get("webhook_url"),
        )
    
    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[Any]]
    ) -> Blueprint:
        whatsapp_webhook = Blueprint("whatsapp_webhook", __name__)
        
        @whatsapp_webhook.route("/", methods=["GET"])
        def health_check():
            return jsonify({"status": "WhatsApp FalconCare is running! 🏥"})
        
        @whatsapp_webhook.route("/webhook", methods=["POST"])
        def webhook():
            return self._handle_webhook(request, on_new_message)
        
        return whatsapp_webhook
    
    def _handle_webhook(self, request, on_new_message):
        """Handle incoming WhatsApp messages"""
        try:
            # Extract WhatsApp message data
            sender_id = request.values.get('From', '').replace('whatsapp:', '')
            message_body = request.values.get('Body', '')
            media_url = request.values.get('MediaUrl0', None)
            
            logger.info(f"WhatsApp message from {sender_id}: {message_body}")
            
            # Create output channel
            output_channel = WhatsAppOutput(
                self.account_sid,
                self.auth_token,
                self.whatsapp_number
            )
            
            # Handle different message types
            if media_url:
                # Handle image/media message
                processed_text = self._process_media_message(media_url, message_body)
            else:
                # Handle text message
                processed_text = self._preprocess_whatsapp_text(message_body)
            
            # Create user message
            user_message = UserMessage(
                text=processed_text,
                output_channel=output_channel,
                sender_id=sender_id,
                input_channel=self.name(),
                metadata={
                    "whatsapp_number": sender_id,
                    "platform": "whatsapp",
                    "media_url": media_url
                }
            )
            
            # Process asynchronously
            asyncio.create_task(on_new_message(user_message))
            
            # Return empty TwiML response
            response = MessagingResponse()
            return str(response)
            
        except Exception as e:
            logger.error(f"WhatsApp webhook error: {e}")
            
            # Send error response
            response = MessagingResponse()
            response.message("क्षमा करें, तकनीकी समस्या है। कृपया फिर से कोशिश करें। 🔧")
            return str(response)
    
    def _preprocess_whatsapp_text(self, text: Text) -> Text:
        """Preprocess WhatsApp text for better understanding"""
        # Convert common WhatsApp shortcuts to full words
        shortcuts = {
            "u": "you",
            "ur": "your", 
            "n": "and",
            "w8": "wait",
            "2": "to",
            "4": "for",
            # Hindi shortcuts
            "kya": "क्या",
            "hai": "है",
            "nhi": "नहीं",
            "thik": "ठीक",
        }
        
        words = text.lower().split()
        processed_words = [shortcuts.get(word, word) for word in words]
        
        return " ".join(processed_words)
    
    def _process_media_message(self, media_url: Text, caption: Text) -> Text:
        """Process media messages (images of symptoms, prescriptions, etc.)"""
        # For now, return caption with media acknowledgment
        # In production, implement image recognition for symptoms
        
        if caption:
            return f"आपकी तस्वीर मिली। {caption}"
        else:
            return "आपकी तस्वीर मिली। कृपया अपनी समस्या के बारे में बताएं।"


# Demo WhatsApp Server
def create_whatsapp_demo_server():
    """Create demo WhatsApp server for SIH presentation"""
    
    app = Flask(__name__)
    
    # Mock credentials for demo
    DEMO_CONFIG = {
        "account_sid": "demo_sid",
        "auth_token": "demo_token", 
        "whatsapp_number": "+14155238886"  # Twilio Sandbox
    }
    
    @app.route("/")
    def index():
        return """
        <h1>🏥 FalconCare - WhatsApp Integration</h1>
        <h2>🎯 For Smart India Hackathon Demo</h2>
        
        <div style="background: #e8f5e8; padding: 20px; margin: 20px; border-radius: 10px;">
            <h3>📱 WhatsApp Demo Instructions</h3>
            <ol>
                <li><strong>Production Setup:</strong> Connect to Twilio WhatsApp Business API</li>
                <li><strong>Demo Mode:</strong> Simulate WhatsApp interface</li>
                <li><strong>Features:</strong> 
                    <ul>
                        <li>✅ Text message support</li>
                        <li>✅ Button interactions</li>
                        <li>✅ Image handling (symptoms)</li>
                        <li>✅ Hindi + English support</li>
                        <li>✅ Emergency escalation</li>
                    </ul>
                </li>
            </ol>
        </div>
        
        <div style="background: #fff3cd; padding: 20px; margin: 20px; border-radius: 10px;">
            <h3>🚀 Quick Start</h3>
            <p><strong>Twilio Sandbox Number:</strong> +1 415 523 8886</p>
            <p><strong>Activation:</strong> Send "join <sandbox-name>" to start</p>
            <p><strong>Test Message:</strong> "मुझे बुखार है" (I have fever)</p>
        </div>
        
        <div style="background: #d1ecf1; padding: 20px; margin: 20px; border-radius: 10px;">
            <h3>🏆 SIH Advantages</h3>
            <ul>
                <li>🌐 2.4 billion WhatsApp users globally</li>
                <li>📱 Works on basic smartphones</li>
                <li>💬 Natural conversation interface</li>
                <li>🔄 Real-time health support</li>
                <li>🏥 Direct integration with health services</li>
            </ul>
        </div>
        """
    
    @app.route("/demo", methods=["GET", "POST"])
    def whatsapp_demo():
        if request.method == "GET":
            return """
            <h2>📱 WhatsApp Chat Simulator</h2>
            <div id="chat" style="border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 10px; background: #f0f0f0;">
                <div style="margin: 5px 0; padding: 10px; background: white; border-radius: 10px;">
                    <strong>FalconCare:</strong><br>
                    🙏 नमस्ते! मैं FalconCare हूं।<br>
                    आपकी स्वास्थ्य सेवा में कैसे मदद कर सकता हूं?
                </div>
            </div>
            
            <form method="POST" style="margin-top: 10px;">
                <input type="text" name="message" placeholder="अपना संदेश यहां लिखें..." 
                       style="width: 70%; padding: 10px;" required>
                <button type="submit" style="padding: 10px 20px;">Send 📤</button>
            </form>
            
            <div style="margin-top: 20px;">
                <h3>💡 Try these examples:</h3>
                <ul>
                    <li>"मुझे बुखार है" (I have fever)</li>
                    <li>"बच्चे का टीका कब लगवाएं" (When to vaccinate child)</li>
                    <li>"नजदीकी अस्पताल कहां है" (Where is nearest hospital)</li>
                    <li>"हल्दी से कैंसर ठीक होता है" (Turmeric cures cancer - myth test)</li>
                </ul>
            </div>
            """
        
        # Handle demo message
        user_message = request.form.get("message", "")
        
        # Simple response simulation
        if "बुखार" in user_message or "fever" in user_message.lower():
            bot_response = """
            🌡️ बुखार की जांच हो रही है...
            
            कब से बुखार है?
            1️⃣ आज से
            2️⃣ 1-2 दिन
            3️⃣ 3-7 दिन
            4️⃣ 1 सप्ताह से ज्यादा
            
            कृपया संख्या भेजें (1-4)
            """
        elif "टीका" in user_message or "vaccine" in user_message.lower():
            bot_response = """
            💉 टीकाकरण की जानकारी
            
            आपका पिनकोड क्या है?
            निकटतम केंद्र खोजने के लिए 6 अंक का कोड भेजें।
            
            उदाहरण: 492001
            """
        else:
            bot_response = """
            मैं समझ गया। आपकी मदद करता हूं! 🤖
            
            मुख्य सेवाएं:
            🤒 लक्षण जांच
            💉 टीकाकरण
            🏥 अस्पताल खोजें
            🩺 स्वास्थ्य सलाह
            """
        
        return f"""
        <div style="margin: 5px 0; padding: 10px; background: #dcf8c6; border-radius: 10px; text-align: right;">
            <strong>You:</strong><br>{user_message}
        </div>
        <div style="margin: 5px 0; padding: 10px; background: white; border-radius: 10px;">
            <strong>FalconCare:</strong><br>{bot_response}
        </div>
        <a href="/demo">🔄 Continue Chat</a>
        """
    
    return app


if __name__ == "__main__":
    # Run demo server
    demo_app = create_whatsapp_demo_server()
    print("🚀 Starting WhatsApp Demo Server...")
    print("📱 Open: http://localhost:5001")
    print("🎯 For SIH judges demonstration")
    demo_app.run(host="0.0.0.0", port=5001, debug=True)