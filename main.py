import streamlit as st
from streamlit_webrtc import webrtc_streamer, get_twilio_ice_servers

frontend_ice_type = st.selectbox("Frontend ICE type", ["Empty", "Google STUN", "Twilio TURN"])
backend_ice_type = st.selectbox("Backend ICE type", ["Empty", "Google STUN", "Twilio TURN"])

if frontend_ice_type == "Empty":
    frontend_rtc_configuration = {
        "iceServers": []
    }
elif frontend_ice_type == "Google STUN":
    frontend_rtc_configuration = {
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
elif frontend_ice_type == "Twilio TURN":
    frontend_rtc_configuration = {
        "iceServers": get_twilio_ice_servers(
            twilio_sid=st.secrets["TWILIO_ACCOUNT_SID"],
            twilio_token=st.secrets["TWILIO_AUTH_TOKEN"],
        )
    }

if backend_ice_type == "Empty":
    backend_rtc_configuration = {
        "iceServers": []
    }
elif backend_ice_type == "Google STUN":
    backend_rtc_configuration = {
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
elif backend_ice_type == "Twilio TURN":
    backend_rtc_configuration = {
        "iceServers": get_twilio_ice_servers(
            twilio_sid=st.secrets["TWILIO_ACCOUNT_SID"],
            twilio_token=st.secrets["TWILIO_AUTH_TOKEN"],
        )
    }

st.write("Frontend ICE configuration:", frontend_rtc_configuration)
st.write("Backend ICE configuration:", backend_rtc_configuration)

webrtc_streamer(
    key="example",
    media_stream_constraints={"video": True, "audio": False},
    frontend_rtc_configuration=frontend_rtc_configuration,
    server_rtc_configuration=backend_rtc_configuration,
)
