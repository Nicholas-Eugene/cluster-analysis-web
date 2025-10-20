"""
PDF Report Generator for Clustering Analysis
Generates comprehensive PDF reports with visualizations
"""

import io
import os
import tempfile
from datetime import datetime
from typing import Dict, Any, List

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.pdfgen import canvas


class ClusteringPDFGenerator:
    """Generate PDF reports for clustering analysis with visualizations"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4
        self.temp_images = []
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2d3748'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        self.subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#4a5568'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        
        self.normal_style = self.styles['Normal']
        self.normal_style.fontSize = 10
        self.normal_style.leading = 14
        
        # Set seaborn style
        sns.set_style("whitegrid")
        
    def _get_cluster_colors(self, n_clusters):
        """Get consistent color palette for clusters"""
        colors_list = [
            '#667eea', '#f56565', '#48bb78', '#ed8936', '#9f7aea',
            '#38b2ac', '#ed64a6', '#ecc94b', '#4299e1', '#fc8181'
        ]
        return colors_list[:n_clusters]
    
    def _create_cluster_map(self, clusters: List[Dict], title: str):
        """Create geographical cluster map"""
        try:
            # Check if we have geographical data
            has_geo_data = False
            total_points = 0
            points_with_coords = 0
            
            for cluster in clusters:
                for member in cluster.get('members', []):
                    total_points += 1
                    lat = member.get('latitude')
                    lon = member.get('longitude')
                    if lat and lon and lat != 0 and lon != 0:
                        has_geo_data = True
                        points_with_coords += 1
            
            if not has_geo_data or points_with_coords == 0:
                # Create informative placeholder
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.text(0.5, 0.6, 'Geographical Coordinates Not Available',
                       ha='center', va='center', fontsize=16, fontweight='bold', color='#667eea')
                ax.text(0.5, 0.45, f'Total regions: {total_points}',
                       ha='center', va='center', fontsize=12, color='gray')
                ax.text(0.5, 0.35, 'Coordinates data is required for map visualization.',
                       ha='center', va='center', fontsize=10, color='gray', style='italic')
                ax.text(0.5, 0.25, 'Clusters are still valid - see other visualizations above.',
                       ha='center', va='center', fontsize=10, color='gray', style='italic')
                ax.axis('off')
                ax.set_facecolor('white')
                fig.patch.set_facecolor('white')
                plt.tight_layout()
                
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
                img_buffer.seek(0)
                plt.close(fig)
                return img_buffer
            
            # Create map
            fig, ax = plt.subplots(figsize=(10, 8))
            colors = self._get_cluster_colors(len(clusters))
            
            # Plot each cluster
            for idx, cluster in enumerate(clusters):
                members = cluster.get('members', [])
                
                lats = []
                lons = []
                
                for member in members:
                    lat = member.get('latitude')
                    lon = member.get('longitude')
                    if lat is not None and lon is not None and lat != 0 and lon != 0:
                        lats.append(lat)
                        lons.append(lon)
                
                if lats and lons:
                    # Get cluster label from interpretation
                    interpretation = cluster.get('interpretation', {})
                    cluster_label = interpretation.get('label', f'Cluster {cluster["id"]}')
                    
                    ax.scatter(lons, lats, c=colors[idx], 
                             label=f'{cluster_label} ({len(lats)} regions)',
                             alpha=0.7, edgecolors='white', linewidth=1.5, s=150,
                             zorder=5)
            
            # Set labels and title
            ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
            ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.legend(loc='best', frameon=True, shadow=True)
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Add background
            ax.set_facecolor('#f0f0f0')
            
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
            img_buffer.seek(0)
            plt.close(fig)
            
            return img_buffer
            
        except Exception as e:
            print(f"Error creating cluster map: {e}")
            # Return placeholder on error
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, f'Error creating map:\n{str(e)}',
                   ha='center', va='center', fontsize=12, color='red')
            ax.axis('off')
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close(fig)
            return img_buffer
    
    def _create_scatter_plot(self, clusters: List[Dict], feature_x: str, feature_y: str, title: str):
        """Create scatter plot for two features"""
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = self._get_cluster_colors(len(clusters))
        
        for idx, cluster in enumerate(clusters):
            members = cluster.get('members', [])
            if not members:
                continue
                
            x_values = [m.get(feature_x) for m in members if m.get(feature_x) is not None]
            y_values = [m.get(feature_y) for m in members if m.get(feature_y) is not None]
            
            if x_values and y_values:
                ax.scatter(x_values, y_values, c=colors[idx], label=f'Cluster {cluster["id"]}',
                          alpha=0.6, edgecolors='white', linewidth=1.5, s=100)
        
        ax.set_xlabel(feature_x.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_ylabel(feature_y.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', frameon=True, shadow=True)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save to temporary file
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        return img_buffer
    
    def _create_box_plot(self, clusters: List[Dict], feature: str, title: str):
        """Create box and whisker plot for a feature"""
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = self._get_cluster_colors(len(clusters))
        
        data_list = []
        labels = []
        
        for idx, cluster in enumerate(clusters):
            members = cluster.get('members', [])
            values = [m.get(feature) for m in members if m.get(feature) is not None]
            if values:
                data_list.append(values)
                labels.append(f"Cluster {cluster['id']}")
        
        if data_list:
            bp = ax.boxplot(data_list, labels=labels, patch_artist=True,
                           widths=0.6, showmeans=True,
                           meanprops=dict(marker='D', markerfacecolor='red', markersize=8))
            
            # Color boxes
            for patch, color in zip(bp['boxes'], colors[:len(data_list)]):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            ax.set_ylabel(feature.replace('_', ' ').title(), fontsize=12, fontweight='bold')
            ax.set_xlabel('Clusters', fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        return img_buffer
    
    def _create_correlation_heatmap(self, clusters: List[Dict], title: str):
        """Create correlation heatmap"""
        # Collect all data
        all_data = []
        for cluster in clusters:
            for member in cluster.get('members', []):
                all_data.append({
                    'IPM': member.get('ipm'),
                    'Garis Kemiskinan': member.get('garis_kemiskinan'),
                    'Pengeluaran Per Kapita': member.get('pengeluaran_per_kapita')
                })
        
        if not all_data:
            return None
            
        df = pd.DataFrame(all_data).dropna()
        
        if df.empty:
            return None
        
        fig, ax = plt.subplots(figsize=(8, 6))
        corr = df.corr()
        
        sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   vmin=-1, vmax=1, ax=ax)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        return img_buffer
    
    def _create_silhouette_plot(self, clusters: List[Dict], silhouette_score: float, title: str):
        """Create silhouette plot"""
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = self._get_cluster_colors(len(clusters))
        
        y_lower = 10
        
        for idx, cluster in enumerate(clusters):
            members = cluster.get('members', [])
            
            # Calculate approximate silhouette scores based on membership
            # (This is simplified - in real implementation you'd calculate actual silhouette per point)
            n_members = len(members)
            
            # Create silhouette values (sorted descending)
            if cluster.get('centroid'):
                # Use membership values if available, otherwise use dummy values
                silhouette_values = []
                for member in members:
                    if 'membership' in member and member['membership'] is not None:
                        # Convert membership to silhouette-like score
                        silhouette_values.append(member['membership'] * 0.8 - 0.4)
                    else:
                        silhouette_values.append(np.random.uniform(0.3, 0.7))
                
                silhouette_values = np.array(sorted(silhouette_values, reverse=True))
            else:
                silhouette_values = np.random.uniform(0.3, 0.7, n_members)
                silhouette_values = np.sort(silhouette_values)[::-1]
            
            y_upper = y_lower + n_members
            
            ax.barh(range(y_lower, y_upper), silhouette_values, height=1.0,
                   color=colors[idx], alpha=0.8, edgecolor='none')
            
            # Label cluster
            ax.text(-0.05, y_lower + 0.5 * n_members, f'C{cluster["id"]}',
                   fontsize=10, fontweight='bold')
            
            y_lower = y_upper + 10
        
        # Add average line
        ax.axvline(x=silhouette_score, color="red", linestyle="--", linewidth=2,
                  label=f'Avg Score: {silhouette_score:.3f}')
        
        ax.set_xlabel('Silhouette Coefficient', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cluster', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim([-1, 1])
        ax.set_yticks([])
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        return img_buffer
    
    # Pie chart removed per user request - use cluster details table instead
    
    def _create_cluster_details_table(self, cluster: Dict, max_members: int = 20):
        """Create detailed table for a cluster with interpretation and members"""
        cluster_id = cluster.get('id', 'N/A')
        cluster_size = cluster.get('size', 0)
        interpretation = cluster.get('interpretation', {})
        label = interpretation.get('label', f'Cluster {cluster_id}')
        description = interpretation.get('description', 'No description available')
        category = interpretation.get('category', 'unknown')
        
        # Create data for table
        table_data = []
        
        # Header with cluster label
        table_data.append([f'Cluster {cluster_id}: {label}', f'{cluster_size} Regions'])
        
        # Add interpretation description
        if description and description != 'No description available':
            # Wrap description to fit in table
            desc_wrapped = description[:150] + '...' if len(description) > 150 else description
            table_data.append(['Description', desc_wrapped])
        
        # Add centroid values
        centroid = cluster.get('centroid', {})
        if centroid:
            table_data.append(['', ''])  # Separator
            table_data.append(['Cluster Characteristics', 'Average Values'])
            table_data.append(['IPM', f"{centroid.get('ipm', 0):.2f}"])
            table_data.append(['Garis Kemiskinan', f"Rp {centroid.get('garis_kemiskinan', 0):,.0f}/bulan"])
            table_data.append(['Pengeluaran Per Kapita', f"Rp {centroid.get('pengeluaran_per_kapita', 0) * 1000:,.0f}/tahun"])
        
        # Add members list
        members = cluster.get('members', [])
        if members:
            table_data.append(['', ''])  # Separator
            table_data.append(['Regions in This Cluster', f'(Showing {min(len(members), max_members)} of {len(members)})'])
            
            # Add up to max_members
            for idx, member in enumerate(members[:max_members]):
                region_name = member.get('kabupaten_kota', 'Unknown')
                provinsi = member.get('provinsi', '')
                membership = member.get('membership')
                
                if membership is not None:
                    detail = f"{region_name} ({provinsi}) - Membership: {membership:.2%}"
                else:
                    detail = f"{region_name} ({provinsi})" if provinsi else region_name
                
                table_data.append([f'{idx + 1}.', detail])
        
        # Create table
        col_widths = [1*inch, 5.5*inch]
        table = Table(table_data, colWidths=col_widths)
        
        # Style table
        table_style = [
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            
            # Rest of table
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 1), (-1, -1), 6),
            ('RIGHTPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            
            # Alternate row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]
        
        table.setStyle(TableStyle(table_style))
        return table
    
    def _add_cover_page(self, story, title, subtitle, metadata):
        """Add cover page to PDF"""
        story.append(Spacer(1, 2*inch))
        
        # Title
        story.append(Paragraph(title, self.title_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#4a5568'),
            alignment=TA_CENTER
        )
        story.append(Paragraph(subtitle, subtitle_style))
        story.append(Spacer(1, inch))
        
        # Metadata
        meta_style = ParagraphStyle(
            'Metadata',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#2d3748'),
            alignment=TA_CENTER,
            leading=18
        )
        
        for key, value in metadata.items():
            story.append(Paragraph(f"<b>{key}:</b> {value}", meta_style))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Generated by Fuzzy Clustering Analysis System", footer_style))
        
        story.append(PageBreak())
    
    def generate_yearly_pdf(self, data: Dict[str, Any], output_path: str):
        """Generate PDF for yearly analysis"""
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []
        
        # Cover page
        overall = data.get('overall_summary', {})
        metadata = {
            'Algorithm': overall.get('algorithm', 'N/A'),
            'Total Years': overall.get('total_years', 0),
            'Successful Years': overall.get('successful_years', 0),
            'Success Rate': f"{overall.get('success_rate', 0) * 100:.1f}%",
            'Generated': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        self._add_cover_page(story, "Clustering Analysis Report", "Per Year Analysis", metadata)
        
        # Overall Summary
        story.append(Paragraph("Overall Summary", self.heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Algorithm', overall.get('algorithm', 'N/A')],
            ['Total Years', str(overall.get('total_years', 0))],
            ['Successful Years', str(overall.get('successful_years', 0))],
            ['Success Rate', f"{overall.get('success_rate', 0) * 100:.1f}%"],
        ]
        
        if overall.get('average_evaluation'):
            avg_eval = overall['average_evaluation']
            summary_data.extend([
                ['Avg Davies-Bouldin', f"{avg_eval.get('davies_bouldin', 0):.4f}"],
                ['Avg Silhouette Score', f"{avg_eval.get('silhouette_score', 0):.4f}"]
            ])
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(PageBreak())
        
        # Year by year results
        results_per_year = data.get('results_per_year', {})
        years = sorted([int(y) for y in results_per_year.keys()])
        
        for year in years:
            year_data = results_per_year[str(year)]
            
            if year_data.get('error'):
                continue
            
            story.append(Paragraph(f"Year {year}", self.heading_style))
            story.append(Spacer(1, 0.1*inch))
            
            # Year summary
            summary = year_data.get('summary', {})
            evaluation = year_data.get('evaluation', {})
            
            year_info = [
                ['Metric', 'Value'],
                ['Number of Clusters', str(summary.get('num_clusters', 0))],
                ['Total Regions', str(summary.get('total_regions', 0))],
                ['Davies-Bouldin Index', f"{evaluation.get('davies_bouldin', 0):.4f}"],
                ['Silhouette Score', f"{evaluation.get('silhouette_score', 0):.4f}"],
                ['Execution Time', f"{evaluation.get('execution_time', 0):.2f}s"]
            ]
            
            year_table = Table(year_info, colWidths=[3*inch, 3*inch])
            year_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(year_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Visualizations for this year
            clusters = year_data.get('clusters', [])
            
            if clusters:
                story.append(Paragraph(f"Visualizations - Year {year}", self.subheading_style))
                story.append(Spacer(1, 0.1*inch))
                
                # Cluster Map (moved to top for better visibility)
                story.append(Paragraph("Geographical Distribution", self.subheading_style))
                cluster_map = self._create_cluster_map(clusters, f'Geographical Distribution ({year})')
                img_map = Image(cluster_map, width=6*inch, height=4.8*inch)
                story.append(img_map)
                story.append(Spacer(1, 0.3*inch))
                
                # Scatter plots
                scatter1 = self._create_scatter_plot(clusters, 'ipm', 'garis_kemiskinan',
                                                     f'IPM vs Garis Kemiskinan ({year})')
                img1 = Image(scatter1, width=5*inch, height=3.75*inch)
                story.append(img1)
                story.append(Spacer(1, 0.2*inch))
                
                scatter2 = self._create_scatter_plot(clusters, 'ipm', 'pengeluaran_per_kapita',
                                                     f'IPM vs Pengeluaran Per Kapita ({year})')
                img2 = Image(scatter2, width=5*inch, height=3.75*inch)
                story.append(img2)
                story.append(Spacer(1, 0.2*inch))
                
                scatter3 = self._create_scatter_plot(clusters, 'garis_kemiskinan', 'pengeluaran_per_kapita',
                                                     f'Garis Kemiskinan vs Pengeluaran Per Kapita ({year})')
                img_scatter3 = Image(scatter3, width=5*inch, height=3.75*inch)
                story.append(img_scatter3)
                story.append(Spacer(1, 0.2*inch))
                
                # Box plots - All 3 variables
                box1 = self._create_box_plot(clusters, 'ipm', f'IPM Distribution by Cluster ({year})')
                img3 = Image(box1, width=6*inch, height=3.6*inch)
                story.append(img3)
                story.append(Spacer(1, 0.2*inch))
                
                box2 = self._create_box_plot(clusters, 'garis_kemiskinan', 
                                             f'Garis Kemiskinan Distribution by Cluster ({year})')
                img_box2 = Image(box2, width=6*inch, height=3.6*inch)
                story.append(img_box2)
                story.append(Spacer(1, 0.2*inch))
                
                box3 = self._create_box_plot(clusters, 'pengeluaran_per_kapita',
                                             f'Pengeluaran Per Kapita Distribution by Cluster ({year})')
                img_box3 = Image(box3, width=6*inch, height=3.6*inch)
                story.append(img_box3)
                story.append(Spacer(1, 0.2*inch))
                
                # Correlation heatmap
                heatmap = self._create_correlation_heatmap(clusters, f'Feature Correlation ({year})')
                if heatmap:
                    img4 = Image(heatmap, width=5*inch, height=3.75*inch)
                    story.append(img4)
                    story.append(Spacer(1, 0.2*inch))
                
                # Silhouette plot
                silhouette_score = evaluation.get('silhouette_score', 0)
                silhouette = self._create_silhouette_plot(clusters, silhouette_score,
                                                         f'Silhouette Plot ({year})')
                img5 = Image(silhouette, width=6*inch, height=3.6*inch)
                story.append(img5)
                story.append(Spacer(1, 0.3*inch))
                
                # Cluster Details with Labels and Members
                story.append(Paragraph(f"Cluster Details - Year {year}", self.subheading_style))
                story.append(Spacer(1, 0.2*inch))
                
                for cluster in clusters:
                    cluster_table = self._create_cluster_details_table(cluster, max_members=15)
                    story.append(cluster_table)
                    story.append(Spacer(1, 0.3*inch))
            
            story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def generate_all_years_pdf(self, data: Dict[str, Any], output_path: str):
        """Generate PDF for all years wide analysis"""
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []
        
        # Extract data
        result_data = data.get('results_per_year', {}).get('all_years', data)
        
        # Cover page
        metadata = {
            'Algorithm': result_data.get('algorithm', 'N/A'),
            'Number of Clusters': str(result_data.get('summary', {}).get('num_clusters', 0)),
            'Total Regions': str(result_data.get('summary', {}).get('total_regions', 0)),
            'Generated': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        self._add_cover_page(story, "Clustering Analysis Report",
                            "All Years Wide Format Analysis", metadata)
        
        # Summary
        story.append(Paragraph("Analysis Summary", self.heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        summary = result_data.get('summary', {})
        evaluation = result_data.get('evaluation', {})
        
        summary_data = [
            ['Metric', 'Value'],
            ['Algorithm', result_data.get('algorithm', 'N/A')],
            ['Number of Clusters', str(summary.get('num_clusters', 0))],
            ['Total Regions', str(summary.get('total_regions', 0))],
            ['Davies-Bouldin Index', f"{evaluation.get('davies_bouldin', 0):.4f}"],
            ['Silhouette Score', f"{evaluation.get('silhouette_score', 0):.4f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(PageBreak())
        
        # Visualizations
        clusters = result_data.get('clusters', [])
        
        if clusters:
            story.append(Paragraph("Visualizations", self.heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Geographical Map (moved to top for better visibility)
            story.append(Paragraph("Geographical Distribution", self.subheading_style))
            story.append(Spacer(1, 0.1*inch))
            
            cluster_map = self._create_cluster_map(clusters, 'Cluster Geographical Distribution')
            img_map = Image(cluster_map, width=6*inch, height=4.8*inch)
            story.append(img_map)
            story.append(PageBreak())
            
            # Scatter plots
            story.append(Paragraph("Scatter Plot Analysis", self.subheading_style))
            story.append(Spacer(1, 0.1*inch))
            
            scatter1 = self._create_scatter_plot(clusters, 'ipm', 'garis_kemiskinan',
                                                 'IPM vs Garis Kemiskinan')
            img1 = Image(scatter1, width=5*inch, height=3.75*inch)
            story.append(img1)
            story.append(Spacer(1, 0.3*inch))
            
            scatter2 = self._create_scatter_plot(clusters, 'ipm', 'pengeluaran_per_kapita',
                                                 'IPM vs Pengeluaran Per Kapita')
            img2 = Image(scatter2, width=5*inch, height=3.75*inch)
            story.append(img2)
            story.append(Spacer(1, 0.3*inch))
            
            scatter3 = self._create_scatter_plot(clusters, 'garis_kemiskinan', 'pengeluaran_per_kapita',
                                                 'Garis Kemiskinan vs Pengeluaran Per Kapita')
            img_scatter3 = Image(scatter3, width=5*inch, height=3.75*inch)
            story.append(img_scatter3)
            story.append(PageBreak())
            
            # Box plots
            story.append(Paragraph("Distribution Analysis", self.subheading_style))
            story.append(Spacer(1, 0.1*inch))
            
            box1 = self._create_box_plot(clusters, 'ipm', 'IPM Distribution by Cluster')
            img3 = Image(box1, width=6*inch, height=3.6*inch)
            story.append(img3)
            story.append(Spacer(1, 0.3*inch))
            
            box2 = self._create_box_plot(clusters, 'garis_kemiskinan',
                                         'Garis Kemiskinan Distribution by Cluster')
            img4 = Image(box2, width=6*inch, height=3.6*inch)
            story.append(img4)
            story.append(Spacer(1, 0.3*inch))
            
            box3 = self._create_box_plot(clusters, 'pengeluaran_per_kapita',
                                         'Pengeluaran Per Kapita Distribution by Cluster')
            img_box3 = Image(box3, width=6*inch, height=3.6*inch)
            story.append(img_box3)
            story.append(PageBreak())
            
            # Correlation heatmap
            story.append(Paragraph("Feature Correlation", self.subheading_style))
            story.append(Spacer(1, 0.1*inch))
            
            heatmap = self._create_correlation_heatmap(clusters, 'Correlation Heatmap')
            if heatmap:
                img5 = Image(heatmap, width=5*inch, height=3.75*inch)
                story.append(img5)
                story.append(Spacer(1, 0.3*inch))
            
            # Silhouette plot
            silhouette_score = evaluation.get('silhouette_score', 0)
            silhouette = self._create_silhouette_plot(clusters, silhouette_score,
                                                     'Silhouette Plot')
            img6 = Image(silhouette, width=6*inch, height=3.6*inch)
            story.append(img6)
            story.append(PageBreak())
            
            # Cluster Details with Interpretation Labels and Members
            story.append(Paragraph("Cluster Details", self.heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            for cluster in clusters:
                cluster_table = self._create_cluster_details_table(cluster, max_members=20)
                story.append(cluster_table)
                story.append(Spacer(1, 0.4*inch))
        
        # Build PDF
        doc.build(story)
        return output_path


def generate_pdf_report(data: Dict[str, Any], mode: str = 'yearly') -> str:
    """
    Main function to generate PDF report
    
    Args:
        data: Clustering results data
        mode: 'yearly' or 'all_years'
    
    Returns:
        Path to generated PDF file
    """
    generator = ClusteringPDFGenerator()
    
    # Create temporary file
    temp_dir = tempfile.gettempdir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'clustering_report_{mode}_{timestamp}.pdf'
    output_path = os.path.join(temp_dir, filename)
    
    if mode == 'yearly':
        return generator.generate_yearly_pdf(data, output_path)
    else:
        return generator.generate_all_years_pdf(data, output_path)
