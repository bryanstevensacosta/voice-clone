/**
 * Generation Entity - Store
 *
 * Zustand store for generation state management.
 */

import { create } from 'zustand';
import { GenerationResult } from './types';

interface GenerationState {
  history: GenerationResult[];
  current: GenerationResult | null;
  loading: boolean;
  error: string | null;

  // Actions
  setHistory: (history: GenerationResult[]) => void;
  setCurrent: (generation: GenerationResult | null) => void;
  addToHistory: (generation: GenerationResult) => void;
  deleteFromHistory: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useGenerationStore = create<GenerationState>((set) => ({
  history: [],
  current: null,
  loading: false,
  error: null,

  setHistory: (history) => set({ history }),
  setCurrent: (generation) => set({ current: generation }),
  addToHistory: (generation) =>
    set((state) => ({
      history: [generation, ...state.history],
    })),
  deleteFromHistory: (id) =>
    set((state) => ({
      history: state.history.filter((g) => g.id !== id),
    })),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));
