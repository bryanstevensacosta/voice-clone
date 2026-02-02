/**
 * Application Constants
 *
 * Shared constants used across the application.
 */

export const APP_NAME = 'TTS Studio';
export const APP_VERSION = '0.1.0';

export const AUDIO_FORMATS = ['wav', 'mp3', 'aac'] as const;
export const SAMPLE_RATE = 12000;

export const ROUTES = {
  HOME: '/',
  PROFILES: '/profiles',
  GENERATE: '/generate',
  BATCH: '/batch',
  MODELS: '/models',
  SETTINGS: '/settings',
} as const;
