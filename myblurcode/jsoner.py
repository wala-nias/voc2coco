import json 


filename = "/home/ec2-user/SageMaker/DL4CV_brand_blurring/Yet-Another-EfficientDet-Pytorch/datasets/cocologos/annotations/instances_val.json"

with open(filename, "r") as f:
    data = json.load(f)
    
for ann in data['annotations']:
    try:
        #print(ann)
        #id = ann['image_id']
        #ann['image_id'] = int(id)
        ann['category_id'] = 1
    except Exception as e:
        print("Error in annotations:", e)

data['categories'] = [data['categories']]
#data['categories'] = data['categories'][0]
#data['categories']['name'] = 'logo'

# for img in data['images']:
#     try:
#         #print(ann)
#         id = img['id']
#         img['id'] = int(id)
#     except Exception as e:
#         print("Error in images:", e)

with open(filename, "w") as f:
    json.dump(data, f)


