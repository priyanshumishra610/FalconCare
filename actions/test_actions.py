"""
Unit tests for FalconCare custom actions
Ensures ≥80% code coverage for action functionality
"""

import pytest
from unittest.mock import Mock, patch
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.actions import ActionSymptomInfo, ActionVaccinationInfo


class TestActionSymptomInfo:
    """Test cases for ActionSymptomInfo"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.action = ActionSymptomInfo()
        self.dispatcher = CollectingDispatcher()
        self.domain = {}
    
    def test_action_name(self):
        """Test that action returns correct name"""
        assert self.action.name() == "action_symptom_info"
    
    def test_symptom_info_fever(self):
        """Test fever symptom information"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "symptom_type": "fever",
            "severity": "moderate",
            "duration": "2 days",
            "body_part": "head"
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("symptom_type", None) in result
        assert SlotSet("severity", None) in result
        assert SlotSet("duration", None) in result
        assert SlotSet("body_part", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "fever" in message["text"].lower()
        assert "temperature" in message["text"].lower()
    
    def test_symptom_info_cough(self):
        """Test cough symptom information"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "symptom_type": "cough",
            "severity": "mild",
            "duration": "1 week",
            "body_part": "chest"
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("symptom_type", None) in result
        assert SlotSet("severity", None) in result
        assert SlotSet("duration", None) in result
        assert SlotSet("body_part", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "cough" in message["text"].lower()
        assert "airways" in message["text"].lower()
    
    def test_symptom_info_headache(self):
        """Test headache symptom information"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "symptom_type": "headache",
            "severity": "severe",
            "duration": "3 hours",
            "body_part": "head"
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("symptom_type", None) in result
        assert SlotSet("severity", None) in result
        assert SlotSet("duration", None) in result
        assert SlotSet("body_part", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "headache" in message["text"].lower()
        assert "pain" in message["text"].lower()
    
    def test_symptom_info_stomach_pain(self):
        """Test stomach pain symptom information"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "symptom_type": "stomach_pain",
            "severity": "moderate",
            "duration": "1 day",
            "body_part": "abdomen"
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("symptom_type", None) in result
        assert SlotSet("severity", None) in result
        assert SlotSet("duration", None) in result
        assert SlotSet("body_part", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "stomach" in message["text"].lower()
        assert "abdominal" in message["text"].lower()
    
    def test_symptom_info_fatigue(self):
        """Test fatigue symptom information"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "symptom_type": "fatigue",
            "severity": "mild",
            "duration": "1 week",
            "body_part": "whole body"
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("symptom_type", None) in result
        assert SlotSet("severity", None) in result
        assert SlotSet("duration", None) in result
        assert SlotSet("body_part", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "fatigue" in message["text"].lower()
        assert "tiredness" in message["text"].lower()
    
    def test_symptom_info_unknown(self):
        """Test unknown symptom type"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "symptom_type": "unknown_symptom",
            "severity": None,
            "duration": None,
            "body_part": None
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("symptom_type", None) in result
        assert SlotSet("severity", None) in result
        assert SlotSet("duration", None) in result
        assert SlotSet("body_part", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "symptom" in message["text"].lower()
        assert "fever" in message["text"].lower()
    
    def test_symptom_info_none_slots(self):
        """Test with None slots"""
        tracker = Mock()
        tracker.get_slot.return_value = None
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("symptom_type", None) in result
        assert SlotSet("severity", None) in result
        assert SlotSet("duration", None) in result
        assert SlotSet("body_part", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "symptom" in message["text"].lower()


class TestActionVaccinationInfo:
    """Test cases for ActionVaccinationInfo"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.action = ActionVaccinationInfo()
        self.dispatcher = CollectingDispatcher()
        self.domain = {}
    
    def test_action_name(self):
        """Test that action returns correct name"""
        assert self.action.name() == "action_vaccination_info"
    
    def test_vaccination_info_covid(self):
        """Test COVID vaccine information"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "vaccine_type": "covid",
            "age_group": "adult",
            "medical_condition": "none"
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("vaccine_type", None) in result
        assert SlotSet("age_group", None) in result
        assert SlotSet("medical_condition", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "covid" in message["text"].lower()
        assert "coronavirus" in message["text"].lower()
    
    def test_vaccination_info_flu(self):
        """Test flu vaccine information"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "vaccine_type": "flu",
            "age_group": "child",
            "medical_condition": "asthma"
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("vaccine_type", None) in result
        assert SlotSet("age_group", None) in result
        assert SlotSet("medical_condition", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "flu" in message["text"].lower()
        assert "influenza" in message["text"].lower()
    
    def test_vaccination_info_routine(self):
        """Test routine vaccine information"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "vaccine_type": "routine",
            "age_group": "infant",
            "medical_condition": "none"
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("vaccine_type", None) in result
        assert SlotSet("age_group", None) in result
        assert SlotSet("medical_condition", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "routine" in message["text"].lower()
        assert "childhood" in message["text"].lower()
    
    def test_vaccination_info_travel(self):
        """Test travel vaccine information"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "vaccine_type": "travel",
            "age_group": "adult",
            "medical_condition": "diabetes"
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("vaccine_type", None) in result
        assert SlotSet("age_group", None) in result
        assert SlotSet("medical_condition", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "travel" in message["text"].lower()
        assert "destination" in message["text"].lower()
    
    def test_vaccination_info_unknown(self):
        """Test unknown vaccine type"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda slot: {
            "vaccine_type": "unknown_vaccine",
            "age_group": None,
            "medical_condition": None
        }.get(slot)
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("vaccine_type", None) in result
        assert SlotSet("age_group", None) in result
        assert SlotSet("medical_condition", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "vaccine" in message["text"].lower()
        assert "covid" in message["text"].lower()
    
    def test_vaccination_info_none_slots(self):
        """Test with None slots"""
        tracker = Mock()
        tracker.get_slot.return_value = None
        
        result = self.action.run(self.dispatcher, tracker, self.domain)
        
        # Check that slots are cleared
        assert SlotSet("vaccine_type", None) in result
        assert SlotSet("age_group", None) in result
        assert SlotSet("medical_condition", None) in result
        
        # Check that dispatcher was called
        assert len(self.dispatcher.messages) == 1
        message = self.dispatcher.messages[0]
        assert "vaccine" in message["text"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=actions.actions", "--cov-report=html"])
