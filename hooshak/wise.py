class Wise:
    def __init__(self, warehouse, cpu):
        self.warehouse = warehouse
        self.cpu = cpu

    def learn(self, user_uid: str, entity_uid: str, value: int, timestamp: int):
        try:
            self.warehouse.get_user_v_by_uid(user_uid)
        except KeyError:
            self.warehouse.add_user(user_uid)
        try:
            self.warehouse.get_entity_v_by_uid(entity_uid)
        except KeyError:
            self.warehouse.add_entity(entity_uid)
        self.warehouse.add_activity(user_uid, entity_uid, value, timestamp)

    def predict(self, user_uid, entity_uid, timestamp):

        """

        per_user -> {third_user:[third_products]}


        :param user_uid:
        :param entity_uid:
        :param timestamp:
        :return:
        """

        try:
            self.warehouse.get_user_v_by_uid(user_uid)
            self.warehouse.get_entity_v_by_uid(entity_uid)
        except:
            # One of user or entity doesn't exists
            return None

        # Sorting data by third_user
        per_user = {}
        for user_uid, entity_uid, alpha, beta, gamma in self.cpu.seek_shared_activity_paths(user_uid=user_uid,
                                                                                            entity_uid=entity_uid):
            if user_uid in per_user:
                per_user[user_uid].append((entity_uid, alpha, beta, gamma))
            else:
                per_user.update({entity_uid: [(entity_uid, alpha, beta, gamma)]})

        for third_user, entities in per_user.items():
            target_values = []
            third_usr_values = []
            for entity_data in entities:
                entity_uid, alpha, beta, gamma = entity_data[0], entity_data[1], entity_data[2], entity_data[3]
                target_values.append(alpha)
                third_usr_values.append(beta)

            

        return 4
