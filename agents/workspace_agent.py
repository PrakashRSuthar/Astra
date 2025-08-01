from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
import json
import os
import subprocess
import webbrowser
import time

WORKSPACE_FILE = "workspaces.json"
# Make sure this path is correct for your system. Use forward slashes.
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe" 

def _load_workspaces():
    if not os.path.exists(WORKSPACE_FILE): return {}
    try:
        with open(WORKSPACE_FILE, "r") as f: return json.load(f)
    except json.JSONDecodeError: return {}

def _save_workspaces(workspaces):
    with open(WORKSPACE_FILE, "w") as f: json.dump(workspaces, f, indent=2)

def _normalize_path(path: str) -> str:
    return path.replace("\\", "/")

@tool
def add_workspace(project_name: str) -> str:
    """Use this tool to add a new project workspace. It will trigger an interactive session to ask for details."""
    print(f"\n--- Starting interactive setup for '{project_name}' workspace ---")
    workspaces = _load_workspaces()
    if project_name in workspaces:
        action = input(f"Workspace '{project_name}' already exists. Overwrite? (y/n): ").lower()
        if action != 'y': return "Workspace setup cancelled."

    apps, folders, tabs, vscode_folders = [], [], [], []

    print("\n--- Section 1: Applications & Shortcuts (.exe, .lnk) ---")
    while True:
        path = input("Enter the full path of an application or shortcut (or type 'done'): ").strip().strip('"')
        if path.lower() == 'done': break
        if path: apps.append(_normalize_path(path))

    print("\n--- Section 2: Folders (to open in File Explorer) ---")
    while True:
        path = input("Enter the full path of a folder to open (or type 'done'): ").strip().strip('"')
        if path.lower() == 'done': break
        if path: folders.append(_normalize_path(path))

    print("\n--- Section 3: Folders (to open in VS Code) ---")
    while True:
        path = input("Enter the project folder path to open in VS Code (or type 'done'): ").strip().strip('"')
        if path.lower() == 'done': break
        if path: vscode_folders.append(_normalize_path(path))

    print("\n--- Section 4: Browser Tabs ---")
    chrome_profile = input("Enter Chrome Profile Directory Name (e.g., 'Default' or 'Profile 1'). Press Enter to skip: ").strip()
    while True:
        url = input("Enter a URL for a browser tab (or type 'done'): ").strip()
        if url.lower() == 'done': break
        if url: tabs.append(url)

    workspaces[project_name] = {
        "apps": apps, "folders": folders, "vscode_folders": vscode_folders,
        "chrome_profile": chrome_profile, "tabs": tabs
    }
    _save_workspaces(workspaces)
    return f"\nSuccessfully created the '{project_name}' workspace."

@tool
def open_workspace(project_name: str) -> str:
    """Use this tool to open a pre-configured project workspace and get a status report."""
    workspaces = _load_workspaces()
    if project_name not in workspaces:
        return f"Error: No workspace named '{project_name}' found."

    config = workspaces[project_name]
    status_report = [f"Executing workspace '{project_name}':"]
    print(f"\n[🖥️ Workspace Agent] opening '{project_name}' workspace...\n")

    # --- VS Code ---
    for folder_path in config.get("vscode_folders", []):
        try:
            if os.path.isdir(folder_path):
                # This is a more robust way to call VS Code with a folder path
                subprocess.run(f'code "{folder_path}"', shell=True, check=True)
                status_report.append(f"  ✅ SUCCESS: Opened '{folder_path}' in VS Code.")
            else:
                status_report.append(f"  ❌ FAILED: VS Code folder not found: {folder_path}")
        except Exception as e:
            status_report.append(f"  ❌ FAILED: Could not open '{folder_path}' in VS Code. Error: {e}")

    # --- Other Apps & Shortcuts ---
    for app_path in config.get("apps", []):
        try:
            if os.path.exists(app_path):
                os.startfile(app_path)
                status_report.append(f"  ✅ SUCCESS: Launched app/shortcut: {os.path.basename(app_path)}")
            else:
                status_report.append(f"  ❌ FAILED: App/shortcut not found: {app_path}")
        except Exception as e:
            status_report.append(f"  ❌ FAILED: Could not launch {os.path.basename(app_path)}. Error: {e}")

    # --- Folders in Explorer ---
    for folder_path in config.get("folders", []):
        try:
            if os.path.isdir(folder_path):
                os.startfile(folder_path)
                status_report.append(f"  ✅ SUCCESS: Opened folder: {folder_path}")
            else:
                status_report.append(f"  ❌ FAILED: Folder not found: {folder_path}")
        except Exception as e:
            status_report.append(f"  ❌ FAILED: Could not open folder {folder_path}. Error: {e}")

    # --- Browser Tabs ---
    chrome_profile = config.get("chrome_profile")
    tabs = config.get("tabs", [])
    if tabs:
        try:
            if chrome_profile and os.path.exists(CHROME_PATH):
                for url in tabs:
                    subprocess.Popen([CHROME_PATH, f"--profile-directory={chrome_profile}", url])
                status_report.append(f"  ✅ SUCCESS: Opened {len(tabs)} tabs in Chrome Profile '{chrome_profile}'.")
            else:
                for i, url in enumerate(tabs):
                    webbrowser.open_new_tab(url) if i > 0 else webbrowser.open_new(url)
                status_report.append(f"  ✅ SUCCESS: Opened {len(tabs)} tabs in default browser.")
        except Exception as e:
            status_report.append(f"  ❌ FAILED: Could not open browser tabs. Error: {e}")
            
    return "\n".join(status_report)

# list_workspaces and open_folder tools remain the same
@tool
def list_workspaces() -> str:
    """Lists all available project workspaces."""
    workspaces = _load_workspaces()
    if not workspaces: return "No workspaces have been configured yet."
    return f"The following workspaces are available: {', '.join(workspaces.keys())}"

@tool
def open_folder(folder_path: str) -> str:
    """Opens a single, specific folder."""
    try:
        normalized_path = _normalize_path(folder_path)
        if os.path.isdir(normalized_path):
            os.startfile(normalized_path)
            return f"Successfully opened the folder: {normalized_path}"
        else:
            return f"Error: The folder path '{normalized_path}' does not exist."
    except Exception as e:
        return f"An error occurred while opening the folder: {e}"