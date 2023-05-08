// Import necessary modules from React and React Native libraries
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View } from 'react-native';

// Define App function as the default export of this module
export default function App() {

  // Declare a state variable called "bikeWeather" and set its initial value to an empty array
  const [bikeWeather, setBikeWeather] = useState([]);

  // Define a side effect to fetch weather data from a remote server when the component mounts
  useEffect(() => {
    fetch('http://10.0.2.2:5000/forecast')  // Send a GET request to the server
      .then(response => response.json())   // Convert the response to JSON format
      .then(data => setBikeWeather(data.okay_to_bike))  // Update the bikeWeather state variable with the received data
      .catch(error => console.error(error));  // Handle any errors that may occur
  }, []);  // The empty dependency array means that this side effect will only run once when the component mounts

  // Render the user interface of the app using JSX
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Fietsweer voor de komende 3 dagen:</Text>
      {/* Use the map method to render a list of weather forecast items */}
      {bikeWeather.map(day => (
        <View key={day.date} style={styles.day}>
          <Text>{day.date}</Text>
          {/* Choose a text style based on whether biking is recommended */}
          <Text style={day.bike_okay ? styles.good : styles.bad}>
            {/* Display a message based on whether biking is recommended */}
            {day.bike_okay ? 'Goed fietsweer!' : 'Niet geschikt om te fietsen.'}
          </Text>
        </View>
      ))}
    </View>
  );
}

// Define a stylesheet for the app using the StyleSheet module
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  day: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    width: '80%',
    marginVertical: 10,
    padding: 10,
    backgroundColor: '#eee',
    borderRadius: 10,
  },
  good: {
    color: 'green',
  },
  bad: {
    color: 'red',
  },
});