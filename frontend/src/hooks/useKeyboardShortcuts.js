import { useEffect } from 'react';

/**
 * Keyboard shortcuts hook for Saarthi AI.
 * @param {Object} handlers - Map of shortcut names to handler functions.
 *   Supported: onNewChat, onSearch, onEscape
 */
export function useKeyboardShortcuts({ onNewChat, onSearch, onEscape }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl+Shift+N → New conversation
      if (e.ctrlKey && e.shiftKey && e.key === 'N') {
        e.preventDefault();
        onNewChat?.();
      }

      // Ctrl+/ → Focus search
      if (e.ctrlKey && e.key === '/') {
        e.preventDefault();
        onSearch?.();
      }

      // Escape → Close modals/drawers
      if (e.key === 'Escape') {
        onEscape?.();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onNewChat, onSearch, onEscape]);
}
