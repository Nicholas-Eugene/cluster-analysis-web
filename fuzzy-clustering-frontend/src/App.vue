<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-logo">
          <h2>Clustering FCM</h2>
        </router-link>
        <ul class="nav-menu">
          <li class="nav-item">
            <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
              Beranda
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/upload" class="nav-link" :class="{ active: $route.path === '/upload' }">
              Unggah Dataset
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/analysis" class="nav-link" :class="{ active: $route.path === '/analysis' }">
              Analisis & Visualisasi
            </router-link>
          </li>
        </ul>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 Clustering Profil Kemiskinan - Fuzzy C-Means Algorithm</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.nav-logo h2 {
  color: white;
  margin: 0;
  font-weight: 600;
  text-decoration: none;
}

.nav-logo {
  text-decoration: none;
}

.nav-menu {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}

.main-content {
  min-height: calc(100vh - 140px);
  padding: 2rem 0;
}

.footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    height: auto;
    padding: 1rem;
  }
  
  .nav-menu {
    margin-top: 1rem;
    gap: 1rem;
  }
  
  .nav-link {
    padding: 0.5rem;
    font-size: 0.9rem;
  }
}
</style>