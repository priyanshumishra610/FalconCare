# 🚀 **HOW TO RUN FALCONCARE - SIMPLE GUIDE**

## **⚡ EASIEST WAY (One Command)**

```bash
cd /workspace
./start_falconcare.sh
```

**What this does:**
- ✅ Installs all dependencies
- ✅ Trains the AI model
- ✅ Starts Rasa chatbot (advanced AI)
- ✅ Starts beautiful web frontend  
- ✅ Starts all demo services

**Then open:** http://localhost:5173

---

## **🎭 FOR SIH JUDGES DEMO**

### **Quick Demo Setup:**
```bash
# 1. Start everything
./start_falconcare.sh

# 2. Open in browser
# Web App: http://localhost:5173
# Click the chat button to talk to FalconCare
```

### **Advanced Features Demo:**
```bash
# While start_falconcare.sh is running, open these in browser:

# Feature Phone Demo: http://localhost:5002  
# Government Dashboard: http://localhost:8501
```

---

## **💬 TEST THE CHATBOT**

### **In Web Interface (http://localhost:5173):**
```
✅ Hindi: "नमस्ते" → Should respond "मैं FalconCare हूं"
✅ Emergency: "सीने में दर्द है" → Should show RED alert
✅ Myth: "हल्दी से कैंसर ठीक होता है" → Should detect myth
✅ Vaccine: "बच्चे का टीका कब लगवाएं" → Should show schedule
```

### **In Terminal (rasa shell):**
```bash
# If you want to test the core AI directly
rasa shell
```

---

## **🔧 ALTERNATIVE: Manual Setup**

If the one-command approach doesn't work:

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

### **Step 2: Train Model**  
```bash
rasa train
```

### **Step 3: Start Services (3 Terminals)**

**Terminal 1: Rasa Actions**
```bash
rasa run actions --debug
```

**Terminal 2: Rasa Core**
```bash  
rasa run --enable-api --cors "*" --port 5005
```

**Terminal 3: Frontend**
```bash
cd frontend && npm run dev
```

**Then open:** http://localhost:5173

---

## **🎯 WHAT YOU'LL SEE**

### **Web Interface Features:**
- 🎨 **Beautiful Modern UI** - Gradient design, animations
- 🤖 **FalconCare Chatbot** - Click floating chat button
- 🗣️ **Multilingual** - Hindi + English support
- 🚨 **Emergency Detection** - RED alerts for serious symptoms
- ❌ **Myth Busting** - Detects health misinformation
- 💉 **Vaccination Info** - Government API integration
- 🏥 **Hospital Finder** - Location-based services

### **Advanced Features:**
- 📱 **Feature Phone Support** - http://localhost:5002
- 📊 **Government Dashboard** - http://localhost:8501  
- 🎯 **Smart Triage** - RED/YELLOW/GREEN classification
- 🌐 **USSD Simulation** - Works without internet

---

## **🚨 TROUBLESHOOTING**

### **If Web Frontend Not Working:**
```bash
# Check if Node.js is installed
node --version
npm --version

# If not installed:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### **If Rasa Not Working:**
```bash
# Reinstall Rasa
pip install --upgrade rasa rasa-sdk

# Train model again
rasa train --force
```

### **If Services Won't Start:**
```bash
# Kill existing processes
pkill -f rasa
pkill -f node
pkill -f python

# Try again
./start_falconcare.sh
```

---

## **✅ SUCCESS INDICATORS**

**You know FalconCare is working when:**

1. ✅ **Web page loads** at http://localhost:5173
2. ✅ **Chat button appears** (floating blue button)
3. ✅ **Bot responds** with "मैं FalconCare हूं" to Hindi greetings
4. ✅ **Emergency detection** works (try "chest pain")
5. ✅ **Myth detection** works (try "turmeric cures cancer")

---

## **🎉 SIH DEMO READY!**

**Judge Demo Sequence:**
1. **Open:** http://localhost:5173
2. **Click:** Floating chat button  
3. **Test:** "नमस्ते" (Hindi greeting)
4. **Test:** "सीने में दर्द है" (Emergency)
5. **Test:** "हल्दी से कैंसर ठीक होता है" (Myth)
6. **Show:** Feature phone demo at http://localhost:5002

**🏆 FalconCare is ready to win Smart India Hackathon! 🎯**

---

## **📞 NEED HELP?**

**Quick Commands:**
```bash
# Check what's running
./start_falconcare.sh

# Test the AI
python test_health_guardian.py

# Train model again
rasa train --force

# Direct chat
rasa shell
```

**🌟 FalconCare - From Village to Victory! 🇮🇳**