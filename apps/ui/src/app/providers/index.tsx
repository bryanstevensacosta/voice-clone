/**
 * App Providers
 *
 * Global providers that wrap the entire application.
 * Includes Router, State Management, Theme, etc.
 */

import { FC, ReactNode } from 'react';

interface ProvidersProps {
  children: ReactNode;
}

export const Providers: FC<ProvidersProps> = ({ children }) => {
  // Providers will be added in Phase 1.4 (Router, Zustand, Theme)
  return <>{children}</>;
};
