import streamlit as st
from openai import OpenAI

# 1. Configuration de la page (Titre, icône...)
st.set_page_config(page_title="L'Expert MarTech", page_icon="🤖")

st.title("🤖 Assistant Expert MarTech & Sales")
st.write(
    "Je suis spécialisé dans la recommandation pragmatique d'outils et de workflows "
    "pour optimiser vos processus marketing et commerciaux. Pas de bla-bla, du ROI."
)

# 2. Gestion de la clé API (Sécurité)
# On demande la clé dans la barre latérale pour ne pas la laisser traîner dans le code public
with st.sidebar:
    st.header("Configuration")
    openai_api_key = st.text_input("Entrez votre clé API OpenAI", type="password")
    st.info("Cette clé n'est pas stockée, elle sert juste pour cette session.")

# 3. Initialisation de l'historique de discussion
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Bonjour. Quel processus cherchez-vous à optimiser aujourd'hui ?"}
    ]

# 4. Affichage des messages précédents
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 5. Zone de saisie utilisateur et logique de réponse
if prompt := st.chat_input():
    if not openai_api_key:
        st.error("Veuillez entrer votre clé API dans la barre latérale pour commencer.")
        st.stop()

    # On affiche le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Connexion à l'IA
    client = OpenAI(api_key=openai_api_key)
    
    # LE CERVEAU : C'est ici qu'on définit l'expertise
    system_prompt = """
    Tu es un expert senior en technologies Marketing (MarTech) et Sales. 
    Ton ton est pragmatique, direct et orienté ROI.
    Ta mission : Recommander des outils et des workflows précis pour optimiser les processus B2B.
    Règles :
    1. Ne propose jamais d'outils "gadgets".
    2. Pour chaque recommandation, explique brièvement pourquoi cet outil et comment l'intégrer.
    3. Si la demande est vague, pose des questions qualifiantes (budget, taille équipe, tech stack actuelle).
    4. Reste courtois mais professionnel, comme un consultant expérimenté.
    """

    # Envoi de la requête à OpenAI
    response = client.chat.completions.create(
        model="gpt-4o", # Le modèle le plus intelligent
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
    )
    
    msg_content = response.choices[0].message.content
    
    # Affichage de la réponse
    st.session_state.messages.append({"role": "assistant", "content": msg_content})
    st.chat_message("assistant").write(msg_content)
