#!/bin/bash

# Solicitar o nome do usuário como entrada
echo "Por favor, digite o nome do usuário:"
read user


sudo apt update
# Baixar git
sudo apt install git -y
# Clonar o repositório
echo "Clonando o repositório..."
git clone https://github.com/nicolasyassuda/scaling-view.git /home/$user/scaling-view

# Garantir que o Python esteja atualizado
echo "Atualizando o Python..."
sudo apt update
sudo apt install -y python3 python3-pip

# Atualizar pip
echo "Atualizando pip..."
sudo python3 -m pip install --upgrade pip

# Instalar as bibliotecas Python necessárias
echo "Instalando as dependências Python..."
sudo python3 -m pip install --break-system-packages blinkt kubernetes

# Criar o arquivo de serviço systemd
echo "Criando o arquivo de serviço systemd..."

cat <<EOF | sudo tee /etc/systemd/system/scaling-view.service
[Unit]
Description=Mostrador via leds quantos pods estão rodando dentro do nó de determinado deployment.
After=network.target

[Service]
Type=simple
User=$user
Group=$user
ExecStart=/usr/bin/python3 /home/$user/scaling-view/scaling-view.py
Restart=always
RestartSec=10
Environment=KUBECONFIG=~/kubeconfig

[Install]
WantedBy=multi-user.target
EOF

# Ativar e iniciar o serviço systemd
echo "Ativando e iniciando o serviço systemd..."
sudo systemctl daemon-reload
sudo systemctl enable scaling-view.service
sudo systemctl start scaling-view.service

# Status do serviço
echo "Verificando o status do serviço..."
sudo systemctl status scaling-view.service
