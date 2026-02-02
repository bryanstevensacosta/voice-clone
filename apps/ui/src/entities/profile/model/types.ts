/**
 * Profile Entity - Types
 *
 * TypeScript types for voice profile entity.
 */

export interface VoiceProfile {
  id: string;
  name: string;
  samples: AudioSample[];
  created_at: string;
  updated_at: string;
  total_duration: number;
  language: string;
  reference_text?: string;
}

export interface AudioSample {
  id: string;
  path: string;
  duration: number;
  sample_rate: number;
  channels: number;
  bit_depth: number;
  valid: boolean;
  validation_errors?: string[];
}

export interface CreateProfileData {
  name: string;
  samplePaths: string[];
  referenceText?: string;
  language: string;
}
