import { View } from 'react-native';
import React from 'react';

//This file creates the background box for the chat box
/* *NOTE*: After implementing the Chat UI module kit, this file is no longer
    implemented in App.js. However, it is being kept to provide documentation into
    our first phases of developing the chatbot.
*/
class Box extends React.Component {
    render() {
        return (
            <View style={styles.rectangle}></View>
        );
    }
}

const styles = {
    rectangle: {
        width: '700px',
        height: '700px',
        backgroundColor: '#EAEAEA',
        border: "2px solid black"
    }
}

export default Box;