#!/bin/bash
# Requisitos
apt install sudo 
apt install hdparm -y
# Função para imprimir uma linha de separação
print_separator() {
  printf -- "========================================\n"
}

# Definir cores
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sem cor

# Verifica a distribuição e a versão do Linux instalado
echo -e "${CYAN}Distribuição e versão do Linux instalado:${NC}"
#lsb_release -a
cat /etc/os-release | grep NAME=
cat /etc/os-release | grep VERSION=
print_separator

# Verifica se a unidade de armazenamento é HDD ou SSD
storage_type=$(cat /sys/block/sda/queue/rotational)
storage_label=""
if [[ $storage_type == "1" ]]; then
  storage_label="${YELLOW}HDD${NC}"
else
  storage_label="${GREEN}SSD${NC}"
fi
echo -e "${CYAN}Tipo de unidade de armazenamento:${NC} $storage_label"
print_separator

# Lista as unidades de armazenamento com o df -h
echo -e "${CYAN}Unidades de armazenamento:${NC}"
df -h
print_separator

# Realiza o teste de velocidade de leitura da unidade de armazenamento
echo -e "${CYAN}Teste de velocidade de leitura:${NC}"
sudo hdparm -Tt /dev/sda
print_separator

# Realiza o teste de velocidade de escrita da unidade de armazenamento
echo -e "${CYAN}Teste de velocidade de escrita:${NC}"
dd if=/dev/zero of=/tmp/testfile bs=1M count=1000 conv=fsync
print_separator

# Verifica as informações de memória RAM
echo -e "${CYAN}Informações de memória RAM:${NC}"
awk '/MemTotal/ {total=$2/1024/1024} /MemFree/ {free=$2/1024/1024} /MemAvailable/ {available=$2/1024/1024} /SwapTotal/ {swap_total=$2/1024/1024} /SwapFree/ {swap_free=$2/1024/1024} END {printf "Total: %.2f GB\nEm uso: %.2f GB\nDisponível: %.2f GB\nSwap Total: %.2f GB\nSwap Free: %.2f GB\n", total, (total - free), available, swap_total, swap_free}' /proc/meminfo
print_separator

# Verifica informações do CPU
echo -e "${CYAN}Informações do CPU:${NC}"
echo -ne "${CYAN}Nome do modelo do CPU:${NC} "
cat /proc/cpuinfo | grep "model name" | head -n 1 | awk -F ': ' '{print $2}'
echo -ne "${CYAN}Quantidade de Cores do CPU:${NC} "
grep "cpu cores" /proc/cpuinfo | uniq | awk -F ': ' '{print $2}'
echo -ne "${CYAN}Quantidade de Threads do CPU:${NC} "
grep "siblings" /proc/cpuinfo | uniq | awk -F ': ' '{print $2}'
print_separator