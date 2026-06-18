'use client';
import { useState, useEffect, useRef, Suspense } from 'react';
import { useRouter } from 'next/navigation';
import { useI18n } from '@/lib/i18n';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

function getToken() {
  if (typeof window === 'undefined') return '';
  return sessionStorage.getItem('token') || '';
}

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${getToken()}`,
  };
}

type Tab = 'profile' | 'documents' | 'voice' | 'password';

interface ProfileData {
  name: string;
  title: string;
  summary: string;
  skills: { name: string; category: string; level: number }[];
  projects: { name: string; description: string; technologies: string[] }[];
  experience: { company: string; role: string; description: string; start_date: string }[];
  education: { institution: string; degree: string; field: string; year: number }[];
}

function ProfileTab() {
  const { t } = useI18n();
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/api/profile`)
      .then(r => r.json())
      .then(setProfile);
  }, []);

  const handleSave = async () => {
    if (!profile) return;
    const res = await fetch(`${API_BASE}/api/profile`, {
      method: 'PUT',
      headers: authHeaders(),
      body: JSON.stringify(profile),
    });
    if (res.ok) setSaved(true);
  };

  const updateField = (field: keyof ProfileData, value: unknown) => {
    setProfile(prev => prev ? { ...prev, [field]: value } : prev);
    setSaved(false);
  };

  const addSkill = () => {
    setProfile(prev =>
      prev ? { ...prev, skills: [...prev.skills, { name: '', category: '', level: 3 }] } : prev
    );
    setSaved(false);
  };

  const updateSkill = (i: number, field: string, value: string | number) => {
    setProfile(prev => {
      if (!prev) return prev;
      const skills = [...prev.skills];
      skills[i] = { ...skills[i], [field]: value };
      return { ...prev, skills };
    });
    setSaved(false);
  };

  const removeSkill = (i: number) => {
    setProfile(prev => prev ? { ...prev, skills: prev.skills.filter((_, j) => j !== i) } : prev);
    setSaved(false);
  };

  const addProject = () => {
    setProfile(prev =>
      prev
        ? { ...prev, projects: [...prev.projects, { name: '', description: '', technologies: [] }] }
        : prev
    );
    setSaved(false);
  };

  const updateProject = (i: number, field: string, value: unknown) => {
    setProfile(prev => {
      if (!prev) return prev;
      const projects = [...prev.projects];
      projects[i] = { ...projects[i], [field]: value };
      return { ...prev, projects };
    });
    setSaved(false);
  };

  const addExperience = () => {
    setProfile(prev =>
      prev
        ? {
            ...prev,
            experience: [...prev.experience, { company: '', role: '', description: '', start_date: '' }],
          }
        : prev
    );
    setSaved(false);
  };

  const updateExperience = (i: number, field: string, value: string) => {
    setProfile(prev => {
      if (!prev) return prev;
      const experience = [...prev.experience];
      experience[i] = { ...experience[i], [field]: value };
      return { ...prev, experience };
    });
    setSaved(false);
  };

  const addEducation = () => {
    setProfile(prev =>
      prev
        ? { ...prev, education: [...prev.education, { institution: '', degree: '', field: '', year: 2020 }] }
        : prev
    );
    setSaved(false);
  };

  const updateEducation = (i: number, field: string, value: string | number) => {
    setProfile(prev => {
      if (!prev) return prev;
      const education = [...prev.education];
      education[i] = { ...education[i], [field]: value };
      return { ...prev, education };
    });
    setSaved(false);
  };

  if (!profile) return <div className="text-center py-8">Loading...</div>;

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
        <input
          type="text"
          value={profile.name}
          onChange={e => updateField('name', e.target.value)}
          className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
        <input
          type="text"
          value={profile.title}
          onChange={e => updateField('title', e.target.value)}
          className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Summary</label>
        <textarea
          value={profile.summary}
          onChange={e => updateField('summary', e.target.value)}
          rows={3}
          className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold text-lg">Skills</h3>
          <button onClick={addSkill} className="text-blue-600 text-sm hover:underline">{t('settings.addSkill')}</button>
        </div>
        {profile.skills.map((s, i) => (
          <div key={i} className="flex gap-2 mb-2 items-center">
            <input
              placeholder="Name"
              value={s.name}
              onChange={e => updateSkill(i, 'name', e.target.value)}
              className="flex-1 border rounded px-2 py-1 text-sm"
            />
            <input
              placeholder="Category"
              value={s.category}
              onChange={e => updateSkill(i, 'category', e.target.value)}
              className="w-32 border rounded px-2 py-1 text-sm"
            />
            <input
              type="number"
              min={1}
              max={5}
              value={s.level}
              onChange={e => updateSkill(i, 'level', Number(e.target.value))}
              className="w-16 border rounded px-2 py-1 text-sm"
            />
            <button onClick={() => removeSkill(i)} className="text-red-500 text-sm">&times;</button>
          </div>
        ))}
      </div>

      <div>
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold text-lg">Projects</h3>
          <button onClick={addProject} className="text-blue-600 text-sm hover:underline">{t('settings.addProject')}</button>
        </div>
        {profile.projects.map((p, i) => (
          <div key={i} className="border rounded p-3 mb-2 space-y-2">
            <input
              placeholder="Project name"
              value={p.name}
              onChange={e => updateProject(i, 'name', e.target.value)}
              className="w-full border rounded px-2 py-1 text-sm"
            />
            <textarea
              placeholder="Description"
              value={p.description}
              onChange={e => updateProject(i, 'description', e.target.value)}
              rows={2}
              className="w-full border rounded px-2 py-1 text-sm"
            />
            <input
              placeholder="Technologies (comma separated)"
              value={p.technologies.join(', ')}
              onChange={e => updateProject(i, 'technologies', e.target.value.split(',').map(s => s.trim()).filter(Boolean))}
              className="w-full border rounded px-2 py-1 text-sm"
            />
          </div>
        ))}
      </div>

      <div>
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold text-lg">Experience</h3>
          <button onClick={addExperience} className="text-blue-600 text-sm hover:underline">{t('settings.addExperience')}</button>
        </div>
        {profile.experience.map((exp, i) => (
          <div key={i} className="border rounded p-3 mb-2 space-y-2">
            <input
              placeholder="Company"
              value={exp.company}
              onChange={e => updateExperience(i, 'company', e.target.value)}
              className="w-full border rounded px-2 py-1 text-sm"
            />
            <input
              placeholder="Role"
              value={exp.role}
              onChange={e => updateExperience(i, 'role', e.target.value)}
              className="w-full border rounded px-2 py-1 text-sm"
            />
            <textarea
              placeholder="Description"
              value={exp.description}
              onChange={e => updateExperience(i, 'description', e.target.value)}
              rows={2}
              className="w-full border rounded px-2 py-1 text-sm"
            />
            <input
              placeholder="Start date"
              value={exp.start_date}
              onChange={e => updateExperience(i, 'start_date', e.target.value)}
              className="w-full border rounded px-2 py-1 text-sm"
            />
          </div>
        ))}
      </div>

      <div>
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold text-lg">Education</h3>
          <button onClick={addEducation} className="text-blue-600 text-sm hover:underline">{t('settings.addEducation')}</button>
        </div>
        {profile.education.map((edu, i) => (
          <div key={i} className="border rounded p-3 mb-2 space-y-2">
            <input
              placeholder="Institution"
              value={edu.institution}
              onChange={e => updateEducation(i, 'institution', e.target.value)}
              className="w-full border rounded px-2 py-1 text-sm"
            />
            <input
              placeholder="Degree"
              value={edu.degree}
              onChange={e => updateEducation(i, 'degree', e.target.value)}
              className="w-full border rounded px-2 py-1 text-sm"
            />
            <input
              placeholder="Field"
              value={edu.field}
              onChange={e => updateEducation(i, 'field', e.target.value)}
              className="w-full border rounded px-2 py-1 text-sm"
            />
            <input
              type="number"
              placeholder="Year"
              value={edu.year}
              onChange={e => updateEducation(i, 'year', Number(e.target.value))}
              className="w-full border rounded px-2 py-1 text-sm"
            />
          </div>
        ))}
      </div>

      <button
        onClick={handleSave}
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition font-medium"
      >
        {saved ? t('settings.saved') : t('settings.save')}
      </button>
    </div>
  );
}

function DocumentsTab() {
  const { t } = useI18n();
  const [docs, setDocs] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/api/knowledge/documents`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    })
      .then(r => r.json())
      .then(data => setDocs(data.documents || data.files || []))
      .catch(() => {});
  }, []);

  const uploadFile = async (file: File) => {
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch(`${API_BASE}/api/knowledge/upload`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${getToken()}` },
        body: formData,
      });
      if (res.ok) {
        const data = await res.json();
        const name = data.filename || file.name;
        setDocs(prev => [...prev, name]);
      }
    } catch {
      // ignore
    }
    setUploading(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const files = Array.from(e.dataTransfer.files).filter(f =>
      /\.(docx|pdf|md|txt)$/i.test(f.name)
    );
    files.forEach(uploadFile);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) Array.from(files).forEach(uploadFile);
  };

  const handleDelete = async (filename: string) => {
    try {
      await fetch(`${API_BASE}/api/knowledge/documents/${encodeURIComponent(filename)}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${getToken()}` },
      });
      setDocs(prev => prev.filter(d => {
        const name = typeof d === 'string' ? d : (d as Record<string, unknown>).name as string || String(d);
        return name !== filename;
      }));
    } catch {
      // ignore
    }
  };

  return (
    <div className="space-y-6">
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition ${
          dragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
        onDragOver={e => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        <p className="text-gray-500 mb-2">Drag & drop documents here</p>
        <p className="text-gray-400 text-sm mb-3">Supports .docx, .pdf, .md</p>
        <label className="inline-block bg-blue-600 text-white px-4 py-2 rounded-lg cursor-pointer hover:bg-blue-700 transition">
          {uploading ? t('settings.uploading') : t('settings.uploadDoc')}
          <input type="file" className="hidden" accept=".docx,.pdf,.md,.txt" multiple onChange={handleFileInput} />
        </label>
      </div>

      <div>
        <h3 className="font-semibold text-lg mb-3">Uploaded Documents</h3>
        {docs.length === 0 ? (
          <p className="text-gray-400">No documents uploaded yet</p>
        ) : (
          <ul className="space-y-2">
            {docs.map((doc, i) => (
              <li key={i} className="flex items-center justify-between bg-gray-50 rounded px-4 py-2">
                <span className="text-sm truncate">{typeof doc === 'string' ? doc : (doc as Record<string, unknown>).name as string || String(doc)}</span>
                <button
                  onClick={() => handleDelete(typeof doc === 'string' ? doc : (doc as Record<string, unknown>).name as string || String(doc))}
                  className="text-red-500 text-sm hover:underline"
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

function VoiceTab() {
  const { t } = useI18n();
  const [recording, setRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [voiceStatus, setVoiceStatus] = useState<Record<string, unknown>>({});
  const [uploadMessage, setUploadMessage] = useState('');
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/voice/status`)
      .then(r => r.json())
      .then(setVoiceStatus)
      .catch(() => {});
  }, []);

  const startRecording = async () => {
    setUploadMessage('');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      chunksRef.current = [];
      const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      recorder.ondataavailable = e => chunksRef.current.push(e.data);
      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setAudioUrl(URL.createObjectURL(blob));
        stream.getTracks().forEach(t => t.stop());
      };
      recorder.start();
      mediaRecorderRef.current = recorder;
      setRecording(true);

      setTimeout(() => {
        if (mediaRecorderRef.current?.state === 'recording') {
          stopRecording();
        }
      }, 10000);
    } catch {
      setUploadMessage('Microphone access denied');
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  };

  const uploadRecording = async () => {
    if (!audioUrl || !chunksRef.current.length) return;
    setUploadMessage('Uploading...');
    try {
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('file', blob, 'speaker_sample.webm');
      const res = await fetch(`${API_BASE}/api/voice/speaker`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${getToken()}` },
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setUploadMessage(`Registered as speaker: ${data.speaker_id}`);
        setAudioUrl(null);
        fetch(`${API_BASE}/api/voice/status`)
          .then(r => r.json())
          .then(setVoiceStatus);
      } else {
        setUploadMessage(data.detail || 'Upload failed');
      }
    } catch {
      setUploadMessage('Network error');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="font-semibold mb-2">Voice Status</h3>
        <pre className="text-xs text-gray-600 overflow-auto">
          {JSON.stringify(voiceStatus, null, 2)}
        </pre>
      </div>

      <div className="text-center">
        <button
          onClick={recording ? stopRecording : startRecording}
          className={`w-24 h-24 rounded-full text-white font-bold text-lg transition ${
            recording ? 'bg-red-500 animate-pulse' : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {recording ? t('settings.stop') : t('settings.record')}
        </button>
        <p className="text-sm text-gray-500 mt-2">
          {recording ? t('settings.recording') : t('settings.recordHint')}
        </p>
      </div>

      {audioUrl && !recording && (
        <div className="space-y-3">
          <audio controls src={audioUrl} className="w-full" />
          <button
            onClick={uploadRecording}
            className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
          >
            {t('settings.uploadSample')}
          </button>
        </div>
      )}

      {uploadMessage && (
        <div className="p-3 bg-blue-50 text-blue-700 rounded text-sm">{uploadMessage}</div>
      )}
    </div>
  );
}

function PasswordTab() {
  const { t } = useI18n();
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    setIsError(false);

    try {
      const res = await fetch(`${API_BASE}/api/auth/reset`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
      });
      const data = await res.json();
      if (res.ok) {
        setMessage(t('settings.passwordUpdated'));
        setCurrentPassword('');
        setNewPassword('');
      } else {
        setMessage(data.detail || t('settings.passwordError'));
        setIsError(true);
      }
    } catch {
      setMessage('Network error');
      setIsError(true);
    }
  };

  return (
    <div className="max-w-md">
      <form onSubmit={handleChangePassword} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">{t('settings.currentPassword')}</label>
          <input
            type="password"
            value={currentPassword}
            onChange={e => setCurrentPassword(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            minLength={4}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">{t('settings.newPassword')}</label>
          <input
            type="password"
            value={newPassword}
            onChange={e => setNewPassword(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            minLength={4}
          />
        </div>
        {message && (
          <div className={`p-3 rounded text-sm ${isError ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}`}>
            {message}
          </div>
        )}
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition font-medium"
        >
          {t('settings.updatePassword')}
        </button>
      </form>
    </div>
  );
}

export default function SettingsPage() {
  const { t } = useI18n();
  const router = useRouter();
  const [tab, setTab] = useState<Tab>('profile');
  const [hasToken] = useState(() => {
    if (typeof window !== 'undefined') return !!getToken();
    return true;
  });

  useEffect(() => {
    if (!hasToken) {
      router.push('/login');
    }
  }, [hasToken, router]);

  if (!hasToken) return null;

  const tabs: { key: Tab; label: string }[] = [
    { key: 'profile', label: t('settings.profile') },
    { key: 'documents', label: t('settings.documents') },
    { key: 'voice', label: t('settings.voice') },
    { key: 'password', label: t('settings.changePassword') },
  ];

  return (
    <Suspense fallback={<div className="max-w-2xl mx-auto py-10 text-center">Loading...</div>}>
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">{t('settings.title')}</h1>
      <div className="flex gap-1 mb-6 border-b">
        {tabs.map(tabItem => (
          <button
            key={tabItem.key}
            onClick={() => setTab(tabItem.key)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition ${
              tab === tabItem.key
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {tabItem.label}
          </button>
        ))}
      </div>
      {tab === 'profile' && <ProfileTab />}
      {tab === 'documents' && <DocumentsTab />}
      {tab === 'voice' && <VoiceTab />}
      {tab === 'password' && <PasswordTab />}
    </div>
    </Suspense>
  );
}
