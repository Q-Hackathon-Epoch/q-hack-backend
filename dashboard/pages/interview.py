from __future__ import annotations
from dotenv import load_dotenv
import os
import reflex as rx
from pathlib import Path
from .. import styles
from ..templates import template  # adjust import as needed

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

AGENT_ID: str = os.getenv("ELEVENLABS_AGENT_ID")
# AGENT_ID: str = os.getenv("ELEVENLABS_AGENT_ID")


# ---------------------------------------------------------------------------
# State: track session object on window only, UI updated via JS
# ---------------------------------------------------------------------------
class VoiceState(rx.State):
    """Dummy state to allow script injection on page."""

    pass


# ---------------------------------------------------------------------------
# Conversation JS logic using @11labs/client
# ---------------------------------------------------------------------------
conv_js = rx.script(
    f"""
import {{ Conversation }} from 'https://cdn.jsdelivr.net/npm/@11labs/client/+esm';

const btn         = document.getElementById('voiceBtn');
const status      = document.getElementById('connectionStatus');
const agentStatus = document.getElementById('agentStatus');
let conv = null;

async function getSignedUrl() {{
  const r = await fetch('/api/get-signed-url');
  if (!r.ok) throw new Error('Cannot obtain signed URL');
  return (await r.json()).signedUrl;
}}

async function toggleConversation() {{
  if (conv) {{
    // Останавливаем сессию
    await conv.endSession();
    conv = null;
    btn.textContent      = 'Start';
    status.textContent   = 'Disconnected';
    // цвет → зелёный
    btn.classList.remove('bg-red-500');
    return;
  }}

  // Запускаем сессию
  try {{
    await navigator.mediaDevices.getUserMedia({{audio:true}});
    const opts = {{
      onConnect:    () => {{ status.textContent = 'Connected';   }},
      onDisconnect: () => {{ status.textContent = 'Disconnected';}},
      onError:      e  => console.error(e),
      onModeChange: m  => {{ agentStatus.textContent = m.mode;   }}
    }};
    { '' if os.getenv('USE_SIGNED_URL') else f"opts.agentId = '{AGENT_ID}';" }
    { 'opts.signedUrl = await getSignedUrl();' if os.getenv('USE_SIGNED_URL') else '' }

    conv = await Conversation.startSession(opts);
    btn.textContent = 'STOP';
    // цвет → красный
    // btn.classList.replace('bg-green-500', 'bg-red-500');
    btn.classList.add('bg-red-500');
  }} catch(err) {{
    console.error('Failed to start conversation', err);
  }}
}}

btn.addEventListener('click', toggleConversation);
""", strategy="afterInteractive", custom_attrs={"type": "module"})

# ---------------------------------------------------------------------------
# Page UI: two buttons and status text
# ---------------------------------------------------------------------------
@template(route="/interview", title="Mock Interview Preparation")
def Interview() -> rx.Component:
    return rx.vstack(
        rx.heading("Let's get you ready for your interview!", size="9", margin_bottom="3rem"),
        rx.flex(
            # Одна кнопка с начальными зелёными стилями
            rx.button(
                "Start",
                id="voiceBtn",
                padding="3rem",
                margin="5px",
                borderRadius="9999px",
                className=" text-white hover:opacity-90 transition",  # <- здесь
            ),
            rx.hstack(
                rx.text("Status: ", as_="span"),
                rx.text("Disconnected", id="connectionStatus", as_="span", font_weight="bold"),
                rx.text(" | Agent is ", as_="span", margin_left="1rem"),
                rx.text("listening", id="agentStatus", as_="span", font_weight="bold"),
                spacing="2",
            ),
            display="flex",
            direction="column",
            align="center",
            justify="center",
            width="100%",
            gap="2rem",
        ),
        conv_js,
        width="100%",
    )

