import React, { useState } from 'react';
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";

import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  Avatar,
  ConversationHeader,
  TypingIndicator,
  Loader
} from "@chatscope/chat-ui-kit-react";

import logo from './assets/temoc-logo.png';

function InputForm() {
  const [inputValue, setInputValue] = useState('');
  const [serverMessage, setServerMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // function called after send (submit button not clickable if no input is entered)
  const handleSend = async (message) => {
    setInputValue(message);
    setLoading(true);
    const response = await fetch('http://localhost:5000/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_input: message }),
    });
    const data = await response.json();
    setLoading(false);
    setMessages([...messages, {
      message, // user message displayed
      direction: 'outgoing',
      position: "single"
    },
    {  
      message: data.message, // server message displayed
      direction: 'incoming',
      position: "single"
    }]);
  };
 
  return (
    <div style={{ position: "relative", height: "500px", width: "700px",overflow: 'hidden' }}>
      <MainContainer>
        <ChatContainer>
          <ConversationHeader>
            <Avatar src={logo} name="CometBot" />
            <ConversationHeader.Content userName="CometBot"/>
          </ConversationHeader>

          <MessageList scrollBehavior="smooth">
            <Message
              // greeting message from bot when you open the chatbot
              model={{
                payload: "Welcome to CometBot. I am here to help you.",
                sentTime: "just now",
                sender: "CometBot",
                direction: 'incoming'
              }} 
            >
            </Message>
            {messages.map((m,i) => <Message key={i} model={m} />)}
            { loading ?             <Message
              // greeting message from bot when you open the chatbot
              model={{
                payload: "Generating response...",
                sentTime: "just now",
                sender: "CometBot",
                direction: 'incoming'
              }} 
            >
            </Message> : <p></p> }
          </MessageList>
          <MessageInput attachButton={false} placeholder="Type message here..." onSend={handleSend}/> 
        </ChatContainer>
      </MainContainer>
    </div>
  );
}

export default InputForm;