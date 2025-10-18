import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

/**
 * Utility class for exporting analysis results to PDF
 */
export class PDFExporter {
  constructor() {
    this.pdf = null
    this.currentY = 0
    this.pageHeight = 0
    this.pageWidth = 0
    this.margin = 20
  }

  /**
   * Initialize new PDF document
   */
  initPDF() {
    this.pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })
    this.pageHeight = this.pdf.internal.pageSize.getHeight()
    this.pageWidth = this.pdf.internal.pageSize.getWidth()
    this.currentY = this.margin
  }

  /**
   * Add new page if needed
   */
  checkPageBreak(requiredHeight) {
    if (this.currentY + requiredHeight > this.pageHeight - this.margin) {
      this.pdf.addPage()
      this.currentY = this.margin
      return true
    }
    return false
  }

  /**
   * Add title to PDF
   */
  addTitle(text, fontSize = 20) {
    this.pdf.setFontSize(fontSize)
    this.pdf.setFont(undefined, 'bold')
    this.pdf.text(text, this.pageWidth / 2, this.currentY, { align: 'center' })
    this.currentY += 10
  }

  /**
   * Add subtitle
   */
  addSubtitle(text, fontSize = 14) {
    this.checkPageBreak(10)
    this.pdf.setFontSize(fontSize)
    this.pdf.setFont(undefined, 'bold')
    this.pdf.text(text, this.margin, this.currentY)
    this.currentY += 8
  }

  /**
   * Add text paragraph
   */
  addText(text, fontSize = 10) {
    this.checkPageBreak(10)
    this.pdf.setFontSize(fontSize)
    this.pdf.setFont(undefined, 'normal')
    
    const lines = this.pdf.splitTextToSize(text, this.pageWidth - 2 * this.margin)
    lines.forEach(line => {
      this.checkPageBreak(5)
      this.pdf.text(line, this.margin, this.currentY)
      this.currentY += 5
    })
    this.currentY += 3
  }

  /**
   * Add key-value pair
   */
  addKeyValue(key, value) {
    this.checkPageBreak(6)
    this.pdf.setFontSize(10)
    this.pdf.setFont(undefined, 'bold')
    this.pdf.text(`${key}:`, this.margin, this.currentY)
    this.pdf.setFont(undefined, 'normal')
    this.pdf.text(String(value), this.margin + 50, this.currentY)
    this.currentY += 6
  }

  /**
   * Add horizontal line
   */
  addLine() {
    this.checkPageBreak(5)
    this.pdf.setLineWidth(0.5)
    this.pdf.line(this.margin, this.currentY, this.pageWidth - this.margin, this.currentY)
    this.currentY += 5
  }

  /**
   * Add spacing
   */
  addSpace(height = 5) {
    this.currentY += height
  }

  /**
   * Capture element as image and add to PDF
   */
  async addElementAsImage(element, maxWidth = null, maxHeight = null) {
    if (!element) {
      console.warn('Element not found for PDF capture')
      return
    }

    try {
      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff'
      })

      const imgData = canvas.toDataURL('image/png')
      const imgWidth = maxWidth || (this.pageWidth - 2 * this.margin)
      const imgHeight = (canvas.height * imgWidth) / canvas.width
      
      const finalHeight = maxHeight && imgHeight > maxHeight ? maxHeight : imgHeight

      // Check if need new page
      this.checkPageBreak(finalHeight)

      this.pdf.addImage(imgData, 'PNG', this.margin, this.currentY, imgWidth, finalHeight)
      this.currentY += finalHeight + 5
    } catch (error) {
      console.error('Error capturing element:', error)
      this.addText('⚠️ Error: Unable to capture visualization')
    }
  }

  /**
   * Add table to PDF
   */
  addTable(headers, rows) {
    const colWidth = (this.pageWidth - 2 * this.margin) / headers.length
    const rowHeight = 8

    // Check space for header
    this.checkPageBreak(rowHeight * 2)

    // Draw headers
    this.pdf.setFontSize(9)
    this.pdf.setFont(undefined, 'bold')
    this.pdf.setFillColor(102, 126, 234) // Purple
    this.pdf.rect(this.margin, this.currentY, this.pageWidth - 2 * this.margin, rowHeight, 'F')
    
    this.pdf.setTextColor(255, 255, 255) // White text
    headers.forEach((header, i) => {
      this.pdf.text(
        String(header),
        this.margin + i * colWidth + 2,
        this.currentY + 5
      )
    })
    this.currentY += rowHeight

    // Draw rows
    this.pdf.setFont(undefined, 'normal')
    this.pdf.setTextColor(0, 0, 0) // Black text
    
    rows.forEach((row, rowIndex) => {
      this.checkPageBreak(rowHeight)
      
      // Alternate row colors
      if (rowIndex % 2 === 0) {
        this.pdf.setFillColor(247, 250, 252)
        this.pdf.rect(this.margin, this.currentY, this.pageWidth - 2 * this.margin, rowHeight, 'F')
      }

      row.forEach((cell, colIndex) => {
        const text = String(cell).substring(0, 30) // Truncate long text
        this.pdf.text(
          text,
          this.margin + colIndex * colWidth + 2,
          this.currentY + 5
        )
      })
      this.currentY += rowHeight
    })

    this.currentY += 5
  }

  /**
   * Save PDF file
   */
  save(filename = 'analysis-report.pdf') {
    if (this.pdf) {
      this.pdf.save(filename)
    }
  }

  /**
   * Add cover page
   */
  addCoverPage(title, subtitle, metadata) {
    this.currentY = this.pageHeight / 3

    // Title
    this.pdf.setFontSize(24)
    this.pdf.setFont(undefined, 'bold')
    this.pdf.text(title, this.pageWidth / 2, this.currentY, { align: 'center' })
    this.currentY += 15

    // Subtitle
    this.pdf.setFontSize(16)
    this.pdf.setFont(undefined, 'normal')
    this.pdf.text(subtitle, this.pageWidth / 2, this.currentY, { align: 'center' })
    this.currentY += 20

    // Metadata
    this.pdf.setFontSize(12)
    Object.entries(metadata).forEach(([key, value]) => {
      this.pdf.text(`${key}: ${value}`, this.pageWidth / 2, this.currentY, { align: 'center' })
      this.currentY += 8
    })

    // Footer
    this.pdf.setFontSize(10)
    this.pdf.setTextColor(128, 128, 128)
    this.pdf.text(
      'Generated by Fuzzy Clustering Analysis System',
      this.pageWidth / 2,
      this.pageHeight - 20,
      { align: 'center' }
    )
    this.pdf.setTextColor(0, 0, 0)

    this.pdf.addPage()
    this.currentY = this.margin
  }

  /**
   * Add page numbers
   */
  addPageNumbers() {
    const pageCount = this.pdf.internal.getNumberOfPages()
    this.pdf.setFontSize(10)
    
    for (let i = 1; i <= pageCount; i++) {
      this.pdf.setPage(i)
      this.pdf.text(
        `Page ${i} of ${pageCount}`,
        this.pageWidth / 2,
        this.pageHeight - 10,
        { align: 'center' }
      )
    }
  }
}

/**
 * Export yearly results to PDF
 */
export async function exportYearlyResultsToPDF(results) {
  const exporter = new PDFExporter()
  exporter.initPDF()

  // Cover page
  const metadata = {
    'Algorithm': results.overall_summary.algorithm,
    'Total Years': results.overall_summary.total_years,
    'Successful Years': results.overall_summary.successful_years,
    'Success Rate': `${(results.overall_summary.success_rate * 100).toFixed(1)}%`,
    'Generated': new Date().toLocaleDateString('id-ID')
  }

  exporter.addCoverPage(
    'Clustering Analysis Report',
    'Per Year Analysis',
    metadata
  )

  // Overall Summary
  exporter.addTitle('Overall Summary', 18)
  exporter.addLine()
  
  exporter.addKeyValue('Algorithm', results.overall_summary.algorithm)
  exporter.addKeyValue('Total Years', results.overall_summary.total_years)
  exporter.addKeyValue('Successful Years', results.overall_summary.successful_years)
  exporter.addKeyValue('Success Rate', `${(results.overall_summary.success_rate * 100).toFixed(1)}%`)
  exporter.addKeyValue('Features Used', results.overall_summary.features_used.join(', '))
  
  if (results.overall_summary.average_evaluation) {
    exporter.addSpace(5)
    exporter.addSubtitle('Average Evaluation Metrics', 12)
    exporter.addKeyValue('Davies-Bouldin Index', results.overall_summary.average_evaluation.davies_bouldin?.toFixed(4) || 'N/A')
    exporter.addKeyValue('Silhouette Score', results.overall_summary.average_evaluation.silhouette_score?.toFixed(4) || 'N/A')
  }

  // Year by year results
  const years = Object.keys(results.results_per_year).sort()
  
  for (const year of years) {
    const yearResult = results.results_per_year[year]
    
    if (yearResult.error) continue

    exporter.pdf.addPage()
    exporter.currentY = exporter.margin

    exporter.addTitle(`Year ${year}`, 16)
    exporter.addLine()

    // Year summary
    exporter.addKeyValue('Number of Clusters', yearResult.summary.num_clusters)
    exporter.addKeyValue('Total Regions', yearResult.summary.total_regions)
    exporter.addKeyValue('Execution Time', `${yearResult.evaluation.execution_time?.toFixed(2)}s`)
    
    exporter.addSpace(5)
    exporter.addSubtitle('Evaluation Metrics', 12)
    exporter.addKeyValue('Davies-Bouldin Index', yearResult.evaluation.davies_bouldin?.toFixed(4))
    exporter.addKeyValue('Silhouette Score', yearResult.evaluation.silhouette_score?.toFixed(4))

    // Cluster details
    exporter.addSpace(5)
    exporter.addSubtitle('Cluster Details', 12)
    
    yearResult.clusters.forEach(cluster => {
      exporter.addSpace(3)
      exporter.addText(`Cluster ${cluster.id} - ${cluster.size} regions`, 11)
      
      if (cluster.centroid) {
        exporter.addText(`  IPM: ${cluster.centroid.ipm?.toFixed(2)}`)
        exporter.addText(`  Garis Kemiskinan: Rp ${cluster.centroid.garis_kemiskinan?.toLocaleString('id-ID')}`)
        exporter.addText(`  Pengeluaran Per Kapita: Rp ${cluster.centroid.pengeluaran_per_kapita?.toLocaleString('id-ID')}`)
      }
    })
  }

  exporter.addPageNumbers()
  
  const filename = `clustering-analysis-yearly-${new Date().getTime()}.pdf`
  exporter.save(filename)
  
  return filename
}

/**
 * Export all years results to PDF
 */
export async function exportAllYearsResultsToPDF(results) {
  const exporter = new PDFExporter()
  exporter.initPDF()

  // Cover page
  const resultData = results.results_per_year?.all_years || results
  
  const metadata = {
    'Algorithm': resultData.algorithm,
    'Years Processed': resultData.summary?.years_processed?.join(', ') || 'Multiple years',
    'Total Clusters': resultData.summary?.num_clusters,
    'Generated': new Date().toLocaleDateString('id-ID')
  }

  exporter.addCoverPage(
    'Clustering Analysis Report',
    'All Years Wide Format Analysis',
    metadata
  )

  // Summary
  exporter.addTitle('Analysis Summary', 18)
  exporter.addLine()
  
  exporter.addKeyValue('Algorithm', resultData.algorithm)
  exporter.addKeyValue('Number of Clusters', resultData.summary.num_clusters)
  exporter.addKeyValue('Total Regions', resultData.summary.total_regions)
  
  if (resultData.evaluation) {
    exporter.addSpace(5)
    exporter.addSubtitle('Evaluation Metrics', 12)
    exporter.addKeyValue('Davies-Bouldin Index', resultData.evaluation.davies_bouldin?.toFixed(4))
    exporter.addKeyValue('Silhouette Score', resultData.evaluation.silhouette_score?.toFixed(4))
  }

  // Cluster details
  exporter.addSpace(10)
  exporter.addSubtitle('Cluster Details', 14)
  
  resultData.clusters.forEach(cluster => {
    exporter.checkPageBreak(40)
    exporter.addSpace(5)
    exporter.addText(`Cluster ${cluster.id} - ${cluster.size} regions`, 12)
    
    if (cluster.centroid) {
      exporter.addText(`Average IPM: ${cluster.centroid.ipm?.toFixed(2)}`)
      exporter.addText(`Average Garis Kemiskinan: Rp ${cluster.centroid.garis_kemiskinan?.toLocaleString('id-ID')}`)
      exporter.addText(`Average Pengeluaran: Rp ${cluster.centroid.pengeluaran_per_kapita?.toLocaleString('id-ID')}`)
    }

    // Sample members
    exporter.addSpace(3)
    exporter.addText('Sample Regions:', 10)
    const sampleMembers = cluster.members.slice(0, 5)
    sampleMembers.forEach(member => {
      exporter.addText(`  • ${member.kabupaten_kota}`, 9)
    })
    
    if (cluster.members.length > 5) {
      exporter.addText(`  ... and ${cluster.members.length - 5} more regions`, 9)
    }
  })

  exporter.addPageNumbers()
  
  const filename = `clustering-analysis-all-years-${new Date().getTime()}.pdf`
  exporter.save(filename)
  
  return filename
}
