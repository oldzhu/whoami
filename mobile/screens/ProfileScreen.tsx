import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet, ActivityIndicator } from 'react-native';
import { apiGet } from '../lib/api-client';

interface Profile {
  name: string;
  title: string;
  summary: string;
  skills: Array<{name: string; category: string; level: number}>;
  projects: Array<{name: string; description: string; technologies: string[]}>;
  experience: Array<{company: string; role: string; description: string; start_date: string}>;
  education: Array<{institution: string; degree: string; field: string; year: number}>;
}

const fallbackProfile: Profile = {
  name: '数字分身',
  title: 'AI Digital Twin',
  summary: 'Loading profile...',
  skills: [],
  projects: [],
  experience: [],
  education: [],
};

export default function ProfileScreen() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet('/api/profile')
      .then(setProfile)
      .catch(() => setProfile(fallbackProfile))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#3b82f6" />
      </View>
    );
  }

  if (!profile) return null;

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>🤖</Text>
        </View>
        <Text style={styles.name}>{profile.name}</Text>
        <Text style={styles.title}>{profile.title}</Text>
        <Text style={styles.summary}>{profile.summary}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Skills</Text>
        {profile.skills.map((s, i) => (
          <View key={i} style={styles.skillRow}>
            <Text style={styles.skillName}>{s.name}</Text>
            <View style={styles.skillBarBg}>
              <View style={[styles.skillBarFill, {width: `${(s.level/5)*100}%`}]} />
            </View>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Projects</Text>
        {profile.projects.map((p, i) => (
          <View key={i} style={styles.card}>
            <Text style={styles.cardTitle}>{p.name}</Text>
            <Text style={styles.cardDesc}>{p.description}</Text>
            <Text style={styles.tech}>{p.technologies.join(', ')}</Text>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Experience</Text>
        {profile.experience.map((e, i) => (
          <View key={i} style={styles.card}>
            <Text style={styles.cardTitle}>{e.role}</Text>
            <Text style={styles.cardSubtitle}>{e.company}</Text>
            <Text style={styles.cardDesc}>{e.description}</Text>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Education</Text>
        {profile.education.map((e, i) => (
          <View key={i} style={styles.card}>
            <Text style={styles.cardTitle}>{e.degree} in {e.field}</Text>
            <Text style={styles.cardSubtitle}>{e.institution} — {e.year}</Text>
          </View>
        ))}
      </View>

      <View style={{height: 40}} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {flex:1, backgroundColor:'#f5f5f5'},
  centered: {flex:1, justifyContent:'center', alignItems:'center'},
  header: {alignItems:'center', paddingVertical:40, paddingHorizontal:20},
  avatar: {width:100, height:100, borderRadius:50, backgroundColor:'#dbeafe', justifyContent:'center', alignItems:'center', marginBottom:16},
  avatarText: {fontSize:48},
  name: {fontSize:28, fontWeight:'bold', marginBottom:4},
  title: {fontSize:18, color:'#666', marginBottom:8},
  summary: {fontSize:14, color:'#999', textAlign:'center'},
  section: {paddingHorizontal:20, marginBottom:24},
  sectionTitle: {fontSize:20, fontWeight:'bold', marginBottom:12},
  skillRow: {marginBottom:10},
  skillName: {fontSize:14, fontWeight:'500', marginBottom:4},
  skillBarBg: {height:8, backgroundColor:'#e5e7eb', borderRadius:4, overflow:'hidden'},
  skillBarFill: {height:8, backgroundColor:'#3b82f6', borderRadius:4},
  card: {backgroundColor:'#fff', borderRadius:8, padding:16, marginBottom:10, shadowColor:'#000', shadowOffset:{width:0,height:1}, shadowOpacity:0.05, shadowRadius:2, elevation:2},
  cardTitle: {fontSize:16, fontWeight:'600', marginBottom:4},
  cardSubtitle: {fontSize:14, color:'#666', marginBottom:4},
  cardDesc: {fontSize:14, color:'#333', lineHeight:20},
  tech: {fontSize:12, color:'#3b82f6', marginTop:8},
});
