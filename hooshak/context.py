from hooshak.cpu import CPU
from hooshak.warehouse import Warehouse
from hooshak.wise import Wise


class _Context:
    warehouse = Warehouse()
    cpu = CPU(warehouse)
    wise = Wise(warehouse, cpu)


hooshex = _Context()
