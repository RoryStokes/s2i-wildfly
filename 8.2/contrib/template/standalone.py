#!/usr/bin/python
from __future__ import print_function
from glob import glob
from string import Template
import os
import subprocess
import sys

def main():
    template_dir = '/usr/local/share'
    resource_dir = os.environ.get("RESOURCE_DIR", "/var/resources")

    with open(os.path.join(template_dir, 'standalone.xml.datasource'), 'r') as f:
        datasource_template = Template(f.read())

    with open(os.path.join(template_dir, 'standalone.xml.template'), 'r') as f:
        standalone_template = Template(f.read())

    datasources = []

    for resource in os.listdir(resource_dir):
        values = {
            'USERNAME': read_secret(resource_dir, resource, 'user'),
            'PASSWORD': read_secret(resource_dir, resource, 'password'),
            'RESOURCE': read_secret(resource_dir, resource, 'resource')
        }

        try:
            values['URL'] = read_secret(resource_dir, resource, 'url')
        except Exception:
            host = read_secret(resurce_dir, resource, 'host')
            port = read_secret(resurce_dir, resource, 'port')
            name = read_secret(resurce_dir, resource, 'name')
            values['URL']  = 'jdbc:oracle:thin:@' + host + ':' + port + ':' + name

        datasources.append(datasource_template.safe_substitute(values))
        
    try:
        with open(os.path.join(template_dir, 'securitydomains.xml'), r) as f:
            extra_securitydomains = f.read()
    except:
        extra_securitydomains = ''

    context = {
        'DATASOURCES': str.join("\n", datasources),
        'SECURITYDOMAINS': extra_securitydomains
    }

    print(standalone_template.safe_substitute(context))

def read_secret(resource_dir, resource, name):
    path = os.path.join(resource_dir, resource, name)
    try:
        with open(path, 'r') as file:
            return file.readline().strip()
    except IOError:
        raise Exception("Could not find expected resource secret file " + path)

if __name__ == "__main__":
    main()