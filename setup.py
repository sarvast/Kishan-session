import subprocess
import sys

def install_requirements():
    print("Installing required packages...")
    packages = [
        "streamlit==1.28.0",
        "Pillow==10.1.0",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "numpy>=1.24.3"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            return False
    return True

if __name__ == "__main__":
    if install_requirements():
        print("\nAll packages installed successfully!")
        print("\nYou can now run the application using:")
        print("streamlit run app.py")
    else:
        print("\nSome packages failed to install. Please check the errors above.") 