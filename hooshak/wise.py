from functools import reduce


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

    def predict(self, user_uid, entity_uid, timestamp, _min=1, _max=5):

        """

        per_user -> {third_user:[third_products]}

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
                per_user.update({user_uid: [(entity_uid, alpha, beta, gamma)]})

        total_final_value = 0
        total_final_coefficient = 0

        for third_user, entities in per_user.items():
            target_values = []
            third_user_values = []
            gamma = None
            for entity_data in entities:
                # Note: gamma is always equal in this loop
                entity_uid, alpha, beta, gamma = entity_data[0], entity_data[1], entity_data[2], entity_data[3]
                target_values.append(alpha)
                third_user_values.append(beta)

            if gamma is None:  # It is almost impossible
                continue

            regression = self.cpu.make_regression(target_values=target_values, third_party_values=third_user_values)
            line_coefficient = self.cpu.coefficient_by_regression(regression=regression)
            if not (0.1 < line_coefficient < 10 or -10 < line_coefficient < -0.1):
                # This is outlier
                continue
            value_prediction = self.cpu.predict_by_regression(regression=regression, x=gamma)
            trusty_coefficient = 1.0 / (self.cpu.mse_by_regression(regression=regression, target_values=target_values,
                                                                   third_party_values=third_user_values) + 1.0)

            if value_prediction < 1:
                value_prediction = 1
            elif value_prediction > 5:
                value_prediction = 5

            total_final_value += value_prediction * trusty_coefficient
            total_final_coefficient += trusty_coefficient

        if total_final_value == 0:
            return None

        final_predict = round(total_final_value / total_final_coefficient, 2)
        return final_predict
