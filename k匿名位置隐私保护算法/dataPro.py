import os
import pandas as pd
from tqdm import tqdm  # 进度条工具，可选安装


def convert_geolife_to_csv(data_root, output_file):
    """
    将GeoLife数据集转换为标准CSV格式
    :param data_root: GeoLife的Data文件夹路径 (e.g., "Geolife Trajectories 1.3/Data")
    :param output_file: 输出CSV文件路径 (e.g., "geolife_formatted.csv")
    """
    records = []

    # 遍历所有用户文件夹 (000, 001, ..., 181)
    user_folders = sorted([f for f in os.listdir(data_root) if f.isdigit()])

    for user_id in tqdm(user_folders, desc="Processing users"):
        traj_dir = os.path.join(data_root, user_id, "Trajectory")
        if not os.path.exists(traj_dir):
            continue

        # 处理该用户的所有轨迹文件
        for traj_file in os.listdir(traj_dir):
            if not traj_file.endswith('.plt'):
                continue

            with open(os.path.join(traj_dir, traj_file), 'r') as f:
                lines = f.readlines()[6:]  # 跳过前6行文件头
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) < 7:
                        continue
                    lon, lat, _, _, _, date, time = parts[:7]
                    timestamp = f"{date} {time}"
                    records.append({
                        'user_id': int(user_id),
                        'longitude': float(lon),
                        'latitude': float(lat),
                        'timestamp': timestamp
                    })

    # 保存为CSV
    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)
    print(f"转换完成！共处理 {len(user_folders)} 个用户，{len(records)} 条记录。")

if __name__ == '__main__':
    convert_geolife_to_csv(
        data_root="Geolife Trajectories 1.3/Data",
        output_file="geolife_formatted.csv"
    )
