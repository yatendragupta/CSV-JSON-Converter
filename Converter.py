import csv
import json
import os
import Logger

# Object holding a dictionary for each level. Keeping its prev level id and its own id
# Parent id and its own id is used to stitch them as parent children later
class Object:
    def __init__(self):  ## Constructor
        self.ParentId = "0"
        self.id = "0"
        self.dict = {}

# LevelObj holding an array of Object which is used to hold all objects of 1 particular level
class LevelObj:
    def __init__(self):  ## Constructor
        self.obj = []

class BaseURL:
    def __init__(self):  ## Constructor
        self.url = "BaseURL"
        self.finalList = []

# to search an Object (containing data for a particualar level and id) in a  array
def search(id, arrayObj):
    for obj in arrayObj:
        if obj.id == id:
            return True
    return False

# This is used when we start stitching children to their parents
def setChild(parentId, prevObjList, currentObj):
    try:
        for prevobj in prevObjList:
            #Logger.logger.info (prevobj.dict)
            if prevobj.id == parentId:
                #Logger.logger.info(prevobj.dict)
                prevobj.dict['children'].append(currentObj.dict)
                return
    except:
        Logger.logger.error("Something wrong while stitching children to parent")

# Get the no of levels in a given csv file
def getLevelCount(csvFilePath):
    ncol = 0
    with open(csvFilePath, 'rt') as csv1:
        reader = csv.reader(csv1)
        ncol = len(next(reader))
        csv1.seek(0)
    x = int((ncol-1)/3)
    Logger.logger.info("Total no of columns in CSV file: " + str(ncol))
    Logger.logger.info("Total count of levels in CSV file: " + str(x))
    return x

# This function takes the csv file name/path and generates a json file and returns its name/path
def convertToJson(csvFilePath, jsonFilePath):
    try:
        if os.stat(csvFilePath).st_size == 0:
            Logger.logger.error("Required Data not found OR Invalid CSV File")
            return "Empty CSV File"

        levelCount = getLevelCount(csvFilePath)
        if levelCount < 1:
            Logger.logger.error("Required Data not found OR Invalid CSV File")
            return "Required Data not found OR Invalid CSV File"

        # creating an array of LevelObj according to no of levels identified
        lvlObjArray = []
        for i in range(levelCount):
            lvlObjArray.append(LevelObj())
        baseURL = []
        # Open a csv reader
        with open(csvFilePath, 'rt') as csvf:
            csvReader = csv.reader(csvf)

            count=1
            # Iterating column fields for each line
            for rows in csvReader:
                # Continue to second line, if iterator reaches to end of line
                if count == 1:
                    count+=1
                    continue
                if not rows[0]:
                    count += 1
                    continue

                # Creating objects for each level and each row
                # And adding them into an array LevelObjct corresponding to its level
                index = 0
                LvlIndx = 0
                while index < len(rows):
                    if not rows[index+1]:
                        break
                    if rows[index -1] not in rows[index + 3]:
                        Logger.logger.error("URL, not containg ID from previous Level, skipping Invalid Record: " + str(rows))
                        break

                    ret = search(rows[index + 2], lvlObjArray[LvlIndx].obj)
                    if ret == False:
                        newObj = Object()
                        newObj.dict['label'] = rows[index + 1]
                        newObj.dict['id'] = rows[index + 2]
                        newObj.dict['link'] = rows[index + 3]
                        newObj.dict['children'] = []
                        newObj.id = rows[index + 2]
                        if index - 1 > 0:
                            newObj.ParentId = rows[index - 1]
                        lvlObjArray[LvlIndx].obj.append(newObj)
                    index+=3
                    LvlIndx+=1
            count+=1

        # Logic of stitching all objects
        Logger.logger.info("Created objects from all levels and now starting the logic of stitching them")
        index = len(lvlObjArray) - 1
        while index >= 0:
            Logger.logger.info ("*************Level: " + str(index))
            for objct in lvlObjArray[index].obj:
                Logger.logger.info("-------- ParentID: " + objct.ParentId+ ", Own ID: " + objct.id)
                Logger.logger.info (objct.dict)
                if index >= 0:
                    setChild(objct.ParentId, lvlObjArray[index-1].obj,objct)
            index-=1
        #print(lvlObjArray[0].obj[0].dict)

        #finalDict = {}
        j = 0
        tmpArray = []
        while j < len(lvlObjArray[0].obj):
            tmpArray.append(lvlObjArray[0].obj[j].dict)
            j+=1
        finalDict = {"Base URL": tmpArray}

        Logger.logger.info("Final Dictionary created after stitching all its children --")
        Logger.logger.info("Creating JSON from this dictionary")

        # Open a json writer, and use the json.dumps() function to dump data
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(finalDict, indent=4))

    except IOError:
        Logger.logger.error("Failed to open a file")
    except IndexError:
        Logger.logger.error("Out of Range error")
