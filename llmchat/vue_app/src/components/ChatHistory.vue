<template>
  <aside id="sidebar" class="col-md-3 col-lg-2 bg-light border-end d-md-block">
    <div class="d-flex flex-column h-100">
      <div class="p-3 border-bottom">
        <button class="btn btn-primary w-100 mb-2" @click="createNewChat">
          <i class="fas fa-plus me-2"></i>New Chat
        </button>
      </div>
      <div class="overflow-auto flex-grow-1 chat-history">
        <div v-for="chat in sortedChats" :key="chat.id" 
          class="chat-history-item" 
          :class="{ active: chat.id === currentChatId }"
          @click="loadChat(chat.id)">
          {{ getChatTitle(chat) }}
        </div>
      </div>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'ChatHistory',
  props: {
    chats: {
      type: Object,
      required: true
    },
    currentChatId: {
      type: String,
      default: null
    }
  },
  computed: {
    sortedChats() {
      return Object.values(this.chats).sort((a, b) => {
        return new Date(b.createdAt) - new Date(a.createdAt);
      });
    }
  },
  methods: {
    getChatTitle(chat) {
      if (chat.messages && chat.messages.length > 0) {
        const firstUserMessage = chat.messages.find(msg => msg.role === 'user');
        if (firstUserMessage) {
          let title = firstUserMessage.content.split('\n')[0].substring(0, 30);
          if (firstUserMessage.content.length > 30) title += '...';
          return title;
        }
      }
      return chat.title;
    },
    createNewChat() {
      this.$emit('new-chat');
    },
    loadChat(chatId) {
      this.$emit('load-chat', chatId);
    }
  }
}
</script>
