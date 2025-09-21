# 🏥 FalconCare - Health Assistant Chatbot

FalconCare is a comprehensive Rasa-based health assistant chatbot designed to provide symptom information, vaccination guidance, and general health advice. The bot supports multiple languages including English and Hindi, making it accessible to a diverse user base.

## 🌟 Features

- **Symptom Analysis**: Provides detailed information about common symptoms like fever, cough, headache, stomach pain, and fatigue
- **Vaccination Guidance**: Offers comprehensive information about COVID, flu, routine, and travel vaccines
- **Multilingual Support**: Supports English and Hindi with examples for each intent
- **Custom Actions**: Intelligent responses using custom actions for symptom and vaccination queries
- **Comprehensive Testing**: Unit tests with ≥80% code coverage
- **Multiple Interfaces**: Console, REST API, and SocketIO support

## 📁 Project Structure

```
FalconCare/
├── actions/
│   ├── __init__.py
│   ├── actions.py           # Custom action code
│   └── test_actions.py      # Unit tests for actions
├── data/
│   ├── nlu.yml              # 50+ FAQ intents & multilingual examples
│   ├── stories.yml          # Conversation flows
│   └── rules.yml            # Optional rules
├── tests/
│   ├── test_nlu.yml         # NLU tests
│   └── test_stories.yml     # Story tests
├── models/                  # Trained Rasa models
├── config.yml               # NLU + policy pipeline
├── domain.yml               # Intents, entities, slots, responses
├── credentials.yml          # WhatsApp/Twilio credentials placeholders
├── endpoints.yml            # Action server endpoints
├── requirements.txt         # Python dependencies
└── run.py                   # Script to run bot programmatically
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FalconCare
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model**
   ```bash
   rasa train
   ```

4. **Start the action server** (in a separate terminal)
   ```bash
   rasa run actions
   ```

5. **Run the bot**
   ```bash
   python run.py console
   ```

## 🎯 Usage

### Console Mode
```bash
python run.py console
```

### REST API Mode
```bash
python run.py rest [host] [port]
# Example: python run.py rest localhost 5005
```

### SocketIO Mode
```bash
python run.py socketio [host] [port]
# Example: python run.py socketio localhost 5005
```

## 🧪 Testing

### Run Unit Tests
```bash
cd actions
python -m pytest test_actions.py -v
```

### Run Tests with Coverage
```bash
cd actions
python -m pytest test_actions.py -v --cov=actions.actions --cov-report=html
```

### Run Rasa Tests
```bash
# Test NLU
rasa test nlu

# Test stories
rasa test stories

# Test all
rasa test
```

## 🔧 Configuration

### Custom Actions

The bot includes two main custom actions:

1. **ActionSymptomInfo**: Provides detailed symptom information
   - Handles fever, cough, headache, stomach pain, and fatigue
   - Includes self-care advice and when to see a doctor
   - Supports severity, duration, and body part context

2. **ActionVaccinationInfo**: Provides vaccination guidance
   - Covers COVID, flu, routine, and travel vaccines
   - Includes schedules, eligibility, and side effects
   - Supports age group and medical condition context

### NLU Intents

The bot supports 50+ intents including:
- Basic interactions (greet, goodbye, thank_you)
- Symptom queries (fever, cough, headache, etc.)
- Vaccination queries (COVID, flu, routine, travel)
- Health categories (mental health, women's health, child health, etc.)
- Emergency and preventive health

### Multilingual Support

The bot includes examples in both English and Hindi:
- English: "I have fever" / "I need vaccine information"
- Hindi: "मुझे बुखार है" / "टीकाकरण की जानकारी"

## 📊 Coverage Report

The test suite ensures ≥80% code coverage for custom actions. To generate a coverage report:

```bash
cd actions
python -m pytest test_actions.py --cov=actions.actions --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the detailed coverage report.

## 🔌 Integration

### WhatsApp Integration

To integrate with WhatsApp Business API, update `credentials.yml`:

```yaml
whatsapp:
  access_token: "your_whatsapp_access_token_here"
  verify_token: "your_whatsapp_verify_token_here"
  phone_number_id: "your_phone_number_id_here"
```

### SMS Integration

To integrate with Twilio SMS, update `credentials.yml`:

```yaml
twilio:
  account_sid: "your_twilio_account_sid_here"
  auth_token: "your_twilio_auth_token_here"
  from_number: "your_twilio_phone_number_here"
```

## 🛠️ Development

### Adding New Intents

1. Add intent examples to `data/nlu.yml`
2. Add corresponding stories to `data/stories.yml`
3. Update `domain.yml` with new intent
4. Retrain the model: `rasa train`

### Adding New Actions

1. Create new action class in `actions/actions.py`
2. Add action to `domain.yml`
3. Write tests in `actions/test_actions.py`
4. Update stories to use the new action

### Adding New Languages

1. Add language examples to `data/nlu.yml`
2. Update `config.yml` with language settings
3. Retrain the model: `rasa train`

## 📝 API Endpoints

When running in REST API mode, the bot exposes:

- `POST /webhooks/rest/webhook` - Send messages to the bot
- `GET /health` - Health check endpoint
- `POST /conversations/{conversation_id}/messages` - Send message to specific conversation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the Rasa documentation: https://rasa.com/docs/
- Review the test files for usage examples

## 🔄 Version History

- **v1.0.0** - Initial release with basic symptom and vaccination support
- Phase 1 complete with 50+ intents and comprehensive testing

---

**Note**: This is a Phase 1 implementation. Future phases will include more advanced features like appointment booking, prescription management, and integration with health databases.