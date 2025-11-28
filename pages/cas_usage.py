import streamlit as st

st.set_page_config(page_title="Bibliothèque de Cas", page_icon="📚")

st.title("📚 Bibliothèque de Cas d'Usage")
st.write("Voici les cas d'usage détectés par l'IA lors des interactions utilisateurs.")

# On vérifie si la bibliothèque existe
if "library" not in st.session_state or len(st.session_state["library"]) == 0:
    st.info("Aucun cas d'usage enregistré pour le moment. Allez discuter avec l'assistant !")
else:
    # On affiche la liste
    for i, cas in enumerate(st.session_state["library"]):
        st.success(f"Cas #{i+1} : {cas}")

    st.write("---")
    st.caption("Cette liste s'alimente automatiquement via le Chatbot.")
