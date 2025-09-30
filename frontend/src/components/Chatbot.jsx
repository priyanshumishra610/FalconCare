import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';

// Chatbot Component
const Chatbot = ({ isOpen, onClose, darkMode }) => {
  const [messages, setMessages] = useState([
    {
      text: "Hello! I'm FALCONCARE Bot, your AI health assistant. How can I help you today?",
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString()
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
      // Call the backend API
      const response = await fetch('http://localhost:5001/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      const botResponse = {
        text: data.message,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        type: data.type,
        severity: data.severity,
        suggestions: data.suggestions
      };
      
      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.error('Error calling backend API:', error);
      const errorResponse = {
        text: "I'm sorry, I'm having trouble connecting to the health database. Please try again in a moment, or contact support if the issue persists.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        type: 'error'
      };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    sendMessage(suggestion);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className={`w-full max-w-md h-[600px] rounded-2xl shadow-2xl flex flex-col ${
        darkMode ? 'bg-gray-800' : 'bg-white'
      }`}>
        {/* Header */}
        <div className="bg-blue-500 text-white p-4 rounded-t-2xl flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold">FALCONCARE Bot</h3>
            <p className="text-sm opacity-90">Your AI health assistant</p>
            <p className="text-[10px] opacity-80">This is not medical advice. Please consult a doctor.</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-blue-600 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 p-4 overflow-y-auto space-y-4">
          {messages.map((message, index) => (
            <div key={index}>
              <div
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-2xl ${
                    message.sender === 'user'
                      ? 'bg-blue-500 text-white'
                      : message.type === 'emergency'
                      ? 'bg-red-500 text-white'
                      : darkMode
                      ? 'bg-gray-700 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <p className="text-sm whitespace-pre-line">{message.text}</p>
                  <p className="text-xs opacity-70 mt-1">{message.timestamp}</p>
                </div>
              </div>
              
              {/* Suggestions */}
              {message.suggestions && message.suggestions.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {message.suggestions.map((suggestion, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSuggestionClick(suggestion)}
                      className={`text-xs px-3 py-1 rounded-full border transition-colors ${
                        darkMode 
                          ? 'border-gray-600 text-gray-300 hover:bg-gray-700' 
                          : 'border-gray-300 text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className={`p-3 rounded-2xl ${
                darkMode ? 'bg-gray-700' : 'bg-gray-100'
              }`}>
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t">
          <div className="flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage(inputMessage)}
              placeholder="Type your health question..."
              className={`flex-1 p-3 rounded-full border focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
              }`}
            />
            <button
              onClick={() => sendMessage(inputMessage)}
              className="bg-blue-500 hover:bg-blue-600 text-white p-3 rounded-full transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          {/* SOS Button */}
          <div className="mt-3 flex justify-between">
            <a href="tel:112" className="text-red-600 text-sm hover:underline">Emergency SOS (112)</a>
            <a href="tel:108" className="text-red-600 text-sm hover:underline">Ambulance (108)</a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
