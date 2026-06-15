'use client';
import { useEffect, useState } from "react";

interface Profile {
  name: string; title: string; summary: string;
  skills: Array<{name: string; category: string; level: number}>;
  projects: Array<{name: string; description: string; technologies: string[]}>;
  experience: Array<{company: string; role: string; description: string; start_date: string}>;
  education: Array<{institution: string; degree: string; field: string; year: number}>;
}

function SkillBar({ name, level }: { name: string; level: number }) {
  return (
    <div className="mb-2">
      <span className="text-sm font-medium">{name}</span>
      <div className="w-full bg-gray-200 rounded h-2 mt-1">
        <div className="bg-blue-600 h-2 rounded" style={{width: `${(level/5)*100}%`}} />
      </div>
    </div>
  );
}

export default function Home() {
  const [profile, setProfile] = useState<Profile | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/profile")
      .then(r => r.json()).then(setProfile)
      .catch(() => setProfile({
        name: "数字分身", title: "AI Digital Twin",
        summary: "Loading profile...", skills: [], projects: [], experience: [], education: []
      }));
  }, []);

  if (!profile) return <div className="text-center py-20">Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto">
      <div className="text-center py-12">
        <div className="w-32 h-32 bg-blue-100 rounded-full mx-auto mb-4 flex items-center justify-center">
          <span className="text-4xl">🤖</span>
        </div>
        <h1 className="text-4xl font-bold mb-2">{profile.name}</h1>
        <p className="text-xl text-gray-600 mb-4">{profile.title}</p>
        <p className="text-gray-500 max-w-xl mx-auto">{profile.summary}</p>
        <a href="/chat" className="inline-block mt-6 bg-blue-600 text-white px-8 py-3 rounded-lg text-lg hover:bg-blue-700 transition">
          与数字分身对话 → / Chat with Digital Twin →
        </a>
      </div>

      <section className="mb-8">
        <h2 className="text-2xl font-bold mb-4">技能 / Skills</h2>
        <div className="bg-white rounded-lg shadow p-6">
          {profile.skills.map((s, i) => <SkillBar key={i} name={s.name} level={s.level} />)}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-bold mb-4">项目 / Projects</h2>
        {profile.projects.map((p, i) => (
          <div key={i} className="bg-white rounded-lg shadow p-6 mb-4">
            <h3 className="text-lg font-semibold">{p.name}</h3>
            <p className="text-gray-600 mt-1">{p.description}</p>
            <div className="flex flex-wrap gap-2 mt-3">
              {p.technologies.map(t => <span key={t} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">{t}</span>)}
            </div>
          </div>
        ))}
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-bold mb-4">经历 / Experience</h2>
        {profile.experience.map((e, i) => (
          <div key={i} className="bg-white rounded-lg shadow p-6 mb-3">
            <div className="flex justify-between">
              <h3 className="font-semibold">{e.role} @ {e.company}</h3>
              <span className="text-gray-500 text-sm">{e.start_date}</span>
            </div>
            <p className="text-gray-600 mt-1">{e.description}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
