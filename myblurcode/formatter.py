import os 
import xml.etree.ElementTree as ET
import shutil

def labelFilename(directory):
    for cat in os.listdir(directory):
        for brand in os.listdir(os.path.join(directory,cat)):
            for root, dirs, files in os.walk(os.path.join(directory, cat, brand)):
                if not files:
                    continue
                prefix = os.path.basename(root)
                for f in files:
                    if "checkpoint" in f:
                        print("Not file: ", os.path.join(directory, cat, brand, f))
                        continue
                    try:
                        if f.endswith('.xml'):
                            et = ET.parse(os.path.join(directory, cat, brand, f))
                            rt = et.getroot()
                            p = rt.find('path') #remove path tag 
                            if p is not None:
                                rt.remove(p)                            
                            et.write(os.path.join(directory, cat, brand, f))
                        os.rename(os.path.join(root, f), os.path.join(root, "{}_{}".format(prefix, f)))
                    except Exception as e:
                            print("File couldn't be processed: ", os.path.join(directory, cat, brand, f), e)
                        
#                             text = rt.find('filename').text
#                             rt.find('filename').text = rt.find('filename').text.replace(text,  "{}_{}".format(prefix, text))

def restructure(directory, images_dir, annot_dir):
    for cat in os.listdir(directory):
        for brand in os.listdir(os.path.join(directory,cat)):
            for root, dirs, files in os.walk(os.path.join(directory, cat, brand)):
                for f in files:
                    if "checkpoint" in f:
                        print("Not file: ", os.path.join(directory, cat, brand, f))
                        continue
                    if f.endswith('.xml'):
                        shutil.copy(os.path.join(directory, cat, brand, f), annot_dir) # move
                    else:
                        shutil.copy(os.path.join(directory, cat, brand, f), images_dir) # move
                        
if __name__ =='__main__':
    directory = "./logos"
    labelFilename(directory)
    
    images_dir = "/home/ec2-user/SageMaker/DL4CV_brand_blurring/dataset/images"
    annot_dir = "/home/ec2-user/SageMaker/DL4CV_brand_blurring/dataset/annotations"
    
    os.makedirs(images_dir)
    os.makedirs(annot_dir)
    restructure(directory, images_dir, annot_dir)