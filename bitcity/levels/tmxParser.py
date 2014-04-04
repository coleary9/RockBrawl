# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Riveria <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>


import xml.etree.ElementTree as ET
import glob
import tile
from collections import defaultdict

''' Parsing for objects : dictionary of the form
    {value:position1, position 2, position 3}
    where position of the form (x,y) and value is the type of the object
    e.g : {enemySpawner: (100, 150), (200, 350)}
'''


def load(fileName):
    tree = ET.parse(glob.getFile(fileName))
    data = parseInput(tree)
    return data


def parseInput(tree):
    """ Parses an xml file to dictionaries used for level loading"""
    root = tree.getroot()
    data = {}
    objects = {}
    for child in root:
        if child.tag == 'tileset':
            glob.tileSize = int(child.attrib['tilewidth'])
            sheet, props = parseSet(child)
        elif child.tag == 'layer':
            for childChild in child:
                mapWidth = int(child.attrib['width'])
                mapHeight = int(child.attrib['height'])
                data = dict(data, **parseData(
                    childChild, mapWidth, sheet, props))
        elif child.tag == 'objectgroup':
            objects = parseObjects(child, props)
    return data, objects, mapWidth, mapHeight


def parseSet(root):
    """ Parses the 'tileSet' part of the level.
    sheet represents a relationship between tiles and the tileSheet
    Props is a mapping from a tile's id to a set of properties
    """
    props = {}
    firstgid = int(root.attrib['firstgid'])
    for child in root:
        if child.tag == 'image':
            sheet = parseSpriteSheet(child, firstgid)
        if child.tag == 'tile':
            # Updates the property dictionary
            props.update(parseTiles(child, firstgid))
    return sheet, props


def parseSpriteSheet(root, firstgid):
    """ Creates a list of surfaces with the image for each tile"""
    spriteSheet = tile.TileSheet(
        root.attrib['source'], firstgid)
    return spriteSheet


def parseTiles(root, firstgid):
    """ Creates a dictionnary between a tile's id and its properties """
    # since ids start at 0, yet gids start at 1
    gid = int(root.attrib['id']) + firstgid
    props = defaultdict(list)
    for child in root:
        if child.tag == 'properties':
            for innerChild in child:  # iterate through each property
                if innerChild.tag == 'property':
                    props[gid].append(innerChild.attrib['value'])

    return props


def parseData(root, width, sheet, props):
    """Creates a list of Tiles"""
    data = {}
    for i, child in enumerate(root):
        gid = int(child.attrib['gid'])
        if 0 < gid < len(sheet.tileImages):
            if gid in props:
                prop = props[gid]
            else:
                prop = ["leftrighttopbottom"]
            data[i] = tile.Tile(gid, i, width, sheet, prop)
    return data


def parseObjects(root, props):
    ''' returns a dictionary between a property, and a list of tupples (x,y)'''
    objects = defaultdict(list)
    for child in root:
        gid = int(child.attrib['gid'])
        coordinate = getAbsolutePos(
            int(child.attrib['x']),
            int(child.attrib['y']))

        for prop in props[gid]:
            objects[prop].append(coordinate)

    return objects


def getAbsolutePos(x, y):
        return (x, y)
