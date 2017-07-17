from igraph import Graph

from hooshak.modeling import HooshakEntityMixin, HooshakActivityMixin, HooshakUserMixin


class Warehouse:
    g = Graph()

    def add_entities(self, *entities: HooshakEntityMixin):
        offset = self.g.vcount()
        self.g.add_vertices(len(entities))
        self.g.vs[offset:]['name'] = [str(e.get_hooshak_uid()) for e in entities]
        self.g.vs[offset:]['type'] = 'entity'

    def add_activities(self, *activities: HooshakActivityMixin):

        # from_list = [self.g.vs.select(id=a.get_hooshak_by(), type='user') for a in activities]

        for a in activities:
            # self.g.add_edge(source=str(a.get_hooshak_by()), target=str(a.get_hooshak_to()), value=a.get_hooshak_value())
            self.g.add_edge(source=1, target=2)

        # self.g.add_edges([(e.get_hooshak_by(), e.get_hooshak_to()) for e in activities])['value'] = \
        #     [e.get_hooshak_value() for e in activities]

    def add_users(self, *users: HooshakUserMixin):
        offset = self.g.vcount()
        self.g.add_vertices(len(users))
        self.g.vs[offset:]['name'] = [str(u.get_hooshak_uid()) for u in users]
        self.g.vs[offset:]['type'] = 'user'
