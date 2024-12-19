import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def calculate_statistics(depth_images_folder):
    # 获取文件夹中的所有图像文件
    image_files = [f for f in os.listdir(depth_images_folder) if f.endswith('.png') or f.endswith('.jpg')]
    
    # 假设图像大小一致，读取第一张图像来获取尺寸
    first_image = cv2.imread(os.path.join(depth_images_folder, image_files[0]), cv2.IMREAD_UNCHANGED)
    image_shape = first_image.shape
    
    # 将图像堆叠成一个NumPy数组
    depth_images = np.zeros((len(image_files), *image_shape), dtype=np.uint16)

    for i, image_file in enumerate(image_files):
        image_path = os.path.join(depth_images_folder, image_file)
        depth_images[i] = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # 计算每个像素的均值和标准差
    mean_image = np.mean(depth_images, axis=0)
    std_image = np.std(depth_images, axis=0)

    # 计算每个像素的最大值和最小值
    max_image = np.max(depth_images, axis=0)
    min_image = np.min(depth_images, axis=0)

    # 计算 max - min 的差值
    range_image = max_image - min_image

    return mean_image, std_image, range_image

def plot_images(mean_image, std_image, range_image):
    # 显示均值图，方差图和最大最小差值图
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 显示均值图
    im0 = axes[0].imshow(mean_image, cmap='jet')
    axes[0].set_title('Mean Depth Image')
    axes[0].axis('off')
    fig.colorbar(im0, ax=axes[0], orientation='vertical')

    # 显示方差图
    im1 = axes[1].imshow(std_image, cmap='jet')
    axes[1].set_title('Std Depth Image')
    axes[1].axis('off')
    fig.colorbar(im1, ax=axes[1], orientation='vertical')

    # 显示最大最小差值图
    im2 = axes[2].imshow(range_image, cmap='jet')
    axes[2].set_title('Max - Min Range Image')
    axes[2].axis('off')
    fig.colorbar(im2, ax=axes[2], orientation='vertical')

    plt.tight_layout()
    plt.show()

def main():
    depth_images_folder = '/home/vision/projects/jiazhu_linux/captured_depth_images'  
    mean_image, std_image, range_image = calculate_statistics(depth_images_folder)
    plot_images(mean_image, std_image, range_image)

if __name__ == "__main__":
    main()
