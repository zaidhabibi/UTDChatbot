import { View } from 'react-native';
import React from 'react';

//This file creates the background box for the chat box

class Box extends React.Component {
    render() {
      return (
        <View style={styles.rectangle}></View>
      );
    }
  }
  
  const styles = {
      rectangle: {
          width: '300px',
          height: '300px',
          backgroundColor: '#EAEAEA',
          border: "1px solid black"
      }
  }

export default Box;