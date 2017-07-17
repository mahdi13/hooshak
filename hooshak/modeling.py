class HooshakEntityMixin:
    __hooshak_identifier__ = None

    def get_hooshak_uid(self):
        raise NotImplementedError

    def get_hooshak_categories(self):
        raise NotImplementedError

    def get_hooshak_tags(self):
        raise NotImplementedError


class HooshakUserMixin:
    __hooshak_identifier__ = None

    def get_hooshak_uid(self):
        raise NotImplementedError


class HooshakActivityMixin:
    __hooshak_identifier__ = None

    def get_hooshak_to(self):
        raise NotImplementedError

    def get_hooshak_by(self):
        raise NotImplementedError

    def get_hooshak_value(self):
        raise NotImplementedError
