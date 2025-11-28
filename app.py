import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="L'Expert MarTech", page_icon="🤖")
st.title("🤖 Assistant Expert MarTech")

# --- CHARGEMENT DE LA CONNAISSANCE (L'ANTISÈCHE) ---
# On essaie de lire le fichier texte s'il existe
try:
    with open("connaissance.txt", "r", encoding="utf-8") as f:
        knowledge_base = f.read()
except FileNotFoundError:
    knowledge_base = "" # Si le fichier n'existe pas, on met une chaîne vide

# --- INITIALISATION DE LA MÉMOIRE ---
if "library" not in st.session_state:
    st.session_state["library"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Bonjour. Quel processus cherchez-vous à optimiser ?"}
    ]

with st.sidebar:
    st.header("Configuration")
    openai_api_key = st.text_input("Clé API OpenAI", type="password")
    
    # Petit indicateur pour voir si la connaissance est chargée
    if knowledge_base:
        st.success("✅ Base de connaissance chargée")
    else:
        st.warning("⚠️ Aucune connaissance spécifique trouvée")

# Affichage discussion
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- LE CŒUR DU SYSTÈME ---
if prompt := st.chat_input():
    if not openai_api_key:
        st.error("Veuillez entrer votre clé API.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client = OpenAI(api_key=openai_api_key)

    # --- INJECTION DU CONTEXTE DANS LE PROMPT ---
    # C'est ici que la magie opère : on fusionne votre expertise avec celle de GPT
    system_prompt = f"""
    Tu es un expert senior en technologies Marketing (MarTech) et Sales.
    Ton ton est pragmatique, direct et orienté ROI.
    
    VOICI DES INFORMATIONS SPÉCIFIQUES ET À JOUR QUE TU DOIS UTILISER :
    --- DÉBUT DE LA CONNAISSANCE INTERNE ---
    {knowledge_base}
    --- FIN DE LA CONNAISSANCE INTERNE ---
    
    Règles :
    1. Si la réponse se trouve dans la "Connaissance Interne", utilise-la en priorité.
    2. Si tu ne sais pas, dis-le, n'invente pas.
    3. Recommande des workflows précis.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
    )
    msg_content = response.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": msg_content})
    st.chat_message("assistant").write(msg_content)

    # --- FONCTION BIBLIOTHÉCAIRE (Cas d'usage) ---
    reformulation_prompt = f"""
    Analyse cette demande utilisateur : "{prompt}".
    Reformule-la en un TITRE de cas d'usage générique (max 10 mots).
    """
    
    summary_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": reformulation_prompt}]
    )
    cas_usage = summary_response.choices[0].message.content.strip().replace('"', '')
    st.session_state["library"].append(cas_usage)
