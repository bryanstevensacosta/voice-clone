/**
 * App Layer - Application initialization
 *
 * This is the entry point for the application.
 * It sets up providers, routing, and global configuration.
 */

import { FC } from 'react';

const App: FC = () => {
  return (
    <div className="app">
      <h1>TTS Studio</h1>
      <p>Desktop application for voice cloning and text-to-speech synthesis</p>
    </div>
  );
};

export default App;
