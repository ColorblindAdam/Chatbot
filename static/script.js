const md = new markdownit();

function addMessageToChatbox(sender, message) {
    const chatbox = document.querySelector(".top-chatbox");

    const messageElement = document.createElement("div");
    messageElement.classList.add(`${sender}-message`);

    const avatarElement = document.createElement("div");
    avatarElement.classList.add("avatar");

    // Set the background image of the avatar element based on the sender
    avatarElement.style.backgroundImage = `url(/static/${sender}.png)`;

    const textElement = document.createElement("div");
    textElement.classList.add("message");

    // Convert the message from Markdown to HTML
    const htmlMessage = md.render(message);

    textElement.innerHTML = htmlMessage;
    
    messageElement.appendChild(avatarElement);
    messageElement.appendChild(textElement);
    chatbox.appendChild(messageElement);

    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {
    const messageInput = document.getElementById("message-input");
    const userMessage = messageInput.value.trim();
    
    if (userMessage.length === 0) {
        return false;
    }

    addMessageToChatbox("user", userMessage);
    messageInput.value = "";

    const response = await fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userMessage })
    });

    const jsonResponse = await response.json();
    const botMessage = jsonResponse.response;

    addMessageToChatbox("bot", botMessage);

    return false;
}

document.querySelector(".form").addEventListener("submit", (event) => {
    event.preventDefault();
    sendMessage();
});
