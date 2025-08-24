// Mock data service untuk demo UI tanpa backend - NO API CALLS
export const mockData = {
  // Sample clustering results
  clusteringResults: {
    summary: {
      total_regions: 34,
      num_clusters: 3,
      iterations: 42,
      execution_time: 2.34
    },
    evaluation: {
      davies_bouldin: 0.8234,
      silhouette_score: 0.6789
    },
    clusters: [
      {
        id: 0,
        centroid: {
          ipm: 81.5,
          garis_kemiskinan: 580000
        },
        members: [
          {
            kabupaten_kota: 'Jakarta Pusat',
            tahun: 2023,
            ipm: 82.5,
            garis_kemiskinan: 532000,
            membership: 0.95
          },
          {
            kabupaten_kota: 'Jakarta Selatan',
            tahun: 2023,
            ipm: 81.3,
            garis_kemiskinan: 580000,
            membership: 0.92
          },
          {
            kabupaten_kota: 'Jakarta Barat',
            tahun: 2023,
            ipm: 79.1,
            garis_kemiskinan: 525000,
            membership: 0.89
          },
          {
            kabupaten_kota: 'Surabaya',
            tahun: 2023,
            ipm: 76.8,
            garis_kemiskinan: 465000,
            membership: 0.87
          },
          {
            kabupaten_kota: 'Yogyakarta',
            tahun: 2023,
            ipm: 83.2,
            garis_kemiskinan: 495000,
            membership: 0.91
          },
          {
            kabupaten_kota: 'Denpasar',
            tahun: 2023,
            ipm: 84.1,
            garis_kemiskinan: 520000,
            membership: 0.93
          }
        ]
      },
      {
        id: 1,
        centroid: {
          ipm: 74.2,
          garis_kemiskinan: 445000
        },
        members: [
          {
            kabupaten_kota: 'Bandung',
            tahun: 2023,
            ipm: 75.2,
            garis_kemiskinan: 485000,
            membership: 0.89
          },
          {
            kabupaten_kota: 'Semarang',
            tahun: 2023,
            ipm: 74.5,
            garis_kemiskinan: 445000,
            membership: 0.91
          },
          {
            kabupaten_kota: 'Makassar',
            tahun: 2023,
            ipm: 73.2,
            garis_kemiskinan: 380000,
            membership: 0.85
          },
          {
            kabupaten_kota: 'Palembang',
            tahun: 2023,
            ipm: 72.8,
            garis_kemiskinan: 415000,
            membership: 0.86
          },
          {
            kabupaten_kota: 'Malang',
            tahun: 2023,
            ipm: 76.1,
            garis_kemiskinan: 425000,
            membership: 0.88
          },
          {
            kabupaten_kota: 'Bekasi',
            tahun: 2023,
            ipm: 73.9,
            garis_kemiskinan: 495000,
            membership: 0.84
          },
          {
            kabupaten_kota: 'Depok',
            tahun: 2023,
            ipm: 75.6,
            garis_kemiskinan: 510000,
            membership: 0.87
          }
        ]
      },
      {
        id: 2,
        centroid: {
          ipm: 68.1,
          garis_kemiskinan: 350000
        },
        members: [
          {
            kabupaten_kota: 'Medan',
            tahun: 2023,
            ipm: 72.1,
            garis_kemiskinan: 420000,
            membership: 0.88
          },
          {
            kabupaten_kota: 'Banjarmasin',
            tahun: 2023,
            ipm: 68.5,
            garis_kemiskinan: 355000,
            membership: 0.82
          },
          {
            kabupaten_kota: 'Pontianak',
            tahun: 2023,
            ipm: 70.2,
            garis_kemiskinan: 340000,
            membership: 0.85
          },
          {
            kabupaten_kota: 'Balikpapan',
            tahun: 2023,
            ipm: 75.8,
            garis_kemiskinan: 390000,
            membership: 0.79
          },
          {
            kabupaten_kota: 'Mataram',
            tahun: 2023,
            ipm: 69.3,
            garis_kemiskinan: 325000,
            membership: 0.83
          },
          {
            kabupaten_kota: 'Palu',
            tahun: 2023,
            ipm: 67.8,
            garis_kemiskinan: 310000,
            membership: 0.86
          },
          {
            kabupaten_kota: 'Kendari',
            tahun: 2023,
            ipm: 68.9,
            garis_kemiskinan: 335000,
            membership: 0.84
          },
          {
            kabupaten_kota: 'Manado',
            tahun: 2023,
            ipm: 74.2,
            garis_kemiskinan: 375000,
            membership: 0.81
          },
          {
            kabupaten_kota: 'Ambon',
            tahun: 2023,
            ipm: 71.5,
            garis_kemiskinan: 360000,
            membership: 0.80
          },
          {
            kabupaten_kota: 'Jayapura',
            tahun: 2023,
            ipm: 65.4,
            garis_kemiskinan: 485000,
            membership: 0.77
          },
          {
            kabupaten_kota: 'Kupang',
            tahun: 2023,
            ipm: 66.8,
            garis_kemiskinan: 295000,
            membership: 0.85
          }
        ]
      }
    ]
  },

  // Sample dataset preview
  datasetPreview: {
    totalRows: 102,
    columns: ['kabupaten_kota', 'tahun', 'ipm', 'garis_kemiskinan'],
    sampleRows: [
      {
        kabupaten_kota: 'Jakarta Pusat',
        tahun: '2023',
        ipm: '82.5',
        garis_kemiskinan: '532000'
      },
      {
        kabupaten_kota: 'Jakarta Utara',
        tahun: '2023',
        ipm: '78.2',
        garis_kemiskinan: '548000'
      },
      {
        kabupaten_kota: 'Jakarta Barat',
        tahun: '2023',
        ipm: '79.1',
        garis_kemiskinan: '525000'
      },
      {
        kabupaten_kota: 'Bandung',
        tahun: '2023',
        ipm: '75.2',
        garis_kemiskinan: '485000'
      },
      {
        kabupaten_kota: 'Surabaya',
        tahun: '2023',
        ipm: '76.8',
        garis_kemiskinan: '465000'
      }
    ]
  },

  // Available years
  availableYears: [2021, 2022, 2023],

  // Processing simulation
  processingSessions: new Map()
}

// Helper functions untuk demo tanpa API
export const mockHelpers = {
  // Simulate delay for realistic UX
  delay: (ms) => new Promise(resolve => setTimeout(resolve, ms)),
  
  // Generate CSV for export
  generateCSV: () => {
    let csv = 'kabupaten_kota,tahun,ipm,garis_kemiskinan,cluster,membership\n'
    mockData.clusteringResults.clusters.forEach((cluster, clusterIndex) => {
      cluster.members.forEach(member => {
        csv += `${member.kabupaten_kota},${member.tahun},${member.ipm},${member.garis_kemiskinan},${clusterIndex + 1},${member.membership}\n`
      })
    })
    return csv
  },
  
  // Generate JSON for export
  generateJSON: () => {
    return JSON.stringify(mockData.clusteringResults, null, 2)
  }
}

export default mockData