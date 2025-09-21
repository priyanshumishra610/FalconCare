#!/usr/bin/env python3
"""
FalconCare Installation Test Script
Verifies that all components are properly installed and configured
"""

import os
import sys
import importlib
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    required_modules = [
        'rasa',
        'rasa_sdk',
        'pytest',
        'numpy',
        'sklearn',
        'tensorflow'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'config.yml',
        'domain.yml',
        'credentials.yml',
        'endpoints.yml',
        'requirements.txt',
        'run.py',
        'setup.py',
        'actions/__init__.py',
        'actions/actions.py',
        'actions/test_actions.py',
        'data/nlu.yml',
        'data/stories.yml',
        'data/rules.yml',
        'tests/test_nlu.yml',
        'tests/test_stories.yml'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_actions():
    """Test if custom actions can be imported"""
    print("\nTesting custom actions...")
    
    try:
        from actions.actions import ActionSymptomInfo, ActionVaccinationInfo
        print("✅ ActionSymptomInfo")
        print("✅ ActionVaccinationInfo")
        return True
    except ImportError as e:
        print(f"❌ Custom actions: {e}")
        return False

def test_yaml_syntax():
    """Test if YAML files have valid syntax"""
    print("\nTesting YAML syntax...")
    
    yaml_files = [
        'config.yml',
        'domain.yml',
        'data/nlu.yml',
        'data/stories.yml',
        'data/rules.yml',
        'tests/test_nlu.yml',
        'tests/test_stories.yml'
    ]
    
    try:
        import yaml
    except ImportError:
        print("❌ PyYAML not installed")
        return False
    
    failed_files = []
    
    for file_path in yaml_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"✅ {file_path}")
        except Exception as e:
            print(f"❌ {file_path}: {e}")
            failed_files.append(file_path)
    
    return len(failed_files) == 0

def main():
    """Main test function"""
    print("🧪 FalconCare Installation Test")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("File Structure", test_file_structure),
        ("Custom Actions", test_actions),
        ("YAML Syntax", test_yaml_syntax)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n{'='*40}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! FalconCare is ready to use.")
        print("\nNext steps:")
        print("1. Run: python setup.py")
        print("2. Start action server: rasa run actions")
        print("3. Run bot: python run.py console")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
