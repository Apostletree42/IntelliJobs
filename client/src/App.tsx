import React from 'react';
import { MantineProvider } from '@mantine/core';
import ChatBox from './components/ChatBox';


function App() {
  return (
    <MantineProvider>
      <ChatBox />
    </MantineProvider>
  );
}

export default App;