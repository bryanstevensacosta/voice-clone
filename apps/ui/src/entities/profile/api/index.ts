/**
 * Profile Entity - API
 *
 * Tauri commands for profile operations.
 * Will be implemented in Phase 2 (Python Bridge).
 */

import { VoiceProfile, CreateProfileData } from '../model/types';

export const profileAPI = {
  async list(): Promise<VoiceProfile[]> {
    // TODO: Implement in Phase 2
    // return invoke<VoiceProfile[]>('list_voice_profiles');
    return [];
  },

  async create(_data: CreateProfileData): Promise<VoiceProfile> {
    // TODO: Implement in Phase 2
    // return invoke<VoiceProfile>('create_voice_profile', data);
    throw new Error('Not implemented');
  },

  async delete(_id: string): Promise<boolean> {
    // TODO: Implement in Phase 2
    // return invoke<boolean>('delete_voice_profile', { profileId: id });
    throw new Error('Not implemented');
  },
};
