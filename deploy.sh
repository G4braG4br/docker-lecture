#!/bin/bash
set -e

echo "Поднимаем виртуальную машину..."
vagrant up --provider=orbstack

echo "Генерируем динамический инвентарь (inventory.yml)..."

SSH_HOST=$(vagrant ssh-config | grep HostName | awk '{print $2}')
SSH_PORT=$(vagrant ssh-config | grep Port | awk '{print $2}')
KEY_PATH=$(vagrant ssh-config | grep IdentityFile | awk '{print $2}' | tr -d '"')

cat <<EOF > inventory.yml
all:
  hosts:
    local_vm:
      ansible_host: ${SSH_HOST}
      ansible_port: ${SSH_PORT}
      ansible_user: vagrant
      ansible_ssh_private_key_file: "${KEY_PATH}"
      ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
EOF

export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

echo "Запускаем Ansible Playbook..."
ansible-playbook -i inventory.yml ansible/playbook.yml