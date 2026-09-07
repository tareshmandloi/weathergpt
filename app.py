"""
WeatherGPT - Streamlit Web Application
Problem Statement: SIH26068 (Conversational AI for Weather Forecasting, Alerts, and Climate Information)
Smart India Hackathon Prototype
"""

import os
import sys

# Ensure UTF-8 support on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import io
import re

from weather_service import get_current_weather
from ai_agent import stream_weather_gpt, ask_weather_gpt, extract_city_from_query

def text_to_audio_bytes(text: str, lang: str = "en") -> bytes:
    """Convert AI text response to audio using Google TTS. Returns mp3 bytes."""
    try:
        from gtts import gTTS
        # Clean text of markdown symbols, emojis before TTS
        clean = re.sub(r"[*_`#>\[\]|]", "", text)
        clean = re.sub(r"!\[.*?\]\(.*?\)", "", clean)
        clean = re.sub(r"https?://\S+", "", clean)
        # Detect language (if Hindi/Hinglish, use hi)
        hi_chars = re.findall(r"[\u0900-\u097F]", clean)
        detected_lang = "hi" if len(hi_chars) > 10 else lang
        # Limit to 3000 chars to avoid timeout
        clean = clean[:3000]
        tts = gTTS(clean, lang=detected_lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None

# 1. Page Configuration
st.set_page_config(
    page_title="WeatherGPT | SIH26068",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished Hackathon Look
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E88E5, #00ACC1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #616161;
        font-size: 1.05rem;
        margin-bottom: 15px;
    }
    .badge {
        display: inline-block;
        background-color: #E3F2FD;
        color: #1565C0;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 12px;
        border-left: 4px solid #1E88E5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/sun.png", width=110)
    st.markdown("### ⚙️ WeatherGPT Intelligence")
    st.markdown("<span class='badge'>SIH26068 AI System</span>", unsafe_allow_html=True)

    # API Connection Status Badges
    current_gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if current_gemini_key:
        st.success("🟢 **Gemini AI (High-Speed)**: Connected")
    else:
        st.warning("🟡 Gemini Key Pending")

    # API Keys Configuration
    with st.expander("🔑 Configure API Keys", expanded=False):
        gemini_key_input = st.text_input(
            "Gemini API Key",
            value=current_gemini_key,
            type="password",
            help="Google AI Studio Gemini API Key"
        )
        weather_key_input = st.text_input(
            "OpenWeather API Key (Optional)",
            value=os.getenv("OPENWEATHER_API_KEY", ""),
            type="password",
            help="Free key from OpenWeatherMap (Optional, satellite telemetry works automatically!)"
        )
        if st.button("Save & Update Keys"):
            os.environ["GEMINI_API_KEY"] = gemini_key_input
            os.environ["OPENWEATHER_API_KEY"] = weather_key_input
            st.success("Keys updated successfully!")
            st.rerun()

    # Active City Selector
    st.markdown("---")
    st.markdown("### 📍 Location Focus")
    city_options = ["Delhi", "Mumbai", "Bengaluru", "Jaipur", "Kolkata", "Pune", "Chennai", "Hyderabad", "Varanasi", "Shimla"]
    selected_city = st.selectbox("Select Quick City", options=city_options, index=0)
    custom_city = st.text_input("Or enter custom city:", placeholder="e.g. Ahmedabad, London")
    active_city = custom_city.strip() if custom_city.strip() else selected_city

    # 1-Click Feature Scenarios
    st.markdown("---")
    st.markdown("### 🎯 Quick Intelligence Scenarios")
    st.caption("Click any scenario below to trigger real-time AI reasoning:")
    
    demo_prompts = [
        "🌧️ Will it rain in Delhi today? Should I carry an umbrella?",
        "🌾 Farming advice for wheat crops in Jaipur with current moisture",
        "🚨 Are there any extreme storm or heatwave alerts in Kolkata?",
        "✈️ Commuter advice: Visibility & road travel safety in Mumbai"
    ]
    
    clicked_prompt = None
    for prompt_text in demo_prompts:
        if st.button(prompt_text, use_container_width=True):
            clicked_prompt = prompt_text

    st.markdown("---")
    st.caption("⚡ **System Status**: Telemetry Pipeline & AI Reasoning Engine Active")

# 3. Main Header & Real-Time Weather Dashboard
st.markdown("<div class='main-title'>🌦️ WeatherGPT</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Conversational AI for Real-Time Forecasting, Disaster Alerts, and Climate Intelligence (SIH26068)</div>", unsafe_allow_html=True)

# Fetch Current Weather for Active City
current_weather = get_current_weather(active_city, weather_key_input)

# Display Extreme Alerts Banner if any
if current_weather.get("alerts"):
    for alert in current_weather["alerts"]:
        if alert["severity"] in ["CRITICAL", "HIGH"]:
            st.error(f"🚨 **{alert['type']}**: {alert['message']}")
        else:
            st.warning(f"⚠️ **{alert['type']}**: {alert['message']}")
elif current_weather.get("note"):
    st.info(f"💡 {current_weather['note']}")

# Top Weather Metrics Ribbon
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label=f"📍 {current_weather['city']} Temp",
        value=f"{current_weather['temperature']}°C",
        delta=f"Feels like {current_weather['feels_like']}°C"
    )
with col2:
    st.metric(
        label="Condition",
        value=current_weather['condition'],
        delta=current_weather.get('description', '')
    )
with col3:
    st.metric(
        label="💧 Humidity",
        value=f"{current_weather['humidity']}%",
        delta=f"{current_weather['pressure']} hPa"
    )
with col4:
    st.metric(
        label="💨 Wind Speed",
        value=f"{current_weather['wind_speed']} km/h",
        delta=f"Visibility {round(current_weather['visibility']/1000, 1)} km"
    )

st.markdown("---")

# 4. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                f"Namaste! 🙏 I am **WeatherGPT**, your AI meteorologist and climate advisor.\n\n"
                f"Currently monitoring **{active_city}** ({current_weather['temperature']}°C, {current_weather['condition']}).\n\n"
                f"You can ask me about:\n"
                f"- 🌦️ **Forecast & Rain probability** (*'Kya aaj barish hogi?'*)\n"
                f"- 🌾 **Farming & Irrigation guidance** (*'Should I water my mustard crops today?'*)\n"
                f"- 🚨 **Extreme weather warnings** (*'Any cyclone or heatwave alerts?'*)\n"
                f"- 🚗 **Travel & Commute safety** (*'Is it safe to drive to Pune tonight?'*)"
            )
        }
    ]

# Session state for audio
if "audio_data" not in st.session_state:
    st.session_state.audio_data = {}

# Display Chat History with audio replay
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Show audio replay button for assistant messages
        if message["role"] == "assistant" and i > 0:
            if st.button(f"🔊 Listen", key=f"replay_{i}", help="Play this response as audio"):
                with st.spinner("Generating audio..."):
                    audio_bytes = text_to_audio_bytes(message["content"])
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                else:
                    st.warning("Audio generation failed. Check internet connection.")

# User Input Handling (From chat input or Demo Prompt button)
user_prompt = st.chat_input("🎙️ Ask WeatherGPT about weather, farming, travel, or climate...")
if clicked_prompt:
    user_prompt = clicked_prompt

if user_prompt:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Process AI Response
    with st.chat_message("assistant"):
        active_key = gemini_key_input.strip() if (gemini_key_input and gemini_key_input.strip()) else current_gemini_key
        # Instant Real-Time Streaming Output
        stream_gen = stream_weather_gpt(
            user_query=user_prompt,
            selected_city=active_city,
            gemini_key=active_key,
            openweather_key=weather_key_input,
            chat_history=st.session_state.messages
        )
        ai_reply = st.write_stream(stream_gen)

        # Auto-play audio immediately after streaming
        with st.spinner("🔊 Generating voice..."):
            audio_bytes = text_to_audio_bytes(ai_reply)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)

    # Save assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# Footer
st.markdown("---")
col_left, col_right = st.columns([3, 1])
with col_left:
    st.caption("Smart India Hackathon (SIH26068) • Built with Streamlit, Google Gemini AI & OpenWeatherMap | 🔊 Powered by gTTS Voice Engine")
with col_right:
    if st.button("🧹 Clear Conversation"):
        st.session_state.messages = []
        st.session_state.audio_data = {}
        st.rerun()
