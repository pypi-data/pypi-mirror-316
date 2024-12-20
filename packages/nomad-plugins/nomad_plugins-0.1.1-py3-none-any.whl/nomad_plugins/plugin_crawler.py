import base64
import json
import os
import re
import shutil
from enum import Enum

import click
import requests
import toml


class OasisURLs(Enum):
    CENTRAL = (
        'https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-distro/-/raw/'
        'main/pyproject.toml'
    )
    EXAMPLE = (
        'https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-distro/-/raw/'
        'test-oasis/pyproject.toml'
    )


# GitHub Code Search API URL
GITHUB_CODE_API = 'https://api.github.com/search/code'
GITHUB_REPO_API = 'https://api.github.com/repos'


def fetch_file_created(repo_name: str, file_path: str, headers: dict) -> str:
    """
    Fetches the creation date of a file in a GitHub repository by retrieving the
    commit history of the file and returning the date of the earliest commit.
    Args:
        repo_name (str): The name of the GitHub repository in the format 'owner/repo'.
        file_path (str): The path to the file within the repository.
        headers (dict): The headers to include in the request, typically containing
                        the authorization token.
    Returns:
        str: The creation date of the file in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ),
             or None if the commits could not be fetched.
    """

    commits_url = f'{GITHUB_REPO_API}/{repo_name}/commits?path={file_path}'
    commits = []
    commits_page = 1

    while True:
        commits_params = {
            'path': file_path,
            'per_page': 30,
            'page': commits_page,
        }
        commits_response = requests.get(
            commits_url, headers=headers, params=commits_params
        )
        if commits_response.ok:
            commits_page_results = commits_response.json()
            commits.extend(commits_page_results)
            if 'next' in commits_response.links:
                commits_page += 1
            else:
                break
        else:
            click.echo(
                f'Failed to fetch commits for {repo_name}: '
                f'{commits_response.status_code}, {commits_response.text}'
            )
            return None
    if commits:
        file_created = commits[-1]['commit']['committer']['date']
        return file_created
    return None


def fetch_repo_details(repo_full_name: str, headers: dict) -> dict:
    """
    Fetches the details of a GitHub repository using the GitHub API.
    Args:
        repo_full_name (str): The full name of the repository (e.g., 'owner/repo').
        headers (dict): The headers to include in the request, typically containing
                        the authorization token.
    Returns:
        dict: A dictionary containing the repository details if the request is
              successful.
              Returns None if the request fails, and prints an error message with the
              status code and response text.
    """

    repo_url = f'{GITHUB_REPO_API}/{repo_full_name}'
    response = requests.get(repo_url, headers=headers)
    if response.ok:
        return response.json()
    else:
        click.echo(
            f'Failed to fetch repository details for {repo_full_name}: '
            f'{response.status_code}, {response.text}'
        )
        return None


def get_toml_project(url: str, subdirectory: str, headers: dict) -> dict:
    """
    Fetches and parses the `pyproject.toml` file from a given GitHub repository.
    Args:
        url (str): The URL of the GitHub repository.
        subdirectory (str): The subdirectory within the repository where the
                            `pyproject.toml` file is located.
        headers (dict): The headers to include in the request, typically containing
                        authorization information.
    Returns:
        dict: A dictionary containing the 'project' section of the `pyproject.toml` file
              if successful, otherwise an empty dictionary.
    """

    repo_api_url = url.replace('https://github.com', GITHUB_REPO_API)
    request_url = f'{repo_api_url}/contents/{subdirectory}pyproject.toml'
    response = requests.get(request_url, headers=headers)
    if response.ok:
        content = response.json().get('content')
        if content:
            toml_content = base64.b64decode(content).decode('utf-8')
            try:
                return toml.loads(toml_content).get('project', {})
            except toml.TomlDecodeError as e:
                click.echo(f'Failed to parse pyproject.toml from {request_url}: {e}')
    elif response.status_code == requests.codes.forbidden:
        msg = 'Too many requests to GitHub API. Please try again later.'
        click.echo(msg)
    else:
        msg = (
            f'Failed to get pyproject.toml from {request_url}: '
            f'{response.json().get("message", "No message")}'
        )
        click.echo(msg)
    return {}


def on_gitlab_oasis(plugin_name: str, oasis_toml: OasisURLs) -> bool:
    """
    Checks if a given plugin name is listed in the plugin dependencies of a
    pyproject.toml file located at a specified URL.
    Args:
        plugin_name (str): The name of the plugin to check for.
        oasis_toml (OasisURLs): An object containing the URL to the pyproject.toml file.
    Returns:
        bool: True if the plugin name is found in the optional dependencies, False
              otherwise.
    """

    response = requests.get(oasis_toml.value)
    if not response.ok:
        msg = f'Failed to get pyproject.toml from {oasis_toml.value}: {response.text}'
        click.echo(msg)
    try:
        pyproject_data = toml.loads(response.text)
    except toml.TomlDecodeError as e:
        click.echo(f'Failed to parse pyproject.toml from {oasis_toml.value}: {e}')
        return False
    name_pattern = re.compile(r'^[^;>=<\s]+')
    plugin_dependencies = pyproject_data['project']['optional-dependencies']['plugins']
    return plugin_name in [name_pattern.match(d).group() for d in plugin_dependencies]


def find_dependencies(project: dict, headers: dict) -> list[dict]:
    """
    Finds and returns a list of plugin dependencies for a given project.
    This function examines the dependencies of a given project and identifies
    those that are related to 'nomad-lab'. It supports both standard PyPI
    dependencies and dependencies specified via git URLs.
    Args:
        project (dict): A dictionary representing the project, which should
                        contain a 'dependencies' key with a list of dependency
                        strings.
        headers (dict): A dictionary of HTTP headers to use when making requests
                        to external services.
    Returns:
        list[dict]: A list of dictionaries, each representing a plugin dependency.
                    Each dictionary contains the following keys:
                    - 'm_def': A string indicating the schema definition.
                    - 'name': The name of the dependency.
                    - 'location': The URL or location of the dependency.
                    - 'toml_directory': The subdirectory within the git repository
                                        where the dependency's pyproject.toml file
                                        is located (if applicable).
    """

    name_pattern = re.compile(r'^[^;>=<\s]+')
    git_pattern = re.compile(r'@ git\+(.*?)\.git(?:@[^#]+)?(?:#subdirectory=(.*))?')
    plugin_dependencies = []
    for dependency in project.get('dependencies', []):
        name = name_pattern.match(dependency).group(0)
        git_match = git_pattern.search(dependency)
        toml_directory = ''
        if git_match:
            location = git_match.group(1)
            if git_match.group(2):
                toml_directory = git_match.group(2) + '/'
            project = get_toml_project(location, toml_directory, headers)
            if not any('nomad-lab' in d for d in project.get('dependencies', [])):
                continue
        else:
            response = requests.get(f'https://pypi.org/pypi/{name}/json')
            if not response.ok:
                continue
            response_json = response.json()
            info = response_json.get('info', {})
            dependencies = info.get('requires_dist', [])
            if not dependencies or not any('nomad-lab' in d for d in dependencies):
                continue
            location = f'https://pypi.org/project/{name}/'

        plugin_dependencies.append(
            dict(
                m_def='nomad_plugins.schema_packages.plugin.PluginReference',
                name=name,
                location=location,
                toml_directory=toml_directory,
            )
        )
    return plugin_dependencies


def get_entry_points(toml_project: dict) -> dict:
    """
    Extracts and categorizes plugin entry points from a given TOML project dictionary.
    Args:
        toml_project (dict): A dictionary representation of the project from a
        pyproject.toml file.
    Returns:
        dict: A list of dictionaries, each representing a plugin entry point with the
            following keys:
            - m_def (str): The module definition for the plugin entry point.
            - name (str): The name of the entry point.
            - module (str): The module path of the entry point.
            - type (str or None): The type of the entry point, which can be one of the
              following:
                'Schema package', 'Parser', 'Normalizer', 'App', 'Example upload',
                'API', or None if no type is matched.
    """

    entry_points = toml_project.get('entry-points', {}).get('nomad.plugin', {})
    plugin_entry_points = []
    for name, entry_point in entry_points.items():
        type = None
        if 'schema' in entry_point or 'schema' in name:
            type = 'Schema package'
        elif 'parser' in entry_point or 'parser' in name:
            type = 'Parser'
        elif 'normalizer' in entry_point or 'normalizer' in name:
            type = 'Normalizer'
        elif 'app' in entry_point or 'app' in name:
            type = 'App'
        elif 'example' in entry_point or 'example' in name:
            type = 'Example upload'
        elif 'api' in entry_point or 'api' in name:
            type = 'API'
        plugin_entry_points.append(
            dict(
                m_def='nomad_plugins.schema_packages.plugin.PluginEntryPoint',
                name=name,
                module=entry_point,
                type=type,
            )
        )
    return plugin_entry_points


def get_plugin(item: dict, headers: dict) -> dict:
    """
    Extracts plugin information from a given repository item and returns it as a
    dictionary.
    Args:
        item (dict): A dictionary containing repository item information, including the
                     repository details and file path.
        headers (dict): A dictionary containing HTTP headers for making requests to
                        external services.
    Returns:
        dict: A dictionary containing the extracted plugin information, including
              repository details, project metadata, and plugin-specific attributes.
              Returns None if required information is missing or cannot be fetched.
    """

    repo_info = item['repository']
    repo_full_name = repo_info['full_name']
    repo_details = fetch_repo_details(repo_full_name, headers)
    if repo_details is None:
        return
    toml_directory = ''
    if not item['path'].startswith('pyproject.toml'):
        toml_directory = item['path'].split('/pyproject.toml')[0] + '/'
    project = get_toml_project(repo_info['url'], toml_directory, headers)
    name = project.get('name', None)
    if name is None:
        return
    plugin = dict(
        m_def='nomad_plugins.schema_packages.plugin.Plugin',
        repository='https://github.com/' + repo_full_name,
        stars=repo_details['stargazers_count'],
        created=fetch_file_created(
            repo_full_name,
            item['path'],
            headers,
        ),
        last_updated=repo_details['pushed_at'],
        owner=repo_info['owner']['login'],
        name=name,
        description=project.get('description', None),
        authors=project.get('authors', []),
        maintainers=project.get('maintainers', []),
        plugin_dependencies=find_dependencies(project, headers),
        on_central=on_gitlab_oasis(name, OasisURLs.CENTRAL),
        on_example_oasis=on_gitlab_oasis(name, OasisURLs.EXAMPLE),
        on_pypi=requests.get(f'https://pypi.org/pypi/{name}/json').ok,
        plugin_entry_points=get_entry_points(project),
    )
    plugin['toml_directory'] = toml_directory[:-1]
    return plugin


def find_plugins(token: str) -> dict:
    """
    Find and retrieve Nomad plugins from GitHub repositories.
    This function searches for repositories containing Nomad plugins by querying
    the GitHub Code Search API. It retrieves the plugins from repositories that
    have 'nomad.plugin' entry points defined in their `pyproject.toml` files.
    Args:
        token (str): GitHub personal access token for authentication.
    Returns:
        dict: A dictionary where keys are plugin names (repository full names with
              slashes replaced by underscores) and values are the plugin data.
    """

    query = "project.entry-points.'nomad.plugin' in:file filename:pyproject.toml"
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': 30,
    }
    headers = {'Authorization': f'token {token}'}

    plugins = {}
    page = 1

    # Initial request to get the total number of items
    response = requests.get(GITHUB_CODE_API, headers=headers, params=params)
    if not response.ok:
        click.echo(f'Failed to fetch data: {response.status_code}, {response.text}')
        return plugins

    search_results = response.json()
    total_items = search_results['total_count']
    click.echo(f'Found {total_items} repositories')

    with click.progressbar(length=total_items, label='Processing repositories') as bar:
        while True:
            params['page'] = page

            response = requests.get(GITHUB_CODE_API, headers=headers, params=params)

            if not response.ok:
                click.echo(
                    f'Failed to fetch data: {response.status_code}, {response.text}'
                )
                break
            search_results = response.json()
            total_items = search_results['total_count']
            for item in search_results['items']:
                plugin_name = item['repository']['full_name'].replace('/', '_')
                plugins[plugin_name] = get_plugin(item, headers)
                bar.update(1)
            if 'next' in response.links:
                page += 1
            else:
                break
    return plugins


def save_plugins(plugins: dict, save_path: str) -> None:
    """
    Save plugins to JSON files and create a zip archive of the saved files.
    Args:
        plugins (dict): A dictionary where keys are plugin names and values are plugin
                        data.
        save_path (str): The directory path where the JSON files will be saved and the
                         zip archive will be created.
    Returns:
        None
    """

    for name, plugin in plugins.items():
        save_file = os.path.join(save_path, f'{name}.archive.json')
        with open(save_file, 'w') as f:
            json.dump({'data': plugin}, f, indent=4)

    shutil.make_archive(save_path, 'zip', save_path)


def get_authentication_token(nomad_url: str, username: str, password: str) -> str:
    """
    Retrieves an authentication token from the specified Nomad URL using the provided
    username and password.
    Args:
        nomad_url (str): The base URL of the Nomad server.
        username (str): The username for authentication.
        password (str): The password for authentication.
    Returns:
        str: The authentication token if successfully retrieved, otherwise None.
    """

    try:
        response = requests.get(
            nomad_url + 'auth/token',
            params=dict(username=username, password=password),
            timeout=10,
        )
        token = response.json().get('access_token')
        if token:
            return token

        click.echo('response is missing token: ')
        click.echo(response.json())
        return
    except Exception:
        click.echo('something went wrong trying to get authentication token')
        return


def upload_to_NOMAD(nomad_url: str, token: str, upload_file: str) -> str:
    """
    Uploads a file to the NOMAD server.
    Args:
        nomad_url (str): The URL of the NOMAD server.
        token (str): The authorization token for accessing the NOMAD server.
        upload_file (str): The path to the file to be uploaded.
    Returns:
        str: The upload ID if the upload is successful, otherwise None.
    """

    with open(upload_file, 'rb') as f:
        try:
            response = requests.post(
                nomad_url + 'uploads',
                headers={
                    'Authorization': f'Bearer {token}',
                    'Accept': 'application/json',
                },
                data=f,
                timeout=30,
            )
            upload_id = response.json().get('upload_id')
            if upload_id:
                return upload_id

            click.echo('response is missing upload_id: ')
            click.echo(response.json())
            return
        except Exception:
            click.echo('something went wrong uploading to NOMAD')
            return


@click.command()
@click.option(
    '--github-token', prompt='GitHub Token', help='Your GitHub personal access token.'
)
@click.option('--nomad-url', prompt='NOMAD URL', help='The NOMAD upload URL.')
@click.option('--nomad-username', prompt='NOMAD Username', help='Your NOMAD username.')
@click.option(
    '--nomad-password',
    prompt='NOMAD Password',
    help='Your NOMAD upload password.',
    hide_input=True,
)
@click.option(
    '--save-path', prompt='Save Path', help='The path to save the plugin archives.'
)
def main(github_token, nomad_url, nomad_username, nomad_password, save_path):
    """
    Main function to find plugins, save them, and upload to NOMAD.
    Args:
        github_token (str): GitHub token for authentication to access plugins.
        nomad_url (str): URL of the NOMAD service.
        nomad_username (str): Username for NOMAD authentication.
        nomad_password (str): Password for NOMAD authentication.
        save_path (str): Path to save the plugins data.
    Returns:
        None
    """

    plugins = find_plugins(github_token)
    save_plugins(plugins, save_path)
    token = get_authentication_token(nomad_url, nomad_username, nomad_password)
    if token:
        upload_id = upload_to_NOMAD(nomad_url, token, save_path + '.zip')
        click.echo(f'Uploaded to NOMAD upload: {upload_id}')


if __name__ == '__main__':
    main()
