/**
 * Profile Entity - Store
 *
 * Zustand store for profile state management.
 */

import { create } from 'zustand';
import { VoiceProfile } from './types';

interface ProfileState {
  profiles: VoiceProfile[];
  selectedProfile: VoiceProfile | null;
  loading: boolean;
  error: string | null;

  // Actions
  setProfiles: (profiles: VoiceProfile[]) => void;
  selectProfile: (profile: VoiceProfile | null) => void;
  addProfile: (profile: VoiceProfile) => void;
  updateProfile: (id: string, updates: Partial<VoiceProfile>) => void;
  deleteProfile: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useProfileStore = create<ProfileState>((set) => ({
  profiles: [],
  selectedProfile: null,
  loading: false,
  error: null,

  setProfiles: (profiles) => set({ profiles }),
  selectProfile: (profile) => set({ selectedProfile: profile }),
  addProfile: (profile) =>
    set((state) => ({
      profiles: [...state.profiles, profile],
    })),
  updateProfile: (id, updates) =>
    set((state) => ({
      profiles: state.profiles.map((p) =>
        p.id === id ? { ...p, ...updates } : p
      ),
    })),
  deleteProfile: (id) =>
    set((state) => ({
      profiles: state.profiles.filter((p) => p.id !== id),
      selectedProfile:
        state.selectedProfile?.id === id ? null : state.selectedProfile,
    })),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));
