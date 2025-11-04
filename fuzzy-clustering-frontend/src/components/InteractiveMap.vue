<template>
  <div class="map-container">
    <div class="map-header">
      <h3>{{ title }}</h3>
      <div class="map-controls">
        <div class="cluster-filter">
          <label>Filter Cluster:</label>
          <select v-model="selectedClusterFilter" @change="updateMapView">
            <option value="all">Semua Cluster</option>
            <option v-for="cluster in clusters" :key="cluster.id" :value="cluster.id">
              {{ cluster.interpretation?.label || `Cluster ${cluster.id}` }}
            </option>
          </select>
        </div>
        <div class="map-info">
          <span>{{ filteredMarkers.length }} daerah ditampilkan</span>
        </div>
      </div>
    </div>
    
    <div class="map-wrapper">
      <div id="map" ref="mapContainer"></div>
    </div>
    
    <div class="map-legend">
      <h4>Legenda Cluster</h4>
      <div class="legend-items">
        <div v-for="(cluster, index) in clusters" :key="cluster.id" class="legend-item">
          <div class="legend-marker" :style="{ backgroundColor: getClusterColor(index) }"></div>
          <span>Cluster {{ cluster.id }} ({{ cluster.size }} daerah)</span>
        </div>
      </div>
      <div class="map-stats">
        <div class="stat-item">
          <strong>Total Daerah:</strong> {{ totalRegions }}
        </div>
        <div class="stat-item">
          <strong>Daerah Terplot:</strong> {{ mappedRegions }}
        </div>
        <div class="stat-item">
          <strong>Coverage:</strong> {{ coveragePercentage }}%
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import L from 'leaflet'

// Fix for default markers in Leaflet with Vite
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

// Indonesian city coordinates - comprehensive dataset
const cityCoords = {
  "Simeulue": [
    2.46158,
    96.38105
  ],
  "Aceh Singkil": [
    2.28411,
    97.79769
  ],
  "Aceh Selatan": [
    3.26142,
    97.17933
  ],
  "Aceh Tenggara": [
    3.48673,
    97.81081
  ],
  "Aceh Timur": [
    4.94789,
    97.77651
  ],
  "Aceh Tengah": [
    4.63464,
    96.84219
  ],
  "Aceh Barat": [
    4.14499,
    96.13576
  ],
  "Aceh Besar": [
    5.29718,
    95.61156
  ],
  "Pidie": [
    5.3855,
    95.96064
  ],
  "Bireuen": [
    5.22198,
    96.71688
  ],
  "Aceh Utara": [
    5.05131,
    97.3212
  ],
  "Aceh Barat Daya": [
    3.74322,
    96.83422
  ],
  "Gayo Lues": [
    3.99633,
    97.34203
  ],
  "Aceh Tamiang": [
    4.33767,
    98.06355
  ],
  "Nagan Raya": [
    4.16932,
    96.32479
  ],
  "Aceh Jaya": [
    4.63544,
    95.58533
  ],
  "Bener Meriah": [
    4.72733,
    96.86034
  ],
  "Pidie Jaya": [
    5.2288,
    96.24542
  ],
  "Banda Aceh": [
    5.54794,
    95.3208
  ],
  "Sabang": [
    5.89285,
    95.32343
  ],
  "Langsa": [
    4.47185,
    97.9708
  ],
  "Lhokseumawe": [
    5.18112,
    97.14196
  ],
  "Subulussalam": [
    2.67207,
    97.99863
  ],
  "Nias": [
    1.184,
    97.71678
  ],
  "Mandailing Natal": [
    0.85762,
    99.55128
  ],
  "Tapanuli Selatan": [
    1.61383,
    99.2638
  ],
  "Tapanuli Tengah": [
    1.68477,
    98.82859
  ],
  "Tapanuli Utara": [
    2.01208,
    98.97541
  ],
  "Toba Samosir": [
    2.33548,
    99.08092
  ],
  "Labuhan Batu": [
    2.07022,
    99.85752
  ],
  "Asahan": [
    2.99027,
    99.6247
  ],
  "Simalungun": [
    2.96527,
    98.86223
  ],
  "Dairi": [
    2.74462,
    98.31267
  ],
  "Karo": [
    3.10541,
    98.49853
  ],
  "Deli Serdang": [
    3.56642,
    98.87351
  ],
  "Langkat": [
    3.75206,
    98.45366
  ],
  "Nias Selatan": [
    0.56867,
    97.81237
  ],
  "Humbang Hasundutan": [
    2.25305,
    98.75239
  ],
  "Pakpak Bharat": [
    2.55477,
    98.32467
  ],
  "Samosir": [
    2.62443,
    98.71453
  ],
  "Serdang Bedagai": [
    3.49339,
    99.12746
  ],
  "Batu Bara": [
    3.1695,
    99.42283
  ],
  "Padang Lawas Utara": [
    1.49467,
    99.62005
  ],
  "Padang Lawas": [
    1.05567,
    99.77641
  ],
  "Labuhan Batu Selatan": [
    1.89094,
    100.09064
  ],
  "Labuhan Batu Utara": [
    2.56308,
    99.65889
  ],
  "Nias Utara": [
    1.62781,
    98.05255
  ],
  "Nias Barat": [
    0.99957,
    97.50747
  ],
  "Sibolga": [
    1.73722,
    98.78456
  ],
  "Tanjung Balai": [
    2.96571,
    99.80037
  ],
  "Pematang Siantar": [
    2.96548,
    99.06529
  ],
  "Tebing Tinggi": [
    3.32635,
    99.15584
  ],
  "Medan": [
    3.59567,
    98.67565
  ],
  "Binjai": [
    3.61307,
    98.50635
  ],
  "Padangsidimpuan": [
    1.37223,
    99.27423
  ],
  "Gunungsitoli": [
    1.28048,
    97.61443
  ],
  "Kepulauan Mentawai": [
    -2.05399,
    99.58156
  ],
  "Pesisir Selatan": [
    -1.34743,
    100.57733
  ],
  "Solok": [
    -0.95199,
    100.62313
  ],
  "Sijunjung": [
    -0.66569,
    100.94518
  ],
  "Tanah Datar": [
    -0.45633,
    100.59637
  ],
  "Padang Pariaman": [
    -0.62037,
    100.30693
  ],
  "Agam": [
    -0.33059,
    100.06728
  ],
  "Lima Puluh Kota": [
    -0.15246,
    100.66111
  ],
  "Pasaman": [
    0.14054,
    100.16767
  ],
  "Solok Selatan": [
    -1.55631,
    101.24231
  ],
  "Dharmasraya": [
    -0.95265,
    101.49455
  ],
  "Pasaman Barat": [
    0.11029,
    99.83117
  ],
  "Padang": [
    -0.94625,
    100.35829
  ],
  "Solok": [
    -0.78917,
    100.65486
  ],
  "Sawah Lunto": [
    -0.59967,
    100.74631
  ],
  "Padang Panjang": [
    -0.46651,
    100.39621
  ],
  "Bukittinggi": [
    -0.30396,
    100.38365
  ],
  "Payakumbuh": [
    -0.22417,
    100.63241
  ],
  "Pariaman": [
    -0.62723,
    100.12094
  ],
  "Kuantan Singingi": [
    -0.50513,
    101.53884
  ],
  "Indragiri Hulu": [
    -0.38902,
    102.54892
  ],
  "Indragiri Hilir": [
    -0.32194,
    103.15294
  ],
  "Pelalawan": [
    0.38379,
    101.84244
  ],
  "Siak": [
    0.80509,
    102.02092
  ],
  "Kampar": [
    0.34134,
    101.02889
  ],
  "Rokan Hulu": [
    0.89319,
    100.30318
  ],
  "Bengkalis": [
    1.49445,
    102.0916
  ],
  "Rokan Hilir": [
    2.1573,
    100.81573
  ],
  "Kepulauan Meranti": [
    0.98296,
    102.69906
  ],
  "Pekanbaru": [
    0.50486,
    101.44115
  ],
  "Dumai": [
    1.66449,
    101.40149
  ],
  "Kerinci": [
    -1.93578,
    101.34254
  ],
  "Merangin": [
    -2.07291,
    102.27457
  ],
  "Sarolangun": [
    -2.31262,
    102.75354
  ],
  "Batang Hari": [
    -1.6597,
    103.28027
  ],
  "Muaro Jambi": [
    -1.44812,
    103.51612
  ],
  "Tanjung Jabung Timur": [
    -1.20569,
    103.79294
  ],
  "Tanjung Jabung Barat": [
    -0.81637,
    103.46271
  ],
  "Tebo": [
    -1.4662,
    102.35888
  ],
  "Bungo": [
    -1.51616,
    102.11988
  ],
  "Jambi": [
    -1.61146,
    103.61261
  ],
  "Sungai Penuh": [
    -2.06345,
    101.3944
  ],
  "Ogan Komering Ulu": [
    -4.11223,
    104.17791
  ],
  "Ogan Komering Ilir": [
    -3.41139,
    104.82364
  ],
  "Muara Enim": [
    -3.66474,
    103.77288
  ],
  "Lahat": [
    -3.78521,
    103.54079
  ],
  "Musi Rawas": [
    -3.24521,
    103.03355
  ],
  "Musi Banyuasin": [
    -2.88888,
    103.84034
  ],
  "Banyu Asin": [
    -2.88766,
    104.39386
  ],
  "Ogan Komering Ulu Selatan": [
    -4.53473,
    104.06858
  ],
  "Ogan Komering Ulu Timur": [
    -4.31419,
    104.34543
  ],
  "Ogan Ilir": [
    -3.24141,
    104.66583
  ],
  "Empat Lawang": [
    -3.59113,
    103.08192
  ],
  "Penukal Abab Lematang Ilir": [
    -3.30959,
    103.88453
  ],
  "Musi Rawas Utara": [
    -2.73513,
    102.90215
  ],
  "Palembang": [
    -2.97622,
    104.77738
  ],
  "Prabumulih": [
    -3.42144,
    104.24406
  ],
  "Pagar Alam": [
    -4.04082,
    103.22557
  ],
  "Lubuklinggau": [
    -3.29964,
    102.85806
  ],
  "Bengkulu Selatan": [
    -4.34188,
    103.04563
  ],
  "Rejang Lebong": [
    -3.46527,
    102.52544
  ],
  "Bengkulu Utara": [
    -3.43868,
    102.1947
  ],
  "Kaur": [
    -4.75886,
    103.34933
  ],
  "Seluma": [
    -4.07749,
    102.55662
  ],
  "Mukomuko": [
    -2.57427,
    101.13082
  ],
  "Lebong": [
    -3.15737,
    102.18304
  ],
  "Kepahiang": [
    -3.65188,
    102.57711
  ],
  "Bengkulu Tengah": [
    -3.77276,
    102.39047
  ],
  "Bengkulu": [
    -3.79143,
    102.25788
  ],
  "Lampung Barat": [
    -5.01884,
    104.06096
  ],
  "Tanggamus": [
    -5.49223,
    104.62189
  ],
  "Lampung Selatan": [
    -5.73466,
    105.59582
  ],
  "Lampung Timur": [
    -5.0684,
    105.54633
  ],
  "Lampung Tengah": [
    -4.98283,
    105.21336
  ],
  "Lampung Utara": [
    -4.82496,
    104.89532
  ],
  "Way Kanan": [
    -4.50596,
    104.51212
  ],
  "Tulangbawang": [
    -4.48052,
    105.24169
  ],
  "Pesawaran": [
    -5.38307,
    105.09003
  ],
  "Pringsewu": [
    -5.34407,
    105.00716
  ],
  "Mesuji": [
    -3.87201,
    105.43494
  ],
  "Tulang Bawang Barat": [
    -4.49926,
    105.12029
  ],
  "Pesisir Barat": [
    -5.19005,
    103.93374
  ],
  "Bandar Lampung": [
    -5.39542,
    105.26403
  ],
  "Metro": [
    -5.11834,
    105.30689
  ],
  "Bangka": [
    -1.87663,
    106.11354
  ],
  "Belitung": [
    -2.74015,
    107.65323
  ],
  "Bangka Barat": [
    -2.06457,
    105.16147
  ],
  "Bangka Tengah": [
    -2.48624,
    106.41238
  ],
  "Bangka Selatan": [
    -2.99909,
    106.46538
  ],
  "Belitung Timur": [
    -2.87051,
    108.27865
  ],
  "Pangkal Pinang": [
    -2.13212,
    106.11606
  ],
  "Karimun": [
    1.03317,
    103.37606
  ],
  "Bintan": [
    1.08914,
    104.50337
  ],
  "Natuna": [
    3.94193,
    108.37965
  ],
  "Lingga": [
    -0.20982,
    104.60489
  ],
  "Kepulauan Anambas": [
    3.21495,
    106.24907
  ],
  "Batam": [
    1.1293,
    104.05023
  ],
  "Tanjung Pinang": [
    0.91815,
    104.46596
  ],
  "Kepulauan Seribu": [
    -5.74657,
    106.61325
  ],
  "Jakarta Selatan": [
    -6.24853,
    106.82941
  ],
  "Jakarta Timur": [
    -6.16631,
    106.76343
  ],
  "Jakarta Pusat": [
    -6.18043,
    106.83372
  ],
  "Jakarta Barat": [
    -6.16637,
    106.76944
  ],
  "Jakarta Utara": [
    -6.14874,
    106.90261
  ],
  "Bogor": [
    -6.48723,
    106.84872
  ],
  "Sukabumi": [
    -7.06086,
    106.71864
  ],
  "Cianjur": [
    -6.81725,
    107.13073
  ],
  "Bandung": [
    -7.02523,
    107.52454
  ],
  "Garut": [
    -7.22791,
    107.9087
  ],
  "Tasikmalaya": [
    -7.35015,
    108.12472
  ],
  "Ciamis": [
    -7.32975,
    108.32957
  ],
  "Kuningan": [
    -6.98333,
    108.48333
  ],
  "Cirebon": [
    -6.75906,
    108.48875
  ],
  "Majalengka": [
    -6.8531,
    108.22589
  ],
  "Sumedang": [
    0.60959,
    110.03306
  ],
  "Indramayu": [
    -6.33632,
    108.3251
  ],
  "Subang": [
    -6.56936,
    107.7524
  ],
  "Purwakarta": [
    -6.53868,
    107.44994
  ],
  "Karawang": [
    -6.32273,
    107.33758
  ],
  "Bekasi": [
    -6.36722,
    107.17228
  ],
  "Bandung Barat": [
    -6.89371,
    107.4322
  ],
  "Pangandaran": [
    -7.6151,
    108.4988
  ],
  "Bogor": [
    -6.59748,
    106.80677
  ],
  "Sukabumi": [
    -6.91776,
    106.93293
  ],
  "Bandung": [
    -6.91776,
    107.62529
  ],
  "Cirebon": [
    -6.73331,
    108.55472
  ],
  "Bekasi": [
    -6.23963,
    106.97715
  ],
  "Depok": [
    -6.40319,
    106.79135
  ],
  "Cimahi": [
    -6.88024,
    107.5355
  ],
  "Tasikmalaya": [
    -7.35152,
    108.21574
  ],
  "Banjar": [
    -7.37129,
    108.53328
  ],
  "Cilacap": [
    -7.69817,
    109.02425
  ],
  "Banyumas": [
    -7.48321,
    109.14044
  ],
  "Purbalingga": [
    -7.39075,
    109.3638
  ],
  "Banjarnegara": [
    -7.40271,
    109.6814
  ],
  "Kebumen": [
    -7.67868,
    109.6565
  ],
  "Purworejo": [
    -7.70973,
    110.008
  ],
  "Wonosobo": [
    -7.36211,
    109.8994
  ],
  "Magelang": [
    -7.55442,
    110.25446
  ],
  "Boyolali": [
    -7.52382,
    110.5959
  ],
  "Klaten": [
    -7.71169,
    110.5955
  ],
  "Sukoharjo": [
    -7.68088,
    110.81953
  ],
  "Wonogiri": [
    -7.81778,
    110.9206
  ],
  "Karanganyar": [
    -7.59611,
    110.95083
  ],
  "Sragen": [
    -7.43023,
    111.0213
  ],
  "Grobogan": [
    -7.02172,
    110.96259
  ],
  "Blora": [
    -6.96932,
    111.41667
  ],
  "Rembang": [
    -6.71124,
    111.3453
  ],
  "Pati": [
    -6.75134,
    111.038
  ],
  "Kudus": [
    -6.80409,
    110.8382
  ],
  "Jepara": [
    -6.55961,
    110.6717
  ],
  "Demak": [
    -6.88811,
    110.6393
  ],
  "Semarang": [
    -7.13652,
    110.4086
  ],
  "Temanggung": [
    -7.31667,
    110.1748
  ],
  "Kendal": [
    -6.91969,
    110.2056
  ],
  "Batang": [
    -6.906159,
    109.72984
  ],
  "Pekalongan": [
    -7.02676,
    109.5805
  ],
  "Pemalang": [
    -6.88423,
    109.378
  ],
  "Tegal": [
    -6.98277,
    109.135513
  ],
  "Brebes": [
    -6.88333,
    109.03947
  ],
  "Magelang": [
    -7.47884,
    110.21993
  ],
  "Surakarta": [
    -7.56667,
    110.81667
  ],
  "Salatiga": [
    -7.30233,
    110.4729
  ],
  "Semarang": [
    -6.98439,
    110.41286
  ],
  "Pekalongan": [
    -6.88981,
    109.67141
  ],
  "Tegal": [
    -6.8796,
    109.12685
  ],
  "Kulon Progo": [
    -7.82668,
    110.16408
  ],
  "Bantul": [
    -7.88461,
    110.33411
  ],
  "Gunung Kidul": [
    -8.03051,
    110.61689
  ],
  "Sleman": [
    -7.71616,
    110.3354
  ],
  "Yogyakarta": [
    -7.79722,
    110.3688
  ],
  "Pacitan": [
    -8.20461,
    111.08769
  ],
  "Ponorogo": [
    -7.86783,
    111.466
  ],
  "Trenggalek": [
    -8.07705,
    111.71667
  ],
  "Tulungagung": [
    -8.06667,
    111.96328
  ],
  "Blitar": [
    -8.11921,
    112.20187
  ],
  "Kediri": [
    -7.77407,
    112.10822
  ],
  "Malang": [
    -8.13084,
    112.56496
  ],
  "Lumajang": [
    -8.13702,
    113.2266
  ],
  "Jember": [
    -8.17236,
    113.7003
  ],
  "Banyuwangi": [
    -8.21861,
    114.36694
  ],
  "Bondowoso": [
    -7.9177,
    113.81348
  ],
  "Situbondo": [
    -7.70253,
    113.95561
  ],
  "Probolinggo": [
    -7.76208,
    113.41848
  ],
  "Pasuruan": [
    -7.60411,
    112.77633
  ],
  "Sidoarjo": [
    -7.45303,
    112.71734
  ],
  "Mojokerto": [
    -7.50421,
    112.5432
  ],
  "Jombang": [
    -7.54684,
    112.22648
  ],
  "Nganjuk": [
    -7.60293,
    111.90181
  ],
  "Madiun": [
    -7.62775,
    111.50548
  ],
  "Magetan": [
    -7.64934,
    111.33816
  ],
  "Ngawi": [
    -7.38993,
    111.46193
  ],
  "Bojonegoro": [
    -7.15353,
    111.88523
  ],
  "Tuban": [
    -6.89481,
    112.04184
  ],
  "Lamongan": [
    -7.11826,
    112.41307
  ],
  "Gresik": [
    -7.15665,
    112.6555
  ],
  "Bangkalan": [
    -7.03069,
    112.74501
  ],
  "Sampang": [
    -7.19119,
    113.24707
  ],
  "Pamekasan": [
    -7.16667,
    113.46667
  ],
  "Sumenep": [
    -6.9254,
    113.90606
  ],
  "Kediri": [
    -7.84829,
    112.01875
  ],
  "Blitar": [
    -8.0955,
    112.15942
  ],
  "Malang": [
    -7.96674,
    112.63178
  ],
  "Probolinggo": [
    -7.77707,
    113.19804
  ],
  "Pasuruan": [
    -7.64752,
    112.89839
  ],
  "Mojokerto": [
    -7.47108,
    112.43992
  ],
  "Madiun": [
    -7.63023,
    111.52805
  ],
  "Surabaya": [
    -7.28917,
    112.7344
  ],
  "Batu": [
    -7.8671,
    112.5239
  ],
  "Pandeglang": [
    -6.31483,
    106.1039
  ],
  "Lebak": [
    -6.5644,
    106.25221
  ],
  "Tangerang": [
    -6.16727,
    106.53228
  ],
  "Serang": [
    -6.04308,
    106.11578
  ],
  "Tangerang": [
    -6.17634,
    106.63012
  ],
  "Cilegon": [
    -6.01698,
    106.04051
  ],
  "Serang": [
    -6.11731,
    106.15438
  ],
  "Tangerang Selatan": [
    -6.28621,
    106.71105
  ],
  "Jembrana": [
    -8.36185,
    114.6418
  ],
  "Tabanan": [
    -8.54452,
    115.12418
  ],
  "Badung": [
    -8.58193,
    115.17706
  ],
  "Gianyar": [
    -8.53724,
    115.32932
  ],
  "Klungkung": [
    -8.53892,
    115.40451
  ],
  "Bangli": [
    -8.4543,
    115.3549
  ],
  "Karang Asem": [
    -6.39961,
    108.0503
  ],
  "Buleleng": [
    -8.11383,
    115.127
  ],
  "Denpasar": [
    -8.65629,
    115.2221
  ],
  "Lombok Barat": [
    -8.64646,
    116.11231
  ],
  "Lombok Tengah": [
    -8.69462,
    116.27771
  ],
  "Lombok Timur": [
    -8.51345,
    116.56099
  ],
  "Sumbawa": [
    -8.65293,
    117.36165
  ],
  "Dompu": [
    -8.49663,
    118.47472
  ],
  "Bima": [
    -8.45506,
    118.53643
  ],
  "Sumbawa Barat": [
    -8.92929,
    116.89103
  ],
  "Lombok Utara": [
    -8.37391,
    116.27771
  ],
  "Mataram": [
    -8.58333,
    116.11667
  ],
  "Bima": [
    -8.46347,
    118.74303
  ],
  "Sumba Barat": [
    -9.65483,
    119.39471
  ],
  "Sumba Timur": [
    -9.98021,
    120.34355
  ],
  "Kupang": [
    -10.07183,
    123.86499
  ],
  "Timor Tengah Selatan": [
    -9.77628,
    124.41982
  ],
  "Timor Tengah Utara": [
    -9.45226,
    124.59713
  ],
  "Belu": [
    -9.41258,
    124.95066
  ],
  "Alor": [
    -8.2754,
    124.72988
  ],
  "Lembata": [
    -8.47191,
    123.48319
  ],
  "Flores Timur": [
    -8.31309,
    122.9663
  ],
  "Sikka": [
    -8.67662,
    122.12918
  ],
  "Ende": [
    -8.85405,
    121.6542
  ],
  "Ngada": [
    -8.74304,
    120.98763
  ],
  "Manggarai": [
    -8.6797,
    120.38967
  ],
  "Rote Ndao": [
    -10.73864,
    123.1239
  ],
  "Manggarai Barat": [
    -8.66881,
    120.06652
  ],
  "Sumba Tengah": [
    -9.48792,
    119.69627
  ],
  "Sumba Barat Daya": [
    -9.53914,
    119.13906
  ],
  "Nagekeo": [
    -8.67535,
    121.30841
  ],
  "Manggarai Timur": [
    -8.62067,
    120.61999
  ],
  "Sabu Raijua": [
    -10.55411,
    121.83349
  ],
  "Malaka": [
    -9.5309,
    124.9066
  ],
  "Kupang": [
    -10.17414,
    123.61184
  ],
  "Sambas": [
    1.36133,
    109.30036
  ],
  "Bengkayang": [
    0.82097,
    109.4777
  ],
  "Landak": [
    0.42373,
    109.75917
  ],
  "Mempawah": [
    0.3897,
    109.1404
  ],
  "Sanggau": [
    0.11928,
    110.5973
  ],
  "Ketapang": [
    -1.8591,
    109.9719
  ],
  "Sintang": [
    0.08024,
    111.4955
  ],
  "Kapuas Hulu": [
    0.85192,
    112.93131
  ],
  "Sekadau": [
    0.01564,
    110.8886
  ],
  "Melawi": [
    -0.70007,
    111.66607
  ],
  "Kayong Utara": [
    -0.92259,
    110.04497
  ],
  "Kubu Raya": [
    -0.35339,
    109.47351
  ],
  "Pontianak": [
    -0.02252,
    109.33031
  ],
  "Singkawang": [
    0.9088,
    108.9846
  ],
  "aringin Barat": [
    -2.6767,
    111.62622
  ],
  "aringin Timur": [
    -2.53939,
    112.95932
  ],
  "Kapuas": [
    -2.87169,
    114.38179
  ],
  "Barito Selatan": [
    -1.87594,
    114.80927
  ],
  "Barito Utara": [
    -0.95871,
    115.09405
  ],
  "Sukamara": [
    -2.62675,
    111.23681
  ],
  "Lamandau": [
    -1.92692,
    111.18912
  ],
  "Seruyan": [
    -3.01235,
    112.42915
  ],
  "Katingan": [
    -1.87189,
    113.41167
  ],
  "Pulang Pisau": [
    -2.68496,
    113.95365
  ],
  "Gunung Mas": [
    -6.70528,
    106.99139
  ],
  "Barito Timur": [
    -2.0124,
    115.18892
  ],
  "Murung Raya": [
    -0.13622,
    114.33414
  ],
  "Palangka Raya": [
    -2.21605,
    113.91059
  ],
  "Tanah Laut": [
    -3.7694,
    114.80927
  ],
  "Baru": [
    -3.65099,
    116.18746
  ],
  "Banjar": [
    -3.41101,
    114.84438
  ],
  "Barito Kuala": [
    -3.07147,
    114.66679
  ],
  "Tapin": [
    -2.91607,
    115.0466
  ],
  "Hulu Sungai Selatan": [
    -2.76627,
    115.23634
  ],
  "Hulu Sungai Tengah": [
    -2.61532,
    115.52074
  ],
  "Hulu Sungai Utara": [
    -2.44212,
    115.18892
  ],
  "Tabalong": [
    -2.16405,
    115.38353
  ],
  "Tanah Bumbu": [
    -3.45122,
    115.94716
  ],
  "Balangan": [
    -2.32604,
    115.61547
  ],
  "Banjarmasin": [
    -3.3285,
    114.5892
  ],
  "Banjar Baru": [
    -3.43978,
    114.82562
  ],
  "Paser": [
    -1.71753,
    115.9468
  ],
  "Kutai Barat": [
    0.13539,
    115.09405
  ],
  "Kutai Kartanegara": [
    -0.13367,
    116.60817
  ],
  "Kutai Timur": [
    0.94338,
    116.98524
  ],
  "Berau": [
    2.04509,
    117.36165
  ],
  "Penajam Paser Utara": [
    -1.29171,
    116.5138
  ],
  "Mahakam Hulu": [
    0.51412,
    115.27025
  ],
  "Balikpapan": [
    -1.26354,
    116.82788
  ],
  "Samarinda": [
    -0.50218,
    117.1538
  ],
  "Bontang": [
    0.11993,
    117.47938
  ],
  "Malinau": [
    3.58422,
    116.6478
  ],
  "Bulungan": [
    2.90425,
    116.98524
  ],
  "Tana Tidung": [
    3.55187,
    117.07941
  ],
  "Nunukan": [
    4.06092,
    117.66695
  ],
  "Tarakan": [
    3.32602,
    117.5777
  ],
  "Bolaang Mongondow": [
    0.6871,
    124.06414
  ],
  "Minahasa": [
    1.30195,
    124.91329
  ],
  "Kepulauan Sangihe": [
    3.53032,
    125.5439
  ],
  "Kepulauan Talaud": [
    4.092,
    126.768
  ],
  "Minahasa Selatan": [
    1.09468,
    124.46418
  ],
  "Minahasa Utara": [
    1.5328,
    124.99475
  ],
  "Bolaang Mongondow Utara": [
    0.81869,
    123.52801
  ],
  "Siau Tagulandang Biaro": [
    2.34596,
    125.41244
  ],
  "Minahasa Tenggara": [
    1.02786,
    124.72988
  ],
  "Bolaang Mongondow Selatan": [
    0.4053,
    123.8411
  ],
  "Bolaang Mongondow Timur": [
    0.7153,
    124.4642
  ],
  "Manado": [
    1.4917,
    124.84284
  ],
  "Bitung": [
    1.45535,
    125.2047
  ],
  "Tomohon": [
    1.32341,
    124.83845
  ],
  "Kotamobagu": [
    0.73333,
    124.31667
  ],
  "Banggai Kepulauan": [
    -1.36872,
    123.16867
  ],
  "Banggai": [
    -0.93818,
    122.79184
  ],
  "Morowali": [
    -2.30031,
    121.93497
  ],
  "Poso": [
    -1.39192,
    120.767
  ],
  "Donggala": [
    -0.42332,
    119.83523
  ],
  "Toli-Toli": [
    0.87682,
    120.75798
  ],
  "Buol": [
    0.96955,
    121.35416
  ],
  "Parigi Moutong": [
    0.58176,
    120.80395
  ],
  "Tojo Una-Una": [
    -0.86865,
    121.58473
  ],
  "Sigi": [
    -1.38341,
    120.06652
  ],
  "Banggai Laut": [
    -1.6735,
    123.5504
  ],
  "Morowali Utara": [
    -1.6312,
    121.3542
  ],
  "Palu": [
    -0.89858,
    119.8506
  ],
  "Kepulauan Selayar": [
    -6.287,
    120.5049
  ],
  "Bulukumba": [
    -5.43294,
    120.20511
  ],
  "Bantaeng": [
    -5.51693,
    120.0203
  ],
  "Jeneponto": [
    -5.55458,
    119.67309
  ],
  "Takalar": [
    -5.41625,
    119.48757
  ],
  "Gowa": [
    -5.31029,
    119.7426
  ],
  "Sinjai": [
    -5.2172,
    120.11274
  ],
  "Maros": [
    -4.94695,
    119.5789
  ],
  "Pangkajene Dan Kepulauan": [
    -4.80504,
    119.55717
  ],
  "Barru": [
    -4.41727,
    119.67309
  ],
  "Bone": [
    -2.08333,
    120.21667
  ],
  "Soppeng": [
    -4.35185,
    119.92779
  ],
  "Wajo": [
    -4.02223,
    120.06652
  ],
  "Sidenreng Rappang": [
    -3.7739,
    120.0203
  ],
  "Pinrang": [
    -3.79307,
    119.6408
  ],
  "Enrekang": [
    -3.56313,
    119.7612
  ],
  "Luwu": [
    -3.30522,
    120.25127
  ],
  "Tana Toraja": [
    -3.0753,
    119.7426
  ],
  "Luwu Utara": [
    -2.26904,
    119.97405
  ],
  "Luwu Timur": [
    -2.58255,
    121.17104
  ],
  "Toraja Utara": [
    -2.86219,
    119.83523
  ],
  "Makassar": [
    -5.13333,
    119.41667
  ],
  "Parepare": [
    -4.0096,
    119.6291
  ],
  "Palopo": [
    -3.00212,
    120.19809
  ],
  "Buton": [
    -5.30964,
    122.98883
  ],
  "Muna": [
    -4.83225,
    122.72062
  ],
  "Konawe": [
    -3.85473,
    122.04333
  ],
  "Kolaka": [
    -4.04967,
    121.5938
  ],
  "Konawe Selatan": [
    -4.20279,
    122.44672
  ],
  "Bombana": [
    -4.65435,
    121.9018
  ],
  "Wakatobi": [
    -5.32644,
    123.59519
  ],
  "Kolaka Utara": [
    -3.13472,
    121.17104
  ],
  "Buton Utara": [
    -4.70234,
    123.03388
  ],
  "Konawe Utara": [
    -3.51208,
    122.11101
  ],
  "Kolaka Timur": [
    -4.2279,
    121.9018
  ],
  "Konawe Kepulauan": [
    -4.1361,
    123.1239
  ],
  "Muna Barat": [
    -4.78957,
    122.49816
  ],
  "Buton Tengah": [
    -5.3891,
    122.5599
  ],
  "Buton Selatan": [
    -5.60681,
    122.6179
  ],
  "Kendari": [
    -3.9722,
    122.5149
  ],
  "Baubau": [
    -5.50588,
    122.60136
  ],
  "Boalemo": [
    0.70134,
    122.26539
  ],
  "Gorontalo": [
    0.66354,
    122.96392
  ],
  "Pohuwato": [
    0.70553,
    121.71955
  ],
  "Bone Bolango": [
    0.56579,
    123.34861
  ],
  "Gorontalo Utara": [
    0.92526,
    122.49201
  ],
  "Gorontalo": [
    0.53333,
    123.06667
  ],
  "Majene": [
    -3.02973,
    118.90628
  ],
  "Polewali Mandar": [
    -3.34193,
    119.13906
  ],
  "Mamasa": [
    -2.96013,
    119.3682
  ],
  "Mamuju": [
    -2.72934,
    118.92957
  ],
  "Mamuju Utara": [
    -1.52645,
    119.51077
  ],
  "Mamuju Tengah": [
    -1.9354,
    119.5108
  ],
  "Maluku Tenggara Barat": [
    -7.98349,
    131.3023
  ],
  "Maluku Tenggara": [
    -5.6631,
    132.73781
  ],
  "Maluku Tengah": [
    -3.01665,
    129.48644
  ],
  "Buru": [
    -3.23143,
    127.09036
  ],
  "Kepulauan Aru": [
    -6.19465,
    134.55019
  ],
  "Seram Bagian Barat": [
    -3.12716,
    128.40084
  ],
  "Seram Bagian Timur": [
    -3.41508,
    130.39049
  ],
  "Maluku Barat Daya": [
    -7.78516,
    126.34981
  ],
  "Buru Selatan": [
    -3.83757,
    126.734305
  ],
  "Ambon": [
    -3.65607,
    128.16642
  ],
  "Tual": [
    -5.64085,
    132.74751
  ],
  "Halmahera Barat": [
    1.07478,
    127.47239
  ],
  "Halmahera Tengah": [
    0.3385,
    127.87139
  ],
  "Kepulauan Sula": [
    -1.86667,
    125.36667
  ],
  "Halmahera Selatan": [
    -0.62584,
    127.4831
  ],
  "Halmahera Utara": [
    1.7251,
    128.00373
  ],
  "Halmahera Timur": [
    0.69114,
    128.28043
  ],
  "Pulau Morotai": [
    2.3657,
    128.4008
  ],
  "Pulau Taliabu": [
    -1.8268,
    124.7741
  ],
  "Ternate": [
    0.78333,
    127.36667
  ],
  "Tidore Kepulauan": [
    0.68333,
    127.44725
  ],
  "Fakfak": [
    -2.88524,
    132.26583
  ],
  "Kaimana": [
    -3.66093,
    133.77451
  ],
  "Teluk Wondama": [
    -2.85517,
    134.32366
  ],
  "Teluk Bintuni": [
    -1.90568,
    133.32947
  ],
  "Manokwari": [
    -0.86145,
    134.06204
  ],
  "Sorong Selatan": [
    -1.44375,
    132.0187
  ],
  "Sorong": [
    -0.956132,
    131.33747
  ],
  "Raja Ampat": [
    -1.09152,
    130.87786
  ],
  "Tambrauw": [
    -0.78186,
    132.39384
  ],
  "Maybrat": [
    -1.2971,
    132.3151
  ],
  "Manokwari Selatan": [
    -1.51673,
    134.17932
  ],
  "Pegunungan Arfak": [
    -1.1555,
    133.7142
  ],
  "Sorong": [
    -0.87883,
    131.2589
  ],
  "Merauke": [
    -8.49604,
    140.39455
  ],
  "Jayawijaya": [
    -4.00045,
    138.79951
  ],
  "Jayapura": [
    -2.54958,
    140.47759
  ],
  "Nabire": [
    -3.50955,
    135.7521
  ],
  "Kepulauan Yapen": [
    -1.74694,
    136.1709
  ],
  "Biak Numfor": [
    -1.0381,
    135.98008
  ],
  "Paniai": [
    -3.78764,
    136.36247
  ],
  "Puncak Jaya": [
    -3.72805,
    137.98589
  ],
  "Mimika": [
    -4.45532,
    137.13621
  ],
  "Boven Digoel": [
    -6.09967,
    140.34818
  ],
  "Mappi": [
    -7.10223,
    139.39639
  ],
  "Asmat": [
    -5.0574,
    138.39882
  ],
  "Yahukimo": [
    -4.88689,
    139.52088
  ],
  "Pegunungan Bintang": [
    -4.55899,
    140.51356
  ],
  "Tolikara": [
    -3.48113,
    138.47873
  ],
  "Sarmi": [
    -1.86873,
    138.74361
  ],
  "Keerom": [
    -3.34495,
    140.76245
  ],
  "Waropen": [
    -2.84357,
    136.67053
  ],
  "Supiori": [
    -0.72951,
    135.63851
  ],
  "Mamberamo Raya": [
    -2.53313,
    137.76376
  ],
  "Nduga": [
    -4.40695,
    138.23935
  ],
  "Lanny Jaya": [
    -3.97103,
    138.31903
  ],
  "Mamberamo Tengah": [
    -3.67108,
    139.0626
  ],
  "Yalimo": [
    -3.78528,
    139.4466
  ],
  "Puncak": [
    -3.97143,
    137.64241
  ],
  "Dogiyai": [
    -4.01939,
    135.96104
  ],
  "Intan Jaya": [
    -3.50764,
    136.74785
  ],
  "Deiyai": [
    -4.09749,
    136.43931
  ],
  "Jayapura": [
    -2.59048,
    140.6754
  ]
}


export default {
  name: 'InteractiveMap',
  props: {
    clusters: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'Peta Sebaran Cluster'
    }
  },
  setup(props) {
    const mapContainer = ref(null)
    const map = ref(null)
    const markersLayer = ref(null)
    const selectedClusterFilter = ref('all')

    // Consistent cluster colors matching the design system
    const colors = [
      '#667eea', // Purple - Primary
      '#48bb78', // Green - Success
      '#ed8936', // Orange - Warning
      '#4299e1', // Blue - Info
      '#f56565', // Red - Danger
      '#38b2ac', // Teal
      '#9f7aea', // Purple Light
      '#ecc94b', // Yellow
      '#f687b3', // Pink
      '#4fd1c5', // Cyan
    ]

    const getClusterColor = (index) => {
      return colors[index % colors.length]
    }

    // Helper function to normalize city names for coordinate lookup
    const normalizeCityName = (cityName) => {
      if (!cityName) return ''
      
      // Convert to string and clean up
      let normalized = String(cityName).trim()
      
      // Handle common variations
      const replacements = {
        'Kab. ': '',
        'Kabupaten ': '',
        'Kota ': '',
        'Administrasi ': '',
        'DKI ': '',
      }
      
      for (const [key, value] of Object.entries(replacements)) {
        normalized = normalized.replace(new RegExp(key, 'gi'), value)
      }
      
      return normalized.trim()
    }

    // Get coordinates for a city
    const getCityCoordinates = (cityName) => {
      const normalized = normalizeCityName(cityName)
      
      // Direct lookup
      if (cityCoords[normalized]) {
        console.log(`✅ Found exact match for: ${cityName} -> ${normalized}`)
        return cityCoords[normalized]
      }
      
      // Fuzzy matching - try to find partial matches
      const cityKeys = Object.keys(cityCoords)
      
      // Try different matching strategies
      let fuzzyMatch = null
      
      // Strategy 1: Exact substring match
      fuzzyMatch = cityKeys.find(key => 
        key.toLowerCase().includes(normalized.toLowerCase()) ||
        normalized.toLowerCase().includes(key.toLowerCase())
      )
      
      if (fuzzyMatch) {
        console.log(`✅ Found fuzzy match for: ${cityName} -> ${fuzzyMatch}`)
        return cityCoords[fuzzyMatch]
      }
      
      // Strategy 2: Remove common words and try again
      const cleanNormalized = normalized
        .replace(/\b(kota|kabupaten|kab|administrasi)\b/gi, '')
        .trim()
      
      fuzzyMatch = cityKeys.find(key => {
        const cleanKey = key
          .replace(/\b(kota|kabupaten|kab|administrasi)\b/gi, '')
          .trim()
        return cleanKey.toLowerCase() === cleanNormalized.toLowerCase()
      })
      
      if (fuzzyMatch) {
        console.log(`✅ Found clean match for: ${cityName} -> ${fuzzyMatch}`)
        return cityCoords[fuzzyMatch]
      }
      
      // Strategy 3: Use fallback coordinates based on region
      const fallbackCoords = getFallbackCoordinates(normalized)
      if (fallbackCoords) {
        console.log(`⚠️ Using fallback coordinates for: ${cityName}`)
        return fallbackCoords
      }
      
      // Log missing coordinates for debugging
      console.warn(`❌ Coordinates not found for: "${cityName}" (normalized: "${normalized}")`)
      return null
    }
    
    // Get fallback coordinates based on province or region
    const getFallbackCoordinates = (cityName) => {
      const fallbacks = {
        // Jakarta area
        'jakarta': [-6.2, 106.8],
        // Java
        'bandung': [-6.9, 107.6],
        'surabaya': [-7.25, 112.75],
        'semarang': [-7.0, 110.4],
        'yogyakarta': [-7.8, 110.4],
        // Sumatra
        'medan': [3.58, 98.67],
        'palembang': [-2.98, 104.77],
        'padang': [-0.95, 100.35],
        'pekanbaru': [0.53, 101.45],
        'bandar lampung': [-5.43, 105.27],
        // Kalimantan
        'pontianak': [-0.02, 109.33],
        'banjarmasin': [-3.32, 114.58],
        'samarinda': [-0.5, 117.15],
        'balikpapan': [-1.25, 116.83],
        // Sulawesi
        'makassar': [-5.13, 119.42],
        'manado': [1.48, 124.85],
        'palu': [-0.88, 119.87],
        'kendari': [-3.98, 122.52],
        // Eastern Indonesia
        'denpasar': [-8.65, 115.22],
        'mataram': [-8.58, 116.12],
        'kupang': [-10.17, 123.58],
        'ambon': [-3.7, 128.17],
        'jayapura': [-2.53, 140.72],
      }
      
      const cityLower = cityName.toLowerCase()
      for (const [key, coords] of Object.entries(fallbacks)) {
        if (cityLower.includes(key) || key.includes(cityLower)) {
          return coords
        }
      }
      
      return null
    }

    const filteredMarkers = computed(() => {
      let allMarkers = []
      
      props.clusters.forEach((cluster, clusterIndex) => {
        if (selectedClusterFilter.value !== 'all' && cluster.id !== selectedClusterFilter.value) {
          return
        }
        
        cluster.members.forEach(member => {
          const coords = getCityCoordinates(member.kabupaten_kota)
          if (coords) {
            allMarkers.push({
              ...member,
              cluster: cluster,
              clusterIndex: clusterIndex,
              coordinates: coords
            })
          }
        })
      })
      
      return allMarkers
    })

    const totalRegions = computed(() => {
      return props.clusters.reduce((total, cluster) => total + cluster.size, 0)
    })

    const mappedRegions = computed(() => {
      return filteredMarkers.value.length
    })

    const coveragePercentage = computed(() => {
      if (totalRegions.value === 0) return 0
      return Math.round((mappedRegions.value / totalRegions.value) * 100)
    })

    const initMap = () => {
      if (!mapContainer.value) return

      // Initialize map centered on Indonesia
      map.value = L.map(mapContainer.value).setView([-2.5, 118], 5)

      // Add OpenStreetMap tiles with better styling
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18
      }).addTo(map.value)

      // Initialize markers layer
      markersLayer.value = L.layerGroup().addTo(map.value)

      // Load initial markers
      updateMapView()
    }

    const updateMapView = () => {
      if (!map.value || !markersLayer.value) return

      // Clear existing markers
      markersLayer.value.clearLayers()

      console.log(`🗺️ Updating map with ${filteredMarkers.value.length} markers`)
      console.log('📊 Clusters data:', props.clusters)
      console.log('🎯 Filtered markers:', filteredMarkers.value.slice(0, 3)) // Show first 3 for debugging

      // Add markers for filtered data
      filteredMarkers.value.forEach((markerData, index) => {
        const { coordinates, cluster, clusterIndex } = markerData
        const color = getClusterColor(clusterIndex)
        
        console.log(`📍 Creating marker ${index + 1}: ${markerData.kabupaten_kota} at [${coordinates[0]}, ${coordinates[1]}] - Cluster ${cluster.id}`)
        
        const marker = L.circleMarker(coordinates, {
          radius: 10,
          fillColor: color,
          color: '#fff',
          weight: 3,
          opacity: 1,
          fillOpacity: 0.9
        })

        // Create popup content with better formatting
        const popupContent = `
          <div class="marker-popup">
            <h4>${markerData.kabupaten_kota}</h4>
            <div class="popup-cluster">
              <span class="cluster-badge" style="background-color: ${color}">
                Cluster ${cluster.id}
              </span>
            </div>
            <div class="popup-stats">
              <div class="stat-row">
                <span class="stat-label">IPM:</span>
                <span class="stat-value">${markerData.ipm?.toFixed(2) || 'N/A'}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">Garis Kemiskinan:</span>
                <span class="stat-value">Rp ${markerData.garis_kemiskinan?.toLocaleString('id-ID') || 'N/A'}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">Pengeluaran per Kapita:</span>
                <span class="stat-value">Rp ${markerData.pengeluaran_per_kapita?.toLocaleString('id-ID') || 'N/A'}</span>
              </div>
              ${markerData.membership ? `
                <div class="stat-row">
                  <span class="stat-label">Membership:</span>
                  <span class="stat-value">${(markerData.membership * 100).toFixed(1)}%</span>
                </div>
              ` : ''}
              ${markerData.tahun ? `
                <div class="stat-row">
                  <span class="stat-label">Tahun:</span>
                  <span class="stat-value">${markerData.tahun}</span>
                </div>
              ` : ''}
            </div>
          </div>
        `

        marker.bindPopup(popupContent, {
          maxWidth: 300,
          className: 'custom-popup'
        })
        
        markersLayer.value.addLayer(marker)
      })

      // Auto-fit map bounds if there are markers
      if (filteredMarkers.value.length > 0) {
        const group = new L.featureGroup(markersLayer.value.getLayers())
        map.value.fitBounds(group.getBounds().pad(0.1))
      }
    }

    onMounted(() => {
      initMap()
    })

    onUnmounted(() => {
      if (map.value) {
        map.value.remove()
      }
    })

    watch(() => props.clusters, () => {
      updateMapView()
    }, { deep: true })

    return {
      mapContainer,
      selectedClusterFilter,
      filteredMarkers,
      totalRegions,
      mappedRegions,
      coveragePercentage,
      getClusterColor,
      updateMapView
    }
  }
}
</script>

<style scoped>
.map-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.map-header h3 {
  color: #2d3748;
  margin: 0;
  font-size: 1.25rem;
}

.map-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.cluster-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cluster-filter label {
  font-weight: 600;
  color: #4a5568;
  font-size: 0.875rem;
}

.cluster-filter select {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  color: #4a5568;
  font-size: 0.875rem;
  min-width: 150px;
}

.map-info {
  background: #f7fafc;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #4a5568;
  border: 1px solid #e2e8f0;
}

.map-wrapper {
  height: 500px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  position: relative;
}

#map {
  height: 100%;
  width: 100%;
}

.map-legend {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.map-legend h4 {
  color: #2d3748;
  margin: 0 0 1rem 0;
  font-size: 1rem;
}

.legend-items {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4a5568;
}

.legend-marker {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1);
}

.map-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.stat-item {
  background: #f7fafc;
  padding: 0.75rem;
  border-radius: 6px;
  text-align: center;
  font-size: 0.875rem;
}

.stat-item strong {
  color: #2d3748;
  display: block;
  margin-bottom: 0.25rem;
}

@media (max-width: 768px) {
  .map-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .map-controls {
    justify-content: center;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .map-wrapper {
    height: 400px;
  }
  
  .legend-items {
    justify-content: center;
  }
  
  .map-stats {
    grid-template-columns: 1fr;
  }
}

/* Custom popup styles */
:global(.custom-popup .leaflet-popup-content) {
  margin: 0;
  padding: 0;
}

:global(.marker-popup) {
  min-width: 250px;
}

:global(.marker-popup h4) {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
  font-size: 1rem;
  font-weight: 600;
}

:global(.popup-cluster) {
  margin-bottom: 0.75rem;
}

:global(.cluster-badge) {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

:global(.popup-stats) {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

:global(.stat-row) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0;
  border-bottom: 1px solid #f1f5f9;
}

:global(.stat-row:last-child) {
  border-bottom: none;
}

:global(.stat-label) {
  font-weight: 500;
  color: #64748b;
  font-size: 0.875rem;
}

:global(.stat-value) {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.875rem;
}
</style>