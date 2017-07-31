import functools
import operator

from graph_tool.all import *
from sklearn.metrics import mean_squared_error

from hooshak.modeling import HooshakEntityMixin, HooshakUserMixin


class CPU:
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.g = warehouse.g

    def calculate_regression(self, target_values: list, third_party_values: list):
        return mean_squared_error(target_values, third_party_values)

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

                                        Third person (2)
                                 gamma     +---+      beta
                                +----------+   +------------+
                                |          +---+            |
                                |                           |
                                v                           v
                               XX                           XX
                              XXXX                         X  X
        Selected entity (3)  XXXXXX                       X    X  Third entity (1)
                              XXXX                         X  X
                               XX                           XX
                                ^                           ^
                                |          +++++            |
                                +----------+++++------------+
                                 unknown   +++++    alpha
                                            Me (0)


        :param user_uid:
        :param entity_uid:
        :return:
        """

        per_user_value = {}
        per_user_simil = {}

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
                simil = (4 - distance)
                # simil = (1 / (distance+1))
                # simil = 1

                # path_list.append(round((alpha * beta * gamma) ** (1. / 3.)))
                # path_list.append(simil * gamma)
                # coefficient_sum += simil
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

                if str(path[2]) in per_user_value:
                    per_user_simil[str(path[2])].append(simil)
                else:
                    per_user_simil.update({str(path[2]): [simil]})
                    per_user_value.update({str(path[2]): gamma})

        # return functools.reduce(operator.add, path_list) / len(path_list)
        # return functools.reduce(operator.add, path_list) / coefficient_sum

        per_result_list = []
        per_coefficient_sum = 0
        for user, simils in per_user_simil.items():
            value = per_user_value[user]
            simil_sum = functools.reduce(operator.add, simils)
            simil_avr = simil_sum / len(simils)

            # if simil_avr < 3:
            #     continue

            per_coefficient_sum += simil_avr
            per_result_list.append(value * simil_avr)

        return functools.reduce(operator.add, per_result_list) / per_coefficient_sum

    def seek_shared_activity_paths(self, user_uid, entity_uid):
        for path in all_paths(
                g=self.g,
                source=self.warehouse.get_user_v_by_uid(user_uid),
                target=self.warehouse.get_entity_v_by_uid(entity_uid),
                cutoff=3

        ):
            if len(path) == 4:
                alpha = self.warehouse.g.properties[('e', 'value')][self.g.edge(path[0], path[1])]
                beta = self.warehouse.g.properties[('e', 'value')][self.g.edge(path[2], path[1])]
                gamma = self.warehouse.g.properties[('e', 'value')][self.g.edge(path[2], path[3])]

                yield self.warehouse.g.properties[('v', 'uid')][self.g.vertex(path[2])], \
                      self.warehouse.g.properties[('v', 'uid')][self.g.vertex(path[1])], \
                      alpha, \
                      beta, \
                      gamma

        return None
