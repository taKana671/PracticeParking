from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape, BulletHeightfieldShape, ZUp
from panda3d.core import NodePath, PandaNode, CardMaker, BitMask32, Vec3, Point3
from panda3d.core import Filename, PNMImage
from panda3d.core import GeoMipTerrain

from parking_lot import ParkingLot


class Terrain(NodePath):

    def __init__(self):
        super().__init__(BulletRigidBodyNode('terrain'))
        self.height = 30
        self.set_pos(Point3(0, 0, 0))
        self.node().set_mass(0)
        # self.set_collide_mask(BitMask32.bit(1))
        self.set_collide_mask(BitMask32.all_on())

        img = PNMImage(Filename('terrains/sample8.png'))
        shape = BulletHeightfieldShape(img, self.height, ZUp)
        shape.set_use_diamond_subdivision(True)
        self.node().add_shape(shape)

        self.terrain = GeoMipTerrain('geomip_terrain')
        self.terrain.set_heightfield('terrains/sample8.png')
        self.terrain.set_border_stitching(True)
        self.terrain.set_block_size(8)
        # self.terrain.set_block_size(32)
        self.terrain.set_min_level(2)
        self.terrain.set_focal_point(base.camera)

        pos = Point3(-256 / 2, -256 / 2, -(self.height / 2))
        self.root = self.terrain.get_root()
        self.root.set_scale(Vec3(1, 1, self.height))
        self.root.set_pos(pos)
        self.terrain.generate()
        self.root.reparent_to(self)

        tex = base.loader.load_texture('textures/grass_02.png')
        self.root.set_texture(tex)



class Ground(NodePath):

    def __init__(self):
        super().__init__(BulletRigidBodyNode('ground'))
        model = self.create_ground()
        model.reparent_to(self)
        # self.set_collide_mask(BitMask32.all_on())
        self.set_collide_mask(BitMask32.bit(1))
        self.node().add_shape(BulletPlaneShape(Vec3.up(), 0))

    def create_ground(self):
        model = NodePath(PandaNode('ground_model'))
        card = CardMaker('card')
        card.set_frame(-1, 1, -1, 1)

        for y in range(-25, 25):
            for x in range(-25, 25):
                g = model.attach_new_node(card.generate())
                g.set_p(-90)
                g.set_pos(x, y, 0)

        tex = base.loader.loadTexture('textures/concrete.jpg')
        model.set_texture(tex)
        model.flatten_strong()
        model.set_pos(0, 0, 0)
        model.reparent_to(self)
        return model


class Scene(NodePath):

    def __init__(self, world):
        super().__init__(PandaNode('scene'))
        self.world = world
        # ground = Ground()
        # ground.reparent_to(self)
        # self.reparent_to(base.render)
        # world.attach(ground.node())
        # self.parking_lot = ParkingLot(self.world)
        self.terrain = Terrain()
        self.terrain.reparent_to(self)
        self.world.attach(self.terrain.node())