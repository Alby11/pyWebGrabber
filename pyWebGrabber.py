import os
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

def get_directory():
    """Prompts user for directory with autocompletion."""
    completer = PathCompleter(expanduser=True)
    return prompt("Enter destination directory: ", completer=completer)

def collect_urls():
    """Collects URLs from user input until 'done' is typed."""
    urls = []
    while True:
        url = input("Enter a website URL (or type 'done' to finish): ").strip()
        if url.lower() == 'done':
            break
        if url:
            urls.append(url)
    return urls

def download_website(url, directory_path):
    """Attempts to download the website using wget with HTTPS first, then HTTP if necessary."""
    protocols = ['https', 'http']
    for protocol in protocols:
        try:
            full_url = f"{protocol}://{url}" if not url.startswith(('http:', 'https:')) else url
            command = [
                "wget", "-k", "-E", "-r", "-l", "10", "-p", "-N", "-P", directory_path, full_url
            ]
            subprocess.run(command, check=True)
            print(f"Downloaded content from {full_url} successfully.")
            return
        except subprocess.CalledProcessError as e:
            print(f"Failed to download content from {full_url} using {protocol}, trying next if available...")
    print(f"Unable to download {url}. Please check the URL and try again.")

def main():
    directory_path = get_directory()
    os.makedirs(directory_path, exist_ok=True)
    urls = collect_urls()

    for url in urls:
        download_website(url, directory_path)

# Uncomment to run
main()
