# 🏥 FalconCare - AI Healthcare Assistant

FalconCare is a revolutionary AI-powered healthcare assistant that combines a stunning 3D-animated React frontend with an intelligent Python backend to provide comprehensive health guidance, symptom analysis, and medical assistance.

## 🌟 Features

### Frontend (React + Three.js)
- **3D Medical Globe**: Interactive 3D visualization with floating particles
- **Modern UI/UX**: Beautiful animations powered by GSAP
- **Dark/Light Mode**: Seamless theme switching
- **Responsive Design**: Works perfectly on all devices
- **Real-time Chat**: Integrated chatbot interface
- **Smooth Animations**: Scroll-triggered animations and transitions

### Backend (Python Flask)
- **Intelligent Health Analysis**: AI-powered symptom recognition
- **Emergency Detection**: Automatic emergency response alerts
- **Comprehensive Knowledge Base**: Covers 100+ health conditions
- **RESTful API**: Clean, well-documented endpoints
- **CORS Support**: Seamless frontend integration
- **Error Handling**: Robust error management

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- pip

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   python3 app.py
   ```
   
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
FalconCare/
├── backend/
│   ├── app.py                 # Flask backend server
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Chatbot.js     # Chatbot component
│   │   ├── App.js             # Main React app
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Global styles
│   ├── index.html             # HTML template
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   └── tailwind.config.js     # Tailwind CSS config
├── data/                      # Rasa training data (legacy)
├── actions/                   # Rasa custom actions (legacy)
└── README.md                  # This file
```

## 🔧 API Endpoints

### Health Check
```
GET /api/health
```
Returns server status and version information.

### Chat with Bot
```
POST /api/chat
Content-Type: application/json

{
  "message": "I have a headache"
}
```

**Response:**
```json
{
  "message": "**Headache Information:**\n\nHeadache is pain or discomfort in the head or neck area.\n\n**Self-care advice:** Rest in a dark room, apply cold compress, and stay hydrated.\n\n**When to see a doctor:** If headache is severe, sudden, or accompanied by fever, neck stiffness, or vision changes.",
  "type": "symptom_info",
  "severity": "moderate",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "symptom": "headache",
  "suggestions": [
    "Describe your symptoms in more detail",
    "How long have you had these symptoms?",
    "Are you taking any medications?",
    "Do you have any allergies?"
  ]
}
```

### Get Available Symptoms
```
GET /api/symptoms
```
Returns list of supported symptoms.

### Get Specific Symptom Info
```
GET /api/symptom/{symptom_name}
```
Returns detailed information about a specific symptom.

## 🎨 Frontend Features

### 3D Animations
- **Medical Globe**: Rotating 3D sphere with particle effects
- **Floating Icons**: Animated health-related symbols
- **Smooth Transitions**: GSAP-powered animations

### Interactive Elements
- **Dark Mode Toggle**: Seamless theme switching
- **Floating Chat Button**: Always-accessible chatbot
- **Scroll Animations**: Elements animate on scroll
- **Hover Effects**: Interactive card animations

### Responsive Design
- **Mobile-First**: Optimized for all screen sizes
- **Touch-Friendly**: Gesture support for mobile devices
- **Performance**: Optimized for smooth 60fps animations

## 🧠 Backend Intelligence

### Symptom Analysis
The backend can recognize and provide information about:
- **Headaches**: Various types and severity levels
- **Fever**: Temperature monitoring and care advice
- **Cough**: Respiratory health guidance
- **Chest Pain**: Emergency detection and response
- **Stomach Pain**: Digestive health information
- **Fatigue**: Energy and wellness guidance

### Emergency Detection
Automatically detects emergency keywords and provides:
- 🚨 Immediate emergency alerts
- Critical care instructions
- Emergency service contact information

### Smart Responses
- **Context-Aware**: Understands conversation flow
- **Suggestion System**: Provides follow-up questions
- **Severity Assessment**: Categorizes health concerns
- **Personalized Advice**: Tailored health recommendations

## 🛠️ Development

### Backend Development
```bash
cd backend
python3 app.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Building for Production
```bash
cd frontend
npm run build
```

## 🔒 Security & Privacy

- **No Data Storage**: Conversations are not permanently stored
- **CORS Protection**: Secure cross-origin requests
- **Input Validation**: All inputs are sanitized
- **Error Handling**: Graceful error management

## 🌐 Deployment

### Backend Deployment
1. Deploy to any Python hosting service (Heroku, Railway, etc.)
2. Set environment variables if needed
3. Ensure CORS is configured for your frontend domain

### Frontend Deployment
1. Build the production version: `npm run build`
2. Deploy the `dist` folder to any static hosting service
3. Configure API endpoints to point to your backend

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the code examples

## 🔮 Future Enhancements

- **Rasa Integration**: Full conversational AI capabilities
- **User Authentication**: Personalized health profiles
- **Medical Database**: Integration with health databases
- **Telemedicine**: Video consultation features
- **Mobile App**: Native iOS/Android applications
- **Analytics**: Health trend tracking and insights

---

**Built with ❤️ for healthcare innovation**

*FalconCare - Revolutionizing healthcare with AI-powered assistance*