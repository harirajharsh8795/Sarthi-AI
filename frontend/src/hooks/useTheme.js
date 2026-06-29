import { useState, useEffect } from 'react';

/**
 * Theme persistence hook for Saarthi AI.
 * Manages dark/light theme state and syncs with localStorage + DOM.
 */
export function useTheme() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('saarthi_theme') || 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('saarthi_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const isDark = theme === 'dark';

  return { theme, toggleTheme, isDark };
}
