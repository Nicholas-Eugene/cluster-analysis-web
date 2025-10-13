#!/usr/bin/env python3
"""
Test script to check if city names in sample data match with coordinate database
"""

import pandas as pd
import json

def test_coordinate_matching():
    """Test coordinate matching with sample data"""
    
    # Load sample data
    try:
        df = pd.read_csv('sample_data_indonesia.csv')
        print(f"=== Coordinate Matching Test ===")
        print(f"Sample data shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Get unique city names
        unique_cities = df['kabupaten_kota'].unique()
        print(f"\nUnique cities in dataset: {len(unique_cities)}")
        
        # Show first 20 city names
        print("\nFirst 20 city names:")
        for i, city in enumerate(unique_cities[:20]):
            print(f"{i+1:2d}. {city}")
        
        # JavaScript coordinate database (subset for testing)
        js_coords = {
            'Jakarta Pusat': [-6.1833, 106.8333],
            'Jakarta Utara': [-6.1333, 106.8500],
            'Jakarta Barat': [-6.1667, 106.7833],
            'Jakarta Selatan': [-6.2667, 106.8167],
            'Jakarta Timur': [-6.2333, 106.8833],
            'Surabaya': [-7.2500, 112.7500],
            'Bandung': [-6.9175, 107.6191],
            'Medan': [3.5833, 98.6667],
            'Semarang': [-7.0000, 110.4167],
            'Makassar': [-5.1333, 119.4167],
            'Palembang': [-2.9833, 104.7667],
            'Yogyakarta': [-7.8000, 110.3667],
            'Denpasar': [-8.6500, 115.2167],
            'Malang': [-7.9833, 112.6167],
            'Padang': [-0.9500, 100.3500],
            'Bogor': [-6.5944, 106.7896],
            'Depok': [-6.4025, 106.7942],
            'Tangerang': [-6.1667, 106.6333],
            'Bekasi': [-6.2409, 106.9921],
            'Batam': [1.0500, 104.0000],
            # Add the missing cities
            'Banjarmasin': [-3.3167, 114.5833],
            'Pontianak': [-0.0167, 109.3333],
            'Samarinda': [-0.5000, 117.1500],
            'Balikpapan': [-1.2500, 116.8333],
            'Manado': [1.4833, 124.8500],
            'Palu': [-0.8833, 119.8667],
            'Kendari': [-3.9833, 122.5167],
            'Jayapura': [-2.5333, 140.7167],
            'Sorong': [-0.8833, 131.2500],
            'Ambon': [-3.7000, 128.1667],
            'Kupang': [-10.1667, 123.5833],
        }
        
        # Test matching
        matched = 0
        unmatched = []
        
        for city in unique_cities:
            # Normalize city name (similar to frontend logic)
            normalized = city.strip()
            for prefix in ['Kab. ', 'Kabupaten ', 'Kota ', 'Administrasi ', 'DKI ']:
                normalized = normalized.replace(prefix, '')
            normalized = normalized.strip()
            
            if normalized in js_coords:
                matched += 1
                print(f"✅ {city} -> {normalized} -> {js_coords[normalized]}")
            else:
                # Try fuzzy matching
                fuzzy_match = None
                for key in js_coords.keys():
                    if (key.lower() in normalized.lower() or 
                        normalized.lower() in key.lower()):
                        fuzzy_match = key
                        break
                
                if fuzzy_match:
                    matched += 1
                    print(f"🔍 {city} -> {fuzzy_match} (fuzzy) -> {js_coords[fuzzy_match]}")
                else:
                    unmatched.append(city)
        
        print(f"\n=== Matching Results ===")
        print(f"Total cities: {len(unique_cities)}")
        print(f"Matched: {matched}")
        print(f"Unmatched: {len(unmatched)}")
        print(f"Match rate: {(matched/len(unique_cities)*100):.1f}%")
        
        if unmatched:
            print(f"\nUnmatched cities (first 10):")
            for city in unmatched[:10]:
                print(f"❌ {city}")
        
        return matched, len(unmatched)
        
    except Exception as e:
        print(f"Error: {e}")
        return 0, 0

def create_test_clustering_data():
    """Create test data with known city names"""
    
    test_data = {
        'kabupaten_kota': [
            'Jakarta Pusat', 'Jakarta Selatan', 'Jakarta Barat',
            'Surabaya', 'Bandung', 'Semarang',
            'Medan', 'Makassar', 'Palembang',
            'Yogyakarta', 'Malang', 'Bogor'
        ],
        'tahun': [2023] * 12,
        'ipm': [85, 83, 82, 78, 76, 75, 72, 70, 73, 80, 77, 79],
        'garis_kemiskinan': [400000, 420000, 450000, 480000, 500000, 470000, 520000, 550000, 510000, 440000, 460000, 430000],
        'pengeluaran_per_kapita': [15000000, 14000000, 13000000, 9000000, 10000000, 8500000, 7000000, 6500000, 7500000, 11000000, 8800000, 12000000]
    }
    
    df = pd.DataFrame(test_data)
    
    # Save as CSV for testing
    df.to_csv('test_map_data.csv', index=False)
    print("✅ Created test_map_data.csv with known city coordinates")
    
    return df

if __name__ == "__main__":
    print("Testing coordinate matching...")
    
    # Test with sample data
    matched, unmatched = test_coordinate_matching()
    
    # Create test data
    test_df = create_test_clustering_data()
    print(f"\nTest data created with {len(test_df)} cities")
    print("Cities in test data:")
    for city in test_df['kabupaten_kota']:
        print(f"  - {city}")