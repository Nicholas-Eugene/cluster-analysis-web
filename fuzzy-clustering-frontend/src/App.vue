<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-logo">
          <h2>Pemetaan Wilayah Kemiskinan</h2>
        </router-link>
        <ul class="nav-menu">
          <li class="nav-item dropdown">
            <a href="#" class="nav-link dropdown-toggle" :class="{ active: $route.path === '/' }" @click.prevent="toggleDropdown">
              Beranda
              <span class="dropdown-arrow">▼</span>
            </a>
            <ul class="dropdown-menu" :class="{ show: isDropdownOpen }">
              <li><a href="/#title" class="dropdown-link" @click="closeDropdown">🏠 Title</a></li>
              <li><a href="/#about" class="dropdown-link" @click="closeDropdown">🌟 Algoritma</a></li>
              <li><a href="/#data" class="dropdown-link" @click="closeDropdown">📊 Data</a></li>
              <li><a href="/#background" class="dropdown-link" @click="closeDropdown">📖 Latar Belakang</a></li>
              <li><a href="/#features" class="dropdown-link" @click="closeDropdown">⚙️ Fitur</a></li>
            </ul>
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
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'App',
  setup() {
    const isDropdownOpen = ref(false)

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }

    const closeDropdown = () => {
      isDropdownOpen.value = false
    }

    return {
      isDropdownOpen,
      toggleDropdown,
      closeDropdown
    }
  }
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
  gap: 1rem;
  align-items: center;
}

.nav-item {
  display: flex;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 1rem;
}

.nav-link:hover,
.nav-link.active {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}

.nav-item.dropdown {
  position: relative;
}

.dropdown-toggle {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.dropdown-arrow {
  font-size: 0.6rem;
  transition: transform 0.3s ease;
  display: inline-block;
  margin-left: 0.25rem;
}

.nav-item.dropdown:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  padding: 0.5rem 0;
  margin-top: 0.5rem;
  list-style: none;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  z-index: 1000;
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-menu li {
  margin: 0;
}

.dropdown-link {
  display: block;
  padding: 0.75rem 1.5rem;
  color: #4a5568;
  text-decoration: none;
  transition: all 0.2s ease;
  font-weight: 500;
}

.dropdown-link:hover {
  background: #f7fafc;
  color: #667eea;
  padding-left: 2rem;
}

.main-content {
  min-height: calc(100vh - 70px);
  padding: 2rem 0;
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