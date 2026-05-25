import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from datetime import datetime
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签SimHei
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号


class KAnonymityLocationProtection:
    def __init__(self, k=5, eps=0.03):
        """
        :param k: 最小匿名集大小
        :param eps: DBSCAN邻域半径(度)
        """
        self.k = k
        self.eps = eps

    def anonymize(self, df):
        """
        对包含位置信息的DataFrame进行k匿名处理
        :param df: 包含['user_id', 'longitude', 'latitude', 'timestamp']的DataFrame
        :return: 匿名化后的DataFrame和聚类信息
        """
        # 提取坐标点
        points = df[['longitude', 'latitude']].values

        # 执行DBSCAN聚类
        clustering = DBSCAN(eps=self.eps, min_samples=self.k).fit(points)

        # 初始化结果存储
        anonymized_data = []
        cluster_info = []

        for cluster_id in set(clustering.labels_):
            if cluster_id == -1:  # 噪声点，不满足k匿名
                continue

            # 获取当前簇的所有点和索引
            cluster_mask = (clustering.labels_ == cluster_id)
            cluster_points = points[cluster_mask]
            cluster_indices = np.where(cluster_mask)[0]

            # 计算簇的统计信息
            min_lon, max_lon = np.min(cluster_points[:, 0]), np.max(cluster_points[:, 0])
            min_lat, max_lat = np.min(cluster_points[:, 1]), np.max(cluster_points[:, 1])
            center_lon, center_lat = np.mean(cluster_points[:, 0]), np.mean(cluster_points[:, 1])

            # 存储聚类信息
            cluster_info.append({
                'cluster_id': cluster_id,
                'count': len(cluster_points),
                'area': [min_lon, min_lat, max_lon, max_lat],
                'center': [center_lon, center_lat],
                'indices': cluster_indices
            })

            # 对簇内所有点使用中心点代替(泛化处理)
            for idx in cluster_indices:
                anonymized_data.append({
                    'user_id': df.iloc[idx]['user_id'],
                    'original_lon': df.iloc[idx]['longitude'],
                    'original_lat': df.iloc[idx]['latitude'],
                    'anonymized_lon': center_lon,
                    'anonymized_lat': center_lat,
                    'timestamp': df.iloc[idx]['timestamp'],
                    'cluster_id': cluster_id
                })

        # 转换为DataFrame
        anonymized_df = pd.DataFrame(anonymized_data)

        return anonymized_df, cluster_info

    def visualize(self, original_df, anonymized_df, cluster_info, zoom_bbox=None):
        """
        可视化原始数据与匿名化结果
        :param original_df: 原始数据DataFrame
        :param anonymized_df: 匿名化后DataFrame
        :param cluster_info: 聚类信息
        :param zoom_bbox: 可选，[min_lon, min_lat, max_lon, max_lat]缩放区域
        """
        plt.figure(figsize=(15, 6))

        # 子图1: 原始数据
        plt.subplot(121)
        plt.scatter(original_df['longitude'], original_df['latitude'],
                    c='blue', s=10, alpha=0.5, label='原始位置')
        plt.title('原始位置数据')
        plt.xlabel('经度')
        plt.ylabel('纬度')
        plt.grid(True)

        # 子图2: 匿名化结果
        plt.subplot(122)
        # 绘制匿名区域矩形
        for cluster in cluster_info:
            min_lon, min_lat, max_lon, max_lat = cluster['area']
            rect = plt.Rectangle((min_lon, min_lat),
                                 max_lon - min_lon, max_lat - min_lat,
                                 fill=False, edgecolor='red', linewidth=1)
            plt.gca().add_patch(rect)
            plt.text(cluster['center'][0], cluster['center'][1],
                     f"{cluster['count']}人", ha='center', va='center')

        # 绘制匿名化后的点
        plt.scatter(anonymized_df['anonymized_lon'], anonymized_df['anonymized_lat'],
                    c='red', s=10, alpha=0.7, label='匿名位置')

        # # 绘制原始点(半透明)
        # plt.scatter(original_df['longitude'], original_df['latitude'],
        #             c='blue', s=5, alpha=0.1)

        plt.title(f'k={self.k}匿名化结果')
        plt.xlabel('经度')
        plt.ylabel('纬度')
        plt.grid(True)
        plt.legend()

        # 如果指定了缩放区域
        if zoom_bbox:
            min_lon, min_lat, max_lon, max_lat = zoom_bbox
            for ax in plt.gcf().axes:
                ax.set_xlim(min_lon, max_lon)
                ax.set_ylim(min_lat, max_lat)

        plt.tight_layout()
        plt.show()

if __name__ == '__main__':

    # 从CSV文件读取数据
    df = pd.read_csv('geolife_formatted.csv')
    print(df)

    df = df.sample(n=10000, random_state=22)

    df.to_csv('random_res_10000.csv', index=False)  # 保存随机数据集，不保存行索引
    # 查看前5行
    print(df.head())

    # 初始化k匿名处理器
    kanon = KAnonymityLocationProtection(k=5, eps=0.1)

    # 执行匿名化
    anonymized_df, cluster_info = kanon.anonymize(df)

    # 可视化结果 (可以指定zoom_bbox参数放大特定区域)
    kanon.visualize(df, anonymized_df, cluster_info,zoom_bbox=[39, 115, 40.4, 118])

    # 查看匿名化结果
    print("\n匿名化结果示例:")
    print(anonymized_df.head())

    print("\n聚类信息示例:")
    print(cluster_info[0])

    # 存储匿名化结果
    anonymized_df.to_csv('anonymized_results_10000.csv', index=False, encoding='utf-8')

    # 存储聚类信息（需转换为DataFrame）
    cluster_df = pd.DataFrame(cluster_info)
    cluster_df.to_csv('cluster_info_10000.csv', index=False, encoding='utf-8')