import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import InputForm from './InputForm';
import Title from './Title';
import Box from './Box';

export default function App() {
  return (
    <View style={styles.container}>
      <Title />
      <Box />
      <InputForm />
      <StatusBar style="auto" />
    </View>
  );
}

/*
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'absolute',
    right: 20,
    top: 300
  },
});
*/

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  app: {
    alignItems: 'center',
    justifyContent: 'center',
    width: '80%',
    height: '80%',
    borderWidth: 1,
    borderColor: '#000',
  },
});