# from igraph import Graph
from graph_tool.all import *

from hooshak.modeling import HooshakEntityMixin, HooshakActivityMixin, HooshakUserMixin


class Warehouse:
    g = Graph(directed=False)
    map_vertex_entities = {}
    map_vertex_users = {}
    map_edges = {}

    def __init__(self):
        self.vprop_type = self.g.new_vertex_property('string')
        self.eprop_value = self.g.new_edge_property('int')
        self.eprop_timestamp = self.g.new_edge_property('int')

    def add_entities(self, *entities: HooshakEntityMixin):

        # gen = self.g.add_vertex(100000)
        # for v in gen:
        #     pass

        # for i in range(100000):
        #     v = self.g.add_vertex()
        # self.g.add_vertex(100000)
        # for v in self.g.add_vertex(10000000):
        #     pass
        for en in entities:
            # pass
            v = self.g.add_vertex()
            self.map_vertex_entities.update({str(en.get_hooshak_uid()): v})
            self.vprop_type[v] = 'entity'

            # offset = self.g.vcount()
            # self.g.add_vertices(len(entities))
            # self.g.vs[offset:]['name'] = [str(e.get_hooshak_uid()) for e in entities]
            # self.g.vs[offset:]['type'] = 'entity'

    def add_activities(self, *activities: HooshakActivityMixin):

        # from_list = [self.g.vs.select(id=a.get_hooshak_by(), type='user') for a in activities]


        for a in activities:
            e = self.g.add_edge(source=self.map_vertex_users[str(a.get_hooshak_by())],
                                target=self.map_vertex_entities[str(a.get_hooshak_to())])
            self.eprop_value[e] = a.get_hooshak_value()

            # for a in activities:
            #     # self.g.add_edge(source=str(a.get_hooshak_by()), target=str(a.get_hooshak_to()), value=a.get_hooshak_value())
            #     self.g.add_edge(source=1, target=2)

            # self.g.add_edges([(e.get_hooshak_by(), e.get_hooshak_to()) for e in activities])['value'] = \
            #     [e.get_hooshak_value() for e in activities]

    def add_users(self, *users: HooshakUserMixin):

        for us in users:
            v = self.g.add_vertex()
            self.map_vertex_users.update({str(us.get_hooshak_uid()): v})
            self.vprop_type[v] = 'user'

            # offset = self.g.vcount()
            # self.g.add_vertices(len(users))
            # self.g.vs[offset:]['name'] = [str(u.get_hooshak_uid()) for u in users]
            # self.g.vs[offset:]['type'] = 'user'

    def add_user(self, uid):
        v = self.g.add_vertex()
        self.map_vertex_users.update({uid: v})
        self.vprop_type[v] = 'user'

    def add_entity(self, uid):
        v = self.g.add_vertex()
        self.map_vertex_entities.update({uid: v})
        self.vprop_type[v] = 'entity'

    def add_activity(self, user_uid, entity_uid, value, timestamp):
        e = self.g.add_edge(source=self.map_vertex_users[user_uid],
                            target=self.map_vertex_entities[entity_uid])
        self.eprop_value[e] = value
        self.eprop_timestamp[e] = timestamp

    def get_user_v_by_uid(self, uid):
        return self.map_vertex_users[str(uid)]

    def get_entity_v_by_uid(self, uid):
        return self.map_vertex_entities[str(uid)]

    def get_activity_by_uid(self, uid):
        return self.map_edges[str(uid)]
