import React, { useState, useEffect, useRef } from 'react';
import { Box, TextInput, Button, Paper, Text, ScrollArea, Title } from '@mantine/core';
import crudServices from '../services/crud';
import ReactMarkdown from 'react-markdown';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const viewport = useRef<HTMLDivElement>(null);

  const handleSend = () => {
    if (input.trim()) {
      const userMessage: Message = { text: input, sender: 'user' };
      setMessages([...messages, userMessage]);
      setInput('');

      // Send the user's message to the server
      crudServices
        .postMessage(userMessage)
        .then(responseMessage => {
            console.log(responseMessage);
            setMessages(prev => [...prev, { text: responseMessage.text, sender: 'bot' }]);
        })
        .catch(err => {
          console.error('Error getting response:', err);
        });
    }
  };

  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <Box style={{ maxWidth: 500, margin: 'auto', marginTop: 20, display: 'flex', flexDirection: 'column', height: '80vh' }}>
      <Paper p="md" shadow="xs" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Title size="xl" mb="md" order={2}>Intellijobs</Title>
        <ScrollArea style={{ flex: 1 }} viewportRef={viewport}>
          <Box style={{ paddingBottom: 60 }}> {/* Extra padding to prevent overlap */}
            {messages.map((message, index) => (
              <Box
                key={index}
                style={{
                  marginBottom: 10,
                  textAlign: message.sender === 'user' ? 'right' : 'left',
                }}
              >
                <Text
                  size="sm"
                  p="xs"
                  style={{
                    display: 'inline-block',
                    backgroundColor: message.sender === 'user' ? '#e3f2fd' : '#f5f5f5',
                    borderRadius: 5,
                    maxWidth: '70%',
                  }}
                >
                    <ReactMarkdown>
                        {message.text}
                    </ReactMarkdown>
                </Text>
              </Box>
            ))}
          </Box>
        </ScrollArea>
        <Box style={{ display: 'flex', marginTop: 'auto' }}> {/* Flex to push input area to the bottom */}
          <TextInput
            placeholder="Type your message..."
            value={input}
            onChange={(event) => setInput(event.currentTarget.value)}
            onKeyPress={(event) => {
              if (event.key === 'Enter') {
                handleSend();
              }
            }}
            style={{ flex: 1 }}
          />
          <Button onClick={handleSend} style={{ marginLeft: 10 }}>Send</Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default ChatBox;
