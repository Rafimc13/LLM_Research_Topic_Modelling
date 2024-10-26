<template>
  <div class="modal-backdrop" v-if="isVisible" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h3>Topics List</h3>
      <div class="topics-list">
        <template v-for="(comment, index) in summary?.comments" :key="index">
          <p v-for="topic in comment.topics">
            {{ topic }}
          </p>
        </template>
      </div>
      <div class="close" @click="closeModal">x</div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue'

// Define the props
const props = defineProps({
  summary: {
    type: Array,
    required: true,
    default: () => [],
  },
  isVisible: {
    type: Boolean,
    required: true,
  },
})

// Define the emits
const emit = defineEmits(['close'])

// Function to close the modal
const closeModal = () => {
  emit('close')
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  position: relative;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 800px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-content ul {
  margin-top: 20px;
  min-height: 500px;
  max-height: 80vh;
}

.close {
  margin-top: 0;
  padding: 10px 15px;
  background-color: #dddddd;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  position: absolute;
  top: 10px;
  right: 10px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #969696;
}

.close:hover {
  background-color: #3f3f3f;
}
.topics-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 30px;
}
.topics-list p {
  padding: 5px 10px;
  background-color: #ffffff;
  border-radius: 5px;
  margin: 0;
  color: #616161;
  font-size: 14px;
  font-weight: 500;
  border: 1px solid #cbcbcb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
