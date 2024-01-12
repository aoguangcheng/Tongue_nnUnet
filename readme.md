# 声明
本项目基于[nnUNet](https://github.com/MIC-DKFZ/nnUNet)开发
# 配置环境
参照 [nnUNet README](./nnunet_readme.md)和[install_instruction](./documentation/installation_instructions.md)安装环境,
### 创建环境
### 安装pytorch
一定要先安装pytorch,同时注意nnunetv2、pytorch、cudnn、cuda、GPU驱动和GPU型号之间的对应关系。
- 查看nnunetv2依赖的版本
安装依赖检查工具，并查看依赖树
```
pip install pipdeptree
pipdeptree -p nnunetv2
```
按照所有的包的依赖版本手动处理，如果自动安装不行的话

nnunetv2有三个位置直接或者间接依赖pytorch，很明显，这里至少要pytorch 2.0.0
```
├── dynamic-network-architectures [required: >=0.2, installed: 0.2]
│   ├── numpy [required: Any, installed: 1.26.3]
│   └── torch [required: >=1.6.0a, installed: 2.1.2]

├── torch [required: >=2.0.0, installed: 2.1.2]

│   ├── SimpleITK [required: Any, installed: 2.3.1]
│   └── torch [required: Any, installed: 2.1.2]
```
安装 pytorch 2.0.0至少要cuda 11.7以上，[pytorch官网](https://pytorch.org/get-started/previous-versions/)上可以查看pytorch和cuda对应的版本
``` 
pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1
```
安装cuda 11.7至少要GPU驱动版本大于450.80.02，[英伟达官网](https://pytorch.org/get-started/previous-versions/)上可以查看cuda版本和GPU驱动版本的对应关系
同时查看设备的GPU驱动版本：
```
(tongue) guangcheng@ps:~/tongue_seg_nnUnet$ nvidia-smi
Fri Jan 12 09:49:25 2024       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 455.28       Driver Version: 455.28       CUDA Version: 11.1   
```
上述流程对推理环境也适用
### 安装nnunetv2
接下来安装nnunetv2，就不会因为已经安装的pytorch版本不满足需求，从而默认安装最新版本的pytorch了，
如果pytorch版本满足nnunetv2的需求，就继续使用已有conda环境下的pip包，
否则，重新解析nnunetv2依赖的pytorch等其他的包，
比如下面的代码，安装nnunetv2的时候显示的本次安装中安装的所有的包，并没有安装pytorch，因为在上一个步骤中已经安装了合适的pytorch。
```
Successfully installed SimpleITK-2.3.1 acvl-utils-0.2 argparse-1.4.0 batchgenerators-0.25 connected-components-3d-3.12.4 dicom2nifti-2.4.9 dynamic-network-architectures-0.2 graphviz-0.20.1 linecache2-1.0.0 nibabel-5.2.0 nnunetv2-2.2.1 pydicom-2.4.4 python-gdcm-3.0.23 traceback2-1.4.0 unittest2-1.1.0 yacs-0.1.8
```
pip 的解析策略也比较草率，默认安装最新的pytorch版本，很明显已有的GPU驱动不支持，
一包茶叶一包烟，一个环境配一天。
```
pip install nnunetv2
pip install -e .
```

## 设置工作目录
运行脚本[set_env.sh](./set_env.sh)设置工作目录：
```
source set_env.sh
```
# 数据集准备
## 数据集转换文件存储结构
其实png文件只是单纯的转换了文件夹的名字和存储位置，是为了方便后续的处理；
所有标注完成的样本的输入和标签必须一样的文件名，分别放在 **/mnt/data/guangcheng/tongue_seg_nnUnet/TongeImageDataset/training/origin_GT** 和 **/mnt/data/guangcheng/tongue_seg_nnUnet/TongeImageDataset/training/origin_Image**文件夹下面；然后执行数据集转换的脚本，
```
python ./nnunetv2/dataset_conversion/Dataset099_Tongue.py
```

脚本的位置在 **/mnt/data/guangcheng/tongue_seg_nnUnet/nnunetv2/dataset_conversion/Dataset099_Tongue.py**

处理结果保存在 **/mnt/data/guangcheng/tongue_seg_nnUnet/nnUNet_raw/Dataset099_Tongue**


## 数据集预处理
这一步骤是自动的根据不同的数据集自动的设计网络结构、参数等等
运行脚本：
```
nnUNetv2_plan_and_preprocess -d DATASET_ID --verify_dataset_integrity
```

举例：
```
nnUNetv2_plan_and_preprocess -d 99 --clean -c 2d -np 8
```
# 模型训练

参考[训练指引](./documentation/how_to_use_nnunet.md)有详细描述；
使用2D的方式训练，五折交叉验证，
数据集编号99
2d分割，需要手动选择，因为nnUNet也支持3D
五折交叉验证选择第0折
```
CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 99 2d 0   
```