#!/usr/bin/env python3
"""
Local Data Processor for STEDI Project
Simulates the Glue ETL pipeline to validate data transformation logic
"""

import json
import pandas as pd
from pathlib import Path

class STEDIDataProcessor:
    def __init__(self, data_root: str):
        self.data_root = Path(data_root)
        self.results = {}
        
    def load_json_files(self, file_pattern: str) -> pd.DataFrame:
        """Load and combine multiple JSON files into a DataFrame"""
        data_files = list(self.data_root.glob(file_pattern))
        all_data = []
        
        for file_path in data_files:
            print(f"Loading {file_path.name}...")
            with open(file_path, 'r') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        all_data.append(record)
                    except json.JSONDecodeError:
                        continue
        
        return pd.DataFrame(all_data)
    
    def process_landing_zone(self):
        """Process landing zone data and calculate counts"""
        print("=== PROCESSING LANDING ZONE ===")
        
        # Load customer data
        customer_df = self.load_json_files("customer/landing/*.json")
        print(f"Customer landing records: {len(customer_df)}")
        
        # Count customers with blank consent (NULL or 0 shareWithResearchAsOfDate)
        blank_consent = customer_df[
            (customer_df['shareWithResearchAsOfDate'].isna()) | 
            (customer_df['shareWithResearchAsOfDate'] == 0)
        ]
        print(f"Customers with blank consent: {len(blank_consent)}")
        
        # Load accelerometer data
        accelerometer_df = self.load_json_files("accelerometer/landing/*.json")
        print(f"Accelerometer landing records: {len(accelerometer_df)}")
        
        # Load step trainer data
        step_trainer_df = self.load_json_files("step_trainer/landing/*.json")
        print(f"Step trainer landing records: {len(step_trainer_df)}")
        
        self.results['landing'] = {
            'customer': len(customer_df),
            'accelerometer': len(accelerometer_df),
            'step_trainer': len(step_trainer_df),
            'customer_blank_consent': len(blank_consent)
        }
        
        return customer_df, accelerometer_df, step_trainer_df
    
    def process_trusted_zone(self, customer_df, accelerometer_df, step_trainer_df):
        """Process trusted zone transformations"""
        print("\n=== PROCESSING TRUSTED ZONE ===")
        
        # Customer trusted: Filter out blank consent
        customer_trusted = customer_df[
            customer_df['shareWithResearchAsOfDate'].notna() &
            (customer_df['shareWithResearchAsOfDate'] != 0)
        ].copy()
        
        # Clean email addresses (lowercase, trim)
        customer_trusted['email'] = customer_trusted['email'].str.lower().str.strip()
        
        print(f"Customer trusted records: {len(customer_trusted)}")
        
        # Accelerometer trusted: Inner join with customer trusted by email
        accelerometer_df['user'] = accelerometer_df['user'].str.lower().str.strip()
        customer_emails = set(customer_trusted['email'].unique())
        
        accelerometer_trusted = accelerometer_df[
            accelerometer_df['user'].isin(customer_emails)
        ].copy()
        
        # Apply consent timestamp filter (stand-out requirement)
        # Join to get consent dates
        accelerometer_with_consent = accelerometer_trusted.merge(
            customer_trusted[['email', 'shareWithResearchAsOfDate']], 
            left_on='user', 
            right_on='email',
            how='inner'
        )
        
        # Filter by consent timestamp 
        accelerometer_consent_filtered = accelerometer_with_consent[
            accelerometer_with_consent['timestamp'] >= accelerometer_with_consent['shareWithResearchAsOfDate']
        ]
        
        print(f"Accelerometer trusted records (basic): {len(accelerometer_trusted)}")
        print(f"Accelerometer trusted records (with consent filter): {len(accelerometer_consent_filtered)}")
        
        # Step trainer trusted: Just deduplicate by serialNumber + sensorReadingTime
        # No customer filtering at this stage
        step_trainer_trusted = step_trainer_df.drop_duplicates(
            subset=['serialNumber', 'sensorReadingTime']
        ).copy()
        print(f"Step trainer trusted records: {len(step_trainer_trusted)}")
        
        self.results['trusted'] = {
            'customer': len(customer_trusted),
            'accelerometer': len(accelerometer_trusted),
            'accelerometer_consent_filtered': len(accelerometer_consent_filtered),
            'step_trainer': len(step_trainer_trusted)
        }
        
        return customer_trusted, accelerometer_trusted, accelerometer_consent_filtered, step_trainer_trusted
    
    def process_curated_zone(self, customer_trusted, accelerometer_trusted, accelerometer_consent_filtered, step_trainer_trusted):
        """Process curated zone transformations"""
        print("\n=== PROCESSING CURATED ZONE ===")
        
        # Customer curated: Inner join customer_trusted with accelerometer_trusted
        # to get only customers who have accelerometer data
        customer_curated = customer_trusted.merge(
            accelerometer_trusted[['user']].drop_duplicates(),
            left_on='email',
            right_on='user',
            how='inner'
        )[list(customer_trusted.columns)]
        
        print(f"Customer curated records: {len(customer_curated)}")
        
        # Step trainer curated: Filter step trainer by customer serial numbers
        # This is the step_trainer_trusted_curated_join job
        customer_serial_numbers = set(customer_curated['serialNumber'].unique())
        step_trainer_curated = step_trainer_trusted[
            step_trainer_trusted['serialNumber'].isin(customer_serial_numbers)
        ].copy()
        
        print(f"Step trainer curated records: {len(step_trainer_curated)}")
        
        # Machine Learning curated: Complex triple join
        # Join accelerometer + customer + step trainer
        
        # First: accelerometer with customer curated
        accel_customer = accelerometer_trusted.merge(
            customer_curated[['email', 'serialNumber']],
            left_on='user',
            right_on='email',
            how='inner'
        )
        
        # Prepare step trainer with matching timestamp column
        step_trainer_for_ml = step_trainer_curated.copy()
        step_trainer_for_ml['timestamp'] = step_trainer_for_ml['sensorReadingTime']
        
        # Final join: accelerometer+customer with step trainer
        ml_curated = accel_customer.merge(
            step_trainer_for_ml[['timestamp', 'serialNumber', 'distanceFromObject']],
            on=['timestamp', 'serialNumber'],
            how='inner'
        )
        
        # Final ML table: only timestamp, x, y, z, distanceFromObject, serialNumber
        # PII removed (no email, customerName, phone)
        ml_final = ml_curated[['timestamp', 'x', 'y', 'z', 'distanceFromObject', 'serialNumber']].copy()
        
        print(f"Machine learning curated records: {len(ml_curated)}")
        
        self.results['curated'] = {
            'customer': len(customer_curated),
            'step_trainer': len(step_trainer_curated),
            'ml_basic': len(ml_curated)
        }
        
        return customer_curated, ml_final
    
    def generate_report(self):
        """Generate a summary report of all counts"""
        print("\n" + "="*50)
        print("STEDI DATA PROCESSING SUMMARY")
        print("="*50)
        
        print("\nLANDING ZONE COUNTS:")
        print(f"  Customer landing: {self.results['landing']['customer']}")
        print(f"  Accelerometer landing: {self.results['landing']['accelerometer']}")
        print(f"  Step trainer landing: {self.results['landing']['step_trainer']}")
        print(f"  Customer blank consent: {self.results['landing']['customer_blank_consent']}")
        
        print("\nTRUSTED ZONE COUNTS:")
        print(f"  Customer trusted: {self.results['trusted']['customer']}")
        print(f"  Accelerometer trusted: {self.results['trusted']['accelerometer']}")
        print(f"  Accelerometer trusted (consent filter): {self.results['trusted']['accelerometer_consent_filtered']}")
        print(f"  Step trainer trusted: {self.results['trusted']['step_trainer']}")
        
        print("\nCURATED ZONE COUNTS:")
        print(f"  Customer curated: {self.results['curated']['customer']}")
        print(f"  Step trainer curated: {self.results['curated']['step_trainer']}")
        print(f"  ML curated: {self.results['curated']['ml_basic']}")
        
        print("\nRUBRIC VALIDATION:")
        expected_landing = [956, 81273, 28680]
        actual_landing = [
            self.results['landing']['customer'],
            self.results['landing']['accelerometer'], 
            self.results['landing']['step_trainer']
        ]
        
        expected_trusted = [482, 40981, 14460]  # From rubric
        actual_trusted = [
            self.results['trusted']['customer'],
            self.results['trusted']['accelerometer'],
            self.results['trusted']['step_trainer']
        ]
        
        expected_curated = [482, 43681]  # From rubric
        actual_curated = [
            self.results['curated']['customer'],
            self.results['curated']['ml_basic']
        ]
        
        print(f"  Landing counts match expected: {actual_landing == expected_landing}")
        print(f"  Expected: {expected_landing}, Actual: {actual_landing}")
        
        print(f"  Trusted counts match expected: {actual_trusted == expected_trusted}")
        print(f"  Expected: {expected_trusted}, Actual: {actual_trusted}")
        
        print(f"  Curated counts match expected: {actual_curated == expected_curated}")
        print(f"  Expected: {expected_curated}, Actual: {actual_curated}")

def main():
    # Process data
    processor = STEDIDataProcessor("Data")
    
    # Load and process landing zone
    customer_df, accelerometer_df, step_trainer_df = processor.process_landing_zone()
    
    # Process trusted zone
    customer_trusted, accelerometer_trusted, accelerometer_consent_filtered, step_trainer_trusted = processor.process_trusted_zone(
        customer_df, accelerometer_df, step_trainer_df
    )
    
    # Process curated zone
    customer_curated, ml_final = processor.process_curated_zone(
        customer_trusted, accelerometer_trusted, accelerometer_consent_filtered, step_trainer_trusted
    )
    
    # Generate report
    processor.generate_report()

if __name__ == "__main__":
    main()