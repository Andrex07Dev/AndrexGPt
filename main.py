import os
import streamlit as st
import time
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# Carica le chiavi dal file .env
load_dotenv()
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
# Configura il modello LLM
llm = GoogleGenerativeAI(model='gemini-pro', temperature=0.1)

# Crea un template per il prompt
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are an excellent content writer so write on a topic given by the user'),
    ('user', '{user_query}')
])

# Funzione per leggere gli utenti dal file
def load_users():
    users = {}
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                email, username, password, user_id = line.strip().split(",")
                users[email] = {"username": username, "password": password, "id": int(user_id)}
    return users

# Funzione per salvare un nuovo utente nel file
def save_user(email, username, password, user_id):
    with open("users.txt", "a") as file:
        file.write(f"{email},{username},{password},{user_id}\n")

# Funzione per verificare le credenziali
def check_login(email, password, users_db):
    user = users_db.get(email)
    return user and user["password"] == password

# Funzione per registrare un nuovo utente
def register_user(email, password, username, users_db, next_user_id):
    if email in users_db:
        return False
    save_user(email, username, password, next_user_id)
    users_db[email] = {"username": username, "password": password, "id": next_user_id}
    return True

# Layout principale
st.set_page_config(page_title="Andrex GPT", layout="centered")

# Nascondi la barra laterale e la barra di opzioni in alto a destra
st.markdown("""
<style>
.css-1yhjh9e {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Funzione per la pagina di login
def login_page(users_db):
    st.title("Benvenuto ad Andrex GPT - Login")
    st.markdown("""
    <style>
    .login-form {
        width: 300px;
        padding: 20px;
        border-radius: 10px;
        background-color: #f7f7f7;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .login-input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .login-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
        border: none;
    }
    .login-button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button('Login'):
        if check_login(email, password, users_db):
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
            st.session_state["username"] = users_db[email]["username"]
            st.session_state["page"] = "chat"  # Direttamente alla pagina della chat
            st.success(f"Login effettuato con successo, {st.session_state['username']}!")
            st.rerun()  # Forza il ricaricamento della pagina per aggiornare lo stato
        else:
            st.error("Credenziali errate. Riprova.")

    # Link per il sign up
    if st.button('Non hai un account? Registrati'):
        st.session_state["page"] = "signup"
        st.rerun()  # Forza il ricaricamento

# Funzione per la pagina di registrazione
def signup_page(users_db, next_user_id):
    st.title("Registrati ad Andrex GPT")
    st.markdown("""
    <style>
    .signup-form {
        width: 300px;
        padding: 20px;
        border-radius: 10px;
        background-color: #f7f7f7;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .signup-input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .signup-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
        border: none;
    }
    .signup-button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

    email = st.text_input("Email", key="signup_email")
    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button('Registrati'):
        if register_user(email, password, username, users_db, next_user_id):
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
            st.session_state["username"] = username
            st.session_state["page"] = "chat"  # Direttamente alla pagina della chat
            st.success(f"Registrazione riuscita! Benvenuto, {st.session_state['username']}.")
            st.rerun()  # Forza il ricaricamento della pagina per aggiornare lo stato
        else:
            st.error("Questo email è già registrato.")

    # Link per il login
    if st.button('Hai già un account? Accedi'):
        st.session_state["page"] = "login"
        st.rerun()  # Forza il ricaricamento

# Funzione per la scrittura graduale della risposta
def gradual_response(response, container, delay=0.05):
    full_text = ""  # Inizializza una variabile per contenere il testo completo
    words = response.split()
    for word in words:
        full_text += word + " "  # Aggiungi ogni parola al testo completo
        container.write(full_text)  # Aggiorna il contenitore con il testo progressivo
        time.sleep(delay)  # Ritardo tra le parole

# Funzione per la pagina Andrex GPT (accessibile dopo login)

def andrex_gpt_page():
    st.title("Andrex GPT - Genera Contenuto")

    user_query_input = st.text_input("Cosa vuoi chiedere ad AndrexGPT?", key="user_query_input")

    if user_query_input:
        # Usa HumanMessage per modelli chat-based
        chat_message = HumanMessage(content=user_query_input)
        response = llm.invoke([chat_message])  # Passa come lista

        # Visualizza la risposta
        response_container = st.empty()
        gradual_response(response.content, response_container)

# Funzione principale per gestire il flusso delle pagine
def main():
    # Carica gli utenti dal file
    users_db = load_users()

    # Trova il prossimo ID utente
    next_user_id = max([user["id"] for user in users_db.values()], default=0) + 1

    # Verifica se l'utente è loggato e in quale pagina è
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["page"] = "login"  # Pagina iniziale è login

    # Gestisci la navigazione tra login, registrazione e chat
    if st.session_state["logged_in"]:
        andrex_gpt_page()
    elif st.session_state["page"] == "login":
        login_page(users_db)
    elif st.session_state["page"] == "signup":
        signup_page(users_db, next_user_id)

if __name__ == "__main__":
    main()
