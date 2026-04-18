import streamlit as st
from chef_logic import BoluluSefBot
import time

# Sayfa yapılandırması
st.set_page_config(
    page_title="Bolulu Şef Chatbot",
    page_icon="👨‍🍳",
    layout="centered"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        color: #ffffff;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }
    .stChatInputContainer {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1 {
        background: -webkit-linear-gradient(#ff8c00, #ff4500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        font-size: 3rem !important;
    }
    .subtitle {
        text-align: center;
        color: #aaa;
        margin-bottom: 2rem;
    }
    .chef-avatar {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .stSidebar [data-testid="stImage"] {
        border-radius: 50%;
        border: 3px solid #ff8c00;
    }
</style>
""", unsafe_allow_html=True)

# Botu yükle
@st.cache_resource
def load_bot():
    return BoluluSefBot()

bot = load_bot()

# Header
st.markdown("<h1>BOLULU ŞEF</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Bolu usulü lezzetler, esprili tarifler!</p>", unsafe_allow_html=True)

# Chat geçmişini başlat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Selam evlat! Ben Bolulu Şef. Mutfakta ne fırtınalar estirelim bugün? İster tarif sor, ister elindeki malzemeleri söyle, gerisini bana bırak!"}
    ]

# Mesajları görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Şefime bir şeyler sor..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot cevabı
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Gerçek cevap logic'i
        assistant_response = bot.get_chef_response(prompt)
        
        # Yazma animasyonu
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Cevabı geçmişe ekle
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar - Proje Bilgileri
with st.sidebar:
    st.image("assets/chef.png", width=150)
    st.title("👨‍🍳 Mutfak Defteri")
    st.info("""
    **Bolulu Şef NLP Projesi**
    - **Model:** Sentence Transformers (SBERT)
    - **Dataset:** Structured Intents + SBERT Embeddings
    - **Kategoriler:**
        - 🥘 Ana Yemekler
        - 🥣 Çorbalar
        - 🍰 Tatlılar
        - 🥗 Salatalar & Mezeler
        - 🥐 Hamur İşleri
    """)
    if st.button("Şefin Notu"):
        st.write("Lezzet Bolu'dan, tarif şeften! Malzemen varsa sor, yoksa çarşıya kadar yolun var evlat. 😄")
