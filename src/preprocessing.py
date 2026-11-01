"""
Data Preprocessing Pipeline for Movie & OTT Platform Content Analysis
Consolidates, cleans, and standardizes datasets from Netflix, Amazon Prime, Disney+, and Hulu.
"""

import os
import re
import pandas as pd
import numpy as np


def clean_duration_and_rating(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fixes data entry shifts where duration values (e.g. '74 min', '2 Seasons')
    were incorrectly placed into the rating column, leaving duration as NaN.
    """
    df = df.copy()
    shifted_mask = df['rating'].astype(str).str.contains(r'min|Season', case=False, na=False)
    
    # If duration is NaN and rating contains min/Season, copy rating into duration
    fix_mask = shifted_mask & df['duration'].isna()
    df.loc[fix_mask, 'duration'] = df.loc[fix_mask, 'rating']
    df.loc[shifted_mask, 'rating'] = np.nan
    
    return df


def categorize_rating(rating: str) -> str:
    """
    Categorizes content age ratings into standard audience brackets:
    Kids, Teens, Adults, or Unrated.
    """
    if pd.isna(rating) or not str(rating).strip():
        return 'Unrated'
    
    r = str(rating).strip().upper()
    
    kids_ratings = {'G', 'TV-G', 'TV-Y', 'TV-Y7', 'TV-Y7-FV', 'ALL', 'ALL_AGES', '7+'}
    teens_ratings = {'PG', 'TV-PG', 'PG-13', 'TV-14', '13+', '16', '16+'}
    adults_ratings = {'R', 'TV-MA', 'NC-17', '18+', 'AGES_18_', 'AGES_16_'}
    unrated_ratings = {'NR', 'UR', 'NOT RATED', 'UNRATED', 'TV-NR', 'NOT_RATE'}
    
    if r in kids_ratings:
        return 'Kids'
    elif r in teens_ratings:
        return 'Teens'
    elif r in adults_ratings:
        return 'Adults'
    elif r in unrated_ratings:
        return 'Unrated'
    else:
        return 'Unrated'


def standardize_dataset(file_path: str, platform_name: str, platform_code: str) -> pd.DataFrame:
    """
    Loads and standardizes a single OTT platform dataset.
    """
    df = pd.read_csv(file_path)
    
    # Standardize column names
    df.columns = [col.strip().lower() for col in df.columns]
    
    # Add platform identifiers
    df['platform'] = platform_name
    df['platform_code'] = platform_code
    
    # Create unique composite title ID to prevent collision across datasets
    df['title_id'] = platform_code + '_' + df['show_id'].astype(str)
    
    # Clean string fields
    for text_col in ['title', 'director', 'cast', 'country', 'rating', 'duration', 'listed_in', 'description', 'type']:
        if text_col in df.columns:
            df[text_col] = df[text_col].astype(str).str.strip().replace({'nan': np.nan, 'None': np.nan, '': np.nan})
            
    # Fix misplaced duration values in rating column
    df = clean_duration_and_rating(df)
    
    # Standardize 'type' (Movie vs TV Show)
    df['type'] = df['type'].fillna('Unknown')
    # Some entries with seasons in duration might be mistakenly marked as Movie
    has_seasons = df['duration'].astype(str).str.contains(r'season', case=False, na=False)
    df.loc[has_seasons & (df['type'] == 'Movie'), 'type'] = 'TV Show'
    
    # Handle missing values
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('Unrated')
    df['description'] = df['description'].fillna('No description available')
    
    # Audience category
    df['rating_category'] = df['rating'].apply(categorize_rating)
    
    # Parse date_added
    df['date_added_clean'] = pd.to_datetime(df['date_added'], errors='coerce', format='mixed')
    df['year_added'] = df['date_added_clean'].dt.year.astype('Int64')
    df['month_added'] = df['date_added_clean'].dt.month_name()
    
    # Standardize release_year
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce').astype('Int64')
    
    # Duration parsing
    # Extract numeric part
    dur_num = df['duration'].str.extract(r'(\d+)')[0]
    df['duration_int'] = pd.to_numeric(dur_num, errors='coerce')
    
    # Unit
    is_season = df['duration'].astype(str).str.contains(r'season', case=False, na=False)
    is_min = df['duration'].astype(str).str.contains(r'min', case=False, na=False)
    duration_unit = pd.Series(np.nan, index=df.index, dtype=object)
    duration_unit[is_season] = 'Seasons'
    duration_unit[is_min] = 'Minutes'
    df['duration_unit'] = duration_unit
    
    # Separate numeric duration for Movies and TV Shows
    df['duration_minutes'] = np.where(df['type'] == 'Movie', df['duration_int'], np.nan)
    df['duration_seasons'] = np.where(df['type'] == 'TV Show', df['duration_int'], np.nan)
    
    # Primary Genre
    df['primary_genre'] = df['listed_in'].astype(str).apply(
        lambda x: x.split(',')[0].strip() if pd.notna(x) and x != 'nan' else 'Unknown'
    )
    
    return df


def build_unified_dataset(
    raw_dir: str = 'data/raw',
    output_path: str = 'data/processed/unified_ott_dataset.csv'
) -> pd.DataFrame:
    """
    Loads all four platform CSVs, standardizes and combines them into unified_ott_dataset.csv.
    """
    platform_configs = [
        ('netflix.csv', 'Netflix', 'NFLX'),
        ('amazon_prime.csv', 'Amazon Prime', 'AMZN'),
        ('disney_plus.csv', 'Disney+', 'DISN'),
        ('hulu.csv', 'Hulu', 'HULU')
    ]
    
    dfs = []
    for file_name, name, code in platform_configs:
        path = os.path.join(raw_dir, file_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Source file {path} not found.")
        print(f"Standardizing {name} from {path}...")
        df_platform = standardize_dataset(path, name, code)
        dfs.append(df_platform)
        print(f"  -> Processed {len(df_platform):,} records.")
        
    unified_df = pd.concat(dfs, ignore_index=True)
    
    # Ensure processed directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save processed unified dataset
    unified_df.to_csv(output_path, index=False)
    print(f"\nUnified dataset created successfully with {len(unified_df):,} records!")
    print(f"Saved to: {output_path}")
    
    return unified_df


if __name__ == '__main__':
    build_unified_dataset()
