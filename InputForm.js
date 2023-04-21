import React, { useState } from 'react';
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  Avatar,
} from "@chatscope/chat-ui-kit-react";

function InputForm() {
  const [inputValue, setInputValue] = useState('');
  const [serverMessage, setServerMessage] = useState('');
  const [messages, setMessages] = useState([]);

  // function called after send (submit button not clickable if no input is entered)
  const handleSend = async (message) => {
    setInputValue(message);

    const response = await fetch('http://localhost:5000/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_input: message }),
    });

    const data = await response.json();
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
    <div style={{ position: "relative", height: "500px", overflow: 'hidden' }}>
      <MainContainer>
        <ChatContainer> 
          <MessageList scrollBehavior="smooth">
            <Message
              // greeting message from bot when you open the chatbot
              model={{
                message: "Welcome to UTDChatbot. I am here to help you.",
                sentTime: "just now",
                sender: "UTDChatbot",
                direction: 'incoming'
              }} 
            >
            </Message>
            {messages.map((m,i) => <Message key={i} model={m} />)}
          </MessageList>  
          <MessageInput attachButton={false} placeholder="Type message here..." onSend={handleSend}/> 
        </ChatContainer>
      </MainContainer>
    </div>
  );
}

export default InputForm;