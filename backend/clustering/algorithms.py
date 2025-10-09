"""
Clustering algorithms implementation for Indonesian regional data analysis.
Includes Fuzzy C-Means and OPTICS clustering with evaluation metrics.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import OPTICS
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import davies_bouldin_score, silhouette_score
import skfuzzy as fuzz
from typing import Dict, List, Tuple, Any
import time


class ClusteringAlgorithms:
    """
    Main class for clustering algorithms implementation.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        
    def reshape_wide_to_long(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Reshape wide format data (year columns) to long format (year rows).
        
        Args:
            df: Wide format dataframe with columns like ipm_2016, pengeluaran_2016, etc.
            
        Returns:
            Long format dataframe with year as a column
        """
        # Extract available years from column names
        years = set()
        for col in df.columns:
            if '_' in col:
                try:
                    year = int(col.split('_')[-1])
                    if 2015 <= year <= 2025:  # Valid year range
                        years.add(year)
                except ValueError:
                    continue
        
        years = sorted(years)
        
        # Prepare long format data
        long_data = []
        
        for _, row in df.iterrows():
            kabupaten_kota = row.get('kabupaten/kota', row.get('kabupaten_kota', ''))
            
            for year in years:
                # Get values for this year
                ipm_col = f'ipm_{year}'
                pengeluaran_col = f'pengeluaran_{year}'
                garis_kemiskinan_col = f'garis_kemiskinan_{year}'
                
                # Check if all required columns exist and have values
                if (ipm_col in df.columns and pengeluaran_col in df.columns and 
                    garis_kemiskinan_col in df.columns):
                    
                    ipm_val = row.get(ipm_col)
                    pengeluaran_val = row.get(pengeluaran_col)
                    garis_kemiskinan_val = row.get(garis_kemiskinan_col)
                    
                    # Only add if all values are not null
                    if (pd.notna(ipm_val) and pd.notna(pengeluaran_val) and 
                        pd.notna(garis_kemiskinan_val)):
                        
                        long_data.append({
                            'kabupaten_kota': kabupaten_kota,
                            'tahun': year,
                            'ipm': float(ipm_val),
                            'pengeluaran_per_kapita': float(pengeluaran_val),
                            'garis_kemiskinan': float(garis_kemiskinan_val)
                        })
        
        return pd.DataFrame(long_data)
        
    def preprocess_data(self, df: pd.DataFrame, features: List[str], 
                       selected_year: str = None) -> Tuple[np.ndarray, pd.DataFrame]:
        """
        Preprocess data for clustering.
        
        Args:
            df: Input dataframe (can be wide or long format)
            features: List of feature column names
            selected_year: Optional year filter
            
        Returns:
            Tuple of (scaled_data, original_dataframe)
        """
        # Check if data is in wide format (has year columns)
        has_year_columns = any('_' in col and col.split('_')[-1].isdigit() 
                              for col in df.columns)
        
        if has_year_columns:
            # Convert wide format to long format
            df_long = self.reshape_wide_to_long(df)
        else:
            # Already in long format
            df_long = df.copy()
        
        # Filter by year if specified
        if selected_year:
            try:
                year_int = int(selected_year)
                df_long = df_long[df_long['tahun'] == year_int]
            except (ValueError, KeyError):
                pass
        
        # Remove rows with missing values in required features
        df_clean = df_long.dropna(subset=features)
        
        if df_clean.empty:
            raise ValueError("No valid data found after preprocessing")
        
        # Extract feature data
        feature_data = df_clean[features].values
        
        # Scale the features
        scaled_data = self.scaler.fit_transform(feature_data)
        
        return scaled_data, df_clean
    
    def fuzzy_c_means(self, df: pd.DataFrame, features: List[str], 
                     n_clusters: int = 3, m: float = 2.0, 
                     max_iter: int = 300, error: float = 1e-5, 
                     selected_year: str = None) -> Dict[str, Any]:
        """
        Perform Fuzzy C-Means clustering.
        
        Args:
            df: Input dataframe
            features: List of feature column names to cluster on
            n_clusters: Number of clusters
            m: Fuzziness parameter
            max_iter: Maximum iterations
            error: Convergence threshold
            
        Returns:
            Dictionary containing clustering results
        """
        start_time = time.time()
        
        # Preprocess data
        scaled_data, df_clean = self.preprocess_data(df, features, selected_year)
        
        # Transpose data for skfuzzy (expects features x samples)
        data_T = scaled_data.T
        
        # Perform FCM clustering
        cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
            data_T, n_clusters, m, error=error, maxiter=max_iter
        )
        
        # Get cluster assignments (highest membership)
        cluster_labels = np.argmax(u, axis=0)
        
        # Calculate evaluation metrics
        db_score = davies_bouldin_score(scaled_data, cluster_labels)
        sil_score = silhouette_score(scaled_data, cluster_labels)
        
        execution_time = time.time() - start_time
        
        # Prepare results
        results = {
            'algorithm': 'Fuzzy C-Means',
            'summary': {
                'total_regions': len(df_clean),
                'num_clusters': n_clusters,
                'iterations': p,
                'execution_time': execution_time,
                'fuzziness_parameter': m,
                'partition_coefficient': float(fpc)
            },
            'evaluation': {
                'davies_bouldin': float(db_score),
                'silhouette_score': float(sil_score)
            },
            'clusters': []
        }
        
        # Create cluster information
        for i in range(n_clusters):
            cluster_mask = cluster_labels == i
            cluster_members = df_clean[cluster_mask].copy()
            
            if len(cluster_members) > 0:
                # Calculate centroid in original scale
                centroid = {}
                for feature in features:
                    centroid[feature] = float(cluster_members[feature].mean())
                
                # Prepare member information
                members = []
                for idx, (_, row) in enumerate(cluster_members.iterrows()):
                    member_info = {
                        'kabupaten_kota': str(row.get('kabupaten_kota', '')),
                        'provinsi': str(row.get('provinsi', '')),
                        'tahun': int(row.get('tahun', 0)),
                        'latitude': float(row.get('latitude', 0.0)),
                        'longitude': float(row.get('longitude', 0.0)),
                        'membership': float(u[i, np.where(cluster_labels == i)[0][idx]])
                    }
                    
                    # Add feature values
                    for feature in features:
                        member_info[feature] = float(row.get(feature, 0.0))
                    
                    members.append(member_info)
                
                cluster_info = {
                    'id': i,
                    'centroid': centroid,
                    'size': len(members),
                    'members': members
                }
                
                results['clusters'].append(cluster_info)
        
        return results
    
    def optics_clustering(self, df: pd.DataFrame, features: List[str],
                         min_samples: int = 5, xi: float = 0.05,
                         min_cluster_size: float = 0.05, 
                         selected_year: str = None) -> Dict[str, Any]:
        """
        Perform OPTICS clustering.
        
        Args:
            df: Input dataframe
            features: List of feature column names to cluster on
            min_samples: Minimum samples in neighborhood
            xi: Minimum steepness on reachability plot
            min_cluster_size: Minimum cluster size (as fraction of data)
            
        Returns:
            Dictionary containing clustering results
        """
        start_time = time.time()
        
        # Preprocess data
        scaled_data, df_clean = self.preprocess_data(df, features, selected_year)
        
        # Perform OPTICS clustering
        optics = OPTICS(
            min_samples=min_samples,
            xi=xi,
            min_cluster_size=min_cluster_size
        )
        
        cluster_labels = optics.fit_predict(scaled_data)
        
        # Handle noise points (labeled as -1)
        n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
        
        execution_time = time.time() - start_time
        
        # Calculate evaluation metrics (excluding noise points)
        if n_clusters > 1 and len(set(cluster_labels)) > 1:
            # Only calculate metrics if we have valid clusters
            valid_mask = cluster_labels != -1
            if np.sum(valid_mask) > 1:
                db_score = davies_bouldin_score(scaled_data[valid_mask], cluster_labels[valid_mask])
                sil_score = silhouette_score(scaled_data[valid_mask], cluster_labels[valid_mask])
            else:
                db_score = float('inf')
                sil_score = -1.0
        else:
            db_score = float('inf')
            sil_score = -1.0
        
        # Prepare results
        results = {
            'algorithm': 'OPTICS',
            'summary': {
                'total_regions': len(df_clean),
                'num_clusters': n_clusters,
                'noise_points': int(np.sum(cluster_labels == -1)),
                'execution_time': execution_time,
                'min_samples': min_samples,
                'xi': xi
            },
            'evaluation': {
                'davies_bouldin': float(db_score) if db_score != float('inf') else None,
                'silhouette_score': float(sil_score)
            },
            'clusters': []
        }
        
        # Create cluster information
        unique_labels = set(cluster_labels)
        for label in unique_labels:
            if label == -1:  # Noise points
                cluster_mask = cluster_labels == label
                noise_members = df_clean[cluster_mask].copy()
                
                members = []
                for _, row in noise_members.iterrows():
                    member_info = {
                        'kabupaten_kota': str(row.get('kabupaten_kota', '')),
                        'provinsi': str(row.get('provinsi', '')),
                        'tahun': int(row.get('tahun', 0)),
                        'latitude': float(row.get('latitude', 0.0)),
                        'longitude': float(row.get('longitude', 0.0)),
                        'membership': 1.0  # Noise points have full membership to noise
                    }
                    
                    # Add feature values
                    for feature in features:
                        member_info[feature] = float(row.get(feature, 0.0))
                    
                    members.append(member_info)
                
                cluster_info = {
                    'id': 'noise',
                    'centroid': None,
                    'size': len(members),
                    'members': members
                }
                
                results['clusters'].append(cluster_info)
            else:  # Regular clusters
                cluster_mask = cluster_labels == label
                cluster_members = df_clean[cluster_mask].copy()
                
                if len(cluster_members) > 0:
                    # Calculate centroid
                    centroid = {}
                    for feature in features:
                        centroid[feature] = float(cluster_members[feature].mean())
                    
                    # Prepare member information
                    members = []
                    for _, row in cluster_members.iterrows():
                        member_info = {
                            'kabupaten_kota': str(row.get('kabupaten_kota', '')),
                            'provinsi': str(row.get('provinsi', '')),
                            'tahun': int(row.get('tahun', 0)),
                            'latitude': float(row.get('latitude', 0.0)),
                            'longitude': float(row.get('longitude', 0.0)),
                            'membership': 1.0  # OPTICS gives hard assignments
                        }
                        
                        # Add feature values
                        for feature in features:
                            member_info[feature] = float(row.get(feature, 0.0))
                        
                        members.append(member_info)
                    
                    cluster_info = {
                        'id': int(label),
                        'centroid': centroid,
                        'size': len(members),
                        'members': members
                    }
                    
                    results['clusters'].append(cluster_info)
        
        return results


def get_clustering_results(df: pd.DataFrame, algorithm: str = 'fcm', 
                          features: List[str] = None, **kwargs) -> Dict[str, Any]:
    """
    Main function to get clustering results.
    
    Args:
        df: Input dataframe
        algorithm: 'fcm' for Fuzzy C-Means or 'optics' for OPTICS
        features: List of feature columns to use for clustering
        **kwargs: Additional parameters for the clustering algorithm
        
    Returns:
        Dictionary containing clustering results
    """
    if features is None:
        features = ['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita']
    
    clustering = ClusteringAlgorithms()
    
    if algorithm.lower() == 'fcm':
        return clustering.fuzzy_c_means(df, features, **kwargs)
    elif algorithm.lower() == 'optics':
        return clustering.optics_clustering(df, features, **kwargs)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}. Use 'fcm' or 'optics'.")