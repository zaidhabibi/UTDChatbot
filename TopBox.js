// this file renders the design for the area around the top border (the colored area)

import { View } from 'react-native';
import React from 'react';

//This file creates the background box for the chat box
/* *NOTE*: After implementing the Chat UI module kit, this file is no longer
    implemented in App.js. However, it is being kept to provide documentation into
    our first phases of developing the chatbot.
*/
class TopBox extends React.Component {
    render() {
        return (
            <View style={styles.rectangle}></View>
        );
    }
}

const styles = {
    rectangle: {
        width: '700px',
        height: '30px',
        backgroundColor: '#ff7f50',
        border: "2px solid black"
    }
}

export default TopBox;