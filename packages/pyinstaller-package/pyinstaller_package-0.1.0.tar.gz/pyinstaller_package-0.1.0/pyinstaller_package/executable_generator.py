import os
import subprocess
import shutil


def create_executable(target_path, python_file):
    print("PyInstaller Executable Generator")
    print("-" * 30)

    # Get the current working directory to save the executable
    current_dir = os.getcwd()
    print(f"Executable will be saved in: {current_dir}")

    # Set the path for the Documents folder
    documents_folder = os.path.expanduser('~\\Documents')  # Windows Documents folder
    print(f"Using Documents folder for temporary files: {documents_folder}")

    # Define the dist and build folder paths inside Documents
    dist_folder = os.path.join(documents_folder, 'dist')
    build_folder = os.path.join(documents_folder, 'build')

    # Run PyInstaller with the --onefile option
    try:
        subprocess.run([ 
            os.path.join(target_path, 'Scripts', 'pyinstaller.exe'),
            '--onefile',
            '--distpath', dist_folder,  # Output the executable to the 'dist' folder in Documents
            '--workpath', build_folder,  # Temporary build files will be stored in the 'build' folder in Documents
            python_file],
            check=True
        )
        print(f"PyInstaller completed successfully for {python_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Error during PyInstaller execution for {python_file}: {e}")
        return

    # Move the executable to the current working directory
    executable_name = os.path.basename(python_file).replace('.py', '.exe')
    executable_path = os.path.join(dist_folder, executable_name)
    if os.path.exists(executable_path):
        shutil.move(executable_path, os.path.join(current_dir, executable_name))
        print(f"Executable moved to: {os.path.join(current_dir, executable_name)}")
    else:
        print(f"Error: Could not locate the generated executable in '{dist_folder}'.")

    # Clean up PyInstaller build directories in Documents folder
    try:
        if os.path.exists(dist_folder):
            shutil.rmtree(dist_folder)
            print(f"Removed dist folder: {dist_folder}")
        if os.path.exists(build_folder):
            shutil.rmtree(build_folder)
            print(f"Removed build folder: {build_folder}")
    except Exception as e:
        print(f"Error during cleanup: {e}")

    print("Done!")


def generate_executables():
    # Get user input for target path and folder containing Python files
    target_path = input("Enter the target Python path (e.g., C:\\Users\\hahmadi\\AppData\\Local\\Programs\\Python\\Python311): ")
    folder_path = input("Enter the folder path containing your Python files: ").strip()

    # Validate the provided folder path
    if not os.path.isdir(folder_path):
        print("Error: The specified folder does not exist.")
        return

    # Loop through all .py files in the folder and create executables
    for file_name in os.listdir(folder_path):
        python_file = os.path.join(folder_path, file_name)

        if os.path.isfile(python_file) and python_file.endswith('.py'):
            create_executable(target_path, python_file)
        else:
            print(f"Skipping non-Python file: {file_name}")

