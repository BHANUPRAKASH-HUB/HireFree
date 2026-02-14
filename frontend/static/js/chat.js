let currentRecipientId = null;
let currentUserEmail = null;
let currentUserId = null;
let conversations = {};
let pollingInterval = null;

document.addEventListener('DOMContentLoaded', async () => {
    if (!window.checkSession()) return;

    const user = window.getUser();
    currentUserEmail = user.email;
    currentUserId = user.id; // Ensure user object has ID, otherwise fetch /users/me/ again

    // Initial Load
    await fetchMessages();

    // Check for new conversation intent
    const urlParams = new URLSearchParams(window.location.search);
    const recipientId = urlParams.get('recipient');
    if (recipientId) {
        await startNewConversation(recipientId);
    }

    // Start Polling
    pollingInterval = setInterval(fetchMessages, 5000); // 5 seconds poll

    // Send Handler
    document.getElementById('message-form').addEventListener('submit', sendMessage);

    // Mobile Back Handler
    document.getElementById('back-to-list').addEventListener('click', () => {
        document.getElementById('chat-window').classList.add('hidden');
        document.querySelector('.w-full.md\\:w-1\\/3').classList.remove('hidden'); // Show sidebar
    });
});

async function startNewConversation(recipientId) {
    recipientId = parseInt(recipientId);
    if (conversations[recipientId]) {
        selectConversation(recipientId);
        return;
    }

    // Fetch user details if not in conversation list
    try {
        const token = window.getAccessToken();
        const res = await fetch(`/api/users/${recipientId}/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("User not found");

        const user = await res.json();

        // Create placeholder conversation
        conversations[recipientId] = {
            id: recipientId,
            email: user.email,
            messages: [],
            lastMessage: { timestamp: new Date(), content: 'Start a new conversation', sender_email: '' },
            unreadCount: 0
        };

        renderConversations();
        selectConversation(recipientId);

        // Clean URL
        window.history.replaceState({}, document.title, "/messages/");
    } catch (e) {
        console.error("Error starting chat", e);
        window.showToast("Could not find user to chat with.", 'error');
    }
}

async function fetchMessages() {
    const token = window.getAccessToken();
    try {
        const res = await fetch('/api/messages/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Failed to fetch messages");

        const data = await res.json(); // Array of messages
        groupMessages(data);
        renderConversations();

        if (currentRecipientId) {
            renderMessages(currentRecipientId);
        }
    } catch (e) {
        console.error("Chat Error", e);
    }
}

function groupMessages(messages) {
    conversations = {};
    messages.forEach(msg => {
        // Identify "Other Person"
        const isSender = msg.sender_email === currentUserEmail;
        const otherId = isSender ? msg.recipient : msg.sender;
        const otherEmail = isSender ? msg.recipient_email : msg.sender_email;

        if (!conversations[otherId]) {
            conversations[otherId] = {
                id: otherId,
                email: otherEmail,
                messages: [],
                lastMessage: null,
                unreadCount: 0
            };
        }

        conversations[otherId].messages.push(msg);
        conversations[otherId].lastMessage = msg;
        if (!isSender && !msg.is_read) {
            conversations[otherId].unreadCount++;
        }
    });
}

function renderConversations() {
    const list = document.getElementById('conversations-list');
    const sortedIds = Object.keys(conversations).sort((a, b) => {
        const dateA = new Date(conversations[a].lastMessage.timestamp);
        const dateB = new Date(conversations[b].lastMessage.timestamp);
        return dateB - dateA;
    });

    if (sortedIds.length === 0) {
        list.innerHTML = '<div class="text-center py-10 text-gray-400">No conversations yet.</div>';
        return;
    }

    list.innerHTML = sortedIds.map(id => {
        const convo = conversations[id];
        const isActive = parseInt(id) === currentRecipientId;
        const initials = convo.email.substring(0, 2).toUpperCase();

        return `
        <div onclick="selectConversation(${id})" 
            class="p-4 flex items-center gap-3 cursor-pointer hover:bg-gray-100 transition border-b border-gray-100 ${isActive ? 'bg-blue-50 border-l-4 border-accent' : ''}">
            <div class="relative">
                <div class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center font-bold text-gray-500 shadow-neu-out">
                    ${initials}
                </div>
                ${convo.unreadCount > 0 ? `<div class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center border-2 border-white">${convo.unreadCount}</div>` : ''}
            </div>
            <div class="flex-1 min-w-0">
                <div class="flex justify-between items-baseline mb-1">
                    <h4 class="font-bold text-primary truncate">${convo.email.split('@')[0]}</h4>
                    <span class="text-xs text-gray-400">${new Date(convo.lastMessage.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
                <p class="text-sm text-gray-500 truncate ${convo.unreadCount > 0 ? 'font-bold text-text' : ''}">
                    ${convo.lastMessage.sender_email === currentUserEmail ? 'You: ' : ''}${convo.lastMessage.content}
                </p>
            </div>
        </div>
        `;
    }).join('');
}

function selectConversation(id) {
    currentRecipientId = parseInt(id);
    const convo = conversations[id];

    // UI Update (Mobile responsive handling)
    document.getElementById('chat-window').classList.remove('hidden');
    if (window.innerWidth < 768) {
        document.querySelector('.w-full.md\\:w-1\\/3').classList.add('hidden'); // Hide sidebar on mobile
    }

    // Header Update
    document.getElementById('chat-header-name').innerText = convo.email.split('@')[0];
    document.getElementById('chat-header-avatar').innerText = convo.email.substring(0, 2).toUpperCase();

    // Enable Input
    document.getElementById('message-input').disabled = false;
    document.getElementById('send-btn').disabled = false;
    document.getElementById('message-input').focus();

    renderMessages(id);
    renderConversations(); // Re-render to highlight active

    // Mark as read (optimistic)
    // In real app, send API call to mark messages as read
}

function renderMessages(id) {
    const convo = conversations[id];
    const container = document.getElementById('messages-container');

    // Group messages by date? For now simple list
    container.innerHTML = convo.messages.map(msg => {
        const isMe = msg.sender_email === currentUserEmail;
        return `
        <div class="flex ${isMe ? 'justify-end' : 'justify-start'}">
            <div class="max-w-[75%] px-4 py-2 rounded-2xl shadow-sm border ${isMe ? 'bg-accent text-white rounded-br-none border-accent' : 'bg-white text-text rounded-bl-none border-gray-200'}">
                <p>${msg.content}</p>
                <div class="text-xs ${isMe ? 'text-blue-200' : 'text-gray-400'} mt-1 text-right">
                    ${new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
            </div>
        </div>
        `;
    }).join('');

    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

async function sendMessage(e) {
    e.preventDefault();
    const input = document.getElementById('message-input');
    const content = input.value.trim();
    if (!content || !currentRecipientId) return;

    input.value = ''; // Optimistic clear

    try {
        const token = window.getAccessToken();
        const res = await fetch('/api/messages/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                recipient: currentRecipientId,
                content: content
            })
        });

        if (res.ok) {
            const newMsg = await res.json();
            // Add to local state immediately
            if (!conversations[currentRecipientId]) {
                // Should ideally handle new conversation creation if not exists
                conversations[currentRecipientId] = { messages: [] };
            }
            conversations[currentRecipientId].messages.push(newMsg);
            conversations[currentRecipientId].lastMessage = newMsg;
            renderMessages(currentRecipientId);
            renderConversations();
        } else {
            window.showToast("Failed to send message", 'error');
        }
    } catch (e) {
        console.error(e);
        window.showToast("Error sending message", 'error');
    }
}
