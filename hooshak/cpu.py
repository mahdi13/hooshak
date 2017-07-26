import functools
import operator

from graph_tool.all import *

from hooshak.modeling import HooshakEntityMixin, HooshakUserMixin


class CPU:
    def __init__(self, g: Graph):
        self.g = g

    # def calculate_smart_score(self, user: HooshakUserMixin, entity: HooshakEntityMixin):
    #     out = []
    #     from hooshak.context import hooshex
    #     for path in all_paths(
    #             g=self.g,
    #             source=hooshex.warehouse.get_user_v_by_uid(user.get_hooshak_uid()),
    #             target=hooshex.warehouse.get_entity_v_by_uid(entity.get_hooshak_uid()),
    #             # weights=hooshex.warehouse.eprop_value,
    #             cutoff=3
    #
    #     ):
    #         if len(path) == 4:
    #             out.append((
    #                            hooshex.warehouse.eprop_value[self.g.edge(path[0], path[1])] *
    #                            hooshex.warehouse.eprop_value[self.g.edge(path[1], path[2])] *
    #                            hooshex.warehouse.eprop_value[self.g.edge(path[2], path[3])]) ** (1. / 3.)
    #                        )
    #             # elif len(path) == 2:
    #             #     return None
    #             #
    #             #     e = self.g.edge(path[0], path[1])
    #             #     self.g.remove_edge(e)
    #             #
    #             #     out = self.calculate_smart_score(user=user, entity=entity)
    #             #
    #             #     self.g.add_edge(path[0], path[1])
    #             #
    #             #     # return out
    #             #     # out.append('shit')
    #
    #         return out

    def calculate_average_vote(self, user_uid, entity_uid):
        from hooshak.context import hooshex

        coefficient_sum = 0
        value_sum = 0
        source = hooshex.warehouse.map_vertex_entities[entity_uid]
        for v in hooshex.warehouse.map_vertex_entities[entity_uid].all_neighbours():
            try:
                e = self.g.edge(v, source)
                value_sum += self.g.properties[('e', 'value')][e]
                coefficient_sum += 1
            except:
                pass

        return value_sum / coefficient_sum

    def calculate_smart_score(self, user_uid, entity_uid):
        """

                                        Third person
                                 gamma     +---+      beta
                                +----------+   +------------+
                                |          +---+            |
                                |                           |
                                v                           v
                               XX                           XX
                              XXXX                         X  X
            Selected entity  XXXXXX                       X    X  Third entity
                              XXXX                         X  X
                               XX                           XX
                                ^                           ^
                                |          +++++            |
                                +----------+++++------------+
                                 unknown   +++++    alpha
                                            Me


        :param user_uid:
        :param entity_uid:
        :return:
        """

        path_list = []
        coefficient_sum = 0

        from hooshak.context import hooshex
        for path in all_paths(
                g=self.g,
                source=hooshex.warehouse.get_user_v_by_uid(user_uid),
                target=hooshex.warehouse.get_entity_v_by_uid(entity_uid),
                # weights=hooshex.warehouse.eprop_value,
                cutoff=3

        ):
            if len(path) == 4:
                alpha = hooshex.warehouse.g.properties[('e', 'value')][self.g.edge(path[0], path[1])]
                beta = hooshex.warehouse.g.properties[('e', 'value')][self.g.edge(path[2], path[1])]
                gamma = hooshex.warehouse.g.properties[('e', 'value')][self.g.edge(path[2], path[3])]

                distance = abs(alpha - beta)
                # simil = (4 - distance) / 4
                # simil = (1 / (distance+1))
                simil = 1

                # path_list.append(round((alpha * beta * gamma) ** (1. / 3.)))
                path_list.append(simil * gamma)
                coefficient_sum += simil
                # elif len(path) == 2:
                #     return None
                #
                #     e = self.g.edge(path[0], path[1])
                #     self.g.remove_edge(e)
                #
                #     out = self.calculate_smart_score(user=user, entity=entity)
                #
                #     self.g.add_edge(path[0], path[1])
                #
                #     # return out
                #     # out.append('shit')

        # return functools.reduce(operator.add, path_list, 1) / len(path_list)
        return functools.reduce(operator.add, path_list, 1) / coefficient_sum
