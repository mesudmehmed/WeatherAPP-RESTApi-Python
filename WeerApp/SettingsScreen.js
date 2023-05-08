import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, Switch, ScrollView, TextInput } from 'react-native';
import { FontAwesome } from 'react-native-vector-icons';
import { TouchableOpacity } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SettingsScreen({ navigation, route }) {
  const [useCelsius, setUseCelsius] = useState(route.params.useCelsius);
  const [city, setCity] = useState(route.params.city);

  const toggleUseCelsius = () => {
    setUseCelsius(!useCelsius);
  };

  const saveSettings = () => {
    if (city) {
      AsyncStorage.setItem('city', city);
    }
    AsyncStorage.setItem('useCelsius', JSON.stringify(useCelsius));
    navigation.navigate('Weather', { useCelsius, city });
  };
  

  const loadSettings = async () => {
    try {
      const useCelsiusValue = await AsyncStorage.getItem('useCelsius');
      const cityValue = await AsyncStorage.getItem('city');
      if (useCelsiusValue !== null && cityValue !== null) {
        setUseCelsius(JSON.parse(useCelsiusValue));
        setCity(cityValue);
      }
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      loadSettings();
    });

    return unsubscribe;
  }, [navigation]);

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scrollContainer}>
        <View style={styles.settingsContainer}>
          <Text style={styles.settingsTitle}>Temperatuureenheid</Text>
          <View style={styles.switchContainer}>
            <Text style={styles.switchText}>Fahrenheit</Text>
            <Switch value={useCelsius} onValueChange={toggleUseCelsius} />
            <Text style={styles.switchText}>Celsius</Text>
          </View>
        </View>
        <View style={styles.settingsContainer}>
          <Text style={styles.settingsTitle}>Locatie van de weer peiling</Text>
          <TextInput
            style={styles.input}
            placeholder="Voer de naam van de stad in"
            value={city}
            onChangeText={(text) => setCity(text)}
          />
        </View>
      </ScrollView>
      <TouchableOpacity style={styles.button} onPress={saveSettings}>
        <Text style={styles.buttonText}>Opslaan</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  scrollContainer: {
    width: '100%',
    paddingHorizontal: 16,
  },
  settingsContainer: {
    backgroundColor: '#eee',
    padding: 16,
    marginBottom: 16,
    borderRadius: 4,
  },
  settingsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  switchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  switchText: {
    flex: 1,
    fontSize: 16,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#2196F3',
    padding: 16,
    width: '100%',
    position: 'absolute',
    top: 0,
    left: 0,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  button: {
    backgroundColor: '#2196F3',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 4,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
  },
  input: {
    height: 40,
    width: '80%',
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 16,
    padding: 8,
  },
});