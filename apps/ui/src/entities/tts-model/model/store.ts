/**
 * TTS Model Entity - Store
 *
 * Zustand store for TTS model state management.
 */

import { create } from 'zustand';
import { InstalledModel, AvailableModel, DownloadProgress } from './types';

interface ModelState {
  installed: InstalledModel[];
  available: AvailableModel[];
  downloading: DownloadProgress | null;
  loading: boolean;
  error: string | null;

  // Actions
  setInstalled: (models: InstalledModel[]) => void;
  setAvailable: (models: AvailableModel[]) => void;
  setDownloading: (progress: DownloadProgress | null) => void;
  addInstalled: (model: InstalledModel) => void;
  removeInstalled: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useModelStore = create<ModelState>((set) => ({
  installed: [],
  available: [],
  downloading: null,
  loading: false,
  error: null,

  setInstalled: (models) => set({ installed: models }),
  setAvailable: (models) => set({ available: models }),
  setDownloading: (progress) => set({ downloading: progress }),
  addInstalled: (model) =>
    set((state) => ({
      installed: [...state.installed, model],
    })),
  removeInstalled: (id) =>
    set((state) => ({
      installed: state.installed.filter((m) => m.id !== id),
    })),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));
