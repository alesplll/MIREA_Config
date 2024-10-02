import configparser
import subprocess
import os

# Read config file


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['DEFAULT']['visualizer_path'], config['DEFAULT']['repo_path'], config['DEFAULT']['file_hash']

# Get commits with the specified file hash


def get_commits_with_file(repo_path, file_hash):
    command = f"git -C {repo_path} log --pretty=format:%H -- {file_hash}"
    result = subprocess.run(
        command, capture_output=True, shell=True, text=True)
    if result.returncode != 0:
        raise Exception("Error getting commits")
    return result.stdout.splitlines()

# Get parent commits for each commit


def get_commit_parents(repo_path, commit_hash):
    command = f"git -C {repo_path} log --pretty=format:%P -n 1 {commit_hash}"
    result = subprocess.run(
        command, capture_output=True, shell=True, text=True)
    if result.returncode != 0:
        raise Exception("Error getting commit parents")
    return result.stdout.split()

# Build dependency graph in PlantUML format


def build_dependency_graph(repo_path, commits):
    edges = []
    for commit in commits:
        parents = get_commit_parents(repo_path, commit)
        for parent in parents:
            edges.append(f'"{parent}" --> "{commit}"')

    graph = "@startuml\n"
    graph += "\n".join(edges)
    graph += "\n@enduml"

    return graph

# Visualize graph using PlantUML


def visualize_graph(uml_code, visualizer_path):
    with open('graph.puml', 'w') as f:
        f.write(uml_code)

    command = f"java -jar {visualizer_path} graph.puml"
    os.system(command)
    os.remove('graph.puml')  # Remove temporary file

# Main function


def main(config_path):
    try:
        visualizer_path, repo_path, file_hash = read_config(config_path)
        commits = get_commits_with_file(repo_path, file_hash)

        if not commits:
            print("No commits found with the given file hash.")
            return

        graph = build_dependency_graph(repo_path, commits)
        visualize_graph(graph, visualizer_path)
    except Exception as e:
        print(f"Error: {e}")


# Run the program
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python visualizer.py <config-file>")
    else:
        main(sys.argv[1])
