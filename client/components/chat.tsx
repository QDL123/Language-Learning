import React, { useState, useEffect } from 'react';

export interface Message {
  sender: 'agent' | 'user';
  text?: string;
}

interface IncomingMessages {
    messages: Message[];
}

const ChatComponent = ({ messages }: IncomingMessages) => {

  return (
    <div>
      {messages.map((message, index) => (
        <div key={index}>
            <p>{message.sender}: {message.text}</p>
        </div>
      ))}
    </div>
  );
};

export default ChatComponent;