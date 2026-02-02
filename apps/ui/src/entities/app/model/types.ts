/**
 * App Entity - Types
 *
 * TypeScript types for application state.
 */

export interface SystemInfo {
  os: string;
  platform: string;
  arch: string;
  python_version: string;
  device: 'cpu' | 'mps' | 'cuda';
}

export type Theme = 'light' | 'dark';
