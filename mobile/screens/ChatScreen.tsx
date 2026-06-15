import React, { useState, useRef } from 'react';
import { View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet } from 'react-native';

const API_BASE = 'http://10.0.2.2:8000';

export default function ChatScreen() {
  const [messages, setMessages] = useState<Array<{role:string;content:string}>>([]);
  const [input, setInput] = useState('');
  const flatListRef = useRef<FlatList>(null);

  const send = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user', content: input.trim() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({message: userMsg.content}),
      });
      const data = await res.json();
      setMessages(prev => [...prev, {role:'assistant', content: data.response}]);
    } catch(e) {
      setMessages(prev => [...prev, {role:'assistant', content: 'Connection error'}]);
    }
  };

  return (
    <View style={styles.container}>
      <FlatList ref={flatListRef} data={messages}
        renderItem={({item}) => <Text style={item.role==='user'?styles.userMsg:styles.aiMsg}>{item.content}</Text>}
        keyExtractor={(_,i)=>String(i)}
        onContentSizeChange={()=>flatListRef.current?.scrollToEnd()}
      />
      <View style={styles.inputRow}>
        <TextInput style={styles.input} value={input} onChangeText={setInput} placeholder="Message..." />
        <TouchableOpacity onPress={send} style={styles.sendBtn}><Text style={{color:'#fff'}}>Send</Text></TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex:1, backgroundColor:'#f5f5f5'},
  userMsg: {alignSelf:'flex-end', backgroundColor:'#3b82f6', color:'#fff', padding:10, margin:5, borderRadius:8, maxWidth:'70%', overflow:'hidden'},
  aiMsg: {alignSelf:'flex-start', backgroundColor:'#fff', padding:10, margin:5, borderRadius:8, maxWidth:'70%', overflow:'hidden'},
  inputRow: {flexDirection:'row', padding:10, backgroundColor:'#fff'},
  input: {flex:1, borderWidth:1, borderColor:'#ddd', borderRadius:8, padding:10, marginRight:10},
  sendBtn: {backgroundColor:'#3b82f6', padding:15, borderRadius:8},
});
