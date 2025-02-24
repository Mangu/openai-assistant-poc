<template>
  <div class="page-container">
    <h3>Chat</h3>
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <span class="close-button" @click="showModal = false">&times;</span>
        <input type="file" @change="handleFileUpload">
      </div>
    </div>
    <div v-if="isSending" class="thinking-animation">Thinking...</div>
    <div class="messages-container">
      <div class="messages" ref="messages">
        <div v-for="(message, index) in messages" :key="index" :class="`chat-bubble ${message.sender}`">
          <div v-html="renderMarkdown(message.text)" class="markdown-content"></div>
          <span class="sender">{{ message.sender }}</span>
        </div>
      </div>
    </div>
    <div class="form-group">
      <input v-model="userInput" class="form-control long-input" placeholder="How can I help you today?" @keyup.enter="sendMessage">
    </div>
    <div class="button-container">
      <button @click="sendMessage" class="btn btn-primary">Go</button>
      <button @click="clearMessage" class="btn btn-primary">Clear</button>
      <!--<button @click="showModal=true" class="btn btn-primary">Add File</button>-->
      <button @click="getThread" class="btn btn-primary">New Thread</button>
      <div class="status-container">{{ status }}</div>
    </div>
  </div>
</template> 

<script>
import MarkdownIt from 'markdown-it';
import assistantService from '../services/assistantService';

const md = new MarkdownIt({ breaks: true, html: true });

export default {
  name: 'Chat',
  
  data() {
    return {
      userInput: '',
      status: '',
      messages: [],
      isSending: false,
      showModal: false,
      selectedFile: null,       
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];        
      this.showModal = false;
    },
    renderMarkdown(text) {
      try {
        // Directly render the Markdown text without replacing \n markers
        const html = md.render(text);
        console.log("Original Text:", text);      // Debug: check original text
        console.log("Rendered HTML:", html);       // Debug: check the rendered HTML output
        return html;
      } catch (error) {
        console.error('Failed to render Markdown:', error);
        return text;
      }
    },
    async sendMessage() {
      this.isSending = true;
      let message = this.userInput;
      this.userInput = '';
      this.messages.push({ sender: 'user', text: message });
      this.scrollToBottom();
       
      let response = '';

      try {
        response = await assistantService.postMessage(message, this.thread);
          
        if (response == null) {
          response = "Sorry, I'm having trouble communicating with the assistant. Create a new thread and try again.";
        }

        console.log('Response:', response);
        this.messages.push({ sender: 'assistant', text: response });
        this.scrollToBottom();
      } catch (error) {
        console.log('Error:', error);
      } finally {
        this.isSending = false;
      }
    },
    clearMessage() {
      this.messages = [];
      this.userInput = '';        
    },
    async getThread() {
      try {
        this.thread = await assistantService.getThread();         
        this.status = 'Thread: ' + this.thread;
      } catch (error) {
        console.log('Error:', error);
        this.status = 'Error: ' + error;
      }            
      this.status = 'Thread: ' + this.thread + ' ';
    },
    scrollToBottom() {
      this.$nextTick(() => {
        this.$refs.messages.scrollTop = this.$refs.messages.scrollHeight;
      });
    },
  },
  async mounted() {
    await this.getThread();
  },
};
</script>  

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 20px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 80%;
  max-width: 500px;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  cursor: pointer;
}

.thinking-animation {
  text-align: center;
  font-size: 18px;
  margin-bottom: 10px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 10px;
}

.messages {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center-align all messages */
  width: 100%; /* Ensure the messages container takes the full width */
}

.chat-bubble {
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
  max-width: 80%; /* Optional: Limit the width of the chat bubbles */
  text-align: left; /* Align text to the left within the chat bubbles */
}

.chat-bubble.user {
  background-color: #d1e7dd;
  align-self: center; /* Align user messages to the right */
}

.chat-bubble.assistanter {
  background-color: #f8d7da;
  align-self: center; /* Align assistant messages to the left */
}

.chat-bubble.system {
  background-color: #e2e3e5;
  align-self: center;
}

.sender {
  font-size: 12px;
  color: #555;
}

.form-group {
  display: flex;
  align-items: center;
}

.form-control {
  flex: 1;
  padding: 10px;
  margin-right: 10px;
}

.button-container {
  display: flex;
  justify-content: space-between;
}

.status-container {
  margin-top: 10px;
  font-size: 14px;
  color: #888;
}

/* Add styles for lists */
.markdown-content ul, .markdown-content ol {
  margin: 0;
  padding-left: 20px;
}

.markdown-content li {
  margin-bottom: 5px;
}
</style>