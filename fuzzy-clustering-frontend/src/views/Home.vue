<template>
  <div class="home">
    <div class="container">
      <section id="title" class="hero">
        <div class="hero-content">
          <h1 class="hero-title">
            Rancangan Pemetaan Wilayah Kemiskinan di Indonesia
            Berdasarkan IPM, Garis Kemiskinan & Pengeluaran Per Kapita
          </h1>
          <p class="hero-subtitle">
            Analisis clustering menggunakan algoritma Fuzzy C-Means dan OPTICS untuk mengidentifikasi 
            pola pembangunan dan kemiskinan di berbagai wilayah Indonesia (2015-2024)
          </p>
          <div class="hero-actions">
            <router-link to="/upload" class="btn btn-lg">
              Mulai Analisis
            </router-link>
            <a href="#about" class="btn btn-secondary btn-lg">
              Pelajari Lebih Lanjut
            </a>
          </div>
        </div>
        <div class="hero-image">
          <div class="hero-illustration">
            <div class="data-points">
              <div class="data-point" v-for="i in 12" :key="i"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- About Algorithm Section -->
      <section id="about" class="about-section">
        <div class="card">
          <h2 class="section-title">Algoritma Clustering yang Didukung</h2>
          <div class="algorithm-grid">
            <div class="algorithm-card">
              <div class="algorithm-header">
                <div class="algorithm-icon">🌟</div>
                <h3>Fuzzy C-Means (FCM)</h3>
              </div>
              <p>
                Algoritma clustering fuzzy yang memberikan tingkat keanggotaan untuk setiap data point ke dalam cluster.
                Sangat efektif untuk data yang memiliki batas cluster yang tidak jelas.
              </p>
              <h4>Keunggulan FCM:</h4>
              <ul class="feature-list">
                <li>Dapat menangani overlapping cluster</li>
                <li>Memberikan informasi tingkat ketidakpastian</li>
                <li>Robust terhadap noise dan outlier</li>
                <li>Fleksibel untuk berbagai jenis data</li>
              </ul>
            </div>
            
            <div class="algorithm-card">
              <div class="algorithm-header">
                <div class="algorithm-icon">🔍</div>
                <h3>OPTICS</h3>
              </div>
              <p>
                Algoritma clustering berbasis density yang dapat menemukan cluster dengan bentuk arbitrary 
                dan menangani noise. Tidak memerlukan penentuan jumlah cluster di awal.
              </p>
              <h4>Keunggulan OPTICS:</h4>
              <ul class="feature-list">
                <li>Mendeteksi cluster dengan bentuk tidak beraturan</li>
                <li>Menangani noise dan outlier dengan baik</li>
                <li>Otomatis menentukan jumlah cluster</li>
                <li>Robust untuk data dengan densitas bervariasi</li>
              </ul>
            </div>
          </div>
            
        </div>
      </section>

      <!-- Data Information Section -->
      <section id="data" class="data-section">
        <div class="card">
          <h2 class="section-title">Data yang Dianalisis</h2>
          <div class="grid grid-3">
            <div class="data-item">
              <div class="data-icon">📊</div>
              <h3>Indeks Pembangunan Manusia (IPM)</h3>
              <p>
                Indikator komposit yang mengukur pencapaian rata-rata dalam dimensi 
                dasar pembangunan manusia: kesehatan, pendidikan, dan standar hidup.
              </p>
            </div>
            <div class="data-item">
              <div class="data-icon">💰</div>
              <h3>Garis Kemiskinan</h3>
              <p>
                Nilai rupiah pengeluaran minimum yang diperlukan untuk memenuhi 
                kebutuhan pokok hidup yang layak di suatu wilayah.
              </p>
            </div>
            <div class="data-item">
              <div class="data-icon">💳</div>
              <h3>Pengeluaran Per Kapita</h3>
              <p>
                Rata-rata pengeluaran per kapita yang mencerminkan daya beli 
                dan standar hidup masyarakat di suatu wilayah.
              </p>
            </div>
          </div>
          <div class="grid grid-2" style="margin-top: 2rem;">
            <div class="data-item">
              <div class="data-icon">🗺️</div>
              <h3>Data Kabupaten/Kota</h3>
              <p>
                Analisis dilakukan pada tingkat kabupaten/kota di seluruh Indonesia 
                dengan data time series untuk melihat tren temporal.
              </p>
            </div>
            <div class="data-item">
              <div class="data-icon">📅</div>
              <h3>Data Time Series (2015-2024)</h3>
              <p>
                Data longitudinal selama 10 tahun untuk menganalisis perubahan 
                pola pembangunan dan kemiskinan dari waktu ke waktu.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Background Section -->
      <section id="background" class="background-section">
        <div class="card">
          <h2 class="section-title">Latar Belakang Penelitian</h2>
          <div class="background-content">
            <p>
              Indonesia sebagai negara kepulauan dengan keragaman ekonomi dan sosial yang tinggi 
              memiliki tantangan dalam pemerataan pembangunan. Disparitas kemiskinan antar wilayah 
              menjadi isu penting yang memerlukan analisis mendalam untuk perumusan kebijakan yang tepat.
            </p>
            
            <p>
              Penelitian ini bertujuan untuk mengidentifikasi pola dan karakteristik kemiskinan 
              di berbagai kabupaten/kota di Indonesia menggunakan pendekatan clustering dengan 
              algoritma Fuzzy C-Means. Dengan menganalisis data IPM dan Garis Kemiskinan, 
              diharapkan dapat diperoleh insights yang berguna untuk:
            </p>
            
            <div class="objectives">
              <div class="objective">
                <h4>🎯 Identifikasi Pola Kemiskinan</h4>
                <p>Mengelompokkan wilayah berdasarkan karakteristik kemiskinan yang serupa</p>
              </div>
              <div class="objective">
                <h4>📈 Analisis Tren Temporal</h4>
                <p>Memahami perubahan profil kemiskinan dari waktu ke waktu</p>
              </div>
              <div class="objective">
                <h4>🏛️ Dukungan Kebijakan</h4>
                <p>Memberikan basis data untuk perumusan kebijakan pembangunan yang targeted</p>
              </div>
              <div class="objective">
                <h4>⚖️ Evaluasi Disparitas</h4>
                <p>Mengukur tingkat kesenjangan pembangunan antar wilayah</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section id="features" class="features-section">
        <div class="card">
          <h2 class="section-title">Fitur Aplikasi</h2>
          <div class="grid grid-3">
            <div class="feature-card">
              <div class="feature-icon">📤</div>
              <h3>Upload Dataset</h3>
              <p>Upload file CSV dengan data IPM, Garis Kemiskinan, dan Pengeluaran Per Kapita per kabupaten/kota</p>
              <router-link to="/upload" class="feature-link">Mulai Upload →</router-link>
            </div>
            <div class="feature-card">
              <div class="feature-icon">⚙️</div>
              <h3>Pilih Algoritma</h3>
              <p>Pilih antara Fuzzy C-Means atau OPTICS dengan konfigurasi parameter yang sesuai</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">📊</div>
              <h3>Visualisasi Interaktif</h3>
              <p>Dashboard dengan peta interaktif, scatter plot, box plot, dan metrik evaluasi clustering</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      // Animation data for hero illustration
    }
  },
  mounted() {
    this.animateDataPoints()
  },
  methods: {
    animateDataPoints() {
      // Simple animation for data points in hero section
      const points = document.querySelectorAll('.data-point')
      points.forEach((point, index) => {
        setTimeout(() => {
          point.style.opacity = '1'
          point.style.transform = 'scale(1)'
        }, index * 100)
      })
    }
  }
}
</script>

<style scoped>
.home {
  padding: 0;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  min-height: 70vh;
}

.hero-content {
  padding: 2rem;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

.hero-image {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.hero-illustration {
  width: 300px;
  height: 300px;
  position: relative;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.data-points {
  position: relative;
  width: 200px;
  height: 200px;
}

.data-point {
  position: absolute;
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  opacity: 0;
  transform: scale(0);
  transition: all 0.5s ease;
}

.data-point:nth-child(1) { top: 20%; left: 50%; }
.data-point:nth-child(2) { top: 35%; left: 75%; }
.data-point:nth-child(3) { top: 50%; left: 85%; }
.data-point:nth-child(4) { top: 65%; left: 75%; }
.data-point:nth-child(5) { top: 80%; left: 50%; }
.data-point:nth-child(6) { top: 65%; left: 25%; }
.data-point:nth-child(7) { top: 50%; left: 15%; }
.data-point:nth-child(8) { top: 35%; left: 25%; }
.data-point:nth-child(9) { top: 45%; left: 45%; }
.data-point:nth-child(10) { top: 55%; left: 55%; }
.data-point:nth-child(11) { top: 40%; left: 60%; }
.data-point:nth-child(12) { top: 60%; left: 40%; }

.section-title {
  font-size: 2.5rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 3rem;
  color: #2d3748;
}

.about-section {
  padding: 4rem 0;
}

.algorithm-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.algorithm-card {
  background: #f7fafc;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.algorithm-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.algorithm-icon {
  font-size: 2rem;
}

.algorithm-card h3 {
  color: #2d3748;
  margin: 0;
  font-size: 1.5rem;
}

.algorithm-card p {
  color: #718096;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.algorithm-card h4 {
  color: #4a5568;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.about-content h3 {
  color: #4a5568;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.about-content p {
  margin-bottom: 2rem;
  line-height: 1.7;
  color: #718096;
}

.feature-list {
  list-style: none;
  padding: 0;
}

.feature-list li {
  padding: 0.5rem 0;
  position: relative;
  padding-left: 2rem;
  color: #718096;
}

.feature-list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #38a169;
  font-weight: bold;
}

.algorithm-steps h3 {
  color: #4a5568;
  margin-bottom: 2rem;
  font-size: 1.5rem;
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.step-number {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content h4 {
  margin-bottom: 0.5rem;
  color: #4a5568;
}

.step-content p {
  color: #718096;
  line-height: 1.5;
}

.data-section {
  padding: 4rem 0;
  background: #f7fafc;
}

.data-item {
  text-align: center;
  padding: 2rem;
}

.data-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.data-item h3 {
  color: #4a5568;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.data-item p {
  color: #718096;
  line-height: 1.6;
}

.background-section {
  padding: 4rem 0;
}

.background-content p {
  margin-bottom: 2rem;
  line-height: 1.7;
  color: #718096;
  font-size: 1.1rem;
}

.objectives {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.objective {
  background: #f7fafc;
  padding: 2rem;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.objective h4 {
  color: #4a5568;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.objective p {
  color: #718096;
  line-height: 1.6;
  margin: 0;
}

.features-section {
  padding: 4rem 0;
  background: #f7fafc;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #4a5568;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.feature-card p {
  color: #718096;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.feature-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.feature-link:hover {
  color: #764ba2;
}

@media (max-width: 968px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 3rem 0;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-actions {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .objectives {
    grid-template-columns: 1fr;
  }
}
</style>