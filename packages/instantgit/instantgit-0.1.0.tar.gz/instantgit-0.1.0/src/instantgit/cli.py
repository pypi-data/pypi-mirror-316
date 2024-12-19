import argparse
import os
from pathlib import Path
from . import templates

def main():
    parser = argparse.ArgumentParser(
        description="InstantGit - The comprehensive .gitignore template manager"
    )
    parser.add_argument(
        "--add",
        action="store_true",
        help="Add the comprehensive .gitignore template to the current directory"
    )
    
    args = parser.parse_args()
    
    if args.add:
        current_dir = Path.cwd()
        gitignore_path = current_dir / ".gitignore"
        
        if gitignore_path.exists():
            print("Warning: .gitignore already exists. Adding content to existing file...")
            with open(gitignore_path, "r") as f:
                existing_content = f.read()
            if templates.COMPREHENSIVE_TEMPLATE in existing_content:
                print("Template already exists in .gitignore!")
                return
            
            with open(gitignore_path, "a") as f:
                f.write("\n# Added by InstantGit\n")
                f.write(templates.COMPREHENSIVE_TEMPLATE)
        else:
            with open(gitignore_path, "w") as f:
                f.write("# Created by InstantGit\n")
                f.write(templates.COMPREHENSIVE_TEMPLATE)
        
        print("Successfully added comprehensive .gitignore template!")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()