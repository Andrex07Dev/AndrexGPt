AndrexGPT
Andrex GPT 🚀 Andrex GPT is a user-friendly content generation web application built using Streamlit and Google Generative AI (Gemini Pro). It features user authentication (login and sign-up functionality) and allows users to generate high-quality content by interacting with the Andrex GPT model.

Features 🎯 User Authentication

Login and registration (stored locally in a text file). Secure credential validation for registered users. Content Generation

Seamlessly generate content on any topic using Google Generative AI's Gemini Pro model. User inputs a query, and the app generates a high-quality response. Session Management

Users remain logged in for seamless usage across pages. Streamlit-Powered UI

Beautiful and responsive interface with custom styling. Installation 🔧 Follow these steps to set up and run Andrex GPT on your local machine:

Clone the Repository git clone https://github.com/Andrex07Dev/AndrexGPT cd andrex-gpt
Set Up Environment Install the required dependencies using pip:
pip install -r requirements.txt 3. Set Up API Keys Edit a .env file in the root directory of the project and add your Google Generative AI API Key and LangChain API Key:

GOOGLE_API_KEY=your_google_api_key LANGCHAIN_API_KEY=your_langchain_api_key 4. Run the Application Run the Streamlit application:

File Structure 📂 andrex-gpt/ │ ├── app.py # Main app file ├── users.txt # File storing user credentials ├── .env # Environment variables for API keys ├── requirements.txt # Project dependencies └── README.md # Project documentation Usage 📝 Login or Sign Up

On launching the app, you can either log in with existing credentials or sign up as a new user. Generate Content

Enter your query or topic in the input box. Click the Generate button, and Andrex GPT will provide content based on your query. Logout

You can close the app or relaunch it. Your session will reset. Dependencies 📦 Google Generative AI (Gemini Pro): Language model for content generation. LangChain: Framework to integrate and manage LLMs. python-dotenv: For managing environment variables. Install dependencies using:

pip install -r requirements.txt API Configuration ⚙️ Google Generative AI

Obtain your API key from Google AI Studio. https://aistudio.google.com/

LangChain https://www.langchain.com/

Contributing 🤝 Contributions are welcome! If you'd like to improve the project, fork the repository and submit a pull request with your changes.

License 📄 This project is licensed under the MIT License.

Contact 📧 If you have questions or suggestions, feel free to contact me.

Email: Not yet GitHub: @Andrex07DEv Happy Coding! 😊🚀
