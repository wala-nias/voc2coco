import os 
import random 
import shutil 
import xml.etree.ElementTree as ET

def rename(input_dir):
    filenames = os.listdir(os.path.join(input_dir, 'images'))
    counter = 0
    for f in filenames:
        #rename image file 
        os.rename(os.path.join(input_dir, 'images', f), os.path.join(input_dir, 'images', '.'.join((str(counter), 'jpg'))))
        #edit corresponding annotation file
        xmlf = os.path.join(input_dir, 'annotations', '.'.join((os.path.splitext(f)[0], 'xml')))
        et = ET.parse(xmlf)
        rt = et.getroot()
        text = rt.find('filename').text
        rt.find('filename').text = rt.find('filename').text.replace(text,  "{}.{}".format(str(counter), 'jpg'))
        et.write(xmlf)
        #rename annoatation file 
        os.rename(xmlf, os.path.join(input_dir, 'annotations', '.'.join((str(counter), 'xml'))))
        counter += 1 
        

def split(input_dir):
    filenames = os.listdir(os.path.join(input_dir, 'images'))
    filenames.sort()
    random.seed(230)
    random.shuffle(filenames)
    split_1 = int(0.8 * len(filenames))
    split_2 = int(0.9 * len(filenames))
    return filenames[:split_1], filenames[split_1:split_2], filenames[split_2:]


def move(lst, input_dir, img_dest, annot_dest):
    for f in lst:
        print(os.path.join(input_dir, 'annotations', '.'.join((os.path.splitext(f)[0], 'xml'))))
        try:
            #move images
            shutil.copy(os.path.join(input_dir, 'images', f), img_dest)
            #move annotations
            print('image moved')
            shutil.copy(os.path.join(input_dir, 'annotations', '.'.join((os.path.splitext(f)[0], 'xml'))), annot_dest)
            print('annotation moved')
        except Exception as e:
            print("File couldn't be moved: ", os.path.splitext(f)[0], e)
        
if __name__ =='__main__':
    dataset = "/home/ec2-user/SageMaker/DL4CV_brand_blurring/dataset"
    #rename(dataset)
    train_filenames, val_filenames, test_filenames = split(dataset)
    
    original_umask = os.umask(0)
    
    print("Starting moving training set...")
    train_img_dest = "/home/ec2-user/SageMaker/DL4CV_brand_blurring/splitted_dataset/logos/train/images"
    train_annot_dest = "/home/ec2-user/SageMaker/DL4CV_brand_blurring/splitted_dataset/logos/train/annotations"
    os.makedirs(train_img_dest, 0o777)
    os.makedirs(train_annot_dest, 0o777)
    move(train_filenames, dataset, train_img_dest, train_annot_dest)
    print("Moving of training set completed !!")
                      
    print("Starting moving validation set...")
    val_img_dest = "/home/ec2-user/SageMaker/DL4CV_brand_blurring/splitted_dataset/logos/val/images"
    val_annot_dest = "/home/ec2-user/SageMaker/DL4CV_brand_blurring/splitted_dataset/logos/val/annotations"
    os.makedirs(val_img_dest, 0o777)
    os.makedirs(val_annot_dest,0o777)
    move(val_filenames, dataset, val_img_dest, val_annot_dest)
    print("Moving of training set completed !!")             
    
    print("Starting moving test set...")
    test_img_dest = "/home/ec2-user/SageMaker/DL4CV_brand_blurring/splitted_dataset/logos/test/images"
    test_annot_dest = "/home/ec2-user/SageMaker/DL4CV_brand_blurring/splitted_dataset/logos/test/annotations"
    os.makedirs(test_img_dest, 0o777)
    os.makedirs(test_annot_dest, 0o777)
    move(test_filenames, dataset, test_img_dest, test_annot_dest)
    print("Moving of test set completed !!")
    
    os.umask(original_umask)