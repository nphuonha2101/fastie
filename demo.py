#!/usr/bin/env python3
"""
Demo script để showcase Fastie CLI capabilities
"""

import os
import subprocess
import time

def run_command(cmd, description):
    """Run a command and display its output"""
    print(f"\n🔄 {description}")
    print(f"💻 Command: {cmd}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print("=" * 50)
        time.sleep(1)  # Brief pause for readability
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main demo function"""
    print("🚀 FASTIE CLI DEMO")
    print("==================")
    print("Đây là demo các tính năng của Fastie CLI - Laravel Artisan cho Python")
    
    # Show CLI help
    run_command("python fastie.py --help", "Xem danh sách commands có sẵn")
    
    # Show make commands
    run_command("python fastie.py make --help", "Xem các code generators")
    
    # Show database commands
    run_command("python fastie.py db --help", "Xem các database commands")
    
    # Generate some example code
    print("\n🎯 DEMO CODE GENERATION")
    print("======================")
    
    # Create a complete Blog feature
    commands = [
        ("python fastie.py make model Blog --fields \"title:str,content:str,slug:str,is_published:bool\"", 
         "Tạo Blog model với fields"),
        ("python fastie.py make schema Blog --type request", 
         "Tạo Blog request schema"),
        ("python fastie.py make schema Blog --type response", 
         "Tạo Blog response schema"),
        ("python fastie.py make repository Blog", 
         "Tạo Blog repository interface và implementation"),
        ("python fastie.py make service Blog", 
         "Tạo Blog service interface và implementation"),
        ("python fastie.py make controller Blog --resource", 
         "Tạo Blog controller với CRUD methods"),
    ]
    
    print("\n📝 Tạo hoàn chỉnh Blog feature:")
    for cmd, desc in commands:
        success = run_command(cmd, desc)
        if not success:
            print(f"❌ Failed to execute: {cmd}")
            break
    
    # Show routes
    run_command("python fastie.py routes", "Xem tất cả routes trong application")
    
    print("\n✅ DEMO COMPLETED!")
    print("==================")
    print("Files được tạo:")
    print("- app/models/blog.py")
    print("- app/schemas/requests/blog/blog_request_schema.py")
    print("- app/schemas/responses/blog/blog_response_schema.py")
    print("- app/repositories/interfaces/blog/i_blog_repository.py")
    print("- app/repositories/implements/blog/blog_repository.py")
    print("- app/services/interfaces/blog/i_blog_service.py")
    print("- app/services/implements/blog/blog_service.py")
    print("- app/api/v1/controllers/blog/blog_controller.py")
    print("\n💡 Để cleanup demo files, chạy: python cleanup_demo.py")

if __name__ == "__main__":
    main() 