#!/usr/bin/env python3
"""
FalconCare Backend API
Extended Flask backend to handle chatbot, blog, symptom checker,
vaccination reminders, alerts, FAQs/tips/myths, hospitals finder,
profiles/diary, forum, and auth.

Disclaimer: This is not medical advice. Please consult a doctor.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from passlib.hash import bcrypt
import json
import re
import os
from datetime import datetime, timedelta
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///falconcare.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ACCESS_TOKEN_EXPIRES'] = timedelta(hours=12)

jwt = JWTManager(app)
db = SQLAlchemy(app)

# Constants
DISCLAIMER = "This is not medical advice. Please consult a doctor."

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(120), default='FalconCare Team')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HealthTip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    locale = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200), default='')


class Myth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    claim = db.Column(db.String(300), nullable=False)
    fact = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(300), default='WHO/ICMR')


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    vaccine = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    contact = db.Column(db.String(255), nullable=True)  # email or push token
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class OutbreakAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(400), nullable=False)
    severity = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class HealthProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    weight_kg = db.Column(db.Float)
    conditions = db.Column(db.String(300), default='')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HealthDiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, default=func.current_date())
    notes = db.Column(db.Text, default='')
    symptoms = db.Column(db.String(300), default='')


class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True)

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
        'version': '2.0.0',
        'disclaimer': DISCLAIMER
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
            'suggestions': get_suggestions(analysis['type']),
            'disclaimer': DISCLAIMER
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
        'information': symptom,
        'disclaimer': DISCLAIMER
    })


# ---------- Auth ----------
@app.post('/api/auth/signup')
def signup():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()
    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'email already registered'}), 409
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=str(user.id))
    return jsonify({'accessToken': token})


@app.post('/api/auth/login')
def login():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'invalid credentials'}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify({'accessToken': token})


# ---------- Blog ----------
@app.get('/api/blog')
def list_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return jsonify([
        {
            'id': p.id,
            'title': p.title,
            'summary': p.summary,
            'author': p.author,
            'created_at': p.created_at.isoformat()
        } for p in posts
    ])


@app.get('/api/blog/<int:post_id>')
def get_post(post_id: int):
    p = BlogPost.query.get_or_404(post_id)
    return jsonify({
        'id': p.id,
        'title': p.title,
        'summary': p.summary,
        'content': p.content,
        'author': p.author,
        'created_at': p.created_at.isoformat(),
        'updated_at': p.updated_at.isoformat(),
        'disclaimer': DISCLAIMER
    })


@app.post('/api/blog')
@jwt_required()
def create_post():
    data = request.get_json() or {}
    if not all([data.get('title'), data.get('summary'), data.get('content')]):
        return jsonify({'error': 'title, summary, content required'}), 400
    post = BlogPost(
        title=data['title'].strip(),
        summary=data['summary'].strip(),
        content=data['content'].strip(),
        author=data.get('author') or 'FalconCare Team'
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({'id': post.id}), 201


@app.put('/api/blog/<int:post_id>')
@jwt_required()
def update_post(post_id: int):
    p = BlogPost.query.get_or_404(post_id)
    data = request.get_json() or {}
    p.title = data.get('title', p.title)
    p.summary = data.get('summary', p.summary)
    p.content = data.get('content', p.content)
    p.author = data.get('author', p.author)
    db.session.commit()
    return jsonify({'status': 'updated'})


@app.delete('/api/blog/<int:post_id>')
@jwt_required()
def delete_post(post_id: int):
    p = BlogPost.query.get_or_404(post_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'status': 'deleted'})


# ---------- Symptom Checker (rule + simple mapping) ----------
DISEASE_RULES = {
    'flu': {'symptoms': {'fever', 'cough', 'sore throat', 'fatigue'}},
    'dengue': {'symptoms': {'fever', 'rash', 'joint pain', 'headache'}},
    'malaria': {'symptoms': {'fever', 'chills', 'sweats', 'headache'}},
}


@app.post('/api/symptom-checker')
def symptom_checker():
    data = request.get_json() or {}
    input_symptoms = {s.strip().lower() for s in (data.get('symptoms') or []) if s.strip()}
    if not input_symptoms:
        return jsonify({'error': 'symptoms array required'}), 400
    matches = []
    for disease, conf in DISEASE_RULES.items():
        overlap = input_symptoms & conf['symptoms']
        if overlap:
            score = round(len(overlap) / len(conf['symptoms']), 2)
            matches.append({'condition': disease, 'score': score})
    matches.sort(key=lambda m: m['score'], reverse=True)
    return jsonify({
        'possible_conditions': matches,
        'disclaimer': DISCLAIMER
    })


# ---------- Vaccination Reminders ----------
@app.get('/api/reminders')
@jwt_required()
def list_reminders():
    user_id = int(get_jwt_identity())
    reminders = Reminder.query.filter_by(user_id=user_id).order_by(Reminder.due_date.asc()).all()
    return jsonify([
        {
            'id': r.id, 'vaccine': r.vaccine, 'due_date': r.due_date.isoformat(), 'contact': r.contact
        } for r in reminders
    ])


@app.post('/api/reminders')
@jwt_required()
def create_reminder():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    if not data.get('vaccine') or not data.get('due_date'):
        return jsonify({'error': 'vaccine and due_date required'}), 400
    due = datetime.fromisoformat(data['due_date'])
    r = Reminder(user_id=user_id, vaccine=data['vaccine'], due_date=due, contact=data.get('contact'))
    db.session.add(r)
    db.session.commit()
    # Stub: send email/push via Firebase/SES, etc.
    return jsonify({'id': r.id}), 201


@app.delete('/api/reminders/<int:reminder_id>')
@jwt_required()
def delete_reminder(reminder_id: int):
    user_id = int(get_jwt_identity())
    r = Reminder.query.get_or_404(reminder_id)
    if r.user_id != user_id:
        return jsonify({'error': 'forbidden'}), 403
    db.session.delete(r)
    db.session.commit()
    return jsonify({'status': 'deleted'})


# ---------- Outbreak Alerts (dummy + external) ----------
@app.get('/api/alerts')
def get_alerts():
    region = request.args.get('region', 'Delhi NCR')
    # Try external source (dummy fallback)
    alerts = OutbreakAlert.query.order_by(OutbreakAlert.created_at.desc()).limit(5).all()
    seeded = [
        {'region': region, 'message': '⚠️ Dengue cases rising in Delhi NCR', 'severity': 'high'}
    ] if not alerts else []
    db_alerts = [
        {'region': a.region, 'message': a.message, 'severity': a.severity, 'created_at': a.created_at.isoformat()}
        for a in alerts
    ]
    return jsonify({'alerts': seeded + db_alerts})


# ---------- Hospitals Finder (Google Places proxy) ----------
@app.get('/api/hospitals')
def hospitals():
    # Accept lat,lng; for demo, return static list if API key missing
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if api_key and lat and lng:
        try:
            resp = requests.get(
                'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
                params={'location': f'{lat},{lng}', 'radius': 5000, 'type': 'hospital', 'key': api_key}, timeout=8
            )
            data = resp.json()
            results = [
                {
                    'name': r.get('name'),
                    'address': r.get('vicinity'),
                    'location': r.get('geometry', {}).get('location')
                } for r in data.get('results', [])
            ]
            return jsonify({'hospitals': results})
        except Exception as e:
            pass
    # Fallback demo data
    return jsonify({'hospitals': [
        {'name': 'City Care Hospital', 'address': 'Sector 21, Delhi', 'location': {'lat': 28.6, 'lng': 77.2}},
        {'name': 'Metro Health Clinic', 'address': 'Noida Phase 2', 'location': {'lat': 28.5, 'lng': 77.3}},
    ]})


# ---------- FAQ / Tips / Myths ----------
@app.get('/api/faq')
def list_faq():
    items = FAQ.query.all()
    return jsonify([{'id': i.id, 'question': i.question, 'answer': i.answer} for i in items])


@app.get('/api/tips/daily')
def daily_tip():
    # Pick one random tip deterministically by date
    tip = HealthTip.query.order_by(func.random()).first()
    if not tip:
        return jsonify({'tip': 'Stay hydrated and take a 10-minute walk today.'})
    return jsonify({'tip': tip.text, 'locale': tip.locale})


@app.get('/api/myths/check')
def check_myth():
    text = (request.args.get('q') or '').lower()
    if not text:
        return jsonify({'error': 'q required'}), 400
    for m in Myth.query.all():
        if m.claim.lower() in text:
            return jsonify({'myth': m.claim, 'fact': m.fact, 'source': m.source})
    return jsonify({'result': 'no_match'})


# ---------- Profiles / Diary ----------
@app.get('/api/profile')
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    p = HealthProfile.query.filter_by(user_id=user_id).first()
    if not p:
        return jsonify({})
    return jsonify({'age': p.age, 'gender': p.gender, 'weight_kg': p.weight_kg, 'conditions': p.conditions})


@app.post('/api/profile')
@jwt_required()
def upsert_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    p = HealthProfile.query.filter_by(user_id=user_id).first()
    if not p:
        p = HealthProfile(user_id=user_id)
        db.session.add(p)
    p.age = data.get('age', p.age)
    p.gender = data.get('gender', p.gender)
    p.weight_kg = data.get('weight_kg', p.weight_kg)
    p.conditions = data.get('conditions', p.conditions)
    db.session.commit()
    return jsonify({'status': 'saved'})


@app.get('/api/diary')
@jwt_required()
def list_diary():
    user_id = int(get_jwt_identity())
    entries = HealthDiaryEntry.query.filter_by(user_id=user_id).order_by(HealthDiaryEntry.date.desc()).limit(14).all()
    return jsonify([
        {'id': e.id, 'date': e.date.isoformat(), 'notes': e.notes, 'symptoms': e.symptoms}
        for e in entries
    ])


@app.post('/api/diary')
@jwt_required()
def add_diary():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    entry = HealthDiaryEntry(user_id=user_id, date=datetime.fromisoformat(data.get('date')).date() if data.get('date') else None,
                             notes=data.get('notes', ''), symptoms=','.join(data.get('symptoms', [])))
    db.session.add(entry)
    db.session.commit()
    return jsonify({'id': entry.id}), 201


# ---------- Forum (anonymous) ----------
@app.get('/api/forum')
def list_forum():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).limit(50).all()
    return jsonify([
        {'id': p.id, 'content': p.content, 'created_at': p.created_at.isoformat()}
        for p in posts if p.is_approved
    ])


@app.post('/api/forum')
def create_forum():
    data = request.get_json() or {}
    if not data.get('content'):
        return jsonify({'error': 'content required'}), 400
    p = ForumPost(content=data['content'][:1000])
    db.session.add(p)
    db.session.commit()
    return jsonify({'id': p.id}), 201

if __name__ == '__main__':
    print("🏥 FalconCare Backend Starting...")
    print("=" * 40)
    print("Health Check: http://localhost:5001/api/health")
    print("Chat API: http://localhost:5001/api/chat")
    print("Symptoms: http://localhost:5001/api/symptoms")
    print("Blog: http://localhost:5001/api/blog")
    print("Auth: http://localhost:5001/api/auth/signup | /login")
    print("=" * 40)
    with app.app_context():
        db.create_all()
        # Seed minimal data if empty
        if not FAQ.query.first():
            faqs = [
                FAQ(question='What are symptoms of dengue?', answer='High fever, severe headache, pain behind the eyes, joint and muscle pain, rash.'),
                FAQ(question='How to prevent malaria?', answer='Use mosquito nets, repellents, and eliminate standing water.')
            ]
            db.session.add_all(faqs)
        if not HealthTip.query.first():
            db.session.add(HealthTip(text='Drink at least 8 glasses of water today.'))
        if not Myth.query.first():
            db.session.add(Myth(claim='Alcohol cures COVID', fact='No. Alcohol does not cure COVID-19. Follow public health guidance.', source='WHO'))
        if not OutbreakAlert.query.first():
            db.session.add(OutbreakAlert(region='Delhi NCR', message='⚠️ Dengue cases rising in Delhi NCR', severity='high'))
        db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', '5001')))
