## UTDChatbot
#### Waheed Anwar, Zaid Habibi, Roopali Kallem, Julia Do, Vasudha Prasad, Nikhil Manda


This is the project's main branch. All files to to run the chatbot are provided. 

First, users must go to this link: https://platform.openai.com/account/api-keys
to create a free OpenAI account and set up their own API keys. 

To install and run the program, the following modules must be downloaded and installed in your
environment, use the command: pip3 install <module name>
  Node.js and NPM
  flask
  flask_restful
  pandas
  openai
  matplotlib
  plotly
  scipy
  scikit-learn
  python-dotenv
  llama_index
  pinecone-client
  flask_cors

To install further essential modules for the UI, run the following commands in the command line:
  npm install expo-cli
  npm install @chatscope/chat-ui-kit-react
  npm install @chatscope/chat-ui-kit-styles

Open one cmd prompt, and type this command: 

python chatbot_api.py


Open a separate cmd prompt, and type this command, then enter the "-w" option:

expo start

