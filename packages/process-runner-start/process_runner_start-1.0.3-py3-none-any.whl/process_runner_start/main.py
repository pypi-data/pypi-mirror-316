import sys
import os
import subprocess


def detect_project_type():
    """Detects the project type based on common files."""
    patterns = {
        'node': ['package.json'],
        'java': ['pom.xml', '*.java'],
        'ruby': ['Gemfile'],
        'go': ['go.mod'],
        'elixir': ['mix.exs'],
        'python': ['requirements.txt'],
        'rust': ['cargo.toml'],
        'c': ['*.c'],
        'c++': ['*.cpp'],
        'powershell': ['*ps1'],
        'csharp': ['*.csproj', '*.sln', '*.cs'],
    }
    for project_type, files in patterns.items():
        for file in files:
            if '*' in file:  # Handle wildcard patterns
                if any(f.endswith(file.lstrip('*')) for f in os.listdir()):
                    return project_type
            elif os.path.exists(file):
                return project_type
    return None

def print_dotnet_sdk_error():
    """Prints an error message if the .NET SDK is not installed."""
    print("\nError: The .NET SDK is not installed or not available in your system's PATH.")
    print("To run C# projects, you need to install the .NET SDK.")
    print("\nFollow these steps to install it:")
    print("1. Visit the .NET download page: https://dotnet.microsoft.com/download")
    print("2. Download the latest version of the .NET SDK for your operating system.")
    print("3. Install the SDK by following the on-screen instructions.")
    print("4. After installation, ensure that the 'dotnet' command is accessible from your terminal.")
    print("\nIf the issue persists, restart your terminal or verify your PATH settings.")


def start_project(project_type):
    """Runs the start command for the given project type."""
    commands = {
        'node': ['npm', 'run', 'start'],
        'java': ['mvn', 'compile', 'exec:java'],
        'ruby': ['bundle', 'exec', 'ruby', 'main.rb'],
        'go': ['go', 'run', '.'],
        'elixir': ['mix', 'run'],
        'python': ['python', 'main.py'],
        'rust': ['cargo', 'run'],
        'c': [
            ['gcc', '-o', 'output', 'main.c'],
            ['output.exe'] if os.name == 'nt' else ['./output'],
        ],
        'c++': [
            ['g++', '-o', 'output', 'main.cpp'],
            ['output.exe'] if os.name == 'nt' else ['./output'],
        ],
        'powershell': : ['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'script.ps1'],
        'csharp': [
            ['dotnet', 'build'],
            ['dotnet', 'run'],
            ['dotnet', 'script', 'main.cs']
        ],
    }
    command = commands.get(project_type)
    if not command:
        print(f"Unknown or unsupported project type: {project_type}")
        return

    try:
        print(f"Running {project_type} project...")
        subprocess.run(command, check=True)
    except FileNotFoundError as e:
            if project_type == 'csharp':
                print_dotnet_sdk_error()
            else:
                print(f"Error: Required tool not found. Ensure it's installed and in your PATH.")
            return
    except subprocess.CalledProcessError as e:
        print(f"Failed to start {project_type} project: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    if len(sys.argv) <= 1 or sys.argv[1].lower() != "start":
        print("Usage: process-runner_start start")
        return

    project_type = detect_project_type()
    if project_type:
        print(f"Detected {project_type} project.")
        start_project(project_type)
    else:
        print("Could not detect project type. Ensure you're in the project root directory or have files corresponding to a project type. (ex: package.json for Node.js projects)")


if __name__ == '__main__':
    main()
