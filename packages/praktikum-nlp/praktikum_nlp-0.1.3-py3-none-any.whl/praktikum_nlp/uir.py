from IPython.display import HTML, display

def ollamaUI():
    display(HTML('''
    <link rel="stylesheet" href="https://cdn2-jsdelivr.pages.dev/main/fontawesome_pro@6.6.0/css/all.css" crossorigin="anonymous">
    <style>
        body { font-family: 'Arial', sans-serif; margin: 0; padding: 0; }
        .chat-container {
            max-width: 650px;
            margin: 50px auto;
            padding: 15px;
            border-radius: 10px;
            background: #ffffff;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .chat-log {
            display: flex;
            flex-direction: column;
            max-height: 500px;
            overflow-y: auto;
            margin-bottom: 10px;
        }
        .chat-bubble {
            padding: 12px 15px;
            margin: 5px 0;
            border-radius: 20px;
            max-width: 70%;
            display: inline-block;
            word-wrap: break-word;
            font-size: 16px;
            line-height: 1.5;
            background-color: #f5f5f5;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        }
        .user {
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
            text-align: justify;
        }
        .assistant {
            background: #e6e6e6;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
            text-align: justify;
        }
        .file-upload-bubble {
            padding: 10px;
            margin: 5px 0;
            border-radius: 12px;
            max-width: 25%;
            display: flex;
            align-items: center;
            background-color: #e6e6e6;
            color: #333;
            position: relative;
        }
        .file-upload-bubble i {
            font-size: 24px;
            color: #007bff;
            margin-right: 10px;
        }
        .file-upload-bubble .file-info {
            display: flex;
            flex-direction: column;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }
        .file-upload-bubble .file-name {
            font-weight: bold;
            color: #007bff;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 120px;
        }
        .file-upload-bubble .file-type {
            font-size: 12px;
            color: #bbb;
        }
        .file-upload-bubble .close-btn {
            position: absolute;
            top: 6px;
            right: -6px;
            background-color: transparent;
            color: #007bff;
            font-size: 16px;
            cursor: pointer;
            border: none;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .file-upload-bubble .close-btn i {
            font-size: 15px;
        }
        .input-container {
            display: flex;
            border-radius: 30px;
            overflow: hidden;
            background-color: #f0f4f8;
            border: 1px solid #ddd;
        }
        .input-container input[type="text"] {
            flex: 1;
            padding: 10px;
            border: none;
            outline: none;
            font-size: 16px;
            border-radius: 30px;
            color: #333;
            background-color: #f9f9f9;
        }
        .input-container button {
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: background-color 0.3s ease;
        }
        .input-container button:hover {
            background-color: #0056b3;
        }
        .input-container button i {
            font-size: 20px;
        }
        .attach-file {
            padding: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s ease;
        }
        .attach-file:hover {
            background-color: #e0e0e0;
        }
        .hidden-file-input {
            display: none;
        }
        .icon-paperclip {
            font-size: 18px;
            color: #007bff;
        }
        .icon-send {
            font-size: 20px;
            color: white;
        }
        .toggle-container {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .toggle-container label {
            font-size: 16px;
            font-weight: bold;
            color: #007bff;
            margin-right: 10px;
        }
        .switch {
            position: relative;
            display: inline-block;
            width: 26px;
            height: 18px;
            margin-left: 2px;
        }
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: 0.4s;
            border-radius: 18px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 14px;
            width: 14px;
            left: 2px;
            bottom: 2px;
            background-color: white;
            transition: 0.4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #007bff;
        }
        input:checked + .slider:before {
            transform: translateX(8px);
        }
        .typing-indicator {
            display: flex;
            align-items: center;
            justify-content: flex-start;
        }
        .typing-indicator .dot {
            height: 8px;
            width: 8px;
            margin: 0 2px;
            background-color: #333;
            border-radius: 50%;
            animation: blink 1.4s infinite both;
        }
        .typing-indicator .dot:nth-child(1) {
            animation-delay: 0s;
        }
        .typing-indicator .dot:nth-child(2) {
            animation-delay: 0.2s;
        }
        .typing-indicator .dot:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes blink {
            0%, 80%, 100% { opacity: 0; }
            40% { opacity: 1; }
        }
    </style>
    <div class="chat-container" id="chat">
        <div class="chat-log" id="chat-log"></div>
        <div class="toggle-container">
            <label for="use-file-checkbox">Enable RAG</label>
            <label class="switch">
                <input type="checkbox" id="use-file-checkbox">
                <span class="slider"></span>
            </label>
        </div>
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Tulis pesan Anda..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <label class="attach-file" for="file-upload">
                <i class="fa-regular fa-paperclip-vertical icon-paperclip"></i>
            </label>
            <input type="file" id="file-upload" class="hidden-file-input" accept=".txt" onchange="uploadFile(this)">
            <button id="send-button" onclick="sendMessage()">
                <i class="fa-sharp-duotone fa-solid fa-circle-arrow-up icon-send"></i>
            </button>
        </div>
    </div>
    <script>
        function disableControls() {
            document.getElementById('user-input').disabled = true;
            document.getElementById('file-upload').disabled = true;
            document.getElementById('send-button').disabled = true;
            document.getElementById('send-button').style.opacity = '0.5';
            document.querySelector('.attach-file').style.pointerEvents = 'none';
            document.querySelector('.attach-file').style.opacity = '0.5';
        }

        function enableControls() {
            document.getElementById('user-input').disabled = false;
            document.getElementById('file-upload').disabled = false;
            document.getElementById('send-button').disabled = false;
            document.getElementById('send-button').style.opacity = '1';
            document.querySelector('.attach-file').style.pointerEvents = 'auto';
            document.querySelector('.attach-file').style.opacity = '1';
        }

        function showTypingIndicator() {
            const chatLog = document.getElementById('chat-log');
            const typingBubble = document.createElement('div');
            typingBubble.classList.add('chat-bubble', 'assistant');
            typingBubble.id = 'typing-indicator';
            typingBubble.innerHTML = `
                <div class="typing-indicator">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            `;
            chatLog.appendChild(typingBubble);
            chatLog.scrollTop = chatLog.scrollHeight;
        }

        function removeTypingIndicator() {
            const typingBubble = document.getElementById('typing-indicator');
            if (typingBubble) {
                typingBubble.remove();
            }
        }

        function appendChat(role, message) {
            const chatLog = document.getElementById('chat-log');

            if (role === 'assistant') {
                removeTypingIndicator();
            }

            const bubble = document.createElement('div');
            bubble.classList.add('chat-bubble', role);
            chatLog.appendChild(bubble);
            chatLog.scrollTop = chatLog.scrollHeight;

            if (role === 'assistant') {
                let i = 0;
                function typingEffect() {
                    if (i < message.length) {
                        bubble.innerHTML += message.charAt(i);
                        i++;
                        setTimeout(typingEffect, 30);
                    } else {
                        enableControls();
                    }
                }
                typingEffect();
            } else {
                bubble.innerText = message;
            }
        }

        function appendFileBubble(fileName) {
            const chatLog = document.getElementById('chat-log');
            const bubble = document.createElement('div');
            bubble.classList.add('file-upload-bubble');
            bubble.innerHTML = `
                <i class="fa-regular fa-file-lines"></i>
                <div class="file-info">
                    <span class="file-name">${fileName}</span>
                    <span class="file-type">Dokumen</span>
                </div>
                <button class="close-btn" onclick="removeFileBubble(this)"><i class="fa-sharp-duotone fa-solid fa-circle-xmark"></i></button>
            `;
            chatLog.appendChild(bubble);
            chatLog.scrollTop = chatLog.scrollHeight;
        }

        function removeFileBubble(element) {
            element.parentElement.remove();
            document.getElementById("file-upload").value = "";
            google.colab.kernel.invokeFunction('notebook.ollama_chat', [null, 'clear'], {});
        }

        function sendMessage() {
            const input = document.getElementById('user-input');
            const userMessage = input.value.trim();
            if (userMessage === '') return;

            disableControls();

            appendChat('user', userMessage);
            input.value = '';

            showTypingIndicator();

            google.colab.kernel.invokeFunction('notebook.ollama_chat', [userMessage, 'message'], {});
        }

        function uploadFile(input) {
            const file = input.files[0];
            if (!file) return;
            if (file.type !== "text/plain") {
                alert('Hanya file format .txt yang dapat diunggah.');
                return;
            }
            const reader = new FileReader();
            reader.onload = function(e) {
                const fileContent = e.target.result;
                google.colab.kernel.invokeFunction('notebook.ollama_chat', [fileContent, 'upload'], {});
                appendFileBubble(file.name);
                document.getElementById("file-upload").value = "";
            };
            reader.readAsText(file);
        }

        document.getElementById('use-file-checkbox').addEventListener('change', function() {
            const use_file = this.checked;
            google.colab.kernel.invokeFunction('notebook.ollama_chat', [use_file, 'use_file'], {});
        });
    </script>
    '''))


def OllamaUI_Vision():
    display(HTML('''
    <link rel="stylesheet" href="https://cdn2-jsdelivr.pages.dev/main/fontawesome_pro@6.6.0/css/all.css" crossorigin="anonymous">
    <style>
        body { font-family: 'Arial', sans-serif; margin: 0; padding: 0; }
        .chat-container {
            max-width: 650px;
            margin: 50px auto;
            padding: 15px;
            border-radius: 10px;
            background: #ffffff;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .chat-log {
            display: flex;
            flex-direction: column;
            max-height: 500px;
            overflow-y: auto;
            margin-bottom: 10px;
        }
        .chat-bubble {
            padding: 12px 15px;
            margin: 5px 0;
            border-radius: 20px;
            max-width: 70%;
            display: inline-block;
            word-wrap: break-word;
            font-size: 16px;
            line-height: 1.5;
            background-color: #f5f5f5;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        }
        .user {
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
            text-align: justify;
        }
        .assistant {
            background: #e6e6e6;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
            text-align: justify;
        }
        .file-upload-bubble {
            margin: 2px 0;
            border-radius: 12px;
            max-width: 20%;
            display: flex;
            align-items: center;
            background-color: #f5f5f5;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            justify-content: center;
            padding: 10px;
            position: relative;
        }
        .file-upload-bubble img {
            max-width: 120px;
            max-height: 120px;
            border-radius: 10px;
            object-fit: cover;
        }
        .file-upload-bubble .close-btn {
            position: absolute;
            top: 6px;
            right: 6px;
            background-color: transparent;
            color: #007bff;
            font-size: 16px;
            cursor: pointer;
            border: none;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .file-upload-bubble .close-btn i {
            font-size: 15px;
        }
        .input-container {
            display: flex;
            border-radius: 30px;
            overflow: hidden;
            background-color: #f0f4f8;
            border: 1px solid #ddd;
        }
        .input-container input[type="text"] {
            flex: 1;
            padding: 10px;
            border: none;
            outline: none;
            font-size: 16px;
            border-radius: 30px;
            color: #333;
            background-color: #f9f9f9;
        }
        .input-container button {
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: background-color 0.3s ease;
        }
        .input-container button:hover {
            background-color: #0056b3;
        }
        .input-container button i {
            font-size: 20px;
        }
        .attach-file {
            padding: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s ease;
        }
        .attach-file:hover {
            background-color: #e0e0e0;
        }
        .hidden-file-input {
            display: none;
        }
        .icon-image {
            font-size: 18px;
            color: #007bff;
        }
        .icon-send {
            font-size: 20px;
            color: white;
        }
        .toggle-container {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .toggle-container label {
            font-size: 16px;
            font-weight: bold;
            color: #007bff;
            margin-right: 10px;
        }
        .switch {
            position: relative;
            display: inline-block;
            width: 26px;
            height: 18px;
            margin-left: 2px;
        }
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: 0.4s;
            border-radius: 18px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 14px;
            width: 14px;
            left: 2px;
            bottom: 2px;
            background-color: white;
            transition: 0.4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #007bff; 
        }
        input:checked + .slider:before {
            transform: translateX(8px);
        }
        .typing-indicator {
            display: flex;
            align-items: center;
            justify-content: flex-start;
        }
        .typing-indicator .dot {
            height: 8px;
            width: 8px;
            margin: 0 2px;
            background-color: #333;
            border-radius: 50%;
            animation: blink 1.4s infinite both;
        }
        .typing-indicator .dot:nth-child(1) {
            animation-delay: 0s;
        }
        .typing-indicator .dot:nth-child(2) {
            animation-delay: 0.2s;
        }
        .typing-indicator .dot:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes blink {
            0%, 80%, 100% { opacity: 0; }
            40% { opacity: 1; }
        }
    </style>
    <div class="chat-container" id="chat">
        <div class="chat-log" id="chat-log"></div>
        <div class="toggle-container">
            <label for="use-vision-checkbox">Enable Vision</label>
            <label class="switch">
                <input type="checkbox" id="use-vision-checkbox">
                <span class="slider"></span>
            </label>
        </div>
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Tulis pesan Anda..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <label class="attach-file" for="file-upload">
                <i class="fa-regular fa-image icon-image"></i>
            </label>
            <input type="file" id="file-upload" class="hidden-file-input" accept="image/*" onchange="uploadFile(this)">
            <button id="send-button" onclick="sendMessage()">
                <i class="fa-sharp-duotone fa-solid fa-circle-arrow-up icon-send"></i>
            </button>
        </div>
    </div>
    <script>
        function disableControls() {
            document.getElementById('user-input').disabled = true;
            document.getElementById('file-upload').disabled = true;
            document.getElementById('send-button').disabled = true;
            document.getElementById('send-button').style.opacity = '0.5';
            document.querySelector('.attach-file').style.pointerEvents = 'none';
            document.querySelector('.attach-file').style.opacity = '0.5';
        }

        function enableControls() {
            document.getElementById('user-input').disabled = false;
            document.getElementById('file-upload').disabled = false;
            document.getElementById('send-button').disabled = false;
            document.getElementById('send-button').style.opacity = '1';
            document.querySelector('.attach-file').style.pointerEvents = 'auto';
            document.querySelector('.attach-file').style.opacity = '1';
        }

        function showTypingIndicator() {
            const chatLog = document.getElementById('chat-log');
            const typingBubble = document.createElement('div');
            typingBubble.classList.add('chat-bubble', 'assistant');
            typingBubble.id = 'typing-indicator';
            typingBubble.innerHTML = `
                <div class="typing-indicator">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            `;
            chatLog.appendChild(typingBubble);
            chatLog.scrollTop = chatLog.scrollHeight;
        }

        function removeTypingIndicator() {
            const typingBubble = document.getElementById('typing-indicator');
            if (typingBubble) {
                typingBubble.remove();
            }
        }

        function appendChat(role, message) {
            const chatLog = document.getElementById('chat-log');

            if (role === 'assistant') {
                removeTypingIndicator();
            }

            const bubble = document.createElement('div');
            bubble.classList.add('chat-bubble', role);
            chatLog.appendChild(bubble);
            chatLog.scrollTop = chatLog.scrollHeight;

            if (role === 'assistant') {
                let i = 0;
                function typingEffect() {
                    if (i < message.length) {
                        bubble.innerHTML += message.charAt(i);
                        i++;
                        setTimeout(typingEffect, 30);
                    } else {
                        enableControls();
                    }
                }
                typingEffect();
            } else {
                bubble.innerText = message;
            }
        }

        function appendFileBubble(fileData) {
            const chatLog = document.getElementById('chat-log');
            const bubble = document.createElement('div');
            bubble.classList.add('file-upload-bubble');
            bubble.innerHTML = `
                <img src="${fileData}" alt="Uploaded Image">
                <button class="close-btn" onclick="removeFileBubble(this)"><i class="fa-sharp-duotone fa-solid fa-circle-xmark"></i></button>
            `;
            chatLog.appendChild(bubble);
            chatLog.scrollTop = chatLog.scrollHeight;
        }

        function removeFileBubble(element) {
            element.parentElement.remove();
            document.getElementById("file-upload").value = "";
            google.colab.kernel.invokeFunction('notebook.ollama_chat', [null, 'clear'], {});
        }

        function sendMessage() {
            const input = document.getElementById('user-input');
            const userMessage = input.value.trim();
            if (userMessage === '') return;

            disableControls();

            appendChat('user', userMessage);
            input.value = '';

            showTypingIndicator();

            const useVision = document.getElementById('use-vision-checkbox').checked;
            google.colab.kernel.invokeFunction('notebook.ollama_chat', [userMessage, 'message', useVision], {});
        }

        function uploadFile(input) {
            const file = input.files[0];
            if (!file) return;
            if (!file.type.startsWith("image/")) {
                alert('Hanya file format gambar yang dapat diunggah.');
                return;
            }
            const reader = new FileReader();
            reader.onload = function(e) {
                const fileContent = e.target.result;
                google.colab.kernel.invokeFunction('notebook.ollama_chat', [fileContent, 'upload'], {});
                appendFileBubble(fileContent);
                document.getElementById("file-upload").value = "";
            };
            reader.readAsDataURL(file);
        }

        document.getElementById('use-vision-checkbox').addEventListener('change', function() {
            const useVision = this.checked;
            google.colab.kernel.invokeFunction('notebook.ollama_chat', [useVision, 'use_vision'], {});
        });
    </script>
    '''))