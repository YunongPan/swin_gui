# DemoSens Training Process
This repo contains a GUI to facilitate the use of [Swin-Transformer-Object-Detection](https://github.com/SwinTransformer/Swin-Transformer-Object-Detection), which is based on [mmdetection](https://github.com/open-mmlab/mmdetection). And the training process, from the labeling of images to the test after the training, will be simply introduced. 

## 1. Labeling
### 1.1. Installation
Please see [labelme](https://github.com/wkentaro/labelme) repo to set up a conda environment and install it.
### 1.2. Resize Image
Before starting to label the image, it is recommended to use some simple code as follows to resize the image, which is too large, to make the file size smaller. This can effectively avoid problems caused by insufficient GPU memory during training.

```
# python
from PIL import Image

image = Image.open('SAMPLE.jpg')
new_image = image.resize((2400, 1600))
new_image.save('SAMPLE_resize.jpg')
```
###1.3. Labeling
Please refer to the Labelme repo to label the image, the labelled data will be saved as a .json file.

It is recommended not to check File-->Save with image data during labeling. 
![image](https://raw.githubusercontent.com/YunongPan/readme_add_pic/main/labelme_1.png)
## 2. Augmentation with CLoDSA

### 2.1. Installation
Please see [CLoDSA](https://github.com/joheras/CLoDSA).
### 2.2. Using
Please see [
Augmentation_CLODSA](https://git.rwth-aachen.de/mobile-robotics/demosens/augmentation/augmentation_clodsa) and clone it.

Some other tips:
1. You may put all the labelled images and corresponding .json files into the labelme_all folder. This folder is like a "Waiting Room" to just make the next steps more convenient.
2. Easily copy and paste the images that need to be augmented, and their corresponding .json files from the labelme_all folder into the label folder.
3. Please don't forget to modify labels.txt to match your labels.
4. Delete the entire input_augmentation folder, and the contents of the output_augmentation and output_augmentation2 folders.
5. Run `python labelme2coco.py label/ input_augmentation/ --labels labels.txt --ann annotations`
6. Open the generated input_augmentation folder, and cut all the images in the images folder, and the annotations.json file in the annotations folder, to the previous directory. It means, put them directly into the input_augmentation folder.
7. Open annotations.json, carefully find all "file_names", delete all "../images/", and only keep the part of "SAMPLE.jpg". Like follows:
![image](https://raw.githubusercontent.com/YunongPan/readme_add_pic/main/clodsa_1.png)
8. Run `python clodsa_1.py`, the generated pictures and annotations.json are in the output_augmentation folder.
9. If it is not enough, run `python clodsa_2.py`, and the generated pictures and annotations.json are in the output_augmentation2 folder. 


##3. Training with GUI
###3.1.Installation 

1. Please set up the environment refer to  [get_started.md](https://github.com/open-mmlab/mmdetection/blob/master/docs/get_started.md) before starting to install mmdetection. it is recommended to create a conda virtual environment and activate it. 
    ```
   conda create -n swin_gui python=3.7 -y
   conda activate swin_gui
    ```
2. It is important to confirm that all package versions match each other! The matching sequence is: GPU + system→CUDA Toolkit→PyTorch→mmcv_full.
3. Here is some successful sequence:
   1. GPU Nvidia 3090→CUDA Toolkit 11.0→PyTorch 1.7.1→mmcv_full 1.3.1
   2. GPU Nvidia 1060→CUDA Toolkit 10.2→PyTorch 1.8.1→mmcv_full 1.3.9
4. Clone this repository and install mmdetection:
    ```
    git clone https://github.com/YunongPan/swin_gui.git
    cd swin_gui
    pip install -r requirements/build.txt
    python setup.py develop
    ```
###3.2. Create COCO data set
1. Create new folders:
    ```
   cd swin_gui
   mkdir data
   cd data
   mkdir coco
   cd coco
   mkdir annotations train2017 val2017 test2017
   ```
2. Create training data set:
   1. As described in Chapter 2.2, generate the output_augmentation folder (or output_augmentation2 folder).
   2. Find the "annotations.json" file in output_augmentation folder. Copy and paste it into /swin_gui/data/coco/annotations. Rename it to "instances_train2017.json"
   3. Copy and paste all the generated images in output_augmentation folder into /swin_gui/data/coco/train2017

3. Create valuation data set:
   1. Similarly, choose some other images to generate another output_augmentation folder (or output_augmentation2 folder).
   2. Find the "annotations.json" file in output_augmentation folder. Copy and paste it into /swin_gui/data/coco/annotations. Rename it to "instances_val2017.json"
   3. Copy and paste all the generated images in output_augmentation folder into /swin_gui/data/coco/val2017
4. Create test data set:
   1. Simply put some images to be tested into the /swin_gui/data/coco/test2017.

###3.3. Prepare a pretrained model
1. Create a new folder:
   ```
   cd swin_gui
   mkdir weights
   ```
2. See [Swin-Transformer-Object-Detection](https://github.com/SwinTransformer/Swin-Transformer-Object-Detection) to download a pretrained model. For example [moby_mask_rcnn_swin_tiny_patch4_window7_3x.pth](https://github.com/SwinTransformer/storage/releases/download/v1.0.3/moby_mask_rcnn_swin_tiny_patch4_window7_3x.pth) 
3. Put the pretrained model into swin_gui/weights

###3.4. Training with GUI
1. Start GUI:
   ```
   conda activate swin_gui
   cd swin_gui
   python swin_app.py
   ```
2. Set parameters:
   1. Click the "Set parameters" button.
   2. Select a config file from swin_gui/configs/swin, which is matching to the pretrained model. For example "mask_rcnn_swin_tiny_patch4_window7_mstrain_480-800_adamw_3x_coco.py" for [moby_mask_rcnn_swin_tiny_patch4_window7_3x.pth](https://github.com/SwinTransformer/storage/releases/download/v1.0.3/moby_mask_rcnn_swin_tiny_patch4_window7_3x.pth)
   3. Modify the "Names of classes". If there is only one class, there must be a comma in the "Names of classes" parameter. Such as: ('person',). If there are two or more classes, then just modify it like this: ('person','bicycle','car'). 
   4. Set "Number of classes" to match the "Name of classes".
   5. Set "Number of test images in dataset" to match the number of images in the /swin_gui/data/coco/test2017 folder.
   6. "Samples per GPU": Batch size of a single GPU
   7. "Workers per GPU": Worker to pre-fetch data for each single GPU
   8. Click "Apply" to change parameters.

3. Choose pretrained model from /swin_gui/weights
4. Select the same config file from swin_gui/configs/swin, which has been modified in step 2.
5. Click "Train" button to start training.

###3.5. Image test with GUI
1. Select the trained model from /swin_gui/work_dirs, the same config file, and the to be tested image (, which must be somewhere under /swin_gui). 
2. Click "Image Test" to start. 

###3.6. Video test with GUI
1. Select the trained model from /swin_gui/work_dirs, the same config file, and the to be tested video (, which must be somewhere under /swin_gui). 
2. Enter the file name of the resulting video.
3. Click "Video Test" to start.

###3.7. Other buttons
1. "Clear terminal": Clear the embedded terminal.
2. "Stop": Stop the current (training or testing) process.
3. "Stop and reset all": Stop the current (training or testing) process and initialize the GUI. But the parameters in config files will not be reset.

