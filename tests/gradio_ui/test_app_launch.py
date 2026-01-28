#!/usr/bin/env python
"""
Quick test script to verify the Gradio app can be created and launched.
"""

from gradio_ui.app import create_app


def test_app_creation() -> bool:
    """Test that the app can be created without errors."""
    try:
        app = create_app()
        print("✅ App created successfully!")
        print(f"✅ App type: {type(app)}")
        print(f"✅ App has launch method: {hasattr(app, 'launch')}")
        return True
    except Exception as e:
        print(f"❌ Error creating app: {e}")
        return False


if __name__ == "__main__":
    success = test_app_creation()
    exit(0 if success else 1)
