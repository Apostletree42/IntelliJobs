import React, { useState, useEffect, useRef } from 'react';
import crudServices from '../services/crud';
import ReactMarkdown from 'react-markdown';
import './ChatBox.css'; // Import the CSS file

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
    <div className="chat-container">
      <div className="chat-box">
        <h2 className="chat-title">Intellijobs</h2>
        <div className="chat-messages" ref={viewport}>
          {messages.map((message, index) => (
            <div
              key={index}
              className={`chat-message ${message.sender === 'user' ? 'chat-message-user' : 'chat-message-bot'}`}
            >
              <div className="chat-message-content">
                <ReactMarkdown>
                  {message.text}
                </ReactMarkdown>
              </div>
            </div>
          ))}
        </div>
        <div className="chat-input-container">
          <input
            className="chat-input"
            placeholder="Type your message..."
            value={input}
            onChange={(event) => setInput(event.currentTarget.value)}
            onKeyPress={(event) => {
              if (event.key === 'Enter') {
                handleSend();
              }
            }}
          />
          <button className="chat-send-button" onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
