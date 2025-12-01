const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const messagesContainer = document.getElementById('messagesContainer');
const welcomeScreen = document.getElementById('welcomeScreen');
const chatMessages = document.getElementById('chatMessages');

// Auto-resize textarea
chatInput.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Enter to send
chatInput.addEventListener('keydown', function(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Send button click
sendButton.addEventListener('click', sendMessage);

function hideWelcome() {
  if (welcomeScreen.style.display !== 'none') {
    welcomeScreen.style.display = 'none';
    messagesContainer.style.display = 'block';
  }
}

function formatBotResponse(text) {
  // Menghilangkan markdown heading dengan ### dan menggantinya dengan HTML heading
  text = text.replace(/###\s*(.+)/g, '<h3>$1</h3>');
  
  // Menghilangkan ** untuk bold dan menggantinya dengan <strong>
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  
  // Menghilangkan * untuk italic dan menggantinya dengan <em>
  text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
  
  // Wrap consecutive <li> tags in <ul>
  text = text.replace(/(<li>.*<\/li>\s*)+/g, function(match) {
    return '<ul>' + match + '</ul>';
  });
  
  // Format untuk numbered list
  text = text.replace(/^\s*\d+\.\s+(.+)/gm, '<li>$1</li>');
  
  // Wrap numbered lists in <ol>
  const lines = text.split('\n');
  let inOrderedList = false;
  let formattedLines = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    if (line.trim().match(/^\d+\.\s+/)) {
      if (!inOrderedList) {
        formattedLines.push('<ol>');
        inOrderedList = true;
      }
      formattedLines.push(line.replace(/^\s*\d+\.\s+(.+)/, '<li>$1</li>'));
    } else {
      if (inOrderedList) {
        formattedLines.push('</ol>');
        inOrderedList = false;
      }
      formattedLines.push(line);
    }
  }
  
  if (inOrderedList) {
    formattedLines.push('</ol>');
  }
  
  text = formattedLines.join('\n');
  
  // Format paragraphs
  text = text.replace(/\n\n/g, '</p><p>');
  
  // Wrap in paragraph if not already wrapped
  if (!text.startsWith('<h3>') && !text.startsWith('<ul>') && !text.startsWith('<ol>')) {
    text = '<p>' + text + '</p>';
  }
  
  // Clean up empty paragraphs
  text = text.replace(/<p>\s*<\/p>/g, '');
  
  // Replace single newlines with <br>
  text = text.replace(/\n/g, '<br>');
  
  return text;
}

function addMessage(type, text) {
  hideWelcome();
  
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}`;
  
  if (type === 'bot') {
    const avatar = document.createElement('div');
    avatar.className = 'bot-avatar';
    avatar.innerHTML = `
      <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
        <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    `;
    messageDiv.appendChild(avatar);
  }
  
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  
  if (type === 'bot') {
    // Format bot response untuk menghilangkan markdown
    bubble.innerHTML = formatBotResponse(text);
  } else {
    // User message tetap simple
    bubble.innerHTML = text.replace(/\n/g, '<br>');
  }
  
  messageDiv.appendChild(bubble);
  messagesContainer.appendChild(messageDiv);
  
  chatMessages.scrollTop = chatMessages.scrollHeight;
  
  return bubble;
}

function addTypingIndicator() {
  hideWelcome();
  
  const messageDiv = document.createElement('div');
  messageDiv.className = 'message bot';
  messageDiv.id = 'typingIndicator';
  
  const avatar = document.createElement('div');
  avatar.className = 'bot-avatar';
  avatar.innerHTML = `
    <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
      <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `;
  messageDiv.appendChild(avatar);
  
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  bubble.innerHTML = '<div class="typing-indicator"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>';
  
  messageDiv.appendChild(bubble);
  messagesContainer.appendChild(messageDiv);
  
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
  const indicator = document.getElementById('typingIndicator');
  if (indicator) {
    indicator.remove();
  }
}

async function typeText(element, html) {
  // Untuk efek typing yang lebih smooth dengan HTML formatting
  element.innerHTML = '';
  
  // Create a temporary div to parse HTML
  const temp = document.createElement('div');
  temp.innerHTML = html;
  
  // Get the text content to type
  const textContent = temp.textContent || temp.innerText;
  const words = textContent.split(' ');
  
  // Type each word
  for (let i = 0; i < words.length; i++) {
    element.textContent += (i > 0 ? ' ' : '') + words[i];
    chatMessages.scrollTop = chatMessages.scrollHeight;
    await new Promise(resolve => setTimeout(resolve, 30));
  }
  
  // Finally set the full HTML content
  element.innerHTML = html;
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
  const question = chatInput.value.trim();
  if (!question) return;

  sendButton.disabled = true;
  addMessage('user', question);
  chatInput.value = '';
  chatInput.style.height = 'auto';
  
  addTypingIndicator();

  try {
    const response = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question })
    });

    const data = await response.json();
    removeTypingIndicator();
    
    // Format the answer untuk menghilangkan markdown
    const formattedAnswer = formatBotResponse(data.answer);
    
    const botBubble = addMessage('bot', data.answer);
    
  } catch (error) {
    removeTypingIndicator();
    addMessage('bot', '⚠️ Maaf, terjadi kesalahan. Pastikan server berjalan di http://localhost:8000');
  } finally {
    sendButton.disabled = false;
    chatInput.focus();
  }
}

// Focus input on load
window.addEventListener('load', () => {
  chatInput.focus();
});