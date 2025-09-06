
<template>
  <div class="modal fade" id="modelSettingsModal" tabindex="-1" aria-labelledby="modelSettingsModalLabel"
    aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modelSettingsModalLabel">Model Settings</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="temperatureSlider" class="form-label">Temperature</label>
              <div class="d-flex align-items-center">
                <input type="range" class="form-range flex-grow-1" min="0" max="2" step="0.1"
                  id="temperatureSlider" v-model.number="localSettings.temperature">
                <span class="ms-2">{{ localSettings.temperature.toFixed(1) }}</span>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label for="topPSlider" class="form-label">Top P</label>
              <div class="d-flex align-items-center">
                <input type="range" class="form-range flex-grow-1" min="0" max="1" step="0.01"
                  id="topPSlider" v-model.number="localSettings.topP">
                <span class="ms-2">{{ localSettings.topP.toFixed(2) }}</span>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="topKSlider" class="form-label">Top K</label>
              <div class="d-flex align-items-center">
                <input type="range" class="form-range flex-grow-1" min="0" max="100" step="1"
                  id="topKSlider" v-model.number="localSettings.topK">
                <span class="ms-2">{{ localSettings.topK }}</span>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label for="frequencyPenaltySlider" class="form-label">Frequency Penalty</label>
              <div class="d-flex align-items-center">
                <input type="range" class="form-range flex-grow-1" min="-2" max="2" step="0.1"
                  id="frequencyPenaltySlider" v-model.number="localSettings.frequencyPenalty">
                <span class="ms-2">{{ localSettings.frequencyPenalty.toFixed(1) }}</span>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="presencePenaltySlider" class="form-label">Presence Penalty</label>
              <div class="d-flex align-items-center">
                <input type="range" class="form-range flex-grow-1" min="-2" max="2" step="0.1"
                  id="presencePenaltySlider" v-model.number="localSettings.presencePenalty">
                <span class="ms-2">{{ localSettings.presencePenalty.toFixed(1) }}</span>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label for="repetitionPenaltySlider" class="form-label">Repetition Penalty</label>
              <div class="d-flex align-items-center">
                <input type="range" class="form-range flex-grow-1" min="0" max="2" step="0.1"
                  id="repetitionPenaltySlider" v-model.number="localSettings.repetitionPenalty">
                <span class="ms-2">{{ localSettings.repetitionPenalty.toFixed(1) }}</span>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="minPSlider" class="form-label">Min P</label>
              <div class="d-flex align-items-center">
                <input type="range" class="form-range flex-grow-1" min="0" max="1" step="0.01"
                  id="minPSlider" v-model.number="localSettings.minP">
                <span class="ms-2">{{ localSettings.minP.toFixed(2) }}</span>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label for="topASlider" class="form-label">Top A</label>
              <div class="d-flex align-items-center">
                <input type="range" class="form-range flex-grow-1" min="0" max="1" step="0.01"
                  id="topASlider" v-model.number="localSettings.topA">
                <span class="ms-2">{{ localSettings.topA.toFixed(2) }}</span>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="seedInput" class="form-label">Seed</label>
              <input type="number" class="form-control" id="seedInput" v-model="localSettings.seed" placeholder="Optional">
            </div>
            <div class="col-md-6 mb-3">
              <label for="maxTokensInput" class="form-label">Max Tokens</label>
              <input type="number" class="form-control" id="maxTokensInput" v-model="localSettings.maxTokens" placeholder="Optional" min="1">
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" id="logprobsCheckbox" v-model="localSettings.logprobs">
                <label class="form-check-label" for="logprobsCheckbox">Logprobs</label>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label for="topLogprobsInput" class="form-label">Top Logprobs</label>
              <input type="number" class="form-control" id="topLogprobsInput" v-model="localSettings.topLogprobs" placeholder="Optional" min="0" max="20">
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" id="streamingCheckbox" v-model="localSettings.streaming">
                <label class="form-check-label" for="streamingCheckbox">Streaming</label>
              </div>
            </div>
          </div>

          <div class="mt-3 border-top pt-3">
            <h6>Reasoning Tokens</h6>
            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="reasoningEffortSelect" class="form-label">Effort</label>
                <select class="form-select" id="reasoningEffortSelect" v-model="localSettings.reasoning.effort">
                  <option value="">None</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div class="col-md-4 mb-3">
                <label for="reasoningTokensInput" class="form-label">Token Limit</label>
                <input type="number" class="form-control" id="reasoningTokensInput" v-model="localSettings.reasoning.maxTokens" placeholder="e.g. 2000">
              </div>
              <div class="col-md-4 mb-3 d-flex align-items-end">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="excludeReasoningCheckbox" v-model="localSettings.reasoning.exclude">
                  <label class="form-check-label" for="excludeReasoningCheckbox">Exclude</label>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="resetSettings">Reset to Defaults</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="saveSettings">Save Settings</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModelSettingsModal',
  props: {
    settings: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localSettings: JSON.parse(JSON.stringify(this.settings))
    };
  },
  methods: {
    resetSettings() {
      this.localSettings = {
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
      };
      this.$emit('reset-settings');
    },
    saveSettings() {
      this.$emit('save-settings', this.localSettings);
    }
  },
  watch: {
    settings: {
      handler(newVal) {
        this.localSettings = JSON.parse(JSON.stringify(newVal));
      },
      deep: true
    }
  }
}
</script>