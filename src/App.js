import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatMessagesRef = useRef(null); // Create a ref for the chat messages container
  const inputRef = useRef(null); // Create a ref for the textarea

  const handleSend = () => {
    if (input.trim()) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'user', text: input }
      ]);
      setInput('');

      // Simulate chatbot response
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', text: `You said: "${input}"` },
        ]);
      }, 500);
    }

    // Reset the cursor position to the start after sending the message
    if (inputRef.current) {
      inputRef.current.setSelectionRange(0, 0); // Move cursor to the start
      inputRef.current.focus(); // Focus the textarea (to ensure the cursor stays active)
    }

    // Reset textarea height to its initial size (e.g., 40px)
    if (inputRef.current) {
      inputRef.current.style.height = '40px'; // Set to the initial height
    }
  };

  const handleInput = (e) => {
    const textarea = e.target;
  
    // Réinitialiser la hauteur avant de calculer la nouvelle hauteur
    textarea.style.height = '40px';

    console.log(textarea.scrollHeight);
  
    // Ajuster la hauteur en fonction du contenu
    if (textarea.scrollHeight > 40) {
      // Si le scrollHeight dépasse 40px, on l'ajuste en fonction du contenu, sans dépasser 100px
      textarea.style.height = `${Math.min(textarea.scrollHeight, 100)}px`;
    }
  
    // Si la hauteur dépasse 100px, activer le défilement
    if (textarea.scrollHeight > 100) {
      textarea.style.overflowY = 'auto';
    } else {
      textarea.style.overflowY = 'hidden';
    }
  
    // Mettre à jour l'état du texte
    setInput(e.target.value);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      if (!e.shiftKey) {
        // Si Enter est pressé sans Shift, envoyer le message
        e.preventDefault(); // Empêcher la nouvelle ligne
        handleSend();
      }
      // Si Shift est pressé avec Enter, permettre un saut de ligne
    }
  };

  // Auto-scroll to the bottom with smooth scrolling whenever the messages change
  useEffect(() => {
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTo({
        top: chatMessagesRef.current.scrollHeight,
        behavior: 'smooth', // Enables smooth scrolling
      });
    }
  }, [messages]); // Trigger this effect when messages state changes

  return (
    <div className="App">
      <header className="App-header">
        <div className="chat-container">
          <div className="chat-messages" ref={chatMessagesRef}>
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender}`}>
                {msg.text.split('\n').map((part, i) => (
                  <React.Fragment key={i}>
                    {part}
                    {i < msg.text.split('\n').length - 1 && <br />}
                  </React.Fragment>
                ))}
              </div>
            ))}
          </div>
          <div className="chat-input">
            <textarea
              ref={inputRef} // Add the ref to the textarea
              value={input}
              onChange={handleInput}
              onKeyDown={handleKeyDown}
              placeholder="Type a message..."
              className="chat-input-field"
            />
            <button onClick={handleSend} className="send-button">
              <span className="material-icons">arrow_upward</span>
            </button>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
