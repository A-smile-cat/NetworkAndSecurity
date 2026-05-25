<p align="center">
  <h1 align="center">基于 DBSCAN 聚类的 k-匿名位置隐私保护算法</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Dataset-Geolife%20GPS-orange.svg" alt="Dataset">
</p>

---

## 目录

- [项目简介](#项目简介)
- [研究背景](#研究背景)
- [算法原理](#算法原理)
- [项目结构](#项目结构)
- [环境配置](#环境配置)
- [数据集准备](#数据集准备)
- [快速开始](#快速开始)
- [算法参数说明](#算法参数说明)
- [输出文件说明](#输出文件说明)
- [实验结果](#实验结果)
- [参考文献](#参考文献)

---

## 项目简介

本项目实现了一种基于 **DBSCAN 密度聚类**的 **k-匿名（k-anonymity）位置隐私保护算法**。算法将地理位置相近的轨迹点聚合为匿名集合，每个集合至少包含 k 个不同的位置点，并以簇中心坐标替代簇内所有点的真实位置（泛化处理），从而在保证数据可用性的前提下实现位置隐私保护。

本项目使用微软亚洲研究院发布的 **Geolife GPS Trajectory** 真实轨迹数据集进行实验验证。

---

## 研究背景

随着基于位置服务（Location-Based Services, LBS）的广泛应用，用户在享受便捷服务的同时，其位置隐私面临严重威胁。攻击者可通过连续的位置轨迹推断用户的家庭住址、工作单位、生活习惯等敏感信息。

**k-匿名模型**是位置隐私保护领域的经典方法：将至少 k 个不同用户的位置记录映射到同一个匿名区域中，使得攻击者无法以高于 1/k 的概率将某条记录关联到特定用户。本算法利用 DBSCAN 的密度聚类特性，将空间上邻近的位置点自然地归入同一簇，使匿名区域更符合真实的地理分布特征。

---

## 算法原理

### 核心思想

1. **DBSCAN 密度聚类**：对空间位置点执行 DBSCAN 聚类，将邻域半径（eps）内至少包含 k 个点的区域标记为一个簇。未被纳入任何簇的点视为噪声点，不参与匿名化处理。
2. **中心点泛化**：对每个簇计算所有成员点的几何中心（经纬度均值），将簇内所有点的原始坐标替换为该中心坐标。
3. **匿名区域标注**：每个簇的包围矩形即为匿名区域，簇内成员数即为该区域的匿名度。

### 算法流程

```
原始轨迹数据 → 随机采样 → DBSCAN 聚类 → 噪声点过滤 → 中心点泛化 → 匿名化结果
```

详细步骤：

| 步骤 | 描述 |
|:---:|------|
| 1 | 加载格式化后的 Geolife 轨迹数据 |
| 2 | 从全量数据中随机抽取 n 条记录作为实验样本 |
| 3 | 基于经纬度坐标执行 DBSCAN 聚类，`min_samples=k` 确保每个簇包含 ≥k 个点 |
| 4 | 过滤噪声点（cluster_id = -1），仅保留满足 k-匿名约束的簇 |
| 5 | 将簇内每个点的经纬度替换为簇中心坐标，完成泛化处理 |
| 6 | 可视化对比原始位置与匿名化位置，标注每个匿名区域的覆盖人数 |

---

## 项目结构

```
k匿名位置隐私保护算法/
├── main.py                              # 主程序：k-匿名算法实现与可视化
├── dataPro.py                           # 数据预处理：Geolife 原始数据 → CSV 格式
├── Figure_1.png                         # 实验结果可视化图 1
├── Figure_2.png                         # 实验结果可视化图 2
├── Figure_3.png                         # 实验结果可视化图 3
├── anonymized_results_1000.csv          # 1000 条样本的匿名化结果
├── anonymized_results_10000.csv         # 10000 条样本的匿名化结果
├── cluster_info_1000.csv                # 1000 条样本的聚类信息
├── cluster_info_10000.csv               # 10000 条样本的聚类信息
├── random_res_1000.csv                  # 随机抽取的 1000 条样本数据
├── random_res_10000.csv                 # 随机抽取的 10000 条样本数据
├── Geolife Trajectories 1.3/            # 原始数据集（未上传至仓库，见数据集准备）
│   └── Data/                            # 182 位用户的 GPS 轨迹数据
│       ├── 000/
│       │   └── Trajectory/              # .plt 轨迹文件
│       ├── 001/
│       │   └── Trajectory/
│       └── ...
└── README.md
```

---

## 环境配置

### 运行环境

- **Python** 3.8 及以上
- **操作系统**：Windows / macOS / Linux

### 依赖安装

```bash
pip install numpy pandas matplotlib scikit-learn tqdm
```

或使用 requirements 文件：

```bash
pip install -r requirements.txt
```

### 依赖列表

| 依赖包 | 版本要求 | 用途 |
|--------|---------|------|
| numpy | ≥ 1.20 | 数值计算 |
| pandas | ≥ 1.3 | 数据处理与 CSV 读写 |
| matplotlib | ≥ 3.4 | 结果可视化 |
| scikit-learn | ≥ 0.24 | DBSCAN 聚类算法 |
| tqdm | ≥ 4.60 | 数据预处理进度条 |

---

## 数据集准备

本项目使用 **Geolife GPS Trajectory** 数据集（微软亚洲研究院发布），包含 182 名用户在 5 年间采集的 17,621 条 GPS 轨迹，总计约 2,500 万条位置记录。

### 下载

> ⚠️ 原始数据集约 1.6GB，格式化后的 CSV 文件约 1.1GB，因体积过大未上传至本仓库。

**官方下载地址**：

[Geolife GPS Trajectory Dataset - Microsoft Research](https://www.microsoft.com/en-us/research/publication/geolife-gps-trajectory-dataset-user-guide/)

### 数据预处理

1. 下载后解压，将 `Geolife Trajectories 1.3/` 文件夹放置于项目根目录下。
2. 运行数据预处理脚本，将原始 `.plt` 轨迹文件转换为统一格式的 CSV：

```bash
python dataPro.py
```

该脚本将遍历所有用户文件夹（000–181），解析每个 `.plt` 文件，提取经度、纬度、时间戳，输出 `geolife_formatted.csv`。预处理过程约需数分钟，具体耗时取决于磁盘性能。

### 数据格式

**geolife_formatted.csv 字段说明**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| user_id | int | 用户编号（0–181） |
| longitude | float | 经度（WGS-84 坐标系） |
| latitude | float | 纬度（WGS-84 坐标系） |
| timestamp | str | 时间戳（格式：YYYY-MM-DD HH:MM:SS） |

---

## 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:A-smile-cat/NetworkAndSecurity.git
cd "NetworkAndSecurity/k匿名位置隐私保护算法"
```

### 2. 准备数据

参照 [数据集准备](#数据集准备) 下载数据集并运行预处理，确保项目根目录下存在 `geolife_formatted.csv`。

### 3. 运行算法

```bash
python main.py
```

程序默认从 `geolife_formatted.csv` 中随机抽取 **10,000** 条记录，以 **k=5、eps=0.1** 的参数执行匿名化处理，并弹出可视化窗口对比原始位置与匿名化结果。

### 4. 查看结果

运行结束后，将在项目目录下生成以下文件：

- `anonymized_results_10000.csv` — 匿名化后的位置数据
- `cluster_info_10000.csv` — 聚类信息（簇 ID、成员数、包围矩形、中心坐标）
- `random_res_10000.csv` — 本次随机采样的原始数据
- 可视化窗口展示原始位置与匿名化位置的对比图

---

## 算法参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `k` | 5 | 最小匿名集大小。k 值越大，隐私保护强度越高，但数据可用性越低，不满足 k-匿名约束的点（噪声点）越多 |
| `eps` | 0.1 | DBSCAN 邻域半径（单位：度）。值越大，聚类覆盖范围越广，单个簇包含的点越多 |
| `n` | 10000 | 随机采样数量。可修改 `df.sample(n=...)` 调整 |
| `random_state` | 22 | 随机种子，用于实验可复现 |

### 参数调节建议

- **k=3~5**：隐私保护强度较低，数据利用率高，适合隐私要求一般的场景。
- **k=10~20**：隐私保护强度较高，部分稀疏区域的点可能被归为噪声。
- **eps=0.01~0.05**：适合城市密集区域，生成较小但紧凑的匿名区域。
- **eps=0.1~0.5**：适合大范围稀疏区域，匿名区域覆盖范围较大。

---

## 输出文件说明

### anonymized_results_\*.csv

匿名化后的位置数据，每条记录包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| user_id | int | 用户编号 |
| original_lon | float | 原始经度 |
| original_lat | float | 原始纬度 |
| anonymized_lon | float | 匿名化经度（簇中心经度） |
| anonymized_lat | float | 匿名化纬度（簇中心纬度） |
| timestamp | str | 时间戳 |
| cluster_id | int | 所属簇编号 |

### cluster_info_\*.csv

聚类信息汇总，每个簇一条记录：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| cluster_id | int | 簇编号 |
| count | int | 簇内成员数量 |
| area | list | 匿名区域包围矩形 [min_lon, min_lat, max_lon, max_lat] |
| center | list | 簇中心坐标 [center_lon, center_lat] |

---

## 实验结果

以下为 k=5、eps=0.1、采样量 n=10000 条件下的实验结果示例：

### 原始位置数据 vs k-匿名化结果

| 指标 | 数值 |
|------|------|
| 采样点总数 | 10,000 |
| 有效聚类数 | — |
| 满足 k-匿名的点数 | — |
| 噪声点数（未满足 k-匿名） | — |
| 匿名化覆盖率 | — |

> 运行 `python main.py` 可获得完整的实验数据与可视化图表。

---

## 参考文献

1. Sweeney, L. (2002). *k-Anonymity: A Model for Protecting Privacy*. International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, 10(5), 557–570.
2. Ester, M., Kriegel, H. P., Sander, J., & Xu, X. (1996). *A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise*. KDD'96, 226–231.
3. Zheng, Y., Zhang, L., Xie, X., & Ma, W. Y. (2009). *Mining Interesting Locations and Travel Sequences from GPS Trajectories*. WWW'09, 791–800.
4. 郭辉, 王璐, 等. 基于聚类的位置隐私保护研究综述. 计算机科学, 2019.

---

## License

本项目仅供学习与研究使用。数据集 Geolife GPS Trajectory 遵循其原始发布方的使用协议。
