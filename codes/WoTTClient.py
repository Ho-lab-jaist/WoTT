
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This is an example of Web of Things consumer ("client" mode) Thing script.
It considers a fictional smart coffee machine in order to demonstrate the capabilities of Web of Things.
The example is ported from the node-wot environment -
https://github.com/eclipse/thingweb.node-wot/blob/master/packages/examples/src/scripts/coffee-machine-client.ts.
'''
import asyncio
import logging
from wotpy.wot.servient import Servient
from wotpy.wot.wot import WoT
import numpy as np
import matplotlib.tri as mtri
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable, get_cmap
from matplotlib.colors import Normalize
import time
import argparse

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
parser = argparse.ArgumentParser(description="Url of server")
parser.add_argument("url", type=str)


def points_extraction(init_points_info):
    init_points = list()
    for i in range(init_points_info['numOfNodes']):
        x_init = init_points_info['arrayOfNodes'][i]['nodeLocation']['x']
        y_init = init_points_info['arrayOfNodes'][i]['nodeLocation']['y']
        z_init = init_points_info['arrayOfNodes'][i]['nodeLocation']['z']
        coordinate = [x_init, y_init, z_init]
        init_points.append(coordinate)
    return np.array(init_points)


def cells_extraction(init_cells_info):
    init_cells = list()
    for i in range(init_cells_info['numOfCells']):
        point_1 = int(init_cells_info['arrayOfCells'][i]['connectedNodes'][0])
        point_2 = int(init_cells_info['arrayOfCells'][i]['connectedNodes'][1])
        point_3 = int(init_cells_info['arrayOfCells'][i]['connectedNodes'][2])
        points = [point_1, point_2, point_3]

        init_cells.append(points)
    return np.array(init_cells)


def compute_triangle_mean(points, cells, slices):
    triangles = []
    for cell in cells:
        triangle = points[cell]
        triangles.extend(triangle)
    triangles = np.array(triangles)
    num_vec = triangles.shape[0]

    x, y, z, _ = np.vstack([triangles.T, np.ones(num_vec)])
    triangles = np.array([np.array((x[s],y[s],z[s])).T for s in slices])
    return triangles.mean(axis=1)


def create_silces(num_triangle):
    start = 0
    stop = 3
    slices = []
    for i in range(num_triangle):
        slices.append(slice(start,stop))
        start +=3
        stop +=3
    return slices


class DigitalTwin(object):
    def __init__(self, init_points, init_cells):
        self.init_points = init_points
        self.x = init_points[:, 0]
        self.y = init_points[:, 1]
        self.z = init_points[:, 2]
        init_cells = init_cells.astype(int)
        list_cells = init_cells.tolist()
        self.triangles = list_cells
        self.slices = create_silces(len(self.triangles))

        self.init_triangles_mean = compute_triangle_mean(self.init_points, self.triangles, self.slices)
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.norm = Normalize(vmin=0, vmax=16)
        mappable = ScalarMappable(cmap='coolwarm', norm=self.norm)
        self.fig.colorbar(mappable, shrink=0.5, aspect=5)
        self.start = time.time()

    def draw(self, points):
        updated_triangles_mean = compute_triangle_mean(points, self.triangles, self.slices)

        d = np.linalg.norm(updated_triangles_mean - self.init_triangles_mean, axis=1)

        triang = mtri.Triangulation(points[:, 0], points[:, 1], triangles=self.triangles)
        z_ls = points[:, 2].tolist()
        skin = self.ax.plot_trisurf(triang, z_ls)
        colors = get_cmap('coolwarm')(self.norm(d))

        skin.set_fc(colors)
        plt.xlim(-self.z.max() / 2, self.z.max() / 2)
        plt.ylim(-self.z.max() / 2, self.z.max() / 2)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.ax.cla()

    def update(self, item):
        data = item.data
        updated_points = list()
        updated_id = list()
        if data['numOfDeformedNodes']>0:
            for i in range(data['numOfDeformedNodes']):
                idx_new = data['arrayOfDeformedNodes'][i]['deformedNodeID']
                x_new = data['arrayOfDeformedNodes'][i]['deformedNodeLocation']['x']
                y_new = data['arrayOfDeformedNodes'][i]['deformedNodeLocation']['y']
                z_new = data['arrayOfDeformedNodes'][i]['deformedNodeLocation']['z']
                coor = [x_new, y_new, z_new]
                updated_points.append(coor)
                updated_id.append(int(idx_new))
            updated_points = np.array(updated_points)
            points = np.array(self.init_points)
            points[updated_id, :] = updated_points
        self.draw(points)


async def main():

    wot = WoT(servient=Servient())
    url_server = parser.parse_args()
    consumed_thing = await wot.consume_from_url(url_server.url)
    LOGGER.info('Consumed Thing: {}'.format(consumed_thing))
    init_points_info = await consumed_thing.read_property('skinNodes')
    init_points = points_extraction(init_points_info)
    init_cells_info = await consumed_thing.read_property('skinCells')
    init_cells = cells_extraction(init_cells_info)
    twin = DigitalTwin(init_points, init_cells)
    twin.draw(init_points)
    consumed_thing.events['skinDeformation'].subscribe(
        on_next=twin.update,
        on_completed=LOGGER.info('Subscribed for an event: skinDeformation'),
        on_error=lambda error: LOGGER.info(f'Error for an event touchDetect: {error}'),
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

