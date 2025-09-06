<template>
  <div class="modal fade" id="leavePageModal" tabindex="-1" aria-labelledby="leavePageModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="leavePageModalLabel">Warning</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to leave? You may lose your chat history unless you export it first.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Stay</button>
          <button type="button" class="btn btn-danger" @click="confirmLeave">Leave</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeavePageModal',
  methods: {
    confirmLeave() {
      this.$emit('confirm-leave');
    }
  }
}
</script>
