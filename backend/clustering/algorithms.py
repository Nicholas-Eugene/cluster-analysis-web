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
        print(f"🔄 Reshaping wide format data...")
        print(f"📊 Input columns: {list(df.columns)}")
        
        # Extract available years from column names
        years = set()
        for col in df.columns:
            if '_' in col and any(metric in col for metric in ['ipm_', 'pengeluaran_', 'garis_kemiskinan_']):
                try:
                    year = int(col.split('_')[-1])
                    if 2015 <= year <= 2025:  # Valid year range
                        years.add(year)
                except ValueError:
                    continue
        
        years = sorted(years)
        print(f"📅 Years found: {years}")
        
        if not years:
            raise ValueError("Tidak ditemukan kolom tahun yang valid. Pastikan format kolom seperti: ipm_2016, pengeluaran_2016, garis_kemiskinan_2016")
        
        # Prepare long format data
        long_data = []
        
        for _, row in df.iterrows():
            # Handle different possible column names for kabupaten/kota
            kabupaten_kota = ''
            for possible_col in ['kabupaten/kota', 'kabupaten_kota', 'Kabupaten/Kota', 'Kabupaten_Kota']:
                if possible_col in df.columns:
                    kabupaten_kota = str(row.get(possible_col, ''))
                    break
            
            if not kabupaten_kota:
                continue  # Skip rows without kabupaten/kota info
            
            for year in years:
                # Get values for this year - exact format as specified
                ipm_col = f'ipm_{year}'
                pengeluaran_col = f'pengeluaran_{year}'
                garis_kemiskinan_col = f'garis_kemiskinan_{year}'
                
                # Check if all required columns exist
                if (ipm_col in df.columns and pengeluaran_col in df.columns and 
                    garis_kemiskinan_col in df.columns):
                    
                    ipm_val = row.get(ipm_col)
                    pengeluaran_val = row.get(pengeluaran_col)
                    garis_kemiskinan_val = row.get(garis_kemiskinan_col)
                    
                    # Only add if all values are not null and not empty
                    if (pd.notna(ipm_val) and pd.notna(pengeluaran_val) and 
                        pd.notna(garis_kemiskinan_val) and
                        str(ipm_val).strip() != '' and 
                        str(pengeluaran_val).strip() != '' and 
                        str(garis_kemiskinan_val).strip() != ''):
                        
                        try:
                            long_data.append({
                                'kabupaten_kota': kabupaten_kota,
                                'tahun': year,
                                'ipm': float(ipm_val),
                                'pengeluaran_per_kapita': float(pengeluaran_val),
                                'garis_kemiskinan': float(garis_kemiskinan_val)
                            })
                        except (ValueError, TypeError) as e:
                            print(f"⚠️ Skipping invalid data for {kabupaten_kota} year {year}: {e}")
                            continue
        
        result_df = pd.DataFrame(long_data)
        print(f"✅ Reshaped to long format: {result_df.shape[0]} rows")
        
        if result_df.empty:
            raise ValueError("Tidak ada data valid yang dapat diproses. Periksa format kolom dan data.")
        
        return result_df
        
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
        # Data is already in long format with standardized column names
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
        
        print(f"🔧 FCM clustering parameters:")
        print(f"   Data size: {len(scaled_data)}")
        print(f"   Features: {features}")
        print(f"   n_clusters: {n_clusters}")
        print(f"   fuzziness (m): {m}")
        print(f"   max_iter: {max_iter}")
        print(f"   tolerance: {error}")
        
        # Check data variance to ensure clustering makes sense
        feature_variance = np.var(scaled_data, axis=0)
        print(f"   Feature variances (scaled): {feature_variance}")
        if np.any(feature_variance < 0.01):
            print("   ⚠️  Warning: Low variance detected in some features")
            
        # Check if we have enough data points for the requested number of clusters
        if len(scaled_data) < n_clusters * 2:
            print(f"   ⚠️  Warning: Only {len(scaled_data)} data points for {n_clusters} clusters")
            print("   Consider reducing the number of clusters")
            
        # Check for duplicate data points
        unique_points = np.unique(scaled_data, axis=0)
        if len(unique_points) < len(scaled_data):
            print(f"   ⚠️  Warning: Found duplicate data points ({len(scaled_data)} -> {len(unique_points)} unique)")
            
        # If we have very few unique points, reduce cluster count
        if len(unique_points) < n_clusters:
            suggested_clusters = max(1, len(unique_points) - 1)
            print(f"   ⚠️  Auto-adjusting clusters: {n_clusters} -> {suggested_clusters} (based on unique points)")
            n_clusters = suggested_clusters
        
        # Transpose data for skfuzzy (expects features x samples)
        data_T = scaled_data.T
        
        # Perform FCM clustering
        cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
            data_T, n_clusters, m, error=error, maxiter=max_iter
        )
        
        # Get cluster assignments (highest membership)
        cluster_labels = np.argmax(u, axis=0)
        
        print(f"✅ FCM clustering completed:")
        print(f"   Iterations: {p}")
        print(f"   Partition coefficient: {fpc:.4f}")
        print(f"   Cluster assignments: {np.bincount(cluster_labels)}")
        print(f"   Unique clusters: {np.unique(cluster_labels)}")
        
        # Calculate evaluation metrics
        try:
            db_score = davies_bouldin_score(scaled_data, cluster_labels)
        except ValueError as e:
            print(f"   ⚠️  Cannot calculate Davies-Bouldin score: {e}")
            db_score = float('inf')
            
        try:
            sil_score = silhouette_score(scaled_data, cluster_labels)
        except ValueError as e:
            print(f"   ⚠️  Cannot calculate Silhouette score: {e}")
            sil_score = -1.0
        
        execution_time = time.time() - start_time
        
        # Prepare results
        results = {
            'algorithm': 'Fuzzy C-Means',
            'summary': {
                'total_regions': int(len(df_clean)),
                'num_clusters': int(n_clusters),
                'iterations': int(p),
                'execution_time': float(execution_time),
                'fuzziness_parameter': float(m),
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
                    'id': int(i),
                    'centroid': centroid,
                    'size': int(len(members)),
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
        
        # Adaptive parameter adjustment based on data size
        n_samples = len(scaled_data)
        
        # Adjust min_samples based on data size
        adaptive_min_samples = max(2, min(min_samples, n_samples // 10))
        
        # Adjust min_cluster_size - use absolute number if fraction results in too large minimum
        if min_cluster_size < 1.0:  # It's a fraction
            min_cluster_absolute = max(2, int(n_samples * min_cluster_size))
            # If the fraction results in too large minimum, use a smaller absolute number
            if min_cluster_absolute > n_samples // 3:
                min_cluster_absolute = max(2, n_samples // 10)
            adaptive_min_cluster_size = min_cluster_absolute / n_samples
        else:  # It's already an absolute number
            adaptive_min_cluster_size = min_cluster_size / n_samples
        
        print(f"🔧 OPTICS adaptive parameters:")
        print(f"   Data size: {n_samples}")
        print(f"   min_samples: {min_samples} -> {adaptive_min_samples}")
        print(f"   min_cluster_size: {min_cluster_size} -> {adaptive_min_cluster_size:.4f}")
        
        # Perform OPTICS clustering
        optics = OPTICS(
            min_samples=adaptive_min_samples,
            xi=xi,
            min_cluster_size=adaptive_min_cluster_size
        )
        
        cluster_labels = optics.fit_predict(scaled_data)
        
        # Handle noise points (labeled as -1)
        n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
        
        print(f"✅ OPTICS clustering completed:")
        print(f"   Found {n_clusters} clusters")
        print(f"   Cluster assignments: {np.bincount(cluster_labels + 1) if -1 in cluster_labels else np.bincount(cluster_labels)}")
        print(f"   Unique labels: {np.unique(cluster_labels)}")
        print(f"   Noise points: {np.sum(cluster_labels == -1)}")
        
        execution_time = time.time() - start_time
        
        # Calculate evaluation metrics (excluding noise points)
        if n_clusters > 1 and len(set(cluster_labels)) > 1:
            # Only calculate metrics if we have valid clusters
            valid_mask = cluster_labels != -1
            if np.sum(valid_mask) > 1:
                try:
                    db_score = davies_bouldin_score(scaled_data[valid_mask], cluster_labels[valid_mask])
                except ValueError as e:
                    print(f"   ⚠️  Cannot calculate Davies-Bouldin score: {e}")
                    db_score = float('inf')
                    
                try:
                    sil_score = silhouette_score(scaled_data[valid_mask], cluster_labels[valid_mask])
                except ValueError as e:
                    print(f"   ⚠️  Cannot calculate Silhouette score: {e}")
                    sil_score = -1.0
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
                'total_regions': int(len(df_clean)),
                'num_clusters': int(n_clusters),
                'noise_points': int(np.sum(cluster_labels == -1)),
                'execution_time': float(execution_time),
                'min_samples': int(min_samples),
                'xi': float(xi)
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
                    'size': int(len(members)),
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
                        'size': int(len(members)),
                        'members': members
                    }
                    
                    results['clusters'].append(cluster_info)
        
        return results


def get_clustering_results_per_year(df: pd.DataFrame, algorithm: str = 'fcm', 
                                   features: List[str] = None, **kwargs) -> Dict[str, Any]:
    """
    Main function to get clustering results per year.
    
    Args:
        df: Input dataframe (wide format)
        algorithm: 'fcm' for Fuzzy C-Means or 'optics' for OPTICS
        features: List of feature columns to use for clustering
        **kwargs: Additional parameters for the clustering algorithm
        
    Returns:
        Dictionary containing clustering results for all years
    """
    if features is None:
        features = ['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita']
    
    clustering = ClusteringAlgorithms()
    
    # Data is already in long format with standardized column names
    available_years = sorted(df['tahun'].unique())
    
    print(f"🗓️ Processing clustering for years: {available_years}")
    
    results_per_year = {}
    overall_summary = {
        'algorithm': algorithm.upper(),
        'years_processed': [int(year) for year in available_years],
        'total_years': int(len(available_years)),
        'features_used': features
    }
    
    for year in available_years:
        print(f"\n📅 Processing year {year}...")
        
        try:
            # Get clustering results for this specific year
            # Create a copy of kwargs and set the selected_year for this iteration
            year_kwargs = kwargs.copy()
            year_kwargs['selected_year'] = str(year)
            
            if algorithm.lower() == 'fcm':
                year_results = clustering.fuzzy_c_means(df, features, **year_kwargs)
            elif algorithm.lower() == 'optics':
                year_results = clustering.optics_clustering(df, features, **year_kwargs)
            else:
                raise ValueError(f"Unknown algorithm: {algorithm}. Use 'fcm' or 'optics'.")
            
            # Add year information to the results
            year_results['year'] = int(year)
            results_per_year[str(year)] = year_results
            
            print(f"✅ Year {year}: {year_results['summary']['num_clusters']} clusters, "
                  f"{year_results['summary']['total_regions']} regions")
            
        except Exception as e:
            print(f"❌ Error processing year {year}: {str(e)}")
            results_per_year[str(year)] = {
                'year': int(year),
                'error': str(e),
                'algorithm': algorithm.upper(),
                'summary': {'total_regions': 0, 'num_clusters': 0},
                'evaluation': {'davies_bouldin': None, 'silhouette_score': None},
                'clusters': []
            }
    
    # Calculate overall statistics
    successful_years = [year for year, result in results_per_year.items() if 'error' not in result]
    failed_years = [year for year, result in results_per_year.items() if 'error' in result]
    
    overall_summary.update({
        'successful_years': int(len(successful_years)),
        'failed_years': int(len(failed_years)),
        'success_rate': float(len(successful_years) / len(available_years)) if available_years else 0.0
    })
    
    # Calculate average evaluation metrics across years
    if successful_years:
        avg_db_scores = []
        avg_sil_scores = []
        
        for year in successful_years:
            result = results_per_year[year]
            if result['evaluation']['davies_bouldin'] is not None:
                avg_db_scores.append(result['evaluation']['davies_bouldin'])
            if result['evaluation']['silhouette_score'] is not None:
                avg_sil_scores.append(result['evaluation']['silhouette_score'])
        
        overall_summary['average_evaluation'] = {
            'davies_bouldin': float(sum(avg_db_scores) / len(avg_db_scores)) if avg_db_scores else None,
            'silhouette_score': float(sum(avg_sil_scores) / len(avg_sil_scores)) if avg_sil_scores else None
        }
    
    return {
        'clustering_type': 'per_year',
        'overall_summary': overall_summary,
        'results_per_year': results_per_year
    }


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
    
    # Check if selected_year is specified for single year clustering
    selected_year = kwargs.get('selected_year')
    
    if selected_year:
        # Single year clustering (existing behavior)
        clustering = ClusteringAlgorithms()
        
        if algorithm.lower() == 'fcm':
            return clustering.fuzzy_c_means(df, features, **kwargs)
        elif algorithm.lower() == 'optics':
            return clustering.optics_clustering(df, features, **kwargs)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}. Use 'fcm' or 'optics'.")
    else:
        # Multi-year clustering (new behavior)
        return get_clustering_results_per_year(df, algorithm, features, **kwargs)