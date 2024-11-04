import os
import json
import subprocess

# Fonction pour obtenir la structure des fichiers du projet
def get_file_structure(root_dir):
    file_structure = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        relative_path = os.path.relpath(dirpath, root_dir)
        file_structure[relative_path] = {
            "directories": dirnames,
            "files": filenames
        }
    return file_structure

# Fonction pour obtenir les dépendances du projet
def get_dependencies():
    dependencies = {}
    # Vérification des fichiers de dépendances communs
    if os.path.isfile('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            dependencies['requirements.txt'] = f.read().splitlines()
    if os.path.isfile('package.json'):
        with open('package.json', 'r') as f:
            package_json = json.load(f)
            dependencies['package.json'] = package_json.get('dependencies', {})
    if os.path.isfile('Pipfile'):
        pipfile_output = subprocess.check_output(['pipenv', 'lock', '--requirements'])
        dependencies['Pipfile'] = pipfile_output.decode().splitlines()
    return dependencies

# Fonction pour obtenir les informations Git
def get_git_info():
    git_info = {}
    git_info['current_branch'] = subprocess.check_output(['git', 'branch', '--show-current']).strip().decode()
    git_info['last_commit'] = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%H']).strip().decode()
    git_info['remote_url'] = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url']).strip().decode()
    return git_info

# Fonction pour obtenir les informations du projet
def get_project_info():
    project_info = {}
    project_info['file_structure'] = get_file_structure('.')
    project_info['dependencies'] = get_dependencies()
    project_info['git_info'] = get_git_info()
    return project_info

# Point d'entrée principal du script
if __name__ == "__main__":
    project_info = get_project_info()
    with open('script_repo.json', 'w') as f:
        json.dump(project_info, f, indent=4)
    print("Project report generated in 'script_repo.json'")
