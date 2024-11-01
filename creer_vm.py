#!/usr/bin/env python3
from pyVim import connect
from pyVmomi import vim
import ssl
import json

def get_config_from_json(json_file):
    """Lecture du fichier de configuration JSON"""
    with open(json_file, 'r') as f:
        return json.load(f)

def creer_vm(vm_name, si, vm_folder, resource_pool, datastore, config):
    
    

def ajouter_disque(vm, datastore, disk_size_gb):
    


def main():
    


if __name__ == "__main__":
    main()