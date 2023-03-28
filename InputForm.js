import React, { useState } from 'react';

function InputForm() {
  const [inputValue, setInputValue] = useState('');
  const [serverMessage, setServerMessage] = useState('');

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
    setInputValue('');
  }

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  return (
    <div>
      {/* Display the server message */}
      <p>{serverMessage}</p>

      <form onSubmit={handleSubmit} style={{ position: "fixed", bottom: 50 }}>
        <input type="text" value={inputValue} onChange={handleInputChange} />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default InputForm;