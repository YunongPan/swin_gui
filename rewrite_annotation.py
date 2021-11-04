
import sys
import json
#It happens to be so that the bounding boxes are lists and not ndarrays? Ndarrays are not JSON serialisable
#TypeError: Argument 'bb' has incorrect type (expected numpy.ndarray, got list)

#Find JSON that gives errors
JSON_LOC="/mnt/HDDData/DemoSens/DemoSens/Segmentation/CBNetV2/segmentation_tools/data/coco/annotations/instances_val2017.json"

#Open JSON
val_json = open(JSON_LOC, "r")
json_object = json.load(val_json)
val_json.close()

for i, instance in enumerate(json_object["annotations"]):
    if len(instance["segmentation"][0]) == 4:
        print("instance number", i, "raises arror:", instance["segmentation"][0])
        json_object["annotations"][i]=[]
        del json_object["annotations"][i]

val_json = open(JSON_LOC, "w")
json.dump(json_object, val_json)
val_json.close()