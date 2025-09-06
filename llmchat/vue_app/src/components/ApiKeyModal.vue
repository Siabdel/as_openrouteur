<template>
  <div class="modal fade" id="apiKeyModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
    aria-labelledby="apiKeyModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="apiKeyModalLabel">Enter Your API Key</h5>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label for="apiKeyInput" class="form-label">OpenRouter API Key</label>
            <input type="password" class="form-control" id="apiKeyInput" v-model="apiKey" placeholder="Enter your API key">
            <div class="form-text text-warning mt-2">
              <i class="fas fa-exclamation-triangle"></i> Warning: Your API key will be stored in session storage for this session only.
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="submitApiKey">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApiKeyModal',
  data() {
    return {
      apiKey: ''
    };
  },
  methods: {
    submitApiKey() {
      this.$emit('api-key-submitted', this.apiKey);
    }
  }
}
</script>
