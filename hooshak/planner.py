class Planner:
    def configure_user(self, config):
        """

        yml config:


        :param config:
        :return:
        """
        pass

    def configure_activities(self, config):
        """

        yml config:

        - name
        - type [boolean (-1, 1), float (0.0, 1.0), unsigned_int (0, 100), signed_int (-100, 100)]
        - coefficient (0.0, 1.0) (default: 1.0)

        :param config:
        :return:
        """
        pass

    def configure_entities(self, config):
        """

        yml config:

        - name

        - activities:
          - activity_name
          - coefficient

        - categories:
          - category_name

        - tags:
          - tag_name

        :param config:
        :return:
        """
        pass

    pass


planner = Planner()
