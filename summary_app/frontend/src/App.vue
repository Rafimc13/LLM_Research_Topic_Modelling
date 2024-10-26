<template>
  <h1>Comments Summary and Topics</h1>

  <!-- File upload form -->
  <div class="file-upload-container">
    <h2>Upload your File</h2>
    <!-- File Upload Drag & Drop Area -->
    <div
      class="drop-zone"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <p>
        Drag & Drop or
        <span class="browse-link" @click="triggerFileInput">browse</span>
      </p>
      <small>Supports: CSV</small>
      <div v-if="selectedFile" class="selected-file">
        <p>Selected File: {{ selectedFile.name }}</p>
      </div>
    </div>

    <!-- Hidden file input field -->
    <input
      type="file"
      ref="fileInput"
      @change="handleFileChange"
      style="display: none"
      accept=".csv"
    />
  </div>

  <div class="inputs-wrapper">
    <!-- Text Inputs for additional form data -->
    <input
      type="text"
      v-model="textColumn"
      placeholder="Enter the column of the comments"
    />
    <input
      type="text"
      v-model="topic"
      placeholder="Enter the topic of the comments"
    />
  </div>
  <button type="button" class="upload-button" @click="uploadFile">
    Generate Summaries
  </button>

  <!-- Placeholder for summaries -->
  <div class="loading-items" v-if="summariesLoading">
    <LoadingItem v-for="index in 3" />
  </div>
  <div v-if="summaries?.grouped_summaries && !summariesLoading">
    <h2>Summaries</h2>
    <div class="summaries-wrapper">
      <div
        v-for="(item, index) in summaries?.grouped_summaries"
        class="summary-item"
      >
        <h3>Summary {{ index + 1 }}</h3>
        <p>
          {{ item.summary }}
        </p>
        <ul v-if="item.top_topics" class="topics-list">
          <li v-for="topic in item.top_topics" class="topic-item">
            <span class="number">{{ topic[1] }}</span>
            <span> {{ topic[0] }}</span>
          </li>
        </ul>
        <button @click="openTopicsModal(item)">View Comments</button>
        <div class="summary-time">
          <div>
            <b>Started: </b>{{ formatDate(item.start_time) }} - <b>Ended: </b
            >{{ formatDate(item.end_time) }}
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Placeholder for final summary -->
  <div v-if="summaries?.final_summary">
    <h2>Final Summary</h2>
    <div class="summary-item">
      {{ summaries?.final_summary }}
    </div>
    <!-- This will display the final summary -->
  </div>
  <Modal
    v-if="currentSummary"
    :summary="currentSummary"
    :isVisible="showModal"
    @close="showModal = false"
  />
</template>

<script setup>
import Modal from './components/Modal.vue'
import LoadingItem from './components/LoadingItem.vue'
import response from './testing/response'
import { formatDate } from './helpers/formaters.js'
import { ref } from 'vue'

const fileInput = ref(null)
const textColumn = ref('')
const topic = ref('')
const summaries = ref(null)
const selectedFile = ref(null)
const summariesLoading = ref(false)
const showModal = ref(false)
const topicsList = ref(['Topic 1', 'Topic 2', 'Topic 3'])
const currentSummary = ref(null)

// console.log(response)
// summaries.value = response //only for testing

// Trigger file input when user clicks on "browse"
function triggerFileInput() {
  fileInput.value.click()
}

// Handle file drop event
function handleDrop(event) {
  const files = event.dataTransfer.files
  processFile(files[0])
}

// Handle file selection from browse
function handleFileChange(event) {
  const file = event.target.files[0]
  processFile(file)
}

// Process the uploaded file
function processFile(file) {
  if (file) {
    selectedFile.value = file // Store the selected file for upload
  }
}

async function uploadFile() {
  if (!selectedFile.value) {
    alert('Please select a file.')
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  formData.append('text_column', textColumn.value)
  formData.append('topic', topic.value)

  // Upload the file and the text column via POST request
  const response = await fetch('/upload', {
    method: 'POST',
    body: formData,
  })

  const data = await response.json()
  if (data.success) {
    summariesLoading.value = true
    fetchSummary()
  } else {
    summariesLoading.value = false
    alert('File upload failed!')
  }
}

async function fetchSummary() {
  summariesLoading.value = true
  const response = await fetch('/get_grouped_summaries', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text_column: textColumn.value }), // pass text column
  })

  const data = await response.json()
  if (data) {
    summaries.value = data
    summariesLoading.value = false
    console.log(data)
  } else {
    summariesLoading.value = false
    alert('Failed to generate summaries.')
  }
}
function openTopicsModal(item) {
  currentSummary.value = item
  showModal.value = true
}
</script>

<style>
/* Styles for the drag and drop file input */
.file-upload-container {
  text-align: center;
  padding: 20px;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 16px;
  margin-bottom: 10px;
}

.drop-zone {
  width: 100%;
  height: 200px;
  border: 2px dashed #c2cdda;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background-color: #fff;
  transition: background-color 0.3s ease;
}

.drop-zone:hover {
  background-color: #f0f8ff;
}

.upload-icon {
  width: 40px;
  margin-bottom: 10px;
}

.browse-link {
  color: #007bff;
  cursor: pointer;
  text-decoration: underline;
}

.drop-zone p {
  margin: 0;
  font-size: 14px;
}

small {
  font-size: 12px;
  color: #6c757d;
}

/* Additional form input styles */
input[type='text'] {
  display: block;
  margin-top: 10px;
}

.upload-button {
  display: block;
  margin: 20px auto;
  padding: 10px 20px;
  font-size: 14px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  min-width: 200px;
}

button:hover {
  background-color: #0056b3;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}
.inputs-wrapper {
  display: flex;
  gap: 30px;
  justify-content: center;
  margin-top: 10px;
  input {
    width: 100%;
    padding: 9px;
    border-radius: 8px;
    border: 1px solid #c1c1c1;
    font-size: 14px;
  }
}

.selected-file {
  margin-top: 10px;
  padding: 5px 20px;
  border-radius: 6px;
  background-color: #21c50044;
}

.summary-item {
  padding: 15px 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.summary-item h3 {
  margin-top: 0;
  font-weight: 500;
  margin-bottom: 5px;
}
.summary-item:hover {
  background-color: #f9f9f9;
}
.summary-item p {
  margin-bottom: 5px;
}
.summary-item button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 7px 20px;
  cursor: pointer;
  font-size: 14px;
  margin-top: 15px;
}
.summary-item button:hover {
  background-color: #0056b3;
}
.topics-list {
  display: flex;
  list-style: none;
  padding: 0;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 15px;
}
.topics-list li {
  display: flex;
  padding: 2px 10px 2px 6px;
  align-items: center;
  border-radius: 20px;
  background-color: #c8e3ff;
  gap: 10px;
}
.topics-list li .number {
  height: 20px;
  width: 20px;
  display: flex;
  padding: 3px;
  background-color: #fff;
  border-radius: 50%;
  align-items: center;
  justify-content: center;
}
.summary-time {
  font-size: 13px;
  text-align: right;
  margin-top: 13px;
  width: fit-content;
  margin-left: auto;
  background-color: #ededed;
  padding: 2px 10px;
  color: #6f6f6f;
  border-radius: 4px;
}
.summary-time b {
  font-weight: 600;
}
</style>
