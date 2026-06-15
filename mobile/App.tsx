import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Text } from 'react-native';
import ChatScreen from './screens/ChatScreen';
import VoiceScreen from './screens/VoiceScreen';
import ProfileScreen from './screens/ProfileScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Chat" component={ChatScreen} options={{tabBarIcon:()=><Text>💬</Text>}} />
        <Tab.Screen name="Voice" component={VoiceScreen} options={{tabBarIcon:()=><Text>🎤</Text>}} />
        <Tab.Screen name="Profile" component={ProfileScreen} options={{tabBarIcon:()=><Text>👤</Text>}} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
