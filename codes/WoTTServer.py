#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is an example of Web of Things producer ("server" mode) Thing script.
It considers a fictional smart coffee machine in order to demonstrate the capabilities of Web of Things.
The example is ported from the node-wot environment -
https://github.com/eclipse/thingweb.node-wot/blob/master/packages/examples/src/scripts/coffee-machine.ts.
'''
import json
import logging
import tornado.gen
from tornado.ioloop import IOLoop
from wotpy.protocols.http.server import HTTPServer
from wotpy.protocols.ws.server import WebsocketServer
from wotpy.wot.servient import Servient
import pandas as pd
from datetime import datetime
import asyncio
import numpy as np

import cv2
import os
import torch

import sensor_process
# import TacNet
from networks.vgg_model import Tactile_VGG11

# import modules related to GAN model
from gan.options.test_options import TestOptions
from gan.models import create_model

opt = TestOptions().parse()  # get test options
model = create_model(opt)      # create a model given opt.model and other options
model.setup(opt)               # regular setup: load and print networks; create schedulers

# Load TacNet
root_dir = '/home/user/remoteDir'
model_name = 'TacNet_21_11_10.pt'
model_name_path = os.path.join('iotouch_env/train_model', model_name)
model_dir = os.path.join(root_dir, model_name_path)
tacnet = Tactile_VGG11()
print('model [Tactile_VGG11] was created')
print('loading the model from {0}'.format(model_dir))
tacnet.load_state_dict(torch.load(model_dir))
print('---------- Tactile Networks initialized -------------')
dev = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
tacnet.to(dev)
tacnet.eval()

init_path = os.path.join(root_dir, 'iotouch_env/train_data/data_0903/ouput_label/init_data.csv')
init_pos_csv = pd.read_csv(init_path)
init_position = np.array(init_pos_csv.iloc[0, 1:], dtype=float)
"""
For sucessfully read two video camera streams simultaneously,
we need to use two seperated USB bus for cameras
e.g, USB ports in front and back of the CPU
"""

cam_bot = cv2.VideoCapture(2)
cam_top = cv2.VideoCapture(0)

CATALOGUE_PORT = 9090
WEBSOCKET_PORT = 9393
HTTP_PORT = 9494

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

TD = {
    "@context": [
        "https://www.w3.org/2019/wot/td/v1"
    ],
    "id": "wot:tactileSensor:demo",
    "title": "tactileSensor",
    "description": "Large-scale Tactile Sensor",
    "properties":{
        "skinColor":{
            "type": "string",
            "title": "skinColor",
            # "readOnly": true,
            # "writeOnly": false,
            # "observable": false,
            "description": "color of sensor skin"
        }, 
        "skinMaterial":{
            "type": "string",
            "title": "skinMaterial",
            # "readOnly": true,
            # "writeOnly": false,
            # "observable": false,
            "description": "material of sensor skin"
        },
        "skinShape":{
            "type": "object",
            "title": "skinShape",
            "description": "Shape and dimension of the tactile sensor",
            # "readOnly": true,
            # "writeOnly": false,
            # "observable": false,
            "oneOf": [
                {
                    "type": "object",
                    "properties": {
                        "name":{
                          "type": "string",
                          "const":  "rectangularPrism"
                        },
                        "lengthDimension": {
                            "type": "number",
                            "unit": "mm"
                        },
                        "widthDimension": {
                            "type": "number",
                            "unit": "mm"
                        },
                        "heightDimension": {
                            "type": "number",
                            "unit": "mm"
                        }
                    }
                },
                {
                    "type": "object",
                    "properties": {
                        "name":{
                          "type": "string",
                          "const":  "cylinder"
                        },
                        "baseRadiusDimension": {
                            "type": "number",
                            "unit": "mm"
                        },
                        "heightDimension": {
                            "type": "number",
                            "unit": "mm"
                        }
                    }
                },
                {
                    "type": "object",
                    "properties": {
                        "name":{
                            "type": "string",
                            "const":  "barrel"
                        },
                        "baseRadiusDimension": {
                            "type": "number",
                            "unit": "mm"
                        },
                        "middleRadiusDimension": {
                            "type": "number",
                            "unit": "mm"
                        },
                        "heightDimension": {
                            "type": "number",
                            "unit": "mm"
                        }
                    }
                }
            ]
        },
        "skinNodes":{
            "type": "object",
            "properties":{
                "numOfNodes":{
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 1000               
                },
                "arrayOfNodes":{
                    "type": "array",
                    "items":{
                        "type":"object",
                        "properties":{
                            "nodeID":{
                                "type": "string"
                            },
                            "nodeLocation":{
                                "type": "object",
                                "properties":{
                                    "x":{
                                        "type": "number",
                                        "unit": "mm"
                                    },
                                    "y":{
                                        "type": "number",
                                        "unit": "mm"
                                    },
                                    "z":{
                                        "type": "number",
                                        "unit": "mm"
                                    }
                                }
                            },
                            "referenceTo":{
                                "type": "string"
                            }
                        }
                    },
                    "minItems": 1,
                    "maxItems": 1000
                }
            },
            "title": "skinNodes",
            "description": "Nodes make up the skin surface"
        },
        "skinCells":{
            "type": "object",
            "properties":{
                "numOfCells":{
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 10000  
                },
                "arrayOfCells":{
                    "type": "array",
                    "items":{
                        "type": "object",
                        "properties":{
                            "numOfConnectedNodes":{
                                "type": "integer"
                            },
                            "connectedNodes":{
                                "type": "array",
                                "items":{
                                    "type": "string"
                                },
                                "minItems": 3,
                                "maxItems": 3
                            }
                        },
                        "minItems": 1,
                        "maxItems": 10000
                    }
                }
            },
            "title": "skinCells",
            "description": "Cells connected by related nodes, which make up the skin surface"
        },
        "coordinateSystem":{
            "type": "string",
            "title": "coordinateSystem",
            "description": "describe the coordinate of sensor link"
        }
    },
    "events": {
        "touchDetected":{
            "description": "Inform when touch detected",
            "data": {
                "type": "string"
            }
        },
        "skinDeformation":{
            "description": "Emits event with deformed skin nodes where the skin is touched.",
            "data": {
                "type": "object",
                "properties":{
                    "numOfDeformedNodes":{
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 1000               
                    },
                    "arrayOfDeformedNodes":{
                        "type": "array",
                        "items":{
                            "type":"object",
                            "properties":{
                                "deformedNodeID":{
                                    "type": "string"
                                },
                                "deformedNodeLocation":{
                                    "type": "object",
                                    "properties":{
                                        "x":{
                                            "type": "number",
                                            "unit": "mm"
                                        },
                                        "y":{
                                            "type": "number",
                                            "unit": "mm"
                                        },
                                        "z":{
                                            "type": "number",
                                            "unit": "mm"
                                        }
                                    }
                                },
                                "referenceTo":{
                                    "type": "string"
                                }
                            }
                        },
                        "minItems": 1,
                        "maxItems": 1000
                    }
                }
            }
        }
    },
    "@type": "Thing"
}

# async def read_shape_hanlder():
#     return {
#         'baseRadiusDimension': 90,
#         'heightDimension': 300
#     }

"""
Utils for handling resources
"""

def extract_initial_node_locations(vtk_file='./resources/skin.vtk'):
    points_ls = []
    with open(vtk_file, 'r') as rf:
        for idx, line in enumerate(rf):
            if 6 <= idx <= 712:
                points = [float(x) for x in line.split()]
                points_ls.append(points)
            elif idx > 712:
                break
            
    return np.array(points_ls, dtype=float)

def extract_skin_cells(vtk_file='./resources/skin.vtk'):
    """
    Returns:
        - list of connected nodes : [[id1, id2, id3], [], ..., []]
    """

    cells_ls = []
    with open(vtk_file, 'r') as rf:
        for idx, line in enumerate(rf):
            if idx < 715:
                continue
            elif 715 <= idx <= 2088:
                cells = line.split()
                cells_ls.append(cells)
            elif idx > 2088:
                break

    return cells_ls

def load_resources(vtk_file='./resources/skin.vtk'):
    init_points = extract_initial_node_locations(vtk_file)
    skin_cells = extract_skin_cells(vtk_file)
    return init_points, skin_cells

"""
Extract TD properties from resrouces
"""

def createSkinNodesProperty(init_points):
    # nodes' location extracted from VTK file
    nodeLocations = np.array(init_points)
    numOfNodes = nodeLocations.shape[0]
    arrayOfNodes = []
    for i in range(numOfNodes):
        nodeLocation = nodeLocations[i]
        nodeDict = {
            'nodeID': str(i),
            'nodeLocation': {
                'x': nodeLocation[0],
                'y': nodeLocation[1],
                'z': nodeLocation[2]
            },
            'referenceTo': 'world'
        }
        arrayOfNodes.append(nodeDict)
    
    return {'numOfNodes': numOfNodes, 'arrayOfNodes': arrayOfNodes}

def createSkinCellsProperty(skin_cells):
    skinCells = list(skin_cells)
    numOfCells = len(skinCells)
    arrayOfCells = []
    for i in range(numOfCells):
        skinCell = skinCells[i]
        numOfConnectedNodes = int(skinCell[0])
        ConnectedNodes = skinCell[1:]
        cellDict = {
            'numOfConnectedNodes': numOfConnectedNodes,
            'connectedNodes': ConnectedNodes
        }
        arrayOfCells.append(cellDict)
    
    return {'numOfCells': numOfCells, 'arrayOfCells': arrayOfCells}


"""
Create tasks for TD events
"""

def create_touch_detected_task(exposed_thing):
    """Inform when touch occurs."""
    async def send_event(exposed_thing):
        count = 0
        while True:
            now = datetime.now() # current date and time
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            print('datetime:{}'.format(date_time))
            resource = date_time
            sec = int(date_time[-1])
            if (sec%2)==0:
                count +=1
                resource = str(count) + ':' + resource
                print('sent: {}'.format(resource))
                exposed_thing.emit_event('touchDetected', resource)

            await asyncio.sleep(1)

    event_loop = asyncio.get_event_loop()
    event_loop.create_task(send_event(exposed_thing))


def create_skin_state_update_task(exposed_thing, init_points):
    """Update node locations where touch is made (change in node locations)."""
    async def send_skin_state(exposed_thing, init_points):
        last_indices = list()
        sent = False
        while True:
            await asyncio.sleep(0.01)
            deformedNodeLocations, indices = sensor_process.extract_skin_state(model, tacnet, cam_bot, cam_top)
            numOfDeformedNodes = len(indices)
            arrayOfDeformedNodes = []
            if numOfDeformedNodes > 0:
                sent = True
                for i in range(numOfDeformedNodes):
                    id = indices[i]
                    deformednodeLocation = deformedNodeLocations[i]
                    deformedNodesDict = {
                        'deformedNodeID': str(id),
                        'deformedNodeLocation': {
                            'x': deformednodeLocation[0],
                            'y': deformednodeLocation[1],
                            'z': deformednodeLocation[2]
                        },
                        'referenceTo': 'world'
                    }
                    arrayOfDeformedNodes.append(deformedNodesDict)
                last_indices =  indices   
                LOGGER.info('Skin Deformed!')
            else:
                if sent:
                    print('clear')
                    numOfDeformedNodes = len(last_indices)
                    arrayOfDeformedNodes = []
                    points_to_clear = init_points[last_indices, :]                  
                    for i in range(numOfDeformedNodes):
                        id = last_indices[i]
                        nodeLocation = points_to_clear[i]
                        deformedNodesDict = {
                                'deformedNodeID': str(id),
                                'deformedNodeLocation': {
                                    'x': nodeLocation[0],
                                    'y': nodeLocation[1],
                                    'z': nodeLocation[2]
                                },
                                'referenceTo': 'world'
                            }
                        arrayOfDeformedNodes.append(deformedNodesDict)
                    sent = False
                else:
                    continue
            exposed_thing.emit_event('skinDeformation', {'numOfDeformedNodes': numOfDeformedNodes, 'arrayOfDeformedNodes': arrayOfDeformedNodes})

    event_loop = asyncio.get_event_loop()
    event_loop.create_task(send_skin_state(exposed_thing, init_points))

@tornado.gen.coroutine
def main():
    LOGGER.info('Creating WebSocket server on: {}'.format(WEBSOCKET_PORT))
    ws_server = WebsocketServer(port=WEBSOCKET_PORT)

    LOGGER.info('Creating HTTP server on: {}'.format(HTTP_PORT))
    http_server = HTTPServer(port=HTTP_PORT)

    LOGGER.info('Creating servient with TD catalogue on: {}'.format(CATALOGUE_PORT))
    servient = Servient(catalogue_port=CATALOGUE_PORT)
    servient.add_server(ws_server)
    servient.add_server(http_server)

    LOGGER.info('Starting servient')
    wot = yield servient.start()

    LOGGER.info('Exposing and configuring Thing')

    # Produce the Thing from Thing Description
    exposed_thing = wot.produce(json.dumps(TD))


    # async def read_color_hanlder():
    #     return "black"

    # exposed_thing.set_property_read_handler("skinColor", read_color_hanlder)
    # exposed_thing.set_property_read_handler("skinShape", read_shape_hanlder)
  
    yield exposed_thing.properties['skinColor'].write('black')
    yield exposed_thing.properties['skinShape'].write({
        'name': 'cylinder',
        'baseRadiusDimension': 60,
        'heightDimension': 260
    })
    
    init_points, skin_cells = load_resources(vtk_file='./resources/skin.vtk')
    # create dictionary for skinNodes dataschema
    skinNodeData = createSkinNodesProperty(init_points)
    yield exposed_thing.properties['skinNodes'].write(skinNodeData)
    # create dictionary for skinCells dataschema
    skinCellData = createSkinCellsProperty(skin_cells)
    yield exposed_thing.properties['skinCells'].write(skinCellData)

    exposed_thing.expose()

    # create_touch_detected_task(exposed_thing)
    create_skin_state_update_task(exposed_thing, init_points)

    LOGGER.info(f'{TD["title"]} is ready')

if __name__ == '__main__':
    LOGGER.info('Starting loop')
    IOLoop.current().add_callback(main)
    IOLoop.current().start()
