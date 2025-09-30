# Health Guardian AI - Government API Integration
# CoWIN, IHIP, Hospital Finder, Disease Surveillance

from typing import Any, Text, Dict, List
import requests
import json
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionCheckVaccination(Action):
    """CoWIN API integration for vaccination center lookup"""

    def name(self) -> Text:
        return "action_check_vaccination"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get pincode from slot or ask user
        pincode = tracker.get_slot("user_location")
        if not pincode or len(pincode) != 6:
            dispatcher.utter_message(text="कृपया अपना 6 अंक का पिनकोड बताएं।")
            return []

        try:
            # CoWIN Public API
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
            today = datetime.now().strftime("%d-%m-%Y")
            
            params = {"pincode": pincode, "date": today}
            headers = {"User-Agent": "Mozilla/5.0"}
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            data = response.json()
            
            if data.get('centers'):
                centers = data['centers'][:3]  # Top 3 centers
                message = "💉 **आपके पास के टीकाकरण केंद्र:**\n\n"
                
                for idx, center in enumerate(centers, 1):
                    message += f"**{idx}. {center['name']}** 📍\n"
                    message += f"   📮 {center['address']}\n"
                    
                    if center['sessions']:
                        session = center['sessions'][0]
                        message += f"   👥 उम्र: {session['min_age_limit']}+\n"
                        message += f"   💊 वैक्सीन: {session['vaccine']}\n"
                        message += f"   📅 तारीख: {session['date']}\n"
                        message += f"   🎟️ स्लॉट: {session['available_capacity']}\n\n"
                
                message += "📱 **CoWIN ऐप से बुकिंग करें** या **आशा कार्यकर्ता से संपर्क करें**"
                
                dispatcher.utter_message(text=message)
            else:
                # Fallback with general vaccination info
                fallback_msg = f"""
💉 **पिनकोड {pincode} पर वैक्सीन की जानकारी:**

🏥 **निकटतम केंद्र खोजने के लिए:**
• CoWIN ऐप डाउनलोड करें
• 104 पर कॉल करें
• आशा कार्यकर्ता से मिलें

📅 **टीकाकरण समय:** सुबह 9 से शाम 5 बजे
💳 **फीस:** मुफ्त (सरकारी केंद्र)

📞 **हेल्पलाइन:** 1075
                """
                dispatcher.utter_message(text=fallback_msg)
        
        except Exception as e:
            dispatcher.utter_message(
                text="क्षमा करें, वैक्सीन की जानकारी लाने में समस्या हुई। कृपया 1075 पर कॉल करें।"
            )
            print(f"CoWIN API Error: {str(e)}")
        
        return []


class ActionDiseaseStats(Action):
    """Mock IHIP integration for disease surveillance data"""

    def name(self) -> Text:
        return "action_disease_stats"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get district from slot or use default
        district = tracker.get_slot("user_location") or "रायपुर"
        
        # Mock IHIP data (in production, connect to real API)
        disease_data = self._get_mock_disease_data()
        
        district_lower = district.lower()
        district_key = self._match_district(district_lower, disease_data.keys())
        
        if district_key:
            stats = disease_data[district_key]
            message = f"📊 **{district.title()} में बीमारियों की स्थिति:**\n\n"
            
            for disease, data in stats.items():
                emoji = self._get_disease_emoji(data)
                trend_hindi = self._get_trend_hindi(data['trend'])
                
                message += f"{emoji} **{disease.title()}:** {data['cases']} मामले ({trend_hindi})\n"
            
            message += f"\n📅 **अपडेट:** {datetime.now().strftime('%d-%m-%Y')}"
            message += "\n💡 **सलाह:** मच्छरों से बचाव करें, साफ पानी पिएं, स्वच्छता बनाए रखें।"
            
            # Add alert if any disease is spiking
            alerts = [d for d, data in stats.items() if data.get('alert')]
            if alerts:
                message += f"\n\n🚨 **चेतावनी:** {', '.join(alerts)} के मामले बढ़ रहे हैं। सावधान रहें!"
            
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(
                text=f"क्षमा करें, {district} के लिए डेटा उपलब्ध नहीं है। कृपया जिले का नाम स्पष्ट रूप से बताएं।"
            )
        
        return []

    def _get_mock_disease_data(self):
        """Mock disease surveillance data for demo"""
        return {
            "raipur": {
                "dengue": {"cases": 145, "trend": "increasing", "alert": True},
                "malaria": {"cases": 67, "trend": "stable", "alert": False},
                "typhoid": {"cases": 23, "trend": "decreasing", "alert": False},
                "diarrhea": {"cases": 89, "trend": "increasing", "alert": False}
            },
            "bilaspur": {
                "dengue": {"cases": 89, "trend": "stable", "alert": False},
                "malaria": {"cases": 134, "trend": "increasing", "alert": True},
                "typhoid": {"cases": 15, "trend": "decreasing", "alert": False},
                "diarrhea": {"cases": 45, "trend": "stable", "alert": False}
            },
            "bhilai": {
                "dengue": {"cases": 78, "trend": "decreasing", "alert": False},
                "malaria": {"cases": 92, "trend": "stable", "alert": False},
                "typhoid": {"cases": 34, "trend": "increasing", "alert": False},
                "diarrhea": {"cases": 67, "trend": "increasing", "alert": True}
            }
        }

    def _match_district(self, input_district, available_districts):
        """Fuzzy match district name"""
        for district in available_districts:
            if input_district in district or district in input_district:
                return district
        return None

    def _get_disease_emoji(self, data):
        """Get appropriate emoji based on disease status"""
        if data['alert']:
            return "🚨"
        elif data['trend'] == "increasing":
            return "⚠️"
        elif data['trend'] == "decreasing":
            return "✅"
        else:
            return "ℹ️"

    def _get_trend_hindi(self, trend):
        """Convert trend to Hindi"""
        trend_map = {
            "increasing": "बढ़ रहे",
            "decreasing": "घट रहे",
            "stable": "स्थिर"
        }
        return trend_map.get(trend, "स्थिर")


class ActionFindHospital(Action):
    """Find nearest hospitals and healthcare facilities"""

    def name(self) -> Text:
        return "action_find_hospital"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Try to get location from slot
        user_location = tracker.get_slot("user_location")
        
        if not user_location:
            # Use default location or ask user
            user_location = "raipur"  # Default to Raipur
        
        # Get hospitals (mock data for demo, use real API in production)
        hospitals = self._get_hospitals_data(user_location)
        
        if hospitals:
            message = "🏥 **आपके पास के अस्पताल/स्वास्थ्य केंद्र:**\n\n"
            
            for idx, hospital in enumerate(hospitals[:3], 1):
                message += f"**{idx}. {hospital['name']}** 📍\n"
                message += f"   📮 {hospital['address']}\n"
                message += f"   📏 दूरी: ~{hospital['distance']} km\n"
                message += f"   📞 फोन: {hospital['phone']}\n"
                message += f"   🚨 आपातकाल: {'हां' if hospital['emergency'] else 'नहीं'}\n"
                message += f"   ⏰ समय: {hospital['timing']}\n\n"
                
            message += "🚨 **आपातकाल में 108 पर कॉल करें**\n"
            message += "📱 **ASHA कार्यकर्ता:** 9876543210"
            
            # Create action buttons
            buttons = [
                {"title": "📞 108 कॉल करें", "payload": "tel:108"},
                {"title": "🏥 और अस्पताल", "payload": "/find_doctor"},
                {"title": "📍 दिशा देखें", "payload": "/get_directions"}
            ]
            
            dispatcher.utter_message(text=message, buttons=buttons)
        else:
            dispatcher.utter_message(
                text="क्षमा करें, पास में अस्पताल नहीं मिले। आपातकाल में 108 पर कॉल करें।"
            )
        
        return []

    def _get_hospitals_data(self, location):
        """Get hospital data (mock for demo)"""
        hospital_database = {
            "raipur": [
                {
                    "name": "जिला अस्पताल रायपुर",
                    "address": "गंधी चौक, रायपुर, छत्तीसगढ़",
                    "distance": 2.5,
                    "phone": "0771-2221111",
                    "emergency": True,
                    "timing": "24x7"
                },
                {
                    "name": "प्राथमिक स्वास्थ्य केंद्र",
                    "address": "सेक्टर 1, रायपुर",
                    "distance": 1.8,
                    "phone": "0771-2222222",
                    "emergency": False,
                    "timing": "9:00 - 17:00"
                },
                {
                    "name": "अपोलो अस्पताल",
                    "address": "कटोरा तालाब, रायपुर",
                    "distance": 3.2,
                    "phone": "0771-2233333",
                    "emergency": True,
                    "timing": "24x7"
                }
            ],
            "bilaspur": [
                {
                    "name": "सरकारी अस्पताल बिलासपुर",
                    "address": "लिंक रोड, बिलासपुर",
                    "distance": 1.5,
                    "phone": "07752-220000",
                    "emergency": True,
                    "timing": "24x7"
                },
                {
                    "name": "CHC बिलासपुर",
                    "address": "बस स्टैंड के पास, बिलासपुर",
                    "distance": 2.1,
                    "phone": "07752-221111",
                    "emergency": False,
                    "timing": "8:00 - 16:00"
                }
            ]
        }
        
        # Match location
        location_lower = location.lower()
        for key in hospital_database.keys():
            if key in location_lower or location_lower in key:
                return hospital_database[key]
        
        # Default to Raipur if no match
        return hospital_database.get("raipur", [])


class ActionVaccinationReminder(Action):
    """Vaccination schedule and reminder system"""

    def name(self) -> Text:
        return "action_vaccination_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get child age if available
        patient_age = tracker.get_slot("patient_age") or ""
        
        try:
            age_months = self._parse_age_to_months(patient_age)
            schedule = self._get_vaccination_schedule(age_months)
            
            if schedule:
                message = f"💉 **बच्चे का टीकाकरण कार्यक्रम ({patient_age}):**\n\n"
                message += schedule
                message += "\n\n📱 **याददाश्त के लिए:** अपने फोन में रिमाइंडर सेट करें"
                message += "\n🏥 **कहां लगवाएं:** नजदीकी आंगनवाड़ी, PHC, या सरकारी अस्पताल"
                
                buttons = [
                    {"title": "📍 नजदीकी केंद्र", "payload": "/find_doctor"},
                    {"title": "📅 अगला टीका", "payload": "/vaccination_schedule"},
                    {"title": "💉 कोविड वैक्सीन", "payload": "/vaccination_covid"}
                ]
                
                dispatcher.utter_message(text=message, buttons=buttons)
            else:
                self._send_general_vaccination_info(dispatcher)
                
        except:
            self._send_general_vaccination_info(dispatcher)
        
        return []

    def _parse_age_to_months(self, age_text):
        """Parse age text to months"""
        import re
        
        # Extract numbers from age text
        numbers = re.findall(r'\d+', age_text)
        if not numbers:
            return None
            
        age_num = int(numbers[0])
        
        if "month" in age_text.lower() or "महीने" in age_text:
            return age_num
        elif "year" in age_text.lower() or "साल" in age_text or "वर्ष" in age_text:
            return age_num * 12
        else:
            # Assume months if no unit specified and < 60
            return age_num if age_num < 60 else age_num * 12

    def _get_vaccination_schedule(self, age_months):
        """Get vaccination schedule based on age"""
        if age_months is None:
            return None
            
        schedule_map = {
            0: "🍼 **जन्म के समय:** BCG, OPV-0, Hepatitis B-1",
            6: "💉 **6 सप्ताह:** DPT-1, OPV-1, Hepatitis B-2, HIB-1, Rotavirus-1, PCV-1",
            10: "💉 **10 सप्ताह:** DPT-2, OPV-2, HIB-2, Rotavirus-2, PCV-2", 
            14: "💉 **14 सप्ताह:** DPT-3, OPV-3, Hepatitis B-3, HIB-3, Rotavirus-3, PCV-3",
            9: "💉 **9 महीने:** Measles-1, JE-1",
            12: "💉 **12 महीने:** Hepatitis A-1",
            15: "💉 **15 महीने:** MMR-1, PCV Booster, JE-2",
            16: "💉 **16-18 महीने:** DPT Booster-1, OPV Booster",
            18: "💉 **18 महीने:** Hepatitis A-2",
            24: "💉 **2 साल:** Measles-2",
            60: "💉 **5 साल:** DPT Booster-2"
        }
        
        # Find next due vaccination
        upcoming = []
        for months, vaccine in schedule_map.items():
            if age_months <= months:
                upcoming.append(vaccine)
                
        if upcoming:
            return upcoming[0] + f"\n\n⏰ **अगला टीका:** {upcoming[0] if len(upcoming) > 0 else 'पूरा हो गया'}"
        else:
            return "✅ **बधाई हो!** सभी बचपन के टीके पूरे हो गए।"

    def _send_general_vaccination_info(self, dispatcher):
        """Send general vaccination information"""
        general_info = """
💉 **बच्चों का टीकाकरण कार्यक्रम:**

🍼 **0-2 साल:** सबसे महत्वपूर्ण टीके
📅 **समय पर टीका:** बीमारी से बचाव के लिए जरूरी
💳 **सभी टीके मुफ्त:** सरकारी केंद्रों पर

📱 **जानकारी के लिए:**
• आशा कार्यकर्ता से मिलें
• नजदीकी आंगनवाड़ी जाएं
• 104 पर कॉल करें

🎯 **याद रखें:** समय पर टीका = स्वस्थ बच्चा
        """
        
        buttons = [
            {"title": "📍 नजदीकी केंद्र", "payload": "/find_doctor"},
            {"title": "📞 104 कॉल करें", "payload": "tel:104"}
        ]
        
        dispatcher.utter_message(text=general_info, buttons=buttons)