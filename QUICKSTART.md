# 🚀 FalconCare Quick Start Guide

Get FalconCare up and running in 5 minutes!

## Prerequisites
- Python 3.8+
- pip

## Installation & Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the model**
   ```bash
   rasa train
   ```

3. **Start the action server** (in a new terminal)
   ```bash
   rasa run actions
   ```

4. **Run the bot**
   ```bash
   python run.py console
   ```

## Quick Test

Try these sample conversations:

**Symptom Query:**
- "I have fever"
- "मुझे बुखार है" (Hindi)
- "I have a headache"

**Vaccination Query:**
- "Tell me about COVID vaccine"
- "कोविड टीका" (Hindi)
- "I need flu vaccine information"

**General Health:**
- "Hello"
- "I need health advice"
- "Thank you"

## Alternative Setup

For automated setup:
```bash
python setup.py
```

## Testing

Run tests to verify everything works:
```bash
python test_installation.py
```

## Troubleshooting

**Model not found?**
- Run `rasa train` first

**Action server not responding?**
- Make sure `rasa run actions` is running in another terminal

**Import errors?**
- Check if all dependencies are installed: `pip install -r requirements.txt`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize intents in `data/nlu.yml`
- Add new actions in `actions/actions.py`
- Configure integrations in `credentials.yml`

Happy chatting! 🏥
