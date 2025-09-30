#!/usr/bin/env python3
"""
FalconCare Backend API
Simple Flask backend to handle chatbot requests
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Simple health knowledge base
HEALTH_KNOWLEDGE = {
    'headache': {
        'description': 'Headache is pain or discomfort in the head or neck area.',
        'advice': 'Rest in a dark room, apply cold compress, and stay hydrated. Avoid triggers like stress and certain foods.',
        'when_to_see_doctor': 'If headache is severe, sudden, or accompanied by fever, neck stiffness, or vision changes.',
        'severity': 'moderate'
    },
    'fever': {
        'description': 'Fever is a temporary increase in body temperature, often a sign of infection.',
        'advice': 'Rest, stay hydrated, and monitor temperature. Seek medical help if fever persists for more than 3 days or exceeds 103°F.',
        'when_to_see_doctor': 'If fever is above 103°F, lasts more than 3 days, or is accompanied by severe symptoms.',
        'severity': 'moderate'
    },
    'cough': {
        'description': 'Cough is a reflex action to clear airways of mucus and irritants.',
        'advice': 'Stay hydrated, use a humidifier, and avoid irritants. Consider over-the-counter cough suppressants for dry coughs.',
        'when_to_see_doctor': 'If cough persists for more than 2 weeks, produces blood, or is accompanied by chest pain.',
        'severity': 'mild'
    },
    'chest pain': {
        'description': 'Chest pain can range from mild discomfort to severe pain that may indicate serious conditions.',
        'advice': '⚠️ If severe, call emergency services immediately. For mild discomfort, rest and monitor symptoms.',
        'when_to_see_doctor': 'Any chest pain should be evaluated by a healthcare professional immediately.',
        'severity': 'high'
    },
    'stomach pain': {
        'description': 'Stomach pain can range from mild discomfort to severe abdominal pain.',
        'advice': 'Avoid solid foods initially, drink clear fluids, and rest. Apply heat to the abdomen for comfort.',
        'when_to_see_doctor': 'If pain is severe, persistent, or accompanied by vomiting, fever, or blood in stool.',
        'severity': 'moderate'
    },
    'fatigue': {
        'description': 'Fatigue is extreme tiredness or lack of energy that doesn\'t improve with rest.',
        'advice': 'Ensure adequate sleep, maintain a balanced diet, and stay hydrated. Consider light exercise.',
        'when_to_see_doctor': 'If fatigue persists for more than 2 weeks or is accompanied by other concerning symptoms.',
        'severity': 'mild'
    }
}

def analyze_symptoms(message):
    """Analyze user message for symptoms and provide appropriate response"""
    message_lower = message.lower()
    
    # Check for emergency keywords
    emergency_keywords = ['chest pain', 'heart attack', 'stroke', 'severe', 'emergency', 'can\'t breathe']
    if any(keyword in message_lower for keyword in emergency_keywords):
        return {
            'response': '🚨 EMERGENCY ALERT: If you are experiencing severe symptoms, please call emergency services (911) immediately or go to the nearest emergency room. This is not a substitute for emergency medical care.',
            'type': 'emergency',
            'severity': 'critical'
        }
    
    # Check for specific symptoms
    for symptom, info in HEALTH_KNOWLEDGE.items():
        if symptom in message_lower:
            return {
                'response': f"**{symptom.title()} Information:**\n\n{info['description']}\n\n**Self-care advice:** {info['advice']}\n\n**When to see a doctor:** {info['when_to_see_doctor']}",
                'type': 'symptom_info',
                'symptom': symptom,
                'severity': info['severity']
            }
    
    # Check for general health questions
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'help']):
        return {
            'response': "Hello! I'm FALCONCARE, your AI health assistant. I can help you with:\n\n• Symptom analysis and health advice\n• General health information\n• When to seek medical attention\n• Preventive care tips\n\nWhat health concern can I help you with today?",
            'type': 'greeting',
            'severity': 'low'
        }
    
    if any(word in message_lower for word in ['appointment', 'doctor', 'visit', 'schedule']):
        return {
            'response': "I can help you find healthcare providers in your area. For appointment scheduling, I recommend:\n\n• Contact your primary care physician\n• Use your insurance provider's directory\n• Check local hospital websites\n• Consider telemedicine options\n\nWhat type of specialist are you looking for?",
            'type': 'appointment',
            'severity': 'low'
        }
    
    if any(word in message_lower for word in ['vaccine', 'vaccination', 'immunization', 'shot']):
        return {
            'response': "I can provide information about various vaccines:\n\n• **COVID-19 vaccines:** Available for ages 6 months and older\n• **Flu vaccines:** Annual vaccination recommended\n• **Routine vaccines:** Follow CDC immunization schedule\n• **Travel vaccines:** Based on destination\n\nWhich type of vaccination information do you need?",
            'type': 'vaccination',
            'severity': 'low'
        }
    
    # Default response for unclear queries
    return {
        'response': "I'm here to help with your health concerns. Could you please provide more details about your symptoms or health questions? I can assist with:\n\n• Symptom analysis\n• Health advice\n• Medical information\n• Emergency guidance\n\nWhat would you like to know?",
        'type': 'general',
        'severity': 'low'
    }

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'FalconCare Backend',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'error': 'Message is required'
            }), 400
        
        # Analyze the message and get response
        analysis = analyze_symptoms(message)
        
        response = {
            'message': analysis['response'],
            'type': analysis['type'],
            'severity': analysis['severity'],
            'timestamp': datetime.now().isoformat(),
            'symptom': analysis.get('symptom'),
            'suggestions': get_suggestions(analysis['type'])
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

def get_suggestions(response_type):
    """Get follow-up suggestions based on response type"""
    suggestions = {
        'emergency': [
            "Call 911 immediately",
            "Go to nearest emergency room",
            "Contact emergency services"
        ],
        'symptom_info': [
            "Describe your symptoms in more detail",
            "How long have you had these symptoms?",
            "Are you taking any medications?",
            "Do you have any allergies?"
        ],
        'greeting': [
            "I have a headache",
            "I feel feverish",
            "I'm experiencing chest pain",
            "I need help with symptoms"
        ],
        'appointment': [
            "Find a cardiologist",
            "Schedule with primary care",
            "Book telemedicine appointment",
            "Find urgent care near me"
        ],
        'vaccination': [
            "COVID vaccine information",
            "Flu shot schedule",
            "Travel vaccines needed",
            "Childhood immunization"
        ],
        'general': [
            "I have symptoms to discuss",
            "I need health advice",
            "I want to know about vaccines",
            "I need emergency help"
        ]
    }
    
    return suggestions.get(response_type, ["How can I help you further?"])

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get list of supported symptoms"""
    return jsonify({
        'symptoms': list(HEALTH_KNOWLEDGE.keys()),
        'count': len(HEALTH_KNOWLEDGE)
    })

@app.route('/api/symptom/<symptom_name>', methods=['GET'])
def get_symptom_info(symptom_name):
    """Get detailed information about a specific symptom"""
    symptom = HEALTH_KNOWLEDGE.get(symptom_name.lower())
    if not symptom:
        return jsonify({
            'error': 'Symptom not found'
        }), 404
    
    return jsonify({
        'symptom': symptom_name,
        'information': symptom
    })

if __name__ == '__main__':
    print("🏥 FalconCare Backend Starting...")
    print("=" * 40)
    print("Health Check: http://localhost:5001/api/health")
    print("Chat API: http://localhost:5001/api/chat")
    print("Symptoms: http://localhost:5001/api/symptoms")
    print("=" * 40)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
