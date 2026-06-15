import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';

export default function VoiceScreen() {
  const handlePress = () => {
    Alert.alert('Voice', 'Voice conversation coming soon');
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.micButton} onPress={handlePress} activeOpacity={0.7}>
        <Text style={styles.micIcon}>🎤</Text>
      </TouchableOpacity>
      <Text style={styles.label}>Voice conversation coming soon</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    justifyContent: 'center',
    alignItems: 'center',
  },
  micButton: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#3b82f6',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 8,
  },
  micIcon: {
    fontSize: 48,
  },
  label: {
    fontSize: 16,
    color: '#666',
  },
});
