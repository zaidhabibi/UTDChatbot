import React, { useState } from 'react';

function InputForm() {
    const [inputValue, setInputValue] = useState('');
    
    const handleSubmit = async (e) => {
        // this done to prevent the page from reloading when a submit button is clicked
        // which is a default for some reason
        e.preventDefault();

        const response = await fetch('http://localhost:5000/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: inputValue }),
        });

        // get the answer and
        const data = await response.json();
        // print it to the console
        console.log(data.message);
    }

    // update the input state when it changes
    const handleInputChange = (e) => {
        setInputValue(e.target.value);
      };

    // it's a form where you can submit an input
    return (
        <form onSubmit={handleSubmit}>
          <input type="text" value={inputValue} onChange={handleInputChange} />
          <button type="submit">Send</button>
        </form>
      );
}

export default InputForm;