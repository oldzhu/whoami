export interface PersonalProfile {
  name: string;
  title: string;
  summary: string;
  skills: string[];
  projects: Project[];
  experience: Experience[];
  education: Education[];
}

export interface Project {
  name: string;
  description: string;
  technologies: string[];
  url?: string;
  start_date?: string;
  end_date?: string;
}

export interface Experience {
  company: string;
  role: string;
  description: string;
  start_date: string;
  end_date?: string;
}

export interface Education {
  institution: string;
  degree: string;
  field: string;
  year: number;
}

export interface Skill {
  name: string;
  category: string;
  level: number;
}
