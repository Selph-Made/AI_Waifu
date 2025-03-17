# /ui.py

import gradio as gr
from profile_manager import ProfileManager
from chatbot import AIChatbot
from database import DatabaseManager
import json
import os
from datetime import datetime

# Initialize components
pm = ProfileManager()
chatbot = AIChatbot(pm)
db = DatabaseManager()

def create_profile_panel():
    with gr.Blocks(visible=False) as panel:
        with gr.Tabs():
            with gr.TabItem("Chatbot Profile"):
                with gr.Row():
                    chatbot_dd = gr.Dropdown(
                        label="Select Chatbot Profile",
                        choices=pm.get_profile_options('chatbot'),
                        interactive=True
                    )
                    chatbot_refresh = gr.Button("🔄", elem_classes="refresh-btn")
                chatbot_name = gr.Textbox(label="Profile Name")
                chatbot_data = gr.JSON(
                    label="Profile Data",
                    value={
                        "personality": "friendly",
                        "interests": ["technology", "philosophy"],
                        "communication_style": "casual"
                    }
                )
                chatbot_save = gr.Button("Save Chatbot Profile", variant="primary")
                chatbot_delete = gr.Button("Delete Profile", variant="stop")

            with gr.TabItem("User Profile"):
                with gr.Row():
                    user_dd = gr.Dropdown(
                        label="Select User Profile",
                        choices=pm.get_profile_options('user'),
                        interactive=True
                    )
                    user_refresh = gr.Button("🔄", elem_classes="refresh-btn")
                user_name = gr.Textbox(label="Profile Name")
                user_data = gr.JSON(
                    label="Profile Data",
                    value={
                        "name": "User",
                        "preferences": {"theme": "dark"},
                        "bio": "AI enthusiast"
                    }
                )
                user_save = gr.Button("Save User Profile", variant="primary")
                user_delete = gr.Button("Delete Profile", variant="stop")

        return panel, {
            "chatbot_dd": chatbot_dd,
            "chatbot_name": chatbot_name,
            "chatbot_data": chatbot_data,
            "chatbot_save": chatbot_save,
            "chatbot_delete": chatbot_delete,
            "user_dd": user_dd,
            "user_name": user_name,
            "user_data": user_data,
            "user_save": user_save,
            "user_delete": user_delete,
            "refresh_btns": [chatbot_refresh, user_refresh]
        }

def create_session_panel():
    with gr.Blocks(visible=False) as panel:
        with gr.Row():
            session_dd = gr.Dropdown(
                label="Saved Sessions",
                choices=[],
                allow_custom_value=True,
                filterable=True
            )
            session_name = gr.Textbox(label="New Session Name")
        with gr.Row():
            save_session = gr.Button("💾 Save Current", variant="primary")
            load_session = gr.Button("📂 Load Selected", variant="secondary")
            delete_session = gr.Button("🗑️ Delete", variant="stop")
        
        session_info = gr.JSON(
            label="Session Details",
            visible=False
        )
        
        return panel, {
            "session_dd": session_dd,
            "session_name": session_name,
            "save_btn": save_session,
            "load_btn": load_session,
            "delete_btn": delete_session,
            "session_info": session_info
        }

def refresh_profiles():
    return [
        gr.update(choices=pm.get_profile_options('chatbot')),
        gr.update(choices=pm.get_profile_options('user'))
    ]

def handle_profile_save(entity_type, name, data):
    try:
        pm.save_profile(entity_type, name, data)
        return f"{entity_type.capitalize()} profile saved!", True
    except Exception as e:
        return str(e), False

def handle_profile_delete(entity_type, name):
    try:
        pm.delete_profile(entity_type, name)
        return f"{entity_type.capitalize()} profile deleted!", True
    except Exception as e:
        return str(e), False

def handle_session_save(name, history):
    if not name:
        return "Session name required!", None
    try:
        pm.save_chat_session(name, history)
        sessions = pm.load_chat_sessions()
        choices = [f"{s[1]} ({s[0]})" for s in sessions]
        return f"Session '{name}' saved!", gr.update(choices=choices)
    except Exception as e:
        return str(e), None

def handle_session_load(session_str):
    try:
        session_id = int(session_str.split("(")[-1].rstrip(")"))
        messages = pm.load_chat_history(session_id)
        session_info = next(s for s in pm.load_chat_sessions() if s[0] == session_id)
        return (
            messages,
            gr.update(value=json.dumps(session_info, default=str)),
            ""
        )
    except Exception as e:
        return [], gr.update(), str(e)

with gr.Blocks(
    title="AI Waifu Companion",
    css="""
    .refresh-btn {max-width: 2em; min-width: 2em !important;}
    .panel {border: 1px solid #666; padding: 1em; margin: 1em 0;}
    """
) as ui:
    # State management
    current_chat = gr.State([])
    active_panel = gr.State("chat")

    # Profile panel components
    profile_panel, profile_comps = create_profile_panel()
    
    # Session panel components
    session_panel, session_comps = create_session_panel()

    # Main chat interface
    with gr.Column(visible=True) as chat_interface:
        chatbot_display = gr.Chatbot(
            label="Conversation History",
            height=600,
            show_label=True
        )
        msg_input = gr.Textbox(
            label="Your Message",
            placeholder="Type your message here...",
            lines=3
        )
        control_row = gr.Row():
            send_btn = gr.Button("Send", variant="primary")
            session_btn = gr.Button("Sessions", variant="secondary")
            profile_btn = gr.Button("Profiles", variant="secondary")
            clear_btn = gr.Button("Clear Chat", variant="stop")

    # Event handlers
    profile_btn.click(
        lambda: [
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False)
        ],
        outputs=[chat_interface, profile_panel, session_panel]
    ).then(
        refresh_profiles,
        outputs=[profile_comps["chatbot_dd"], profile_comps["user_dd"]]
    )

    session_btn.click(
        lambda: [
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True)
        ],
        outputs=[chat_interface, profile_panel, session_panel]
    ).then(
        lambda: gr.update(choices=[
            f"{s[1]} ({s[0]})" for s in pm.load_chat_sessions()
        ]),
        outputs=session_comps["session_dd"]
    )

    # Profile save handlers
    for entity in ["chatbot", "user"]:
        profile_comps[f"{entity}_save"].click(
            lambda e=entity: handle_profile_save(
                e,
                profile_comps[f"{entity}_name"].value,
                profile_comps[f"{entity}_data"].value
            ),
            outputs=[gr.Markdown(), gr.JSON()]
        ).then(
            refresh_profiles,
            outputs=[profile_comps["chatbot_dd"], profile_comps["user_dd"]]
        )

        profile_comps[f"{entity}_delete"].click(
            lambda e=entity: handle_profile_delete(
                e,
                profile_comps[f"{entity}_dd"].value
            ),
            outputs=[gr.Markdown(), gr.JSON()]
        ).then(
            refresh_profiles,
            outputs=[profile_comps["chatbot_dd"], profile_comps["user_dd"]]
        )

    # Session handlers
    session_comps["save_btn"].click(
        handle_session_save,
        inputs=[session_comps["session_name"], current_chat],
        outputs=[gr.Markdown(), session_comps["session_dd"]]
    )

    session_comps["load_btn"].click(
        handle_session_load,
        inputs=session_comps["session_dd"],
        outputs=[chatbot_display, session_comps["session_info"], gr.Markdown()]
    ).then(
        lambda x: x,
        inputs=current_chat,
        outputs=current_chat
    )

    # Chat interaction
    send_btn.click(
        lambda msg, hist: hist + [(msg, chatbot.respond(msg))],
        inputs=[msg_input, current_chat],
        outputs=[chatbot_display, current_chat]
    ).then(
        lambda: "",
        outputs=msg_input
    )

    clear_btn.click(
        lambda: [],
        outputs=[current_chat, chatbot_display]
    )

if __name__ == "__main__":
    ui.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )

