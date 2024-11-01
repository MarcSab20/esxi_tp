#!/usr/bin/env python3
from pyVim import connect
from pyVmomi import vim
import ssl
import json
import os
from time import sleep

def get_config_from_json(json_file):
    """Lecture du fichier de configuration JSON"""
    with open(json_file, 'r') as f:
        return json.load(f)

def deployer_ova(si, ova_path, num_instances, datacenter_name, datastore_name, cluster_name):
    """Fonction pour déployer plusieurs instances d'un OVA"""
    # Récupération des objets nécessaires
    content = si.RetrieveContent()
    datacenter = None
    for child in content.rootFolder.childEntity:
        if child.name == datacenter_name:
            datacenter = child
            break
    
    if not datacenter:
        raise Exception(f"Datacenter {datacenter_name} non trouvé")

    # Récupération du datastore
    datastore = None
    for ds in datacenter.datastore:
        if ds.name == datastore_name:
            datastore = ds
            break

    if not datastore:
        raise Exception(f"Datastore {datastore_name} non trouvé")

    # Récupération du cluster
    cluster = None
    for cluster_obj in datacenter.hostFolder.childEntity:
        if cluster_obj.name == cluster_name:
            cluster = cluster_obj
            break

    if not cluster:
        raise Exception(f"Cluster {cluster_name} non trouvé")

    # Paramètres de déploiement
    ovf_manager = content.ovfManager
    
    # Déploiement des instances
    for i in range(num_instances):
        vm_name = f"TinyVM_{i+1}"
        
        # Spécifications du déploiement
        spec_params = vim.OvfManager.CreateImportSpecParams()
        spec_params.entityName = vm_name
        spec_params.diskProvisioning = "thin"
        
        # Création des spécifications d'importation
        import_spec = ovf_manager.CreateImportSpec(
            ovfDescriptor=ova_path,
            resourcePool=cluster.resourcePool,
            datastore=datastore,
            cisp=spec_params
        )

        # Démarrage du déploiement
        lease = cluster.resourcePool.ImportVApp(
            import_spec.importSpec,
            datacenter.vmFolder
        )

        # Attente de la fin du déploiement
        while lease.state == vim.HttpNfcLease.State.running:
            sleep(1)

        print(f"VM {vm_name} déployée avec succès")

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
        deployer_ova(
            si,
            config['ova_path'],
            config['num_instances'],
            config['datacenter_name'],
            config['datastore_name'],
            config['cluster_name']
        )
    finally:
        # Assure la déconnexion propre même en cas d'erreur
        connect.Disconnect(si)

if __name__ == "__main__":
    main()