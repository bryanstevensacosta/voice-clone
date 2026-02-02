/**
 * App Entity - Store
 *
 * Zustand store for application state management.
 */

import { create } from 'zustand';
import { SystemInfo, Theme } from './types';

interface AppState {
  // UI State
  theme: Theme;
  sidebarOpen: boolean;

  // System State
  systemInfo: SystemInfo | null;
  pythonReady: boolean;

  // Actions
  setTheme: (theme: Theme) => void;
  toggleSidebar: () => void;
  setSystemInfo: (info: SystemInfo) => void;
  setPythonReady: (ready: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  theme: 'light',
  sidebarOpen: true,
  systemInfo: null,
  pythonReady: false,

  setTheme: (theme) => set({ theme }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSystemInfo: (info) => set({ systemInfo: info }),
  setPythonReady: (ready) => set({ pythonReady: ready }),
}));
