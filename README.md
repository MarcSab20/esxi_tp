
## Table des Matières
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Fonctionnalités](#fonctionnalités)
- [Explication et difficulté](#Explication)
- [Auteur](#Auteur)

# ESXi Automation Scripts

Scripts Python pour l'automatisation des tâches VMware ESXi utilisant PyVmomi.
FOTSO NANA

## installation

déployer automatiquement plusieurs instances d'une machine virtuelle à partir d'un fichier OVA. Fonctionnalités :
- Déploiement multiple en parallèle
- Personnalisation du nom des VMs
- Vérification des ressources (datacenter, datastore, cluster)
- Suivi du statut de déploiement

Création de VM (create_vm.py) [En développement]

Script pour créer des VMs from scratch. Actuellement en développement avec les fonctionnalités suivantes :
- Création basique de VM  À venir
- Configuration mémoire et CPU  À venir
   
Difficultés rencontrées
Installation et Configuration ESXi
- L'installation de l'ESXi nécessite une attention particulière aux compatibilités matérielles
- La configuration réseau initiale peut être délicate, notamment pour :
- La configuration des VLANs
- La mise en place du management network
- L'activation de SSH pour l'administration à distance et des protocoles Tlsv1..

Création de disques virtuels
La gestion des disques virtuels avec PyVmomi s'est révélée complexe 

Documentation PyVmomi

Bien que la documentation de PyVmomi soit structurée, plusieurs défis ont été rencontrés :
- Exemples limités pour certains cas d'usage
- Complexité de l'API VMware vSphere sous-jacente
- L'apprentissage doit être plus long. les premiers pas avec pyVmomi étaient difficile

Liens utiles
- Documentation officielle PyVmomi
- Documentation API vSphere
- Exemples PyVmomi

En cours de développement


## Prérequis

- Python 3.x
- PyVmomi
- Accès à un serveur ESXi

## Fonctionnalités

- Déploiement d'OVA
- Clonage de VMs
- Création de VMs from scratch (en cours)




 
