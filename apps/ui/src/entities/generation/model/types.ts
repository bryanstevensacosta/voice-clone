/**
 * Generation Entity - Types
 *
 * TypeScript types for audio generation entity.
 */

export interface GenerationRequest {
  profile_id: string;
  text: string;
  temperature: number;
  speed: number;
  mode: 'clone' | 'custom' | 'design';
}

export interface GenerationResult {
  id: string;
  profile_id: string;
  text: string;
  output_path: string;
  duration: number;
  created_at: string;
  parameters: {
    temperature: number;
    speed: number;
    mode: string;
  };
}

export interface BatchRequest {
  profile_id: string;
  script_path: string;
}
