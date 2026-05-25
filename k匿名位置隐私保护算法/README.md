# k匿名位置隐私保护算法

基于 DBSCAN 聚类的 k-匿名位置隐私保护算法实现，使用 Geolife GPS 轨迹数据集进行实验验证。

## 算法原理

该算法通过 DBSCAN 密度聚类将地理位置相近的点分组为匿名集，每个集合至少包含 k 个点，然后用簇中心点代替簇内所有点的真实位置（泛化处理），从而实现位置隐私保护。

- **k 值**：最小匿名集大小，k 值越大隐私保护强度越高，但数据可用性越低
- **eps**：DBSCAN 邻域半径（单位：度），控制聚类的空间范围

## 项目结构

```
├── main.py                          # 主程序：k匿名算法实现与可视化
├── dataPro.py                       # 数据预处理：Geolife原始数据转CSV格式
├── Figure_1.png                     # 运行结果图1
├── Figure_2.png                     # 运行结果图2
├── Figure_3.png                     # 运行结果图3
├── anonymized_results_1000.csv      # 1000条样本的匿名化结果
├── anonymized_results_10000.csv     # 10000条样本的匿名化结果
├── cluster_info_1000.csv            # 1000条样本的聚类信息
├── cluster_info_10000.csv           # 10000条样本的聚类信息
├── random_res_1000.csv              # 随机抽取的1000条样本数据
├── random_res_10000.csv             # 随机抽取的10000条样本数据
└── Geolife Trajectories 1.3/        # 原始数据集（未上传，见下方说明）
```

## 数据集

本项目使用 **Geolife GPS Trajectory** 数据集，由微软亚洲研究院发布。

> ⚠️ 由于原始数据集体积过大（约 1.6GB），未上传至本仓库。如需运行完整实验，请从以下地址下载：
>
> **下载地址**：https://www.microsoft.com/en-us/research/publication/geolife-gps-trajectory-dataset-user-guide/

下载后将 `Geolife Trajectories 1.3/` 文件夹放置于项目根目录下，然后运行数据预处理：

```bash
python dataPro.py
```

这将生成 `geolife_formatted.csv` 文件（约 1.1GB）。

## 使用方法

### 环境依赖

```bash
pip install numpy pandas matplotlib scikit-learn tqdm
```

### 运行

```bash
python main.py
```

程序将从 `geolife_formatted.csv` 中随机抽取 10000 条记录，执行 k=5 的匿名化处理，并可视化对比原始位置与匿名化结果。

## 算法流程

1. **数据加载**：读取格式化后的 Geolife 轨迹数据
2. **随机采样**：从全量数据中抽取样本
3. **DBSCAN 聚类**：基于空间密度将位置点聚类，`min_samples=k` 确保每个簇至少包含 k 个点
4. **泛化处理**：将簇内所有点的经纬度替换为簇中心坐标
5. **结果可视化**：对比展示原始位置与匿名化位置，标注每个匿名区域的覆盖人数
