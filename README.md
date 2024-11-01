# ESXi Automation Scripts

Scripts Python pour l'automatisation des tâches VMware ESXi utilisant PyVmomi.

## Fonctionnalités

- Déploiement d'OVA
- Clonage de VMs
- Création de VMs from scratch

## Prérequis

- Python 3.x
- PyVmomi
- Accès à un serveur ESXi

## installtion

```bash
pip install -r requirements.txt

## utilisation


python3 deploy_ova.py
python3 clone_vm.py
python3 create_vm.py