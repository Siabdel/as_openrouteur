
<template>
  <div id="app">
    <!-- API Key Modal -->
    <api-key-modal 
      v-if="!apiKey" 
      @api-key-submitted="setApiKey"
    />

    <!-- Leave Page Warning Modal -->
    <leave-page-modal 
      @confirm-leave="confirmLeavePage"
    />

    <!-- Model Settings Modal -->
    <model-settings-modal 
      :settings="settings" 
      @update-setting="updateSetting"
      @reset-settings="resetSettings"
      @save-settings="saveModelSettings"
    />

    <!-- Main Application Layout -->
    <div class="container-fluid vh-100 d-flex flex-column">
      <!-- Header -->
      <header class="row py-2 bg-dark text-white">
        <div class="col d-flex align-items-center justify-content-between">
          <div class="d-flex align-items-center">
            <button class="btn btn-outline-light me-2" @click="toggleSidebar">
              <i class="fas fa-bars"></i>
            </button>
            <h1 class="h5 mb-0">OpenRouter Chat Application</h1>
          </div>
          <div class="d-flex align-items-center">
            <div class="dropdown me-2">
              <button class="btn btn-outline-light dropdown-toggle" type="button" id="modelDropdown"
                data-bs-toggle="dropdown" aria-expanded="false">
                {{ selectedModelLabel }}
              </button>
              <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="modelDropdown">
                <li v-for="model in models" :key="model.value">
                  <a class="dropdown-item" href="#" :class="{ active: model.value === selectedModel }"
                    @click.prevent="changeModel(model.value)">
                    {{ model.label }}
                  </a>
                </li>
              </ul>
            </div>
            <div class="btn-group" role="group">
              <button type="button" class="btn btn-outline-light" data-bs-toggle="modal" data-bs-target="#modelSettingsModal"
                title="Model Settings">
                <i class="fas fa-sliders"></i>
              </button>
              <button type="button" class="btn btn-outline-light" @click="exportChat" title="Export Chat">
                <i class="fas fa-file-export"></i>
              </button>
              <button type="button" class="btn btn-outline-light" @click="importChat" title="Import Chat">
                <i class="fas fa-file-import"></i>
              </button>
              <button type="button" class="btn btn-outline-light" @click="deleteCurrentChat" title="Delete Current Chat">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content Area -->
      <div class="row g-0 flex-grow-1">
        <!-- Sidebar -->
        <chat-history 
          :chats="chats" 
          :currentChatId="currentChatId"
          @new-chat="createNewChat"
          @load-chat="loadChat"
        />

        <!-- Chat Area -->
        <main id="mainContent" class="col-md-9 col-lg-10 d-flex flex-column" :class="{ 'expanded': !sidebarVisible }">
          <!-- Chat Messages -->
          <chat-messages 
            :messages="currentMessages" 
            :waitingForResponse="currentlyStreaming" 
            :error="error"
            :selectedModel="selectedModel"
            :models="models"
            @edit-message="editUserMessage"
            @regenerate-response="regenerateResponse"
            @retry-request="retryApiRequest"
          />

          <!-- Input Area -->
          <chat-input 
            @send-message="sendUserMessage"
            @upload-files="handleFileUpload"
          />
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import ApiKeyModal from './components/ApiKeyModal.vue'
import LeavePageModal from './components/LeavePageModal.vue'
import ModelSettingsModal from './components/ModelSettingsModal.vue'
import ChatHistory from './components/ChatHistory.vue'
import ChatMessages from './components/ChatMessages.vue'
import ChatInput from './components/ChatInput.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    ApiKeyModal,
    LeavePageModal,
    ModelSettingsModal,
    ChatHistory,
    ChatMessages,
    ChatInput
  },
  data() {
    return {
      // État de l'application
      apiKey: null,
      currentChatId: null,
      chats: {},
      selectedModel: 'deepseek/deepseek-chat-v3-0324:free',
      models: [
        { label: 'Gemini 2.5 Pro Experimental (1,048,576 context)', value: 'google/gemini-2.5-pro-exp-03-25:free', context: 1048576 },
        { label: 'Gemini 2.0 Flash (1,048,576 context)', value: 'google/gemini-2.0-flash-exp:free', context: 1048576 },
        { label: 'DeepSeek V3 0324 (163,840 context)', value: 'deepseek/deepseek-chat-v3-0324:free', context: 163840 },
        { label: 'DeepSeek R1 (163,840 context)', value: 'deepseek/deepseek-r1:free', context: 163840 },
        { label: 'DeepSeek V3 Base (163,840 context)', value: 'deepseek/deepseek-v3-base:free', context: 163840 },
        { label: 'DeepSeek R1 Zero (163,840 context)', value: 'deepseek/deepseek-r1-zero:free', context: 163840 },
        { label: 'Gemma 3 27B (131,072 context)', value: 'google/gemma-3-27b-it:free', context: 131072 },
        { label: 'Qwen 2.5 VL 72B (131,072 context)', value: 'qwen/qwen2.5-vl-72b-instruct:free', context: 131072 },
        { label: 'Llama 3.2 1B (131,072 context)', value: 'meta-llama/llama-3.2-1b-instruct:free', context: 131072 },
        { label: 'DeepSeek R1 Distill Llama 70B (128,000 context)', value: 'deepseek/deepseek-r1-distill-llama-70b:free', context: 128000 }
      ],
      settings: {
        temperature: 1.0,
        topP: 1.0,
        topK: 0,
        frequencyPenalty: 0.0,
        presencePenalty: 0.0,
        repetitionPenalty: 1.0,
        minP: 0.0,
        topA: 0.0,
        seed: null,
        maxTokens: null,
        logprobs: false,
        topLogprobs: null,
        streaming: true,
        reasoning: {
          effort: null,
          maxTokens: null,
          exclude: false
        }
      },
      fallbackModels: ['google/gemini-2.0-flash-exp:free', 'deepseek/deepseek-v3-base:free'],
      uploadedFiles: [],
      currentlyStreaming: false,
      streamController: null,
      error: null,
      sidebarVisible: true
    }
  },
  computed: {
    currentMessages() {
      if (this.currentChatId && this.chats[this.currentChatId]) {
        return this.chats[this.currentChatId].messages
      }
      return []
    },
    selectedModelLabel() {
      const model = this.models.find(m => m.value === this.selectedModel)
      return model ? model.label : 'Select Model'
    }
  },
  mounted() {
    this.initializeApp()
  },
  methods: {
    initializeApp() {
      // Initialiser AOS
      if (typeof AOS !== 'undefined') {
        AOS.init({
          duration: 800,
          once: true
        })
      }
      
      // Vérifier la clé API dans le sessionStorage
      const storedApiKey = sessionStorage.getItem('apiKey')
      if (storedApiKey) {
        this.apiKey = storedApiKey
        this.initializeAfterAuth()
      } else {
        // Afficher le modal API key via Bootstrap
        $('#apiKeyModal').modal('show')
      }
    },
    
    setApiKey(apiKey) {
      if (apiKey) {
        this.apiKey = apiKey
        sessionStorage.setItem('apiKey', apiKey)
        $('#apiKeyModal').modal('hide')
        this.initializeAfterAuth()
      }
    },
    
    async initializeAfterAuth() {
      // Charger l'état de l'application depuis l'API Django
      await this.loadAppState()
      
      // Créer un nouveau chat s'il n'en existe pas
      if (Object.keys(this.chats).length === 0) {
        this.createNewChat()
      } else {
        // Charger le chat le plus récent
        const chatIds = Object.keys(this.chats)
        const lastChatId = chatIds[chatIds.length - 1]
        this.loadChat(lastChatId)
      }
    },
    
    async loadAppState() {
      try {
        // Charger les paramètres utilisateur depuis l'API Django
        const response = await axios.get('/api/settings/')
        if (response.data.length > 0) {
          this.settings = response.data[0].settings
        }
        
        // Charger les chats depuis l'API Django
        const chatResponse = await axios.get('/api/chats/')
        chatResponse.data.forEach(chat => {
          this.chats[chat.id] = chat
        })
      } catch (error) {
        console.error('Error loading app state:', error)
        // Fallback sur le localStorage si l'API n'est pas disponible
        const savedState = localStorage.getItem('llmChatAppState')
        if (savedState) {
          const parsedState = JSON.parse(savedState)
          this.chats = parsedState.chats || {}
          this.selectedModel = parsedState.selectedModel || 'google/gemini-2.0-flash-thinking-exp:free'
          this.settings = parsedState.settings || this.settings
        }
      }
    },
    
    async saveAppState() {
      try {
        // Sauvegarder les paramètres via l'API Django
        await axios.post('/api/settings/', { settings: this.settings })
        
        // Sauvegarder les chats via l'API Django
        for (const chatId in this.chats) {
          const chat = this.chats[chatId]
          await axios.post('/api/chats/', chat)
        }
      } catch (error) {
        console.error('Error saving app state:', error)
        // Fallback sur le localStorage si l'API n'est pas disponible
        const stateToSave = {
          chats: this.chats,
          selectedModel: this.selectedModel,
          settings: this.settings
        }
        localStorage.setItem('llmChatAppState', JSON.stringify(stateToSave))
      }
    },
    
    changeModel(modelValue) {
      this.selectedModel = modelValue
      this.createNewChat()
      this.saveAppState()
    },
    
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible
    },
    
    createNewChat() {
      // Générer un nouvel ID de chat
      const chatId = 'chat_' + Date.now()

      // Créer un nouvel objet chat
      this.chats[chatId] = {
        id: chatId,
        title: 'New Conversation',
        model: this.selectedModel,
        messages: [],
        createdAt: new Date().toISOString()
      }

      // Définir comme chat courant
      this.currentChatId = chatId

      // Sauvegarder l'état
      this.saveAppState()

      // Ajouter un message système
      const systemMessageElement = document.createElement('div')
      systemMessageElement.className = 'system-message'
      systemMessageElement.textContent = `New conversation started with ${this.getModelLabel(this.selectedModel)}`
      document.getElementById('chatMessages').appendChild(systemMessageElement)
    },
    
    getModelLabel(modelValue) {
      const model = this.models.find(m => m.value === modelValue)
      return model ? model.label : modelValue
    },
    
    loadChat(chatId) {
      if (!this.chats[chatId]) return

      // Set current chat
      this.currentChatId = chatId

      // Clear chat messages display
      const chatMessages = document.getElementById('chatMessages')
      if (chatMessages) {
        chatMessages.innerHTML = ''
      }

      // Add system message about loaded chat
      const chat = this.chats[chatId]
      const systemMessageElement = document.createElement('div')
      systemMessageElement.className = 'system-message'
      systemMessageElement.textContent = `Loaded conversation with ${this.getModelLabel(chat.model)}`
      document.getElementById('chatMessages').appendChild(systemMessageElement)

      // Render messages
      chat.messages.forEach(message => {
        this.renderMessage(message)
      })

      // Scroll to bottom
      this.scrollToBottom()
    },
    
    updateSetting(setting, value) {
      if (setting.includes('.')) {
        const [parent, child] = setting.split('.')
        this.settings[parent][child] = value
      } else {
        this.settings[setting] = value
      }
    },
    
    resetSettings() {
      this.settings = {
        temperature: 1.0,
        topP: 1.0,
        topK: 0,
        frequencyPenalty: 0.0,
        presencePenalty: 0.0,
        repetitionPenalty: 1.0,
        minP: 0.0,
        topA: 0.0,
        seed: null,
        maxTokens: null,
        logprobs: false,
        topLogprobs: null,
        streaming: true,
        reasoning: {
          effort: null,
          maxTokens: null,
          exclude: false
        }
      }
    },
    
    saveModelSettings() {
      this.saveAppState()
    },
    
    handleFileUpload(files) {
      // Implémentation de la gestion des fichiers uploadés
      console.log('Files uploaded:', files)
      // Ajouter ici le code pour traiter les fichiers
    },
    
    sendUserMessage(content, files) {
      // Implémentation de l'envoi de message
      console.log('Message sent:', content, files)
      // Ajouter ici le code pour envoyer le message à l'API
    },
    
    editUserMessage(message) {
      // Implémentation de l'édition de message
      console.log('Edit message:', message)
      // Ajouter ici le code pour éditer le message
    },
    
    regenerateResponse(message) {
      // Implémentation de la régénération de réponse
      console.log('Regenerate response:', message)
      // Ajouter ici le code pour régénérer la réponse
    },
    
    retryApiRequest() {
      // Implémentation de la réessaye de requête API
      console.log('Retry API request')
      // Ajouter ici le code pour réessayer la requête API
    },
    
    exportChat() {
      // Implémentation de l'export de chat
      console.log('Export chat')
      // Ajouter ici le code pour exporter le chat
    },
    
    importChat() {
      // Implémentation de l'import de chat
      console.log('Import chat')
      // Ajouter ici le code pour importer un chat
    },
    
    deleteCurrentChat() {
      // Implémentation de la suppression de chat
      console.log('Delete current chat')
      // Ajouter ici le code pour supprimer le chat courant
    },
    
    confirmLeavePage() {
      // Implémentation de la confirmation de départ
      console.log('Confirm leave page')
      // Ajouter ici le code pour gérer la confirmation de départ
    },
    
    scrollToBottom() {
      const chatMessages = document.getElementById('chatMessages')
      if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight
      }
    },
    
    renderMessage(message) {
      // Implémentation du rendu de message
      console.log('Render message:', message)
      // Ajouter ici le code pour rendre le message dans l'interface
    }
  }
}
</script>

<style>
/* Styles globaux de l'application */
@import './styles.css';
</style>