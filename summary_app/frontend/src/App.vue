<template>
  <div class="app-container">
    <h1>Comments Summary and Topics</h1>

    <!-- File upload form -->
    <form id="uploadForm" class="upload-form" enctype="multipart/form-data">
      <input type="file" id="fileInput" name="file" accept=".csv" class="file-input">
      <input type="text" id="textColumnInput" name="text_column" placeholder="Enter the column of the comments" class="input-box">
      <input type="text" id="topicInput" name="topic" placeholder="Enter the topic of the comments" class="input-box">
      <button type="button" class="upload-button" @click="uploadFile">Upload CSV</button>
    </form>

    <!-- Topics and Summaries Section -->
    <div class="content-container">
      <div id="summary-container" class="summary-container">
        <!-- Loop through groupedSummaries -->
        <div v-for="(group, groupIndex) in groupedSummaries" :key="groupIndex" class="group-item">

          <!-- Topics displayed horizontally for each comment -->
          <div class="comments-topics-horizontal">
            <!-- Loop through comments for each group -->
            <div v-for="(comment, commentIndex) in group.comments" :key="commentIndex" class="comment-topics">
              <!-- Display topics as horizontal nodes for each comment -->
              <div class="topics">
                <span v-for="(topic, topicIndex) in comment.topics" :key="topicIndex" class="topic-node">
                  {{ topic }}
                </span>
              </div>
            </div>
          </div>

          <!-- Group Summary -->
          <div class="group-summary">
            <h4>Summary of Above Comments:</h4>
            <p>{{ group.summary }}</p>
          </div>

        </div>
      </div>
    </div>

    <!-- Final Summary Section -->
    <div id="final-summary-container" class="final-summary-container">
      <h2>Final Summary</h2>
      <p id="final-summary">{{ finalSummary }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const groupedSummaries = ref([]);
const finalSummary = ref('');

async function uploadFile() {
  const formData = new FormData();
  const fileInput = document.getElementById('fileInput');
  const textColumnInput = document.getElementById('textColumnInput').value;
  const topicInput = document.getElementById('topicInput').value;
  formData.append('file', fileInput.files[0]);
  formData.append('text_column', textColumnInput);
  formData.append('topic', topicInput);

  const response = await fetch('/upload', {
    method: 'POST',
    body: formData
  });

  const data = await response.json();
  if (data.success) {
    alert("File uploaded successfully! Processing...");
    fetchCompleteSummary();
  } else {
    alert("File upload failed!");
  }
}

async function fetchCompleteSummary() {
  const response = await fetch('/get_grouped_summaries', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text_column: document.getElementById('textColumnInput').value,
      topic: document.getElementById('topicInput').value
    })
  });
  const data = await response.json();

  console.log(data);

  groupedSummaries.value = data.grouped_summaries;
  finalSummary.value = data.final_summary;
}
</script>

<style scoped>
.app-container {
  background-color: #f4f4f4;
  padding: 50px;
  border-radius: 20px;
  max-width: 100%;
  margin: 40px auto; 
  font-family: 'Arial', sans-serif;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* Added shadow for a clean look */
}

h1 {
  text-align: center;
  font-size: 32px; /* Increased font size */
  color: #333;
}

.upload-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px; /* Increased gap */
  margin-bottom: 30px; /* Increased margin */
}

.file-input, .input-box {
  padding: 12px;
  font-size: 16px;
  width: 1000px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.upload-button {
  background-color: #007bff;
  color: white;
  padding: 12px 25px;
  font-size: 16px; /* Increased font size */
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.upload-button:hover {
  background-color: #0056b3;
}

.content-container {
  background-color: white;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.1);
}

.summary-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.group-item {
  display: flex;
  flex-direction: column;
  background-color: #f0f8ff;
  padding: 20px;
  border: 2px solid #007bff;  /* Added blue border */
  border-radius: 15px;
  margin-bottom: 40px; /* Added spacing between groups */
}

.comments-topics-horizontal {
  display: flex; /* Makes topics horizontal */
  flex-wrap: wrap; /* Ensures topics wrap to the next line if they overflow */
  gap: 20px; /* Space between topics */
  margin-bottom: 20px; /* Space between topics and summary */
}

.topic-node {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border-radius: 50px;
  font-size: 14px;
  text-align: center;
  display: inline-block;
}

.group-summary {
  font-size: 18px;
  margin-top: 15px;
}

.group-summary h4 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.final-summary-container {
  margin-top: 50px;
  background-color: #f8f9fa;
  padding: 40px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 28px;
  color: #333;
}

#final-summary {
  font-size: 20px;
  color: #555;
}
</style>
