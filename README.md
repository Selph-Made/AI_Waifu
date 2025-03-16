### **Application Name**
**AI Waifu Companion**

### **Description**
AI Waifu Companion is an interactive AI chatbot designed for private, unlimited, and offline use. It engages users in natural conversations, generates images based on user prompts, and learns from interactions. The application is built to provide a personalized experience while ensuring that all data remains local and private, with no external servers involved. It can handle NSFW content, making it suitable for adult users who seek a more unrestricted interaction.

### **Features**
- **Private and Offline Use**: All data processing occurs locally, ensuring user privacy and security. No information is sent over the internet.
- **Unlimited Interaction**: Users can engage with the chatbot without restrictions on conversation length or content.
- **NSFW Content Handling**: Capable of generating and discussing adult content without censorship, tailored to user preferences.
- **Conversational AI**: Engages users in dynamic, context-aware conversations.
- **Image Generation**: Generates images using models like Stable Diffusion based on user requests.
- **Profile Management**: Supports multiple user and chatbot profiles with customizable settings.
- **Self-Learning**: Learns from user interactions and stores knowledge in a local database.
- **Approval Workflows**: Requires user approval for new knowledge entries to ensure accuracy.
- **Memory Management**: Remembers facts and allows users to forget them upon request.
- **Version Control**: Maintains a history of changes and allows rollback to previous states.
- **Secure Input Handling**: Sanitizes and validates user input to prevent security vulnerabilities.
- **User -Friendly Interface**: Provides a Gradio-based web interface for easy interaction.

### **Prerequisites**
1. **Software Requirements**:
   - **Python 3.8 or higher**: The application is built using Python.
   - **CUDA Toolkit (optional)**: For GPU acceleration during image generation (if using a compatible NVIDIA GPU).
   - **SQLite**: For local database management (included in Python standard library).
   - **Gradio**: For creating the web interface.
   - **Torch**: For model loading and inference.

2. **Hardware Requirements**:
   - **CPU**: A modern multi-core processor (Intel i5/Ryzen 5 or better recommended).
   - **RAM**: Minimum of 8GB (16GB or more recommended for better performance).
   - **GPU (optional)**: NVIDIA GPU with at least 6GB VRAM for faster image generation (e.g., GTX 1060 or better).
   - **Disk Space**: At least 10GB of free space for model files and databases.

3. **Internet Access**: Required for the initial setup to download model files and dependencies, but not needed for regular operation.

### **Steps to Make It Operable**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ai-waifu.git
   cd ai-waifu
   ```

2. **Install Dependencies**:
   - Create a virtual environment (optional but recommended):
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
   - Install required packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Download Model Files**:
   - Place the GGUF model files in the `gguf/` directory. Ensure you have the necessary models for the application to function.

4. **Set Up Database**:
   - The application will automatically create the necessary SQLite databases in the `data/` directory upon first run.

5. **Run the Application**:
   - Start the Gradio interface:
     ```bash
     python ui.py
     ```
   - Open a web browser and navigate to `http://localhost:7860` to interact with the chatbot.

6. **Configure Profiles**:
   - Use the interface to create and manage user and chatbot profiles, including settings for NSFW content.

7. **Interact with the Chatbot**:
   - Begin chatting with the AI Waifu and explore its features, including image generation and learning capabilities.

### **Requirements**
- **Python Packages**:
  - `torch`: For model loading and inference.
  - `transformers`: For handling language models.
  - `gradio`: For creating the web interface.
  - `sqlite3`: For database management (included in Python standard library).
  - `PIL`: For image processing.
  - `numpy`: For numerical operations.
  - `requests`: For any potential HTTP requests (if needed).
  - `html`: For HTML sanitization.
  - `pickle`: For object serialization.

- **Model Files**:
  - GGUF model files (e.g., `mistral-7b-instruct-v0.1.Q4_K_M.gguf`).
  - Image generation models (e.g., Stable Diffusion).

### **Summary**
The AI Waifu Companion is designed for users seeking a private, unrestricted, and customizable AI interaction experience. With its ability to handle NSFW content and operate entirely offline, it provides a unique platform for personalized conversations and creative expression. This comprehensive overview includes all necessary information to regenerate the application, ensuring it meets user needs for privacy and functionality.
