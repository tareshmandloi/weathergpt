# WeatherGPT: Conversational AI for Weather Forecasting, Alerts & Climate Information

**Problem Statement ID**: SIH26068  
**Built for**: Smart India Hackathon (SIH)  
**Technology Stack**: Python 3.14, Streamlit, Google Gemini 2.5 Flash, OpenWeatherMap API

---

## 🌟 Key Features
1. **Natural Conversational Forecasting**: Chat naturally in English, Hindi, or Hinglish to ask about rain probability, temperatures, and 5-day trends.
2. **Disaster & Extreme Weather Alert Engine**: Automatic telemetry scan for Heatwaves, Thunderstorms, High Winds, Heavy Rain/Flooding, and Low Visibility/Fog.
3. **Domain-Specific Advisory**:
   - 🌾 **Agricultural & Farmers Advisory**: Soil moisture & humidity analysis, crop irrigation guidelines, fungal pest risk prediction.
   - 🚗 **Commuter & Travel Insights**: Road safety, fog/mist visibility cautions, umbrella recommendations.
4. **Resilient Fail-Safe Architecture**: Built-in intelligent simulation mode ensures the live demonstration **never crashes** if network is slow or API keys are activating.

---

## 🚀 How to Run the Application

### 1. Open Terminal or PowerShell
Navigate to the project folder:
```powershell
cd C:\Users\asus\.gemini\antigravity\scratch\weathergpt
```

### 2. Launch the Web App
Run the following command:
```powershell
python -m streamlit run app.py
```
Your browser will automatically open at `http://localhost:8501`!

---

## 🔑 Adding Free API Keys
You can either:
1. Put them in the `.env` file:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   OPENWEATHER_API_KEY=your_openweather_key_here
   ```
2. **OR** enter them directly into the **"API Key Settings"** panel in the left sidebar of the web app during your live demo!

---

## 🏆 Presentation Tips for Internal Hackathon Judges
1. **Start with the Problem**: *"Current weather apps only show raw numbers that common citizens, farmers, and daily commuters find difficult to interpret."*
2. **Show the Solution**: *"WeatherGPT translates complex meteorological data into conversational, actionable advice in real time."*
3. **Demonstrate 3 Core Scenarios**:
   - Scenario 1: **Daily Citizen** (*"Will it rain today? Do I need an umbrella?"*)
   - Scenario 2: **Farmer Support** (*"Farming advice for wheat crops in Jaipur"* - shows irrigation & humidity tips)
   - Scenario 3: **Disaster Safety** (*"Alerts for extreme weather"* - shows the red alert banner)
