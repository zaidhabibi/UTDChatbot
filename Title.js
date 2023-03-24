import React from 'react';
//import ReactDOM from 'react-dom/client';

//This file creates the title for the chat box

/*
function Title() {
    return (
        <div>
            <h1 style={{
                color: "green",
                padding: "10px",
                fontFamily: "Serif"
            }}>UTD Chatbot</h1>
        </div>
    );
}
*/

function Title() {
    return (
        <div style={
            {
                position: 'absolute', top: 0, right: 0
            }}>

            <h1 style={{
                color: "green",
                padding: "10px",
                fontFamily: "Serif",
                textAlign: "right"
            }}>CometBot</h1>
        </div>
    );
}

// ALTERNATE METHOD TO RENDER IN OFFICIAL DOCUMENTATION //
//const root = ReactDOM.createRoot(document.getElementById('root'));
//root.render(<Title />);

export default Title;
