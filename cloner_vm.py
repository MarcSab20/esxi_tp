#!/usr/bin/env python3
from pyVim import connect
from pyVmomi import vim
import ssl
import json
from time import sleep

def get_config_from_json(json_file):
    """Lecture du fichier de configuration JSON"""
    with open(json_file, 'r') as f:
        return json.load(f)

def cloner_vm(si, source_vm_name, num_clones):
    """Fonction pour cloner une VM existante"""
    content = si.RetrieveContent()
    
    # Recherche de la VM source
    vm = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    
    for managed_object_ref in container.view:
        if managed_object_ref.name == source_vm_name:
            vm = managed_object_ref
            break
    
    container.Destroy()
    
    if not vm:
        raise Exception(f"VM source {source_vm_name} non trouvée")

    # Récupération des objets nécessaires
    datacenter = content.rootFolder.childEntity[0]
    resource_pool = datacenter.hostFolder.childEntity[0].resourcePool
    
    # Création des clones
    for i in range(num_clones):
        clone_name = f"{source_vm_name}_clone_{i+1}"
        
        # Configuration de la relocation
        relospec = vim.vm.RelocateSpec()
        relospec.pool = resource_pool

        # Configuration du clone
        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = False
        clonespec.template = False

        # Lancement du clonage
        print(f"Clonage de la VM {clone_name} en cours...")
        task = vm.Clone(
            folder=datacenter.vmFolder,
            name=clone_name,
            spec=clonespec
        )

        # Attente de la fin du clonage
        while task.info.state not in [vim.TaskInfo.State.success,
                                    vim.TaskInfo.State.error]:
            sleep(1)

        if task.info.state == vim.TaskInfo.State.success:
            print(f"Clone {clone_name} créé avec succès")
        else:
            print(f"Erreur lors du clonage de {clone_name}")

def main():
    # Configuration SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_NONE

    # Lecture de la configuration
    config = get_config_from_json('config.json')

    # Connexion à vSphere
    si = connect.SmartConnect(
        host=config['esxi_host'],
        user=config['esxi_user'],
        pwd=config['esxi_password'],
        sslContext=context
    )

    try:
        cloner_vm(
            si,
            config['source_vm_name'],
            config['num_clones']
        )
    finally:
        connect.Disconnect(si)

if __name__ == "__main__":
    main()