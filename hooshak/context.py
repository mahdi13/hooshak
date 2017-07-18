from hooshak.warehouse import Warehouse
from hooshak.cpu import CPU


class _Context:
    warehouse = Warehouse()
    cpu = CPU(warehouse.g)


hooshex = _Context()
