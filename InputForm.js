import React, { useState } from 'react';
import './inputform_style.css';
import './text_boundary.css';

function InputForm() {
  const [inputValue, setInputValue] = useState('');
  const [serverMessage, setServerMessage] = useState('');
  const [showPromptText, setPromptText] = useState(true); //default message before any conversation begins
  //const [showUserText, setUserText] = useState(false); //user message will not appear on app until message sent

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('http://localhost:5000/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_input: inputValue }),
    });

    const data = await response.json();
    setServerMessage(data.message);
    setPromptText(false);
    //setUserText(true);
  }

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  return (
    <div className="input-container">
      
      {showPromptText && <p className="placeholder-bot-text">Successfully connected to UTD Admissions Chatbot.</p>}
      {/* Display the server message */}
      <p className="text-boundary">{serverMessage}</p>

      <form onSubmit={handleSubmit} style={{ position: "absolute", bottom: 50 }}>
        <input type="text" className="input-field" placeholder="Ask us something!" value={inputValue} onChange={handleInputChange} />
        <button type="submit" className="input-button">Send</button>
      </form>
    </div>
  );
}

export default InputForm;