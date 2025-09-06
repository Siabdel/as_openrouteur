<template>
  <div class="chat-input-area p-3 border-top">
    <div class="file-attachments mb-2">
      <div v-for="(file, index) in uploadedFiles" :key="index" class="file-attachment">
        <i class="fas fa-file"></i>
        <span class="file-name">{{ file.name }}</span>
        <i class="fas fa-times remove-file" @click="removeFile(index)"></i>
      </div>
    </div>
    <div class="input-group">
      <div class="form-control position-relative">
        <div contenteditable="true" class="promptEditor" ref="promptEditor" 
          @input="updateContent"
          @keydown.ctrl.enter="sendMessage"
          @keydown.meta.enter="sendMessage"
          placeholder="Type your message here..."></div>
      </div>
      <button class="btn btn-outline-secondary" type="button" @click="triggerFileUpload">
        <i class="fas fa-paperclip"></i>
      </button>
      <button class="btn btn-primary" type="button" @click="sendMessage" :disabled="!content.trim()">
        <i class="fas fa-paper-plane"></i>
      </button>
    </div>
    <div class="d-flex justify-content-between align-items-center mt-2">
      <div class="text-muted small">~{{ tokenCount }} tokens</div>
      <input type="file" ref="fileInput" multiple style="display:none" @change="handleFileUpload">
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatInput',
  data() {
    return {
      content: '',
      uploadedFiles: []
    };
  },
  computed: {
    tokenCount() {
      return Math.ceil(this.content.length / 4);
    }
  },
  methods: {
    updateContent() {
      this.content = this.$refs.promptEditor.innerText;
    },
    sendMessage() {
      if (this.content.trim()) {
        this.$emit('send-message', this.content, this.uploadedFiles);
        this.clearInput();
      }
    },
    clearInput() {
      this.content = '';
      this.$refs.promptEditor.innerText = '';
      this.uploadedFiles = [];
    },
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const files = event.target.files;
      if (!files.length) return;
      
      this.$emit('upload-files', files);
    },
    removeFile(index) {
      this.uploadedFiles.splice(index, 1);
    }
  }
}
</script>