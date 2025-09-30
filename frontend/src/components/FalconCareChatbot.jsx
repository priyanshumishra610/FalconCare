import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Phone, AlertTriangle, CheckCircle, MapPin } from 'lucide-react';

// Enhanced FalconCare Chatbot Component with Rasa Integration
const FalconCareChatbot = ({ isOpen, onClose, darkMode }) => {
  const [messages, setMessages] = useState([
    {
      text: "🙏 नमस्ते! मैं FalconCare हूं - आपका डिजिटल स्वास्थ्य सहायक। \n\nI can help you with:\n• 🤒 Symptom checking (लक्षण जांच)\n• 💉 Vaccination info (टीकाकरण)\n• 🏥 Find hospitals (अस्पताल खोजें)\n• 🚨 Emergency help (आपातकाल)\n• ❌ Myth-busting (गलत जानकारी की पहचान)\n\nHow can I help you today? / आप कैसे हैं?",
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString(),
      type: 'greeting'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (message) => {
    if (!message.trim()) return;

    const userMessage = {
      text: message,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      // Connect to Rasa REST API (port 5005)
      const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          sender: 'user',
          message: message 
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to connect to FalconCare');
      }

      const data = await response.json();
      
      // Process Rasa responses
      if (data && data.length > 0) {
        data.forEach((rasaResponse, index) => {
          setTimeout(() => {
            const botResponse = {
              text: rasaResponse.text || rasaResponse.custom?.text || "I'm processing your request...",
              sender: 'bot',
              timestamp: new Date().toLocaleTimeString(),
              type: detectResponseType(rasaResponse.text),
              buttons: rasaResponse.buttons || [],
              image: rasaResponse.image
            };
            
            setMessages(prev => [...prev, botResponse]);
          }, index * 500); // Stagger multiple responses
        });
      } else {
        // Fallback response
        const fallbackResponse = {
          text: "मैं समझ नहीं पाया। कृपया अपनी समस्या सरल शब्दों में बताएं।\n\nI didn't understand. Please describe your health concern in simple words.",
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString(),
          type: 'fallback'
        };
        setMessages(prev => [...prev, fallbackResponse]);
      }
      
    } catch (error) {
      console.error('Error connecting to FalconCare:', error);
      
      // Fallback to local processing for demo
      const fallbackResponse = await getFallbackResponse(message);
      setMessages(prev => [...prev, fallbackResponse]);
      
    } finally {
      setIsTyping(false);
    }
  };

  const detectResponseType = (text) => {
    if (!text) return 'general';
    
    const textLower = text.toLowerCase();
    
    if (textLower.includes('🚨') || textLower.includes('emergency') || textLower.includes('आपातकाल')) {
      return 'emergency';
    } else if (textLower.includes('⚠️') || textLower.includes('warning') || textLower.includes('चेतावनी')) {
      return 'warning';
    } else if (textLower.includes('❌') || textLower.includes('myth') || textLower.includes('गलत')) {
      return 'myth';
    } else if (textLower.includes('💉') || textLower.includes('vaccine') || textLower.includes('टीका')) {
      return 'vaccination';
    } else if (textLower.includes('🏥') || textLower.includes('hospital') || textLower.includes('अस्पताल')) {
      return 'hospital';
    }
    
    return 'general';
  };

  const getFallbackResponse = async (message) => {
    // Enhanced fallback with health context
    const messageLower = message.toLowerCase();
    
    if (messageLower.includes('fever') || messageLower.includes('बुखार') || messageLower.includes('bukhar')) {
      return {
        text: "🌡️ **Fever Assessment**\n\nI understand you have fever. Let me help:\n\n• How long have you had fever?\n• Is it mild or severe?\n• Any other symptoms?\n\n**बुखार की जांच:**\n• कब से बुखार है?\n• हल्का है या तेज?\n• और कोई परेशानी?",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        type: 'symptom',
        buttons: [
          { title: "1-2 days / 1-2 दिन", payload: "1-2 days fever" },
          { title: "3+ days / 3+ दिन", payload: "3+ days fever" },
          { title: "Very high / बहुत तेज", payload: "severe fever" }
        ]
      };
    }
    
    if (messageLower.includes('chest pain') || messageLower.includes('सीने में दर्द')) {
      return {
        text: "🚨 **EMERGENCY ALERT**\n\nChest pain can be serious!\n\n**Immediate Action Required:**\n📞 Call 108 (Ambulance)\n🏥 Go to nearest hospital\n\n**तत्काल कार्रवाई:**\n📞 108 पर कॉल करें\n🏥 नजदीकी अस्पताल जाएं",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        type: 'emergency',
        buttons: [
          { title: "📞 Call 108", payload: "tel:108" },
          { title: "🏥 Find Hospital", payload: "find hospital" }
        ]
      };
    }
    
    if (messageLower.includes('vaccine') || messageLower.includes('टीका') || messageLower.includes('vaccination')) {
      return {
        text: "💉 **Vaccination Information**\n\nI can help you find:\n• COVID vaccine centers\n• Child vaccination schedule\n• Nearby vaccination facilities\n\n**टीकाकरण की जानकारी:**\n• कोविड वैक्सीन केंद्र\n• बच्चों का टीकाकरण\n• पास के केंद्र",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        type: 'vaccination',
        buttons: [
          { title: "COVID Vaccine", payload: "covid vaccine" },
          { title: "Child Vaccines", payload: "child vaccination" },
          { title: "Find Centers", payload: "vaccination centers" }
        ]
      };
    }
    
    if (messageLower.includes('myth') || messageLower.includes('हल्दी') || messageLower.includes('cure')) {
      return {
        text: "❌ **Myth Detection Alert**\n\nI detected potential health misinformation!\n\n**सावधान:**\n• केवल डॉक्टर की सलाह मानें\n• घरेलू नुस्खों पर भरोसा न करें\n• सरकारी स्रोतों से जानकारी लें\n\n**Trust only:**\n• Government health sources\n• Licensed doctors\n• Medical professionals",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        type: 'myth',
        buttons: [
          { title: "Find Doctor", payload: "find doctor" },
          { title: "Government Info", payload: "government health info" }
        ]
      };
    }
    
    // Default response
    return {
      text: "मैं FalconCare हूं। मैं इन चीजों में मदद कर सकता हूं:\n\n🤒 **Symptoms** - बुखार, खांसी, दर्द\n💉 **Vaccines** - टीकाकरण की जानकारी\n🏥 **Hospitals** - नजदीकी अस्पताल\n🚨 **Emergency** - आपातकालीन मदद\n❌ **Myth Check** - गलत जानकारी की पहचान\n\nWhat's your health concern? / आपकी क्या समस्या है?",
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString(),
      type: 'general',
      buttons: [
        { title: "🤒 Check Symptoms", payload: "I have symptoms" },
        { title: "💉 Vaccination", payload: "vaccination info" },
        { title: "🏥 Find Hospital", payload: "find hospital" },
        { title: "🚨 Emergency", payload: "emergency help" }
      ]
    };
  };

  const handleButtonClick = (buttonPayload) => {
    sendMessage(buttonPayload);
  };

  const getMessageStyle = (message) => {
    if (message.sender === 'user') {
      return 'bg-blue-500 text-white ml-auto';
    }
    
    switch (message.type) {
      case 'emergency':
        return 'bg-red-500 text-white';
      case 'warning':
        return 'bg-yellow-500 text-black';
      case 'myth':
        return 'bg-orange-500 text-white';
      case 'vaccination':
        return 'bg-green-500 text-white';
      default:
        return darkMode ? 'bg-gray-700 text-white' : 'bg-gray-100 text-gray-900';
    }
  };

  const getMessageIcon = (type) => {
    switch (type) {
      case 'emergency':
        return <AlertTriangle className="w-4 h-4 text-red-500 inline mr-1" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-500 inline mr-1" />;
      case 'myth':
        return <X className="w-4 h-4 text-orange-500 inline mr-1" />;
      case 'vaccination':
        return <CheckCircle className="w-4 h-4 text-green-500 inline mr-1" />;
      case 'hospital':
        return <MapPin className="w-4 h-4 text-blue-500 inline mr-1" />;
      default:
        return null;
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className={`w-full max-w-md h-[700px] rounded-2xl shadow-2xl flex flex-col ${
        darkMode ? 'bg-gray-800' : 'bg-white'
      }`}>
        {/* Enhanced Header */}
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 rounded-t-2xl flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
              <MessageCircle className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold">FalconCare AI</h3>
              <p className="text-sm opacity-90">🩺 Smart Health Assistant</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white hover:bg-opacity-20 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Status Indicator */}
        <div className="px-4 py-2 bg-green-50 border-b flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-green-700 font-medium">FalconCare Online - Ready to Help</span>
        </div>

        {/* Messages */}
        <div className="flex-1 p-4 overflow-y-auto space-y-4">
          {messages.map((message, index) => (
            <div key={index}>
              <div
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] p-4 rounded-2xl shadow-md ${
                    getMessageStyle(message)
                  }`}
                >
                  <div className="flex items-start gap-2">
                    {message.sender === 'bot' && getMessageIcon(message.type)}
                    <div>
                      <p className="text-sm whitespace-pre-line leading-relaxed">{message.text}</p>
                      <p className="text-xs opacity-70 mt-2">{message.timestamp}</p>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Action Buttons */}
              {message.buttons && message.buttons.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-3 ml-2">
                  {message.buttons.map((button, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleButtonClick(button.payload || button.title)}
                      className={`text-xs px-4 py-2 rounded-full border transition-all duration-200 hover:scale-105 ${
                        button.title.includes('108') || button.title.includes('Emergency')
                          ? 'bg-red-500 text-white border-red-500 hover:bg-red-600'
                          : button.title.includes('Hospital') || button.title.includes('अस्पताल')
                          ? 'bg-blue-500 text-white border-blue-500 hover:bg-blue-600'
                          : darkMode 
                          ? 'border-gray-600 text-gray-300 hover:bg-gray-700' 
                          : 'border-gray-300 text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      {button.title}
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className={`p-4 rounded-2xl ${
                darkMode ? 'bg-gray-700' : 'bg-gray-100'
              }`}>
                <div className="flex items-center space-x-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                  <span className="text-sm text-gray-500">FalconCare is thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Actions Bar */}
        <div className="px-4 py-2 border-t border-gray-200 flex gap-2 overflow-x-auto">
          <button
            onClick={() => sendMessage("मुझे बुखार है")}
            className="whitespace-nowrap text-xs px-3 py-2 bg-red-100 text-red-700 rounded-full hover:bg-red-200 transition-colors"
          >
            🤒 Fever / बुखार
          </button>
          <button
            onClick={() => sendMessage("टीका कहां मिलेगा")}
            className="whitespace-nowrap text-xs px-3 py-2 bg-green-100 text-green-700 rounded-full hover:bg-green-200 transition-colors"
          >
            💉 Vaccine / टीका
          </button>
          <button
            onClick={() => sendMessage("नजदीकी अस्पताल")}
            className="whitespace-nowrap text-xs px-3 py-2 bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
          >
            🏥 Hospital / अस्पताल
          </button>
          <button
            onClick={() => sendMessage("emergency")}
            className="whitespace-nowrap text-xs px-3 py-2 bg-red-100 text-red-700 rounded-full hover:bg-red-200 transition-colors"
          >
            🚨 Emergency
          </button>
        </div>

        {/* Input */}
        <div className="p-4">
          <div className="flex space-x-3">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage(inputMessage)}
              placeholder="Type your health question... / अपनी समस्या लिखें..."
              className={`flex-1 p-3 rounded-full border-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all ${
                darkMode ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' : 'bg-white border-gray-300 placeholder-gray-500'
              }`}
            />
            <button
              onClick={() => sendMessage(inputMessage)}
              disabled={!inputMessage.trim()}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white p-3 rounded-full transition-all duration-200 transform hover:scale-105 disabled:scale-100"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          
          {/* Language Toggle */}
          <div className="flex justify-center mt-3 gap-2">
            <button
              onClick={() => sendMessage("हिंदी में बात करें")}
              className="text-xs px-3 py-1 bg-orange-100 text-orange-700 rounded-full hover:bg-orange-200 transition-colors"
            >
              🇮🇳 हिंदी
            </button>
            <button
              onClick={() => sendMessage("speak in english")}
              className="text-xs px-3 py-1 bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
            >
              🇺🇸 English
            </button>
          </div>
        </div>

        {/* Footer Info */}
        <div className="px-4 pb-3 text-center">
          <p className="text-xs text-gray-500">
            🤖 Powered by FalconCare AI • 🏥 For Health Guidance Only • 🚨 Emergency: Call 108
          </p>
        </div>
      </div>
    </div>
  );
};

export default FalconCareChatbot;