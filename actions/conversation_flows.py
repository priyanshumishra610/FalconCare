# FalconCare - Conversation Flow Management
# Context-aware follow-up questions and conversation management

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction


class ActionAskDuration(Action):
    """Ask for symptom duration with context-aware buttons"""

    def name(self) -> Text:
        return "action_ask_duration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptom = tracker.get_slot("symptom") or "समस्या"
        
        buttons = [
            {"title": "आज से", "payload": '/inform_duration{"duration":"today"}'},
            {"title": "1-2 दिन", "payload": '/inform_duration{"duration":"1-2 days"}'},
            {"title": "3-7 दिन", "payload": '/inform_duration{"duration":"3-7 days"}'},
            {"title": "1 सप्ताह से ज्यादा", "payload": '/inform_duration{"duration":"more than week"}'}
        ]

        dispatcher.utter_message(
            text=f"कब से {symptom} है? कृपया बताएं:",
            buttons=buttons
        )
        
        return []


class ActionAskSeverity(Action):
    """Ask for symptom severity with intuitive options"""

    def name(self) -> Text:
        return "action_ask_severity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = [
            {"title": "हल्की तकलीफ", "payload": '/inform_severity{"severity":"mild"}'},
            {"title": "मध्यम तकलीफ", "payload": '/inform_severity{"severity":"moderate"}'},
            {"title": "बहुत तेज तकलीफ", "payload": '/inform_severity{"severity":"severe"}'}
        ]

        dispatcher.utter_message(
            text="कितनी तकलीफ है?",
            buttons=buttons
        )
        
        return []


class ActionAskOtherSymptoms(Action):
    """Ask for additional symptoms based on primary symptom"""

    def name(self) -> Text:
        return "action_ask_other_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        primary_symptom = tracker.get_slot("symptom") or ""
        
        # Context-aware symptom suggestions
        if "fever" in primary_symptom.lower() or "बुखार" in primary_symptom:
            buttons = [
                {"title": "सिरदर्द", "payload": '/inform_symptom{"symptom":"headache"}'},
                {"title": "शरीर दर्द", "payload": '/inform_symptom{"symptom":"body ache"}'},
                {"title": "उल्टी", "payload": '/inform_symptom{"symptom":"vomiting"}'},
                {"title": "कोई और नहीं", "payload": "/affirm"}
            ]
        elif "cough" in primary_symptom.lower() or "खांसी" in primary_symptom:
            buttons = [
                {"title": "बुखार", "payload": '/inform_symptom{"symptom":"fever"}'},
                {"title": "सांस फूलना", "payload": '/inform_symptom{"symptom":"breathing problem"}'},
                {"title": "सीने में दर्द", "payload": '/inform_symptom{"symptom":"chest pain"}'},
                {"title": "कोई और नहीं", "payload": "/affirm"}
            ]
        else:
            buttons = [
                {"title": "बुखार", "payload": '/inform_symptom{"symptom":"fever"}'},
                {"title": "सिरदर्द", "payload": '/inform_symptom{"symptom":"headache"}'},
                {"title": "कमजोरी", "payload": '/inform_symptom{"symptom":"weakness"}'},
                {"title": "कोई और नहीं", "payload": "/affirm"}
            ]

        dispatcher.utter_message(
            text="और कोई परेशानी है?",
            buttons=buttons
        )
        
        return []


class ActionAskLocation(Action):
    """Ask for user location for finding nearby services"""

    def name(self) -> Text:
        return "action_ask_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = [
            {"title": "रायपुर", "payload": '/inform_location{"location":"raipur"}'},
            {"title": "बिलासपुर", "payload": '/inform_location{"location":"bilaspur"}'},
            {"title": "भिलाई", "payload": '/inform_location{"location":"bhilai"}'},
            {"title": "दुर्ग", "payload": '/inform_location{"location":"durg"}'}
        ]

        dispatcher.utter_message(
            text="आप कहां रहते हैं? अपना जिला या पिनकोड बताएं:",
            buttons=buttons
        )
        
        return []


class ActionAskAge(Action):
    """Ask for patient age for personalized advice"""

    def name(self) -> Text:
        return "action_ask_age"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        patient_relation = tracker.get_slot("patient_relation") or ""
        
        if "child" in patient_relation.lower() or "बच्चा" in patient_relation:
            question = "बच्चे की उम्र कितनी है?"
            buttons = [
                {"title": "1 साल से कम", "payload": '/inform_age{"age":"under 1 year"}'},
                {"title": "1-5 साल", "payload": '/inform_age{"age":"1-5 years"}'},
                {"title": "5-12 साल", "payload": '/inform_age{"age":"5-12 years"}'},
                {"title": "12-18 साल", "payload": '/inform_age{"age":"12-18 years"}'}
            ]
        else:
            question = "मरीज की उम्र कितनी है?"
            buttons = [
                {"title": "18-30 साल", "payload": '/inform_age{"age":"18-30 years"}'},
                {"title": "30-50 साल", "payload": '/inform_age{"age":"30-50 years"}'},
                {"title": "50-65 साल", "payload": '/inform_age{"age":"50-65 years"}'},
                {"title": "65+ साल", "payload": '/inform_age{"age":"65+ years"}'}
            ]

        dispatcher.utter_message(text=question, buttons=buttons)
        return []


class ActionProvidePreventionAdvice(Action):
    """Provide contextual prevention advice based on symptoms/diseases"""

    def name(self) -> Text:
        return "action_provide_prevention_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_intent = tracker.latest_message.get('intent', {}).get('name', '')
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Provide specific prevention advice based on intent
        if current_intent == "prevention_hygiene" or "hygiene" in user_message:
            advice = self._get_hygiene_advice()
        elif current_intent == "prevention_nutrition" or "nutrition" in user_message:
            advice = self._get_nutrition_advice()
        elif current_intent == "prevention_exercise" or "exercise" in user_message:
            advice = self._get_exercise_advice()
        elif "dengue" in user_message or "डेंगू" in user_message:
            advice = self._get_dengue_prevention()
        elif "malaria" in user_message or "मलेरिया" in user_message:
            advice = self._get_malaria_prevention()
        else:
            advice = self._get_general_prevention()

        dispatcher.utter_message(text=advice)
        
        # Offer related services
        buttons = [
            {"title": "🏥 नजदीकी अस्पताल", "payload": "/find_doctor"},
            {"title": "💉 टीकाकरण", "payload": "/vaccination_schedule"},
            {"title": "📊 बीमारी की स्थिति", "payload": "/disease_stats"}
        ]
        
        dispatcher.utter_message(text="और कोई मदद चाहिए?", buttons=buttons)
        
        return []

    def _get_hygiene_advice(self):
        return """
🧼 **स्वच्छता के महत्वपूर्ण नियम:**

✋ **हाथ धोना:**
• खाना खाने से पहले
• शौच के बाद
• घर आने पर
• 20 सेकंड तक साबुन से धोएं

💧 **पानी की सुरक्षा:**
• उबालकर या फिल्टर करके पानी पिएं
• पानी को ढककर रखें
• टंकी की नियमित सफाई करें

🏠 **घर की सफाई:**
• कूड़ा ढके डस्टबिन में डालें
• घर के आसपास पानी न जमने दें
• शौचालय का उपयोग करें

🦟 **कीटों से बचाव:**
• मच्छरदानी का इस्तेमाल करें
• गंदे पानी को न जमने दें
        """

    def _get_nutrition_advice(self):
        return """
🥗 **संतुलित आहार के लिए:**

🌾 **अनाज और दालें:**
• चावल, गेहूं, ज्वार, बाजरा
• दाल, राजमा, चना
• दिन में 2-3 बार

🥬 **सब्जी और फल:**
• हरी पत्तेदार सब्जियां
• रंग-बिरंगे फल
• दिन में 4-5 बार

🥛 **दूध और डेयरी:**
• दूध, दही, पनीर
• कैल्शियम और प्रोटीन के लिए
• दिन में 2 बार

💧 **पानी:**
• दिन में 8-10 गिलास
• नींबू पानी, छाछ भी पिएं

❌ **कम करें:**
• तली हुई चीजें
• मिठाई और नमकीन
• धूम्रपान और शराब
        """

    def _get_exercise_advice(self):
        return """
🏃‍♂️ **दैनिक व्यायाम के फायदे:**

🚶‍♀️ **रोजाना टहलना:**
• सुबह-शाम 30 मिनट
• तेज़ी से चलें
• दिल और दिमाग के लिए अच्छा

🧘‍♀️ **योग और प्राणायाम:**
• सुबह 15-20 मिनट
• तनाव कम करता है
• लचीलापन बढ़ाता है

💪 **घरेलू काम:**
• साफ-सफाई
• बागवानी
• सीढ़ी चढ़ना

🎯 **लक्ष्य:**
• सप्ताह में 150 मिनट exercise
• धीरे-धीरे बढ़ाएं
• अपनी क्षमता के अनुसार करें

⚠️ **सावधानी:**
• डॉक्टर की सलाह लें (विशेषकर 50+ उम्र में)
• दर्द हो तो रुकें
        """

    def _get_dengue_prevention(self):
        return """
🦟 **डेंगू से बचाव:**

💧 **पानी का प्रबंधन:**
• कूलर, टंकी साफ रखें
• फूलदान का पानी रोज बदलें
• बारिश का पानी न जमने दें

🏠 **घर की सुरक्षा:**
• खिड़कियों पर जाली लगाएं
• मच्छरदानी का उपयोग करें
• शाम को घर बंद रखें

👕 **कपड़े:**
• पूरे बाजू के कपड़े पहनें
• हल्के रंग के कपड़े
• मच्छर भगाने वाली क्रीम लगाएं

🚨 **लक्षण दिखने पर:**
• तेज बुखार
• सिरदर्द और आंखों में दर्द
• तुरंत डॉक्टर को दिखाएं
        """

    def _get_malaria_prevention(self):
        return """
🦟 **मलेरिया से बचाव:**

🌙 **रात की सुरक्षा:**
• सोते समय मच्छरदानी जरूर लगाएं
• खिड़की-दरवाजे बंद रखें
• मच्छर कॉइल या वेपराइज़र का उपयोग

🏠 **आसपास की सफाई:**
• नालियों को साफ रखें
• पानी की टंकी को ढकें
• कूड़ा-करकट न फैलाएं

💊 **इलाज:**
• बुखार आते ही डॉक्टर को दिखाएं
• खून की जांच कराएं
• दवा पूरा कोर्स लें

🎯 **विशेष सावधानी:**
• गर्भवती महिलाओं को
• छोटे बच्चों को
• बुजुर्गों को ज्यादा सावधानी
        """

    def _get_general_prevention(self):
        return """
🛡️ **सामान्य बीमारियों से बचाव:**

💪 **इम्युनिटी बढ़ाएं:**
• संतुलित आहार लें
• नियमित व्यायाम करें
• पर्याप्त नींद लें (7-8 घंटे)

🧼 **स्वच्छता बनाए रखें:**
• बार-बार हाथ धोएं
• साफ कपड़े पहनें
• घर और आसपास की सफाई करें

💉 **टीकाकरण:**
• समय पर टीके लगवाएं
• बच्चों का पूरा कोर्स कराएं
• कोविड बूस्टर भी लगवाएं

🏥 **नियमित जांच:**
• साल में एक बार हेल्थ चेकअप
• डॉक्टर की सलाह मानें
• बीमारी के शुरुआती लक्षणों को नज़रअंदाज़ न करें
        """


class ActionDefaultFallback(Action):
    """Intelligent fallback with health context and helpful suggestions"""

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Analyze conversation context to provide better fallback
        conversation_stage = tracker.get_slot("conversation_stage")
        last_intent = tracker.latest_message.get('intent', {}).get('name', '')
        
        if conversation_stage == "symptom_assessment":
            fallback_message = """
क्षमा करें, मैं आपकी स्वास्थ्य समस्या को पूरी तरह समझ नहीं पाया। 🤔

**कृपया सरल शब्दों में बताएं:**
• "मुझे बुखार है"
• "पेट में दर्द है" 
• "सिरदर्द हो रहा है"
• "सांस लेने में तकलीफ है"
            """
        else:
            fallback_message = """
क्षमा करें, मैं समझ नहीं पाया। 🤔

**मैं इन चीजों में मदद कर सकता हूं:**
• लक्षणों की जांच करना
• टीकाकरण की जानकारी देना  
• नजदीकी अस्पताल खोजना
• स्वास्थ्य की सलाह देना
• गलत जानकारी की पहचान करना

**कृपया सरल शब्दों में अपनी समस्या बताएं**
            """

        buttons = [
            {"title": "🤒 लक्षण जांच", "payload": "/symptom_fever"},
            {"title": "💉 टीकाकरण", "payload": "/vaccination_schedule"},
            {"title": "🏥 नजदीकी अस्पताल", "payload": "/find_doctor"},
            {"title": "ℹ️ मेरी सुविधाएं", "payload": "/bot_capabilities"}
        ]

        dispatcher.utter_message(text=fallback_message, buttons=buttons)
        
        return [SlotSet("conversation_stage", "fallback")]