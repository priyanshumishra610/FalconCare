# Health Guardian AI - Main Actions Module
# Imports all custom health actions for the chatbot

# Import core health actions
from .health_actions import (
    ActionTriageSymptoms,
    ActionEmergencyCall,
    ActionDetectMyth
)

# Import government API integrations
from .govt_apis import (
    ActionCheckVaccination,
    ActionDiseaseStats,
    ActionFindHospital,
    ActionVaccinationReminder
)

# Import conversation flow actions
from .conversation_flows import (
    ActionAskDuration,
    ActionAskSeverity,
    ActionAskOtherSymptoms,
    ActionAskLocation,
    ActionAskAge,
    ActionProvidePreventionAdvice,
    ActionDefaultFallback
)

# Additional health information actions
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionMedicineInformation(Action):
    """Provide medicine information and dosage guidance"""

    def name(self) -> Text:
        return "action_medicine_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_intent = tracker.latest_message.get('intent', {}).get('name', '')
        user_message = tracker.latest_message.get('text', '').lower()

        if current_intent == "medicine_dosage" or "dosage" in user_message:
            medicine_advice = """
💊 **दवा लेने के सामान्य नियम:**

⏰ **समय:**
• डॉक्टर के बताए अनुसार
• खाना खाने से पहले/बाद (जैसा लिखा हो)
• पूरा कोर्स करें, बीच में न छोड़ें

🥛 **कैसे लें:**
• साफ पानी के साथ
• दूध के साथ केवल डॉक्टर कहे तो
• गोली को तोड़ें नहीं (जब तक न कहा जाए)

⚠️ **सावधानी:**
• दूसरों की दवा न लें
• एक्सपायरी डेट चेक करें
• साइड इफेक्ट दिखे तो डॉक्टर को बताएं

📱 **आपातकाल:** 102 या नजदीकी अस्पताल
            """
        else:  # medicine_side_effects
            medicine_advice = """
⚠️ **दवा के साइड इफेक्ट्स:**

🤢 **आम साइड इफेक्ट्स:**
• जी मिचलाना
• चक्कर आना
• पेट दर्द
• कमजोरी लगना

🚨 **गंभीर साइड इफेक्ट्स (तुरंत डॉक्टर को दिखाएं):**
• सांस लेने में तकलीफ
• चेहरे पर सूजन
• तेज चकत्ते
• बेहोशी

💡 **क्या करें:**
• दवा बंद कर दें
• तुरंत डॉक्टर से संपर्क करें
• एलर्जी की लिस्ट बनाकर रखें

📞 **आपातकाल:** 108 या 102
            """

        dispatcher.utter_message(text=medicine_advice)

        buttons = [
            {"title": "🏥 नजदीकी अस्पताल", "payload": "/find_doctor"},
            {"title": "📞 108 कॉल करें", "payload": "tel:108"}
        ]
        
        dispatcher.utter_message(text="और कोई सवाल है?", buttons=buttons)
        
        return []


# Export all actions for easy import
__all__ = [
    'ActionTriageSymptoms',
    'ActionEmergencyCall', 
    'ActionDetectMyth',
    'ActionCheckVaccination',
    'ActionDiseaseStats',
    'ActionFindHospital',
    'ActionVaccinationReminder',
    'ActionAskDuration',
    'ActionAskSeverity', 
    'ActionAskOtherSymptoms',
    'ActionAskLocation',
    'ActionAskAge',
    'ActionProvidePreventionAdvice',
    'ActionMedicineInformation',
    'ActionDefaultFallback'
]
