


# 有几张标签标注反了，手动处理一下
def img_invert():
    import cv2 as opencv
    import os
    filelists = ["266.png", "278.png", "284.png"]
    path = "./TongeImageDataset/origin_GT"
    for filename in filelists:
        if(os.path.exists(path=os.path.join(path, filename)) is False):
            print("file is not existed", os.path.join(path, filename))
        img = opencv.imread(os.path.join(path, filename), opencv.IMREAD_GRAYSCALE)
        img_invert = opencv.bitwise_not(img)
        opencv.imwrite("./" + filename, img_invert)
        

def cuda_test():
    import torch
    a = torch.ones(100, 100)
    b = torch.ones(100, 100)
    a = a.to(torch.device("cuda:1"))
    b = b.to(torch.device("cuda:1"))
    c = a + b
    print(c.mean())


if __name__ == "__main__":
    # img_invert()
    cuda_test()