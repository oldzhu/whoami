'use client';
import { useState } from 'react';

export function NavLinks() {
  const [loggedIn] = useState(() => {
    if (typeof window !== 'undefined') return !!sessionStorage.getItem('token');
    return false;
  });

  if (!loggedIn) return null;

  return <a href="/settings">Settings</a>;
}
