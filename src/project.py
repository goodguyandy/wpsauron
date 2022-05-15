import os
from definitions import ROOT_DIR
from src.utils import waybackurls, scrape_domain_and_get_plugins_info, download_plugin_and_extract


class Project:
    def __init__(self, name, include_subdomains=False):
        self.name = name
        self.plugins = []
        self.include_subdomains = include_subdomains
        self.projects_base_path = ROOT_DIR + "/projects/"
        self.project_path = self.projects_base_path + f"/{name}/"
        self.project_plugins_path = self.project_path + "/plugins/"
        self.compose_template = ROOT_DIR + "/compose_template.yml"
        self.project_docker_compose = self.project_path + "/docker-compose.yml"
        self.init_project()

    def _init_projects_folders(self):
        if not os.path.exists(self.projects_base_path):
            os.makedirs(self.projects_base_path)
        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)
        if not os.path.exists(self.project_plugins_path):
            os.makedirs(self.project_plugins_path)

    def _init_docker_compose(self):
        data = ""
        with open(self.compose_template, 'r') as f:
            data = f.read()
            #data = data.replace("#PROJECT_PLUGIN_PATH#", self.project_plugins_path )
            # we could copy the file, but maybe in the future we need to change someting
        with open(self.project_docker_compose, 'w') as f:
            f.write(data)
    def init_project(self):
        self._init_projects_folders()
        self._init_docker_compose()

    def get_plugins(self):
        self.plugins = scrape_domain_and_get_plugins_info(self.name)
        return self.plugins

    def downloads_plugins_and_extract(self):
        for plugin in self.plugins:
            path = self.project_plugins_path
            if "download_url" in self.plugins[plugin]:
                download_url = self.plugins[plugin]["download_url"]
                download_plugin_and_extract(download_url, path)


