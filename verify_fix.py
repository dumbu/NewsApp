#!/usr/bin/env python3
"""
Simple verification script that the back button fix is in place.
This script uses only standard library and doesn't require dependencies.
"""

import ast
import sys
from pathlib import Path


def verify_fix():
    """Verify that the fix for the back button is present in main.py."""
    
    # Read the main.py file
    main_py_path = Path(__file__).parent / "src" / "main.py"
    
    if not main_py_path.exists():
        print(f"❌ Could not find {main_py_path}")
        return False
    
    with open(main_py_path, 'r') as f:
        content = f.read()
        tree = ast.parse(content)
    
    # Find the NewsAppUI class
    news_app_ui_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "NewsAppUI":
            news_app_ui_class = node
            break
    
    if not news_app_ui_class:
        print("❌ Could not find NewsAppUI class")
        return False
    
    # Check for the correct message handler method
    handler_found = False
    old_handler_found = False
    
    for item in news_app_ui_class.body:
        if isinstance(item, ast.FunctionDef):
            if item.name == "on_back_to_dashboard_message":
                handler_found = True
                
                # Verify the method signature
                args = item.args.args
                if len(args) < 2:
                    print("❌ Handler method has incorrect number of parameters")
                    return False
                
                # Check parameter names
                if args[0].arg != 'self' or args[1].arg != 'message':
                    print("❌ Handler method has incorrect parameter names")
                    return False
                
                # Check that it calls _show_dashboard
                calls_show_dashboard = False
                for node in ast.walk(item):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Attribute):
                            if node.func.attr == "_show_dashboard":
                                calls_show_dashboard = True
                
                if not calls_show_dashboard:
                    print("❌ Handler method doesn't call _show_dashboard()")
                    return False
            
            elif item.name == "on_message":
                # Check if the old problematic handler still exists and handles BackToDashboardMessage
                has_dashboard_check = False
                for node in ast.walk(item):
                    if isinstance(node, ast.Name) and node.id == "BackToDashboardMessage":
                        has_dashboard_check = True
                        break
                
                if has_dashboard_check:
                    old_handler_found = True
    
    if not handler_found:
        print("❌ New message handler 'on_back_to_dashboard_message' not found")
        return False
    
    if old_handler_found:
        print("⚠️  Warning: Old 'on_message' handler with BackToDashboardMessage handling still exists")
        print("   This could cause conflicts. Consider removing the old handler.")
    
    # All checks passed
    print("✅ Back button fix verified successfully!")
    print()
    print("Details:")
    print("  ✓ Handler method 'on_back_to_dashboard_message' exists")
    print("  ✓ Method has correct signature: (self, message: BackToDashboardMessage)")
    print("  ✓ Method calls _show_dashboard()")
    print()
    print("The fix follows Textual's message handling pattern:")
    print("  - Messages are handled by methods named 'on_<message_name>'")
    print("  - BackToDashboardMessage → on_back_to_dashboard_message")
    print()
    print("Next steps:")
    print("  1. Test manually in Docker: docker compose up --build")
    print("  2. Press 'S' to open Settings")
    print("  3. Click '← Back' button")
    print("  4. Verify you return to the dashboard")
    
    return True


if __name__ == "__main__":
    try:
        success = verify_fix()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
