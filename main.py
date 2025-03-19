import streamlit as st
from streamlit_webrtc import webrtc_streamer, get_hf_ice_servers, get_twilio_ice_servers, __version__ as st_webrtc_version

frontend_ice_type = st.selectbox("Frontend ICE type", ["Empty", "Google STUN", "Twilio TURN", "HF TURN only", "HF TURN and Google STUN"])
backend_ice_type = st.selectbox("Backend ICE type", ["Empty", "Google STUN", "Twilio TURN", "HF TURN only", "HF TURN and Google STUN"])

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
elif frontend_ice_type == "HF TURN only":
    hf_ice_servers = get_hf_ice_servers(token=st.secrets["HF_TOKEN"])
    frontend_rtc_configuration = {
        "iceServers": hf_ice_servers
    }
elif frontend_ice_type == "HF TURN and Google STUN":
    hf_ice_servers = get_hf_ice_servers(token=st.secrets["HF_TOKEN"])
    ice_servers = hf_ice_servers + [{"urls": ["stun:stun.l.google.com:19302"]}]
    frontend_rtc_configuration = {
        "iceServers": ice_servers
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
elif backend_ice_type == "HF TURN only":
    hf_ice_servers = get_hf_ice_servers(token=st.secrets["HF_TOKEN"])
    backend_rtc_configuration = {
        "iceServers": hf_ice_servers
    }
elif backend_ice_type == "HF TURN and Google STUN":
    hf_ice_servers = get_hf_ice_servers(token=st.secrets["HF_TOKEN"])
    ice_servers = hf_ice_servers + [{"urls": ["stun:stun.l.google.com:19302"]}]
    backend_rtc_configuration = {
        "iceServers": ice_servers
    }


st.write("Frontend ICE configuration:", frontend_rtc_configuration)
st.write("Backend ICE configuration:", backend_rtc_configuration)

webrtc_streamer(
    key="example",
    media_stream_constraints={"video": True, "audio": False},
    frontend_rtc_configuration=frontend_rtc_configuration,
    server_rtc_configuration=backend_rtc_configuration,
)

st.write(f"Streamlit version: {st.__version__}")
st.write(f"Streamlit-Webrtc version: {st_webrtc_version}")
