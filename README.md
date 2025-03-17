Filename: /README.md
Project Name: # AI Waifu Companion

A customizable AI companion with profile management capabilities.

## Features
- Dual profile system (Chatbot & User)
- Persistent SQLite storage
- GGUF model support
- Gradio-based UI
- Stateful conversation history

## Setup
1. Install requirements:
   ```bash
   pip install -r requirements.txt

### **Key Features**
1. **State Persistence**:
   - Chat history preserved between UI views
   - Profile selections maintained during navigation
   - Unsaved changes retained in UI fields

2. **Profile Management**:
   - Separate chatbot/user profiles
   - JSON-based profile data storage
   - Version tracking through SQLite

3. **Error Handling**:
   - Database transaction rollback
   - Model loading validation
   - Input sanitization

4. **Performance**:
   - Async database operations
   - Model unloading during profile changes
   - Memory cleanup handlers

This implementation provides a complete solution with profile management, state persistence, and modular architecture while maintaining compatibility with resource-constrained systems.

# Creating and Activating the Virtual Environment for AI-Waifu:

- Linux
    - Creation: python3 -m venv ~/ai_waifu_env
    - Activation: source ~/ai_waifu_env/bin/activate
    
- Windows 
    - Creation: python3 -m D:/AI/venv ai_waifu_env 
    - Activation: D:\AI\venv\ai_waifu_env\Scripts\activate



