<template>
  <div class="loading-card">
    <div class="loading-line"></div>
    <div class="loading-line"></div>
    <div class="loading-line short"></div>
    <div class="loading-line short"></div>
  </div>
</template>

<script setup>
// No extra logic required for this simple component
</script>

<style scoped>
.loading-card {
  width: 100%;
  height: 130px;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  background-color: #f9f9f9;
  margin-bottom: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.loading-line {
  height: 15px;
  background-color: #e0e0e0;
  border-radius: 5px;
  animation: loading 1.5s infinite;
}

.loading-line.short {
  width: 70%;
}

@keyframes loading {
  0% {
    background-color: #e0e0e0;
  }
  50% {
    background-color: #d0d0d0;
  }
  100% {
    background-color: #e0e0e0;
  }
}
</style>
