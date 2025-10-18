import numpy as np
import pandas as pd
from sklearn.cluster import OPTICS
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import davies_bouldin_score, silhouette_score
import skfuzzy as fuzz
from typing import Dict, List, Tuple, Any
import time

# --- Utility Function ---


def long_to_wide(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert long-format dataframe (with columns: kabupaten_kota, tahun, ipm, garis_kemiskinan, pengeluaran_per_kapita)
    into wide-format dataframe with columns like ipm_2016, garis_kemiskinan_2016, ..., pengeluaran_per_kapita_2021.

    This function is robust to variations in column names like 'kabupaten/kota'
    and 'pengeluaran_perkapita'.
    """
    print("🔄 Converting long-format data to wide-format...")

    df_copy = df.copy()

    # Define potential name variations and their standard form
    rename_map = {
        "kabupaten/kota": "kabupaten_kota",  # Handles your "kabupaten/kota"
        "pengeluaran_perkapita": "pengeluaran_per_kapita",  # Handles your "pengeluaran_perkapita"
    }

    df_copy.rename(columns=rename_map, inplace=True)

    # Define the standardized columns to be used
    index_col = "kabupaten_kota"
    value_cols = ["ipm", "garis_kemiskinan", "pengeluaran_per_kapita"]

    # --- End Fix ---

    # Check that all required columns are present after standardization
    required_cols_check = [index_col, "tahun"] + value_cols
    missing_cols = [col for col in required_cols_check if col not in df_copy.columns]

    if missing_cols:
        raise ValueError(
            f"Missing required columns after standardization: {missing_cols}. "
            f"Available columns: {df_copy.columns.tolist()}"
        )

    try:
        wide_df = df_copy.pivot(
            index=index_col,  # Use the standardized index column
            columns="tahun",
            values=value_cols,  # Use the standardized value columns
        )
    except Exception as e:
        print(f"❌ Error during pivot operation: {e}")
        # This often happens if there are duplicate (kabupaten_kota, tahun) entries
        print(
            "ℹ️  This error can be caused by duplicate 'kabupaten_kota' entries for the same 'tahun'."
        )
        # Handle duplicates by taking the mean (or first, last, etc.)
        print("Attempting to fix by aggregating duplicates (using mean)...")
        agg_map = {col: "mean" for col in value_cols}
        df_agg = df_copy.groupby([index_col, "tahun"]).agg(agg_map).reset_index()

        wide_df = df_agg.pivot(index=index_col, columns="tahun", values=value_cols)
        print("✅ Successfully pivoted after aggregation.")

    # Create friendlier column names like 'ipm_2016'
    wide_df.columns = [f"{feat}_{int(year)}" for feat, year in wide_df.columns]
    wide_df = wide_df.reset_index()
    print(f"✅ Conversion complete. New shape: {wide_df.shape}")
    return wide_df


# --- Core Clustering Engine ---


class ClusteringAlgorithms:
    """
    Main class for clustering algorithms implementation.
    This class handles the core logic for a *single* clustering run.
    """

    def __init__(self):
        self.scaler = StandardScaler()

    def preprocess_data(
        self, df: pd.DataFrame, features: List[str], selected_year: str = None
    ) -> Tuple[np.ndarray, pd.DataFrame]:
        """
        Preprocess data for clustering.
        - If 'selected_year' is provided, it filters the long-format 'df' for that year.
        - If 'selected_year' is None, it assumes 'df' is already in the correct format (e.g., wide-format).
        """
        df_to_process = df.copy()

        # Filter by year if specified (for per-year clustering)
        if selected_year:
            try:
                year_int = int(selected_year)
                df_to_process = df_to_process[df_to_process["tahun"] == year_int]
            except (ValueError, KeyError):
                print(f"⚠️ Could not filter for year {selected_year}. Using all data.")

        # Remove rows with missing values in required features
        df_clean = df_to_process.dropna(subset=features)

        if df_clean.empty:
            raise ValueError(
                f"No valid data found after preprocessing for year '{selected_network}' and features '{features}'."
            )

        # Extract feature data
        feature_data = df_clean[features].values

        # Scale the features
        scaled_data = self.scaler.fit_transform(feature_data)

        return scaled_data, df_clean

    def fuzzy_c_means(
        self,
        df: pd.DataFrame,
        features: List[str],
        n_clusters: int = 3,
        m: float = 2.0,
        max_iter: int = 300,
        error: float = 1e-5,
        selected_year: str = None,
    ) -> Dict[str, Any]:
        """
        Perform a single run of Fuzzy C-Means clustering.
        """
        start_time = time.time()
        # Preprocess data
        scaled_data, df_clean = self.preprocess_data(df, features, selected_year)

        print(f"🔧 FCM clustering parameters:")
        print(f"   Data size: {len(scaled_data)}")
        print(f"   Features: {features}")
        print(f"   n_clusters: {n_clusters}")

        # Check for potential issues
        if len(scaled_data) < n_clusters:
            print(
                f"   ⚠️ Warning: Data points ({len(scaled_data)}) < clusters ({n_clusters}). Adjusting clusters."
            )
            n_clusters = max(1, len(scaled_data))
            print(f"   New n_clusters: {n_clusters}")

        if n_clusters <= 1:
            raise ValueError(
                f"Cannot perform clustering with n_clusters <= 1. (Data points: {len(scaled_data)})"
            )

        # Transpose data for skfuzzy (expects features x samples)
        data_T = scaled_data.T

        # Perform FCM clustering
        cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
            data_T, n_clusters, m, error=error, maxiter=max_iter, seed=42
        )

        # Get cluster assignments (highest membership)
        cluster_labels = np.argmax(u, axis=0)

        print(f"✅ FCM clustering completed in {p} iterations.")

        # Calculate evaluation metrics
        try:
            db_score = davies_bouldin_score(scaled_data, cluster_labels)
        except ValueError as e:
            print(f"   ⚠️ Cannot calculate Davies-Bouldin score: {e}")
            db_score = None
        try:
            sil_score = silhouette_score(scaled_data, cluster_labels)
        except ValueError as e:
            print(f"   ⚠️ Cannot calculate Silhouette score: {e}")
            sil_score = -1.0

        execution_time = time.time() - start_time

        # Prepare results
        results = {
            "algorithm": "Fuzzy C-Means",
            "summary": {
                "total_regions": int(len(df_clean)),
                "num_clusters": int(n_clusters),
                "iterations": int(p),
                "execution_time": float(execution_time),
                "fuzziness_parameter": float(m),
                "partition_coefficient": float(fpc),
            },
            "evaluation": {
                "davies_bouldin": float(db_score) if db_score is not None else None,
                "silhouette_score": float(sil_score),
            },
            "clusters": [],
        }

        # Create cluster information
        for i in range(n_clusters):
            cluster_mask = cluster_labels == i
            cluster_members_df = df_clean[cluster_mask].copy()

            if len(cluster_members_df) > 0:
                # Calculate centroid in original scale
                centroid = {
                    feat: float(cluster_members_df[feat].mean()) for feat in features
                }

                # Prepare member information
                members = []
                # Get the membership values for this cluster
                cluster_memberships = u[i, cluster_mask]

                for idx, (_, row) in enumerate(cluster_members_df.iterrows()):
                    member_info = {
                        "kabupaten_kota": str(row.get("kabupaten_kota", "")),
                        "provinsi": str(row.get("provinsi", "")),
                        "tahun": (
                            int(row.get("tahun", 0)) if "tahun" in row else None
                        ),  # Year might not exist in wide-format
                        "latitude": float(row.get("latitude", 0.0)),
                        "longitude": float(row.get("longitude", 0.0)),
                        "membership": float(cluster_memberships[idx]),
                    }
                    # Add feature values
                    for feature in features:
                        member_info[feature] = float(row.get(feature, 0.0))
                    members.append(member_info)

                results["clusters"].append(
                    {
                        "id": int(i),
                        "centroid": centroid,
                        "size": int(len(members)),
                        "members": members,
                    }
                )

        return results

    def optics_clustering(
        self,
        df: pd.DataFrame,
        features: List[str],
        min_samples: int = 5,
        xi: float = 0.05,
        min_cluster_size: float = 0.05,
        selected_year: str = None,
    ) -> Dict[str, Any]:
        """
        Perform a single run of OPTICS clustering.
        """
        start_time = time.time()

        # Preprocess data
        scaled_data, df_clean = self.preprocess_data(df, features, selected_year)

        print(f"🔧 OPTICS clustering parameters:")
        print(f"   Data size: {len(scaled_data)}")
        print(f"   Features: {features}")

        # Perform OPTICS clustering
        optics = OPTICS(
            min_samples=min_samples,
            xi=xi,
            min_cluster_size=min_cluster_size,
        )
        cluster_labels = optics.fit_predict(scaled_data)

        # Handle noise points (labeled as -1)
        n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
        n_noise = int(np.sum(cluster_labels == -1))

        print(f"✅ OPTICS clustering completed.")
        print(f"   Found {n_clusters} clusters and {n_noise} noise points.")

        execution_time = time.time() - start_time

        # Calculate evaluation metrics (excluding noise points)
        db_score = None
        sil_score = -1.0
        if n_clusters > 1:
            valid_mask = cluster_labels != -1
            if np.sum(valid_mask) > 1:
                try:
                    db_score = davies_bouldin_score(
                        scaled_data[valid_mask], cluster_labels[valid_mask]
                    )
                except ValueError as e:
                    print(f"   ⚠️ Cannot calculate Davies-Bouldin score: {e}")
                try:
                    sil_score = silhouette_score(
                        scaled_data[valid_mask], cluster_labels[valid_mask]
                    )
                except ValueError as e:
                    print(f"   ⚠️ Cannot calculate Silhouette score: {e}")

        # Prepare results
        results = {
            "algorithm": "OPTICS",
            "summary": {
                "total_regions": int(len(df_clean)),
                "num_clusters": int(n_clusters),
                "noise_points": n_noise,
                "execution_time": float(execution_time),
                "min_samples": int(min_samples),
                "xi": float(xi),
            },
            "evaluation": {
                "davies_bouldin": float(db_score) if db_score is not None else None,
                "silhouette_score": float(sil_score),
            },
            "clusters": [],
        }

        # Create cluster information
        unique_labels = set(cluster_labels)
        for label in unique_labels:
            cluster_mask = cluster_labels == label
            cluster_members_df = df_clean[cluster_mask].copy()

            if len(cluster_members_df) > 0:
                cluster_id = "noise" if label == -1 else int(label)

                # Calculate centroid (None for noise)
                centroid = None
                if label != -1:
                    centroid = {
                        feat: float(cluster_members_df[feat].mean())
                        for feat in features
                    }

                # Prepare member information
                members = []
                for _, row in cluster_members_df.iterrows():
                    member_info = {
                        "kabupaten_kota": str(row.get("kabupaten_kota", "")),
                        "provinsi": str(row.get("provinsi", "")),
                        "tahun": int(row.get("tahun", 0)) if "tahun" in row else None,
                        "latitude": float(row.get("latitude", 0.0)),
                        "longitude": float(row.get("longitude", 0.0)),
                        "membership": 1.0,  # OPTICS gives hard assignments
                    }
                    # Add feature values
                    for feature in features:
                        member_info[feature] = float(row.get(feature, 0.0))
                    members.append(member_info)

                results["clusters"].append(
                    {
                        "id": cluster_id,
                        "centroid": centroid,
                        "size": int(len(members)),
                        "members": members,
                    }
                )

        return results


def run_clustering_per_year(
    df: pd.DataFrame, algorithm: str = "fcm", features: List[str] = None, **kwargs
) -> Dict[str, Any]:
    """
    API FEATURE 1: Cluster data for each year individually.

    Args:
        df: Input dataframe (MUST be in LONG format with a 'tahun' column)
        algorithm: 'fcm' or 'optics'
        features: List of feature columns to use (e.g., ["ipm", "garis_kemiskinan"])
        **kwargs: Additional parameters for the clustering algorithm
                  (e.g., n_clusters=3 for fcm)

    Returns:
        Dictionary containing clustering results for all years
    """
    if features is None:
        features = ["ipm", "garis_kemiskinan", "pengeluaran_per_kapita"]

    clustering = ClusteringAlgorithms()
    available_years = sorted(df["tahun"].unique())

    print(
        f"🗓️ Starting 'per_year' clustering for {len(available_years)} years: {available_years}"
    )

    results_per_year = {}
    for year in available_years:
        print(f"\n📅 Processing year {year}...")
        try:
            # Pass the full 'df' and the 'selected_year' to the class methods
            year_kwargs = kwargs.copy()
            year_kwargs["selected_year"] = str(year)

            if algorithm.lower() == "fcm":
                year_results = clustering.fuzzy_c_means(df, features, **year_kwargs)
            elif algorithm.lower() == "optics":
                year_results = clustering.optics_clustering(df, features, **year_kwargs)
            else:
                raise ValueError(
                    f"Unknown algorithm: {algorithm}. Use 'fcm' or 'optics'."
                )

            year_results["year"] = int(year)
            results_per_year[str(year)] = year_results
            print(
                f"✅ Year {year}: {year_results['summary']['num_clusters']} clusters, {year_results['summary']['total_regions']} regions"
            )

        except Exception as e:
            print(f"❌ Error processing year {year}: {str(e)}")
            results_per_year[str(year)] = {
                "year": int(year),
                "error": str(e),
                "algorithm": algorithm.upper(),
                "summary": {},
                "evaluation": {},
                "clusters": [],
            }

    # --- Build final response object ---
    successful_years = [r for r in results_per_year.values() if "error" not in r]
    avg_db = [
        r["evaluation"]["davies_bouldin"]
        for r in successful_years
        if r["evaluation"]["davies_bouldin"] is not None
    ]
    avg_sil = [
        r["evaluation"]["silhouette_score"]
        for r in successful_years
        if r["evaluation"]["silhouette_score"] is not None
    ]

    overall_summary = {
        "algorithm": algorithm.upper(),
        "years_processed": [int(y) for y in available_years],
        "total_years": int(len(available_years)),
        "successful_years": len(successful_years),
        "features_used": features,
        "average_evaluation": {
            "davies_bouldin": float(np.mean(avg_db)) if avg_db else None,
            "silhouette_score": float(np.mean(avg_sil)) if avg_sil else None,
        },
    }

    return {
        "clustering_type": "per_year",
        "overall_summary": overall_summary,
        "results_per_year": results_per_year,
    }


# --- API Function 2: Cluster All Years (Wide Format) ---


def run_clustering_all_years(
    df: pd.DataFrame, algorithm: str = "fcm", **kwargs
) -> Dict[str, Any]:
    """
    API FEATURE 2: Converts long-format data to wide-format, then clusters once.

    Args:
        df: Input dataframe (MUST be in LONG format with 'tahun' column)
        algorithm: 'fcm' or 'optics'
        **kwargs: Additional parameters for the clustering algorithm

    Returns:
        Dictionary in the *same structure* as 'per_year', but with a single
        result key: 'all_years'.
    """
    # 1. Convert long data to wide format
    try:
        wide_df = long_to_wide(df)
    except Exception as e:
        print(f"❌ Error during long-to-wide conversion: {e}")
        return (
            {
                "clustering_type": "all_years_wide",
                "overall_summary": {"error": f"Data conversion failed: {e}"},
                "results_per_year": {},
            },
        )

    # 2. Auto-detect all wide features
    wide_features = [
        col
        for col in wide_df.columns
        if any(
            metric in col for metric in ["ipm_", "pengeluaran_", "garis_kemiskinan_"]
        )
    ]

    if not wide_features:
        print("❌ No valid wide-format features found (e.g., 'ipm_2016').")
        return {
            "clustering_type": "all_years_wide",
            "overall_summary": {
                "error": "No valid wide-format features found after conversion."
            },
            "results_per_year": {},
        }

    print(
        f"🚀 Starting 'all_years' (wide) clustering with {len(wide_features)} features..."
    )

    # 3. Run clustering *once*
    clustering = ClusteringAlgorithms()
    results_per_year = {}
    try:
        if algorithm.lower() == "fcm":
            # Pass wide_df, wide_features, and no 'selected_year'
            result = clustering.fuzzy_c_means(wide_df, wide_features, **kwargs)
        elif algorithm.lower() == "optics":
            result = clustering.optics_clustering(wide_df, wide_features, **kwargs)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}. Use 'fcm' or 'optics'.")

        result["year"] = None  # No single year applies
        results_per_year["all_years"] = result

        print(f"✅ 'all_years' clustering complete.")

        # 4. Build final response object (matching per_year structure)
        overall_summary = {
            "algorithm": algorithm.upper(),
            "years_processed": sorted(df["tahun"].unique().tolist()),
            "total_years": len(df["tahun"].unique()),
            "successful_years": 1,
            "features_used": wide_features,
            "average_evaluation": result[
                "evaluation"
            ],  # Use the single run's evaluation
        }

    except Exception as e:
        print(f"❌ Error during 'all_years' clustering: {e}")
        overall_summary = {
            "algorithm": algorithm.upper(),
            "features_used": wide_features,
            "error": str(e),
        }
        results_per_year["all_years"] = {"error": str(e)}

    return {
        "clustering_type": "all_years_wide",
        "overall_summary": overall_summary,
        "results_per_year": results_per_year,
    }
