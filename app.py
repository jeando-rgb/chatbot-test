import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="L'Expert MarTech", page_icon="🤖")

st.title("🤖 Assistant Expert MarTech")

# --- INITIALISATION DE LA MÉMOIRE (La bibliothèque) ---
if "library" not in st.session_state:
    st.session_state["library"] = [] # Une liste vide pour commencer

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Bonjour. Quel processus cherchez-vous à optimiser ?"}
    ]

with st.sidebar:
    st.header("Configuration")
    openai_api_key = st.text_input("Clé API OpenAI", type="password")

# Affichage discussion
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- LE CŒUR DU SYSTÈME ---
if prompt := st.chat_input():
    if not openai_api_key:
        st.error("Veuillez entrer votre clé API.")
        st.stop()

    # 1. On affiche la question utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client = OpenAI(api_key=openai_api_key)

    # 2. On génère la réponse de l'Expert
    system_prompt = "Tu es un expert MarTech pragmatique. Réponds de façon concise et orientée ROI."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
    )
    msg_content = response.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": msg_content})
    st.chat_message("assistant").write(msg_content)

    # --- NOUVEAU : LA FONCTION "BIBLIOTHÉCAIRE" (En arrière-plan) ---
    # On demande à l'IA de créer un titre pour ce cas d'usage
    reformulation_prompt = f"""
    Analyse cette demande utilisateur : "{prompt}".
    Reformule-la en un TITRE de cas d'usage générique (max 10 mots).
    Exemple : "Automatisation de la relance client via LinkedIn"
    """
    
    summary_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": reformulation_prompt}]
    )
    cas_usage = summary_response.choices[0].message.content.strip().replace('"', '')
    
    # On stocke le résultat dans la mémoire partagée
    st.session_state["library"].append(cas_usage)
    # On affiche une petite notification discrète
    st.toast(f"Nouveau cas d'usage identifié : {cas_usage}")
