<template>
    <h1>Comments Summary and Topics</h1>

    <!-- File upload form -->
    <form id="uploadForm" enctype="multipart/form-data">
        <input type="file" id="fileInput" name="file" accept=".csv">
        <input type="text" id="textColumnInput" name="text_column" placeholder="Enter the column of the comments"
               style="height: 16px; width: 200px; font-size: 11px;">
        <input type="text" id="topicInput" name="topic" placeholder="Enter the topic of the comments"
               style="height: 16px; width: 200px; font-size: 11px;">
        <button type="button" @click="uploadFile">Upload CSV</button>
    </form>

    <!-- Placeholder for summaries -->
    <div id="summary-container"></div>

    <!-- Placeholder for final summary -->
    <div id="final-summary-container" style="margin-top: 20px;">
        <h2>Final Summary</h2>
        <p id="final-summary"></p> <!-- This will display the final summary -->
    </div>

</template>
<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'

 async function uploadFile() {
            const formData = new FormData();
            const fileInput = document.getElementById('fileInput');
            const textColumnInput = document.getElementById('textColumnInput').value;
            const topicInput = document.getElementById('topicInput').value;
            formData.append('file', fileInput.files[0]);
            formData.append('text_column', textColumnInput);
            formData.append('topic', topicInput);

            // Upload the file and the text column via POST request
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (data.success) {
                alert("File uploaded successfully! Processing...");
                // Now, you can trigger the fetch summary or topic extraction functions
                fetchSummary();
                //fetchTopics();
            } else {
                alert("File upload failed!");
            }
        }

        async function fetchSummary() {
            const response = await fetch('/get_grouped_summaries', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text_column: document.getElementById('textColumnInput').value  // pass text column
                })
            });
            const data = await response.json();
            console.log(data);
            document.getElementById('summary-container').innerText = data.summaries.join("\n");
        }

        async function fetch_finalSummary() {
            const response = await fetch('/get_final_summary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    topic: document.getElementById('topicInput').value  // pass topic if needed
                })
            });

            const data = await response.json();

            // Check if the final_summary exists in the response
            if (data.final_summary) {
                // Display the final summary in the designated paragraph element
                document.getElementById('final-summary').innerText = data.final_summary;
            } else {
                // Handle error or empty response
                alert('No final summary available or an error occurred.');
            }
        }

        function visualizeTopics(data) {
            const ctx = document.getElementById('topicsChart').getContext('2d');
            const topics = data.map(item => item.topics);

            // Visualization of topics over time using Chart.js
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.map(item => item.comment),  // Use comment index as labels
                    datasets: [{
                        label: 'Topics Over Time',
                        data: topics,
                        fill: false,
                        borderColor: 'blue',
                        tension: 0.1
                    }]
                }
            });
        }

</script>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
