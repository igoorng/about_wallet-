
## 脚本功能
```
生成指定数量的evm钱包，钱包保存在当前目录下，生成两个文件，一个txt文件，一个excel文件。
```

## 脚本使用可以使用conda创建虚拟环境
### 创建conda基础环境
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
source ~/miniconda3/bin/activate
```
### 使用conda创建虚拟环境
```
conda create -n web3 python=3.10
```
## 激活虚拟环境
```
conda activate web3
```
## 脚本安装ubuntu系统依赖
```
# 在linux上使用，需要安装gcc，以下命令使用的是ubuntu
apt install build-essential gcc
```
## 脚本安装python所需要的库
```
pip install pandas mnemonic solana bip-utils openpyxl
```
## 执行脚本
```
python generate_solana_wallet.py
```
