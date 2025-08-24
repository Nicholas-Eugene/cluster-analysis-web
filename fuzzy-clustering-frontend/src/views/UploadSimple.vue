<template>
  <div class="upload-page">
    <div class="container">
      <h1>Test Upload Page</h1>
      <p>Jika halaman ini muncul, berarti routing berfungsi dengan baik.</p>
      
      <div class="card">
        <h2>Basic Upload Form</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Upload File:</label>
            <input type="file" ref="fileInput" accept=".csv" />
          </div>
          
          <div class="form-group">
            <label>Jumlah Cluster:</label>
            <input type="number" v-model="numClusters" min="2" max="10" />
          </div>
          
          <button type="submit" class="btn">Submit</button>
        </form>
        
        <div v-if="message" class="alert">
          {{ message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'UploadSimple',
  setup() {
    const fileInput = ref(null)
    const numClusters = ref(3)
    const message = ref('')
    
    const handleSubmit = () => {
      message.value = 'Form submitted successfully!'
      console.log('File:', fileInput.value?.files[0])
      console.log('Clusters:', numClusters.value)
    }
    
    return {
      fileInput,
      numClusters,
      message,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.upload-page {
  padding: 2rem;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin: 2rem 0;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn {
  background: #007bff;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background: #0056b3;
}

.alert {
  margin-top: 1rem;
  padding: 1rem;
  background: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 4px;
  color: #155724;
}
</style>