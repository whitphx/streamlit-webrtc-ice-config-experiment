import streamlit as st
from streamlit_webrtc import webrtc_streamer, get_hf_ice_servers, get_twilio_ice_servers, __version__ as st_webrtc_version
import aiortc
import aioice

import logging
logging.basicConfig(level=logging.INFO)

aioice_logger = logging.getLogger("aioice")
aioice_logger.setLevel(logging.DEBUG)

aiortc_logger = logging.getLogger("aiortc")
aiortc_logger.setLevel(logging.DEBUG)
aiortc_rtcrtpreceiver_logger = logging.getLogger("aiortc.rtcrtpreceiver")
aiortc_rtcrtpreceiver_logger.setLevel(logging.INFO)
aiortc_rtcrtpsender_logger = logging.getLogger("aiortc.rtcrtpsender")
aiortc_rtcrtpsender_logger.setLevel(logging.INFO)


frontend_ice_type = st.selectbox("Frontend ICE type", ["Empty", "Google STUN", "Twilio STUN/TURN", "Twilio STUN/TURN and Google STUN", "HF TURN only", "HF TURN and Google STUN", "None configured"])
backend_ice_type = st.selectbox("Backend ICE type", ["Empty", "Google STUN", "Twilio STUN/TURN", "Twilio STUN/TURN and Google STUN", "HF TURN only", "HF TURN and Google STUN", "None configured"])

# google_stun_ice_servers = [{"urls": ["stun:stun.l.google.com:19302"]}]
google_stun_ice_servers = [{"urls": "stun:stun.l.google.com:19302", "url": "stun:stun.l.google.com:19302"}]

if frontend_ice_type == "Empty":
    frontend_rtc_configuration = {
        "iceServers": []
    }
elif frontend_ice_type == "Google STUN":
    frontend_rtc_configuration = {
        "iceServers": google_stun_ice_servers
    }
elif frontend_ice_type == "Twilio STUN/TURN":
    frontend_rtc_configuration = {
        "iceServers": get_twilio_ice_servers(
            twilio_sid=st.secrets["TWILIO_ACCOUNT_SID"],
            twilio_token=st.secrets["TWILIO_AUTH_TOKEN"],
        )
    }
elif frontend_ice_type == "Twilio STUN/TURN and Google STUN":
    frontend_rtc_configuration = {
        "iceServers": google_stun_ice_servers + get_twilio_ice_servers(
            twilio_sid=st.secrets["TWILIO_ACCOUNT_SID"],
            twilio_token=st.secrets["TWILIO_AUTH_TOKEN"],
        )
    }
elif frontend_ice_type == "HF TURN only":
    frontend_rtc_configuration = {
        "iceServers": get_hf_ice_servers(token=st.secrets["HF_TOKEN"])
    }
elif frontend_ice_type == "HF TURN and Google STUN":
    frontend_rtc_configuration = {
        "iceServers": get_hf_ice_servers(token=st.secrets["HF_TOKEN"]) + google_stun_ice_servers
    }
elif frontend_ice_type == "None configured":
    frontend_rtc_configuration = None

if backend_ice_type == "Empty":
    backend_rtc_configuration = {
        "iceServers": []
    }
elif backend_ice_type == "Google STUN":
    backend_rtc_configuration = {
        "iceServers": google_stun_ice_servers
    }
elif backend_ice_type == "Twilio STUN/TURN":
    backend_rtc_configuration = {
        "iceServers": get_twilio_ice_servers(
            twilio_sid=st.secrets["TWILIO_ACCOUNT_SID"],
            twilio_token=st.secrets["TWILIO_AUTH_TOKEN"],
        )
    }
elif backend_ice_type == "Twilio STUN/TURN and Google STUN":
    backend_rtc_configuration = {
        "iceServers": google_stun_ice_servers + get_twilio_ice_servers(
            twilio_sid=st.secrets["TWILIO_ACCOUNT_SID"],
            twilio_token=st.secrets["TWILIO_AUTH_TOKEN"],
        ) + google_stun_ice_servers
    }
elif backend_ice_type == "HF TURN only":
    backend_rtc_configuration = {
        "iceServers": get_hf_ice_servers(token=st.secrets["HF_TOKEN"])
    }
elif backend_ice_type == "HF TURN and Google STUN":
    backend_rtc_configuration = {
        "iceServers": get_hf_ice_servers(token=st.secrets["HF_TOKEN"]) + google_stun_ice_servers
    }
elif backend_ice_type == "None configured":
    backend_rtc_configuration = None


if st.checkbox("Add invalid TURN server"):
    backend_rtc_configuration["iceServers"].append({
        "urls":"turn:gradio-turn.com:80",
        "username":"non-existing-username",
        "credential":"non-existing-credential"
    })


st.write("Frontend ICE configuration:", frontend_rtc_configuration)
st.write("Backend ICE configuration:", backend_rtc_configuration)

webrtc_streamer(
    key="example",
    media_stream_constraints={"video": True, "audio": False},
    frontend_rtc_configuration=frontend_rtc_configuration,
    server_rtc_configuration=backend_rtc_configuration,
)

st.write(f"Streamlit version: {st.__version__}")
st.write(f"Streamlit-WebRTC version: {st_webrtc_version}")
st.write(f"aiortc version: {aiortc.__version__}")
st.write(f"aioice version: {aioice.__version__}")
