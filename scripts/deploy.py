#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fnmatch
import os
import subprocess
import yaml


FILE_EXT = "yaml"
ARTIFACT_URL = "https://github.com/luanvuhlu/bookstore-microservices"
DEVELOPER = {
    'mail': 'luanvuhlu@gmail.com',
    'name': 'luanvu'
}
DEFAULT_VESION = "1.0.0"
DEFAULT_OUT = "out/"
FIND_FOLDER = "api/"
CLI_FILE = "scripts/openapi-generator-cli.jar"

def main():
    os.makedirs(DEFAULT_OUT)
    for root, dirnames, filenames in os.walk(FIND_FOLDER):
        for filename in fnmatch.filter(filenames, '*.' + FILE_EXT):
            project_name = filename[:-len(FILE_EXT)-1]
            file_specs = os.path.join(root, filename)
            specs = {
                'file': file_specs,
                'project_name': project_name,
                'groupId': '.'.join(file_specs.split("/")[1:-1]) + '.' + project_name,
                'base_package': '.'.join(file_specs.split("/")[1:-1]) + '.' + project_name,
                'artifactId': project_name + '-api',
                'out': DEFAULT_OUT + project_name
            }
            run_deploy(specs)


def get_version(file_specs):
    with open(file_specs, "r") as stream:
        try:
            return yaml.safe_load(stream)['info']['version']
        except yaml.YAMLError as exc:
            return DEFAULT_VESION


def run_deploy(specs):
    subprocess.call([
        "java", 
        "-jar",
        CLI_FILE,
        "generate",
        "-i",
        specs['file'],
        "-g",
        "java",
        "-o",
        specs['out'],
        "--additional-properties=groupId="+specs['groupId']+",artifactId="+specs['artifactId']+",artifactUrl="+ARTIFACT_URL+",library=resttemplate,modelPackage="+specs['base_package']+".client.model,apiPackage="+specs['base_package']+".client.api,artifactVersion=1.0.0,java8=true,developerEmail="+DEVELOPER['mail']+",developerName="+DEVELOPER['name']
        ])
    # subprocess.call([
    #     "mvn",
    #     "deploy",
    #     "-DaltDeploymentRepository=repositoryId::default::https://maven.pkg.github.com/luanvuhlu/bookstore-openapi",
    #     # "clean",
    #     # "install",
    #     "-f",
    #     specs['out'] + '/pom.xml'  
    # ])

if __name__ == "__main__":
    main()
