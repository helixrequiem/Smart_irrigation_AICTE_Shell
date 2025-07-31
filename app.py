import streamlit as st
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt

model = joblib.load("Farm_Irrigation_System.pkl")

st.set_page_config(page_title="Irrigo: The Enchanted Garden Assistant", layout="wide")

st.markdown("""
    <style>
    html, body, .stApp {
        background: linear-gradient(135deg, #e0f7fa, #e1bee7, #fff3e0);
        animation: gradientShift 20s ease infinite;
        background-size: 400% 400%;
    }

    @keyframes gradientShift {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .title {
        font-size: 3.5em;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(to right, #4caf50, #81c784, #aed581);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        font-size: 1.3em;
        color: #555;
        margin-bottom: 2rem;
    }

    .magic-box {
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
        font-weight: 600;
        transition: 0.3s;
    }

    .on {
        background: linear-gradient(to right, #c8e6c9, #a5d6a7);
        color: #2e7d32;
    }

    .off {
        background: linear-gradient(to right, #ffcdd2, #ef9a9a);
        color: #b71c1c;
    }

    .magic-box:hover {
        transform: scale(1.03);
    }

    .chart-title {
        font-size: 1.5em;
        font-weight: bold;
        color: #3f51b5;
        margin-top: 1.5rem;
        text-align: center;
    }

    footer {
        text-align: center;
        font-size: 0.9em;
        color: gray;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🌺 Welcome to Irrigo’s Enchanted Irrigation Sytem</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>“Adjust the soil sensors, and I shall whisper to the sprinklers…” 🌧️🧙‍♀️</div>", unsafe_allow_html=True)
st.markdown("---")

sensor_values = []
st.markdown("### 🌱 Tell me, how moist is your soil today?")
cols = st.columns(4)
for i in range(20):
    with cols[i % 4]:
        val = st.slider(f"Sensor {i}", 0.0, 1.0, 0.5, 0.01, help="Scaled from dry (0.0) to wet (1.0)")
        sensor_values.append(val)

if st.button("🔍 Ask Irrigo for Guidance"):
    with st.spinner("Reading soil memories and consulting the sky spirits... ✨"):
        input_array = np.array(sensor_values).reshape(1, -1)
        prediction = model.predict(input_array)[0]

    st.success("The sprinklers have received my command 🪄")

    st.markdown("## 💧 Sprinkler Prophecy")
    result_cols = st.columns(4)
    for i, status in enumerate(prediction):
        msg = f"Sprinkler {i} {'💦 Water flows!' if status else '🌵 Peaceful slumber.'}"
        box_class = 'on' if status else 'off'
        with result_cols[i % 4]:
            st.markdown(f"<div class='magic-box {box_class}'>{msg}</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-title'>🌼 Smart Hydration Summary</div>", unsafe_allow_html=True)
    df = pd.DataFrame({
        'Sprinkler': [f"Sprinkler {i}" for i in range(len(prediction))],
        'Status': ['ON' if s == 1 else 'OFF' for s in prediction]
    })

    counts = df['Status'].value_counts()
    fig, ax = plt.subplots()
    ax.bar(counts.index, counts.values, color=['#81c784' if s == 'ON' else '#ef5350' for s in counts.index])
    ax.set_ylabel("Number of Sprinklers")
    ax.set_title("🪴 ON vs OFF Status")
    st.pyplot(fig)

    st.balloons()
    
st.markdown("---")
st.markdown("<footer>Made with 🌿 by Irrigo — Your Smart Irrigation Companion</footer>", unsafe_allow_html=True)
