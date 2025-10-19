"""
Production Configuration Updater

Run this script to update all configuration files with your actual AWS resources.

Usage:
    python update_config.py --bucket your-bucket-name

This will update:
- src/config.py
- glue_job_settings.json  
- All SQL DDL files
"""

import json
import argparse
from pathlib import Path

def update_config_py(bucket_name: str):
    """Update the config.py file with actual bucket name"""
    config_file = Path("src/config.py")
    content = config_file.read_text()
    content = content.replace("your-bucket", bucket_name)
    config_file.write_text(content)
    print(f"✅ Updated {config_file}")

def update_glue_settings(bucket_name: str):
    """Update glue_job_settings.json with actual bucket name"""
    settings_file = Path("glue_job_settings.json")
    with open(settings_file, 'r') as f:
        data = json.load(f)
    
    # Update bucket references in all job configs
    json_str = json.dumps(data, indent=2)
    json_str = json_str.replace("bucket", bucket_name)
    
    with open(settings_file, 'w') as f:
        f.write(json_str)
    print(f"✅ Updated {settings_file}")

def update_ddl_files(bucket_name: str):
    """Update all DDL files with actual bucket name"""
    ddl_dir = Path("sql/landing_ddls")
    for ddl_file in ddl_dir.glob("*.sql"):
        content = ddl_file.read_text()
        content = content.replace("your-bucket", bucket_name)
        ddl_file.write_text(content)
        print(f"✅ Updated {ddl_file}")

def main():
    parser = argparse.ArgumentParser(description="Update configuration with production values")
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    args = parser.parse_args()
    
    print(f"🚀 Updating configuration with bucket: {args.bucket}")
    
    update_config_py(args.bucket)
    update_glue_settings(args.bucket)
    update_ddl_files(args.bucket)
    
    print("\n✨ Configuration update complete!")
    print(f"📝 Next steps:")
    print(f"   1. Create S3 bucket: {args.bucket}")
    print(f"   2. Upload data to landing zones")
    print(f"   3. Create Glue database: stedi_db")
    print(f"   4. Run DDL scripts to create tables")
    print(f"   5. Execute Glue jobs in order")

if __name__ == "__main__":
    main()