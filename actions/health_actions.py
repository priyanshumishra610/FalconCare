# Health Guardian AI - Core Medical Actions
# Smart Triage System, Myth Busting, Emergency Response

from typing import Any, Text, Dict, List
import requests
import json
import re
from datetime import datetime
from fuzzywuzzy import fuzz

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction


class ActionTriageSymptoms(Action):
    """
    Intelligent medical triage system with RED/YELLOW/GREEN classification
    Analyzes symptoms, duration, severity, and patient age for risk assessment
    """

    def name(self) -> Text:
        return "action_triage_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Emergency symptoms requiring immediate attention (RED)
        RED_FLAGS = [
            "chest pain", "सीने में दर्द", "difficulty breathing", "सांस नहीं आ रही",
            "unconscious", "बेहोश", "heart attack", "दिल का दौरा",
            "severe bleeding", "खून बह रहा", "stroke", "लकवा",
            "severe chest pain", "तेज सीने का दर्द", "can't breathe", "सांस फूल रही",
            "suicide", "आत्महत्या", "bleeding heavily", "बहुत खून",
            "accident", "दुर्घटना", "seizure", "दौरा पड़ना"
        ]

        # Warning symptoms needing medical attention (YELLOW)
        YELLOW_FLAGS = [
            "high fever 3 days", "3 दिन से तेज बुखार", "severe vomiting", "बहुत उल्टी",
            "blood in vomit", "खून की उल्टी", "severe diarrhea", "बहुत दस्त",
            "dehydration", "पानी की कमी", "persistent fever", "लगातार बुखार",
            "blood in stool", "खून के दस्त", "severe headache", "तेज सिरदर्द",
            "very weak", "बहुत कमजोरी", "fever with rash", "बुखार और दाने"
        ]

        # Extract information from tracker
        current_intent = tracker.latest_message.get('intent', {}).get('name', '')
        user_message = tracker.latest_message.get('text', '').lower()
        
        symptom = tracker.get_slot("symptom") or ""
        duration = tracker.get_slot("duration") or ""
        severity = tracker.get_slot("severity") or ""
        patient_age = tracker.get_slot("patient_age") or ""

        # Calculate risk score
        risk_score = 0
        triage_level = "GREEN"

        # Check for emergency symptoms (RED flags)
        for red_flag in RED_FLAGS:
            if red_flag.lower() in user_message or red_flag.lower() in symptom.lower():
                risk_score += 100
                triage_level = "RED"
                break

        # Check for warning symptoms (YELLOW flags) if not RED
        if triage_level != "RED":
            for yellow_flag in YELLOW_FLAGS:
                if yellow_flag.lower() in user_message or yellow_flag.lower() in symptom.lower():
                    risk_score += 50
                    triage_level = "YELLOW"
                    break

        # Severity multiplier
        if "severe" in severity.lower() or "तेज" in severity or "बहुत" in severity:
            risk_score += 30
        elif "moderate" in severity.lower() or "मध्यम" in severity:
            risk_score += 15

        # Duration factor
        if any(term in duration.lower() for term in ["week", "सप्ताह", "month", "महीना"]):
            risk_score += 20
        elif any(term in duration.lower() for term in ["3 days", "3 दिन", "4 days", "4 दिन"]):
            risk_score += 15

        # Age factor (higher risk for children and elderly)
        try:
            age_num = int(re.findall(r'\d+', patient_age)[0]) if patient_age else 25
            if age_num < 5 or age_num > 60:
                risk_score += 10
        except:
            pass

        # Emergency intent check
        if current_intent in ["emergency_severe", "ambulance_help"]:
            risk_score += 100
            triage_level = "RED"

        # Final triage classification based on total risk score
        if risk_score >= 80:
            triage_level = "RED"
        elif risk_score >= 40:
            triage_level = "YELLOW"
        else:
            triage_level = "GREEN"

        # Generate appropriate response
        if triage_level == "RED":
            dispatcher.utter_message(response="utter_emergency_alert")
            return [
                SlotSet("triage_level", "RED"),
                FollowupAction("action_emergency_call")
            ]
        
        elif triage_level == "YELLOW":
            dispatcher.utter_message(response="utter_moderate_warning")
            return [
                SlotSet("triage_level", "YELLOW"),
                FollowupAction("action_find_hospital")
            ]
        
        else:  # GREEN
            dispatcher.utter_message(response="utter_mild_advice")
            # Provide specific home care advice based on symptom
            if "fever" in symptom.lower() or "बुखार" in symptom:
                advice = "💧 पानी पिएं, आराम करें, पैरासिटामोल ले सकते हैं। अगर 48 घंटे में सुधार न हो तो डॉक्टर से मिलें।"
            elif "cough" in symptom.lower() or "खांसी" in symptom:
                advice = "🍯 गुनगुना पानी और शहद लें। भाप लें। धूम्रपान से बचें।"
            elif "stomach" in symptom.lower() or "पेट" in symptom:
                advice = "💧 ORS घोल पिएं। हल्का भोजन लें। तली चीजें न खाएं।"
            else:
                advice = "💧 आराम करें, पानी पिएं। 2-3 दिन में सुधार न हो तो डॉक्टर से मिलें।"
            
            dispatcher.utter_message(text=advice)
            return [SlotSet("triage_level", "GREEN")]


class ActionEmergencyCall(Action):
    """Emergency response action for RED triage cases"""

    def name(self) -> Text:
        return "action_emergency_call"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptom = tracker.get_slot("symptom") or "आपातकाल"
        
        emergency_message = f"""
🚨 **आपातकालीन सहायता**

📞 **तुरंत कॉल करें:**
• एम्बुलेंस: 108
• आपातकाल: 102

🏥 **समस्या:** {symptom}
⏰ **समय:** {datetime.now().strftime('%H:%M')}

🗺️ **निकटतम अस्पताल देखने के लिए "नजदीकी अस्पताल" लिखें**
        """

        # Create call buttons
        buttons = [
            {
                "title": "📞 108 कॉल करें",
                "payload": "tel:108",
                "type": "phone_number"
            },
            {
                "title": "🏥 नजदीकी अस्पताल",
                "payload": "/find_doctor"
            }
        ]

        dispatcher.utter_message(text=emergency_message, buttons=buttons)
        
        # Log emergency case for health authorities
        self._log_emergency_case(tracker)
        
        return []

    def _log_emergency_case(self, tracker):
        """Log emergency case for health department dashboard"""
        try:
            emergency_data = {
                "timestamp": datetime.now().isoformat(),
                "user_id": tracker.sender_id,
                "symptom": tracker.get_slot("symptom"),
                "triage_level": "RED",
                "location": tracker.get_slot("user_location"),
                "alert_sent": True
            }
            # In production, save to database
            print(f"EMERGENCY ALERT: {emergency_data}")
        except Exception as e:
            print(f"Error logging emergency: {e}")


class ActionDetectMyth(Action):
    """Detect and counter health myths and misinformation"""

    def name(self) -> Text:
        return "action_detect_myth"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()
        
        # Load myths database
        myths = self._load_myths_database()
        
        # Check for myths in user message
        detected_myth = self._detect_myth_in_text(user_message, myths)
        
        if detected_myth:
            dispatcher.utter_message(response="utter_myth_detected")
            
            myth_response = f"""
❌ **गलत जानकारी:** {detected_myth['myth_statement']}

✅ **सही जानकारी:**
{detected_myth['fact']}

📚 **स्रोत:** {detected_myth['source']}

🩺 **सलाह:** किसी भी स्वास्थ्य समस्या के लिए योग्य डॉक्टर से सलाह लें।
            """
            
            dispatcher.utter_message(text=myth_response)
            return [SlotSet("myth_detected", True)]
        
        return [SlotSet("myth_detected", False)]

    def _load_myths_database(self):
        """Load comprehensive Indian health myths database"""
        myths = [
            {
                "keywords": ["haldi", "turmeric", "cancer", "cure", "हल्दी", "कैंसर"],
                "myth_statement": "हल्दी से कैंसर ठीक हो जाता है",
                "fact": "हल्दी में एंटी-इंफ्लामेटरी गुण हैं लेकिन यह कैंसर का इलाज नहीं है। कैंसर के लिए चिकित्सक की सलाह और उचित इलाज जरूरी है।",
                "source": "भारतीय चिकित्सा अनुसंधान परिषद (ICMR)"
            },
            {
                "keywords": ["tb", "touch", "chhune", "फैलता", "tuberculosis"],
                "myth_statement": "TB छूने से फैलता है",
                "fact": "TB हवा के जरिए फैलता है, छूने से नहीं। TB मरीज़ के खांसने या छींकने से हवा में बैक्टीरिया फैलता है।",
                "source": "राष्ट्रीय क्षय रोग उन्मूलन कार्यक्रम"
            },
            {
                "keywords": ["vaccine", "autism", "टीका", "बीमारी", "side effect"],
                "myth_statement": "वैक्सीन से बच्चे बीमार हो जाते हैं",
                "fact": "वैक्सीन सुरक्षित हैं और बीमारियों से बचाती हैं। हल्के साइड इफेक्ट्स हो सकते हैं लेकिन गंभीर बीमारियों से बचाव जरूरी है।",
                "source": "भारत सरकार स्वास्थ्य मंत्रालय"
            },
            {
                "keywords": ["antibiotics", "virus", "cold", "flu", "एंटीबायोटिक"],
                "myth_statement": "एंटीबायोटिक हर बीमारी ठीक करता है",
                "fact": "एंटीबायोटिक केवल बैक्टीरियल संक्रमण के लिए है, वायरल बीमारी (जुकाम, फ्लू) के लिए नहीं। गलत उपयोग से प्रतिरोध बढ़ता है।",
                "source": "WHO और भारत सरकार"
            },
            {
                "keywords": ["cow urine", "गौमूत्र", "covid", "corona"],
                "myth_statement": "गौमूत्र से कोविड ठीक होता है",
                "fact": "गौमूत्र से कोविड का इलाज नहीं होता। कोविड के लिए वैक्सीन, मास्क, सामाजिक दूरी और डॉक्टर की सलाह जरूरी है।",
                "source": "WHO और भारत सरकार"
            }
        ]
        return myths

    def _detect_myth_in_text(self, text, myths):
        """Detect if text contains health myth using fuzzy matching"""
        for myth in myths:
            # Check if multiple keywords match
            matched_keywords = 0
            for keyword in myth['keywords']:
                if keyword.lower() in text or fuzz.partial_ratio(keyword.lower(), text) > 80:
                    matched_keywords += 1
            
            # If 2+ keywords match, consider it a myth
            if matched_keywords >= 2:
                return myth
        
        return None