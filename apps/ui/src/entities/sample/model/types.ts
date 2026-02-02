/**
 * Sample Entity - Types
 *
 * TypeScript types for audio sample entity.
 */

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

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}
