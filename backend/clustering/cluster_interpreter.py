"""
Cluster Interpretation Module
Automatically interprets and labels clusters based on their characteristics
"""

import numpy as np
from typing import Dict, List, Any


def interpret_cluster_label(centroid: Dict[str, float], all_centroids: List[Dict[str, float]]) -> Dict[str, Any]:
    """
    Interpret cluster based on its centroid values relative to other clusters
    
    Args:
        centroid: The centroid of the cluster to interpret
        all_centroids: All cluster centroids for comparison
    
    Returns:
        Dictionary with label and description
    """
    
    # Extract values
    ipm = centroid.get('ipm', 0)
    garis_kemiskinan = centroid.get('garis_kemiskinan', 0)  # rupiah/kapita/bulan
    pengeluaran = centroid.get('pengeluaran_per_kapita', 0)  # ribu rupiah/orang/tahun
    
    # Convert pengeluaran to rupiah/kapita/bulan for comparison
    # From: ribu rupiah/orang/tahun
    # To: rupiah/kapita/bulan
    pengeluaran_per_bulan = (pengeluaran * 1000) / 12  # rupiah/kapita/bulan
    
    # Calculate relative values across all clusters
    ipm_values = [c.get('ipm', 0) for c in all_centroids]
    pengeluaran_values = [c.get('pengeluaran_per_kapita', 0) for c in all_centroids]
    
    ipm_min = min(ipm_values)
    ipm_max = max(ipm_values)
    ipm_range = ipm_max - ipm_min
    
    pengeluaran_min = min(pengeluaran_values)
    pengeluaran_max = max(pengeluaran_values)
    pengeluaran_range = pengeluaran_max - pengeluaran_min
    
    # Normalize values (0-1 scale)
    if ipm_range > 0:
        ipm_normalized = (ipm - ipm_min) / ipm_range
    else:
        ipm_normalized = 0.5
    
    if pengeluaran_range > 0:
        pengeluaran_normalized = (pengeluaran - pengeluaran_min) / pengeluaran_range
    else:
        pengeluaran_normalized = 0.5
    
    # Compare pengeluaran with garis kemiskinan
    ratio_to_poverty = pengeluaran_per_bulan / garis_kemiskinan if garis_kemiskinan > 0 else 1.0
    
    # Determine cluster label based on characteristics
    label = ""
    description = ""
    category = ""
    color_code = ""
    
    # IPM thresholds (normalized)
    IPM_LOW = 0.33
    IPM_HIGH = 0.67
    
    # Poverty line ratio thresholds
    BELOW_POVERTY = 1.0
    SLIGHTLY_ABOVE = 1.3
    WELL_ABOVE = 2.0
    
    # Interpret cluster
    if ipm_normalized < IPM_LOW and ratio_to_poverty < BELOW_POVERTY:
        # Cluster Miskin
        label = "Cluster Miskin"
        category = "poor"
        color_code = "#f56565"  # Red
        description = (
            f"IPM rendah ({ipm:.2f}), "
            f"pengeluaran per kapita ({pengeluaran:.0f} ribu/tahun atau "
            f"Rp {pengeluaran_per_bulan:,.0f}/bulan) berada di bawah garis kemiskinan "
            f"(Rp {garis_kemiskinan:,.0f}/bulan). "
            f"Daerah dalam cluster ini memerlukan perhatian khusus untuk program pengentasan kemiskinan."
        )
        
    elif ipm_normalized > IPM_HIGH and ratio_to_poverty > WELL_ABOVE:
        # Cluster Tidak Miskin / Sejahtera
        label = "Cluster Sejahtera"
        category = "prosperous"
        color_code = "#48bb78"  # Green
        description = (
            f"IPM tinggi ({ipm:.2f}), "
            f"pengeluaran per kapita ({pengeluaran:.0f} ribu/tahun atau "
            f"Rp {pengeluaran_per_bulan:,.0f}/bulan) jauh di atas garis kemiskinan "
            f"(Rp {garis_kemiskinan:,.0f}/bulan). "
            f"Daerah dalam cluster ini memiliki kesejahteraan yang baik dan dapat menjadi role model."
        )
        
    elif ipm_normalized <= IPM_LOW and ratio_to_poverty > BELOW_POVERTY:
        # IPM rendah tapi pengeluaran di atas garis kemiskinan
        label = "Cluster Rentan"
        category = "vulnerable"
        color_code = "#ed8936"  # Orange
        description = (
            f"IPM rendah ({ipm:.2f}) meskipun pengeluaran per kapita "
            f"({pengeluaran:.0f} ribu/tahun atau Rp {pengeluaran_per_bulan:,.0f}/bulan) "
            f"di atas garis kemiskinan (Rp {garis_kemiskinan:,.0f}/bulan). "
            f"Daerah ini memerlukan peningkatan kualitas pendidikan dan kesehatan."
        )
        
    elif ipm_normalized > IPM_HIGH and ratio_to_poverty < SLIGHTLY_ABOVE:
        # IPM tinggi tapi pengeluaran rendah
        label = "Cluster Berkembang"
        category = "developing"
        color_code = "#4299e1"  # Blue
        description = (
            f"IPM tinggi ({ipm:.2f}) namun pengeluaran per kapita "
            f"({pengeluaran:.0f} ribu/tahun atau Rp {pengeluaran_per_bulan:,.0f}/bulan) "
            f"masih mendekati garis kemiskinan (Rp {garis_kemiskinan:,.0f}/bulan). "
            f"Daerah ini memerlukan peningkatan ekonomi untuk meningkatkan daya beli."
        )
        
    else:
        # Cluster Sedang / Menengah
        label = "Cluster Menengah"
        category = "middle"
        color_code = "#ecc94b"  # Yellow
        
        if ratio_to_poverty < SLIGHTLY_ABOVE:
            description = (
                f"IPM sedang ({ipm:.2f}), "
                f"pengeluaran per kapita ({pengeluaran:.0f} ribu/tahun atau "
                f"Rp {pengeluaran_per_bulan:,.0f}/bulan) sedikit di atas garis kemiskinan "
                f"(Rp {garis_kemiskinan:,.0f}/bulan). "
                f"Daerah dalam cluster ini memerlukan program berkelanjutan untuk mencegah kemiskinan dan meningkatkan kesejahteraan."
            )
        else:
            description = (
                f"IPM sedang ({ipm:.2f}), "
                f"pengeluaran per kapita ({pengeluaran:.0f} ribu/tahun atau "
                f"Rp {pengeluaran_per_bulan:,.0f}/bulan) di atas garis kemiskinan "
                f"(Rp {garis_kemiskinan:,.0f}/bulan). "
                f"Daerah dalam cluster ini berada dalam kondisi cukup baik namun masih dapat ditingkatkan."
            )
    
    # Additional metrics
    metrics = {
        'ipm_level': _get_ipm_level(ipm_normalized),
        'poverty_status': _get_poverty_status(ratio_to_poverty),
        'ipm_score': ipm,
        'poverty_line_ratio': ratio_to_poverty,
        'expenditure_per_month': pengeluaran_per_bulan,
        'poverty_line': garis_kemiskinan
    }
    
    return {
        'label': label,
        'category': category,
        'description': description,
        'color_code': color_code,
        'metrics': metrics
    }


def _get_ipm_level(ipm_normalized: float) -> str:
    """Get IPM level description"""
    if ipm_normalized < 0.33:
        return "Rendah"
    elif ipm_normalized < 0.67:
        return "Sedang"
    else:
        return "Tinggi"


def _get_poverty_status(ratio: float) -> str:
    """Get poverty status description"""
    if ratio < 1.0:
        return "Di Bawah Garis Kemiskinan"
    elif ratio < 1.3:
        return "Sedikit Di Atas Garis Kemiskinan"
    elif ratio < 2.0:
        return "Di Atas Garis Kemiskinan"
    else:
        return "Jauh Di Atas Garis Kemiskinan"


def add_cluster_interpretations(clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Add interpretation labels to all clusters
    
    Args:
        clusters: List of cluster dictionaries
    
    Returns:
        Clusters with added interpretation
    """
    if not clusters:
        return clusters
    
    # Extract all centroids for comparison
    all_centroids = [cluster.get('centroid', {}) for cluster in clusters]
    
    # Add interpretation to each cluster
    for cluster in clusters:
        centroid = cluster.get('centroid', {})
        if centroid:
            interpretation = interpret_cluster_label(centroid, all_centroids)
            cluster['interpretation'] = interpretation
    
    return clusters


def get_cluster_summary_stats(clusters: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get summary statistics of cluster interpretations
    
    Args:
        clusters: List of clusters with interpretations
    
    Returns:
        Summary statistics
    """
    if not clusters:
        return {}
    
    categories = {}
    total_regions = sum(cluster.get('size', 0) for cluster in clusters)
    
    for cluster in clusters:
        interpretation = cluster.get('interpretation', {})
        category = interpretation.get('category', 'unknown')
        size = cluster.get('size', 0)
        
        if category not in categories:
            categories[category] = {
                'count': 0,
                'regions': 0,
                'percentage': 0
            }
        
        categories[category]['count'] += 1
        categories[category]['regions'] += size
    
    # Calculate percentages
    for category in categories:
        if total_regions > 0:
            categories[category]['percentage'] = (categories[category]['regions'] / total_regions) * 100
    
    return {
        'total_clusters': len(clusters),
        'total_regions': total_regions,
        'categories': categories
    }
