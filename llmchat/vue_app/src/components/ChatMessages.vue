<template>
  <div class="chat-messages-container">
    <div class="chat-messages h-100 overflow-auto" ref="messagesContainer">
      <div v-for="message in messages" :key="message.timestamp" 
        :class="['chat-bubble', message.role === 'user' ? 'user-bubble' : 'assistant-bubble']"
        data-aos="fade-up">
        <div class="bubble-actions">
          <button class="btn btn-sm btn-outline-secondary copy-btn" title="Copy message" @click="copyMessage(message.content)">
            <i class="fas fa-copy"></i>
          </button>
          <button v-if="message.role === 'user'" class="btn btn-sm btn-outline-secondary edit-btn" title="Edit message" @click="editMessage(message)">
            <i class="fas fa-edit"></i>
          </button>
          <button v-else class="btn btn-sm btn-outline-secondary regenerate-btn" title="Regenerate response" @click="regenerateResponse(message)">
            <i class="fas fa-redo-alt"></i>
          </button>
        </div>
        
        <div v-if="message.role === 'user'" class="message-content">{{ message.content }}</div>
        <div v-else class="markdown-content" v-html="renderMarkdown(message.content)"></div>
        
        <div class="bubble-metadata">
          <div v-if="message.role === 'assistant'">Model: {{ getModelLabel(message.model) }}</div>
          <div v-if="message.processingTime">Time: {{ message.processingTime.toFixed(2) }}s</div>
          <div v-if="message.usage && message.usage.total_tokens">Tokens: {{ message.usage.total_tokens }}</div>
          <div>{{ formatTime(message.timestamp) }}</div>
        </div>
      </div>
      
      <div v-if="waitingForResponse" class="waiting-indicator">
        <div class="typing-indicator me-2">
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
        </div>
        <span>Waiting for response...</span>
      </div>
      
      <div v-if="error" class="error-message">
        <div class="d-flex justify-content-between align-items-start">
          <div>
            <i class="fas fa-exclamation-circle me-2"></i>
            <strong>Error:</strong> {{ error }}
          </div>
          <button class="btn btn-sm btn-danger retry-btn" @click="$emit('retry-request')">
            <i class="fas fa-redo-alt me-1"></i> Retry
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatMessages',
  props: {
    messages: {
      type: Array,
      default: () => []
    },
    waitingForResponse: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    },
    selectedModel: {
      type: String,
      default: ''
    },
    models: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    renderMarkdown(content) {
      return marked.parse(content || '');
    },
    copyMessage(content) {
      navigator.clipboard.writeText(content);
    },
    editMessage(message) {
      this.$emit('edit-message', message);
    },
    regenerateResponse(message) {
      this.$emit('regenerate-response', message);
    },
    getModelLabel(modelValue) {
      const model = this.models.find(m => m.value === modelValue);
      return model ? model.label : modelValue;
    },
    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString();
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    }
  },
  watch: {
    messages: {
      handler() {
        this.scrollToBottom();
      },
      deep: true
    }
  },
  mounted() {
    this.scrollToBottom();
  }
}
</script>
