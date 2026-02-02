/**
 * TTS Model Entity - Types
 *
 * TypeScript types for TTS model entity.
 */

export interface InstalledModel {
  id: string;
  name: string;
  author: string;
  version: string;
  size_bytes: number;
  install_path: string;
  installed_at: string;
  last_used_at?: string;
  use_count: number;
}

export interface AvailableModel {
  id: string;
  name: string;
  author: string;
  version: string;
  size_bytes: number;
  description: string;
  languages: string[];
}

export interface DownloadProgress {
  model_id: string;
  progress: number;
  downloaded_bytes: number;
  total_bytes: number;
  speed_mbps: number;
  eta_seconds: number;
}
