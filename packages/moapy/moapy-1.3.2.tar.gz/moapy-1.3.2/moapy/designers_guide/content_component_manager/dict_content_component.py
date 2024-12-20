from copy import deepcopy
from typing import Optional

from moapy.designers_guide.content_component_manager.content_component import (
    Component,
    Content,
    DataTable,
)
from moapy.designers_guide.resource.content_component import (
    SERVER_URL,
    binary_operators,
    relation_operators,
    function_operators,
)


class DictContentComponentManager:
    def __init__(self):
        self._component: dict[str, Component] = {}
        self._data_table: dict[str, DataTable] = {}
        self._content: dict[str, Content] = {}

    def _add_content(self, content: Content) -> None:
        if not content["id"]:
            raise ValueError("Content id is required")
        if content["id"] in self._content:
            raise ValueError(f"Content with id {content['id']} already exists")
        self._content[content["id"]] = deepcopy(content)

    def add_content(self, content: Content | list[Content]) -> None:
        for cont in content:
            self._add_content(cont)

    def _add_component(self, component: Component) -> None:
        if not component["id"]:
            raise ValueError("Component id is required")
        if component["id"] in self._component:
            raise ValueError(f"Component with id {component['id']} already exists")
        self._component[component["id"]] = deepcopy(component)

    def add_component(self, component: Component | list[Component]) -> None:
        for comp in component:
            self._add_component(comp)

    def _add_data_table(self, data_table: DataTable) -> None:
        if not data_table["id"]:
            raise ValueError("Data table id is required")
        if data_table["id"] not in self._component:
            raise ValueError(
                f"Data table with id {data_table['id']} not found in component"
            )
        if data_table["id"] in self._data_table:
            raise ValueError(f"Data table with id {data_table['id']} already exists")
        self._data_table[data_table["id"]] = deepcopy(data_table)

    def add_data_table(self, data_table: DataTable | list[DataTable]) -> None:
        for dt in data_table:
            self._add_data_table(dt)

    @property
    def component_list(self) -> list[Component]:
        return deepcopy(list(self._component.values()))

    @property
    def data_table(self) -> list[DataTable]:
        return deepcopy(list(self._data_table.values()))

    @property
    def content_list(self) -> list[Content]:
        return deepcopy(list(self._content.values()))

    def find_component_by_id(self, id: str) -> Optional[Component]:
        return self._component.get(id, None)

    def find_content_by_id(self, id: str) -> Optional[Content]:
        return self._content.get(id, None)

    def update_component(self, id: str, component: Component) -> None:
        if id not in self._component:
            raise ValueError(f"Component with id {id} not found")
        self._component[id] = component

    def find_by_latex_symbol(self, target_latex_symbol: str) -> Optional[Component]:
        for comp in self._component.values():
            if comp["latex_symbol"] == target_latex_symbol:
                return comp
        return None

    def find_comp(
        self, latex_symbol: str, standard: str, reference: str
    ) -> Optional[Component]:
        for comp in self._component.values():
            if (
                comp["latex_symbol"] == latex_symbol
                and comp["standard"] == standard
                and comp["reference"] == reference
            ):
                return comp
        return None

    def get_table_by_component(self, comp: Component) -> Optional[DataTable]:
        if "table" in comp:
            return self._data_table.get(comp["id"])
        return None

    def get_table_enum_by_component(self, comp: Component) -> Optional[list[dict]]:
        table = self.get_table_by_component(comp)
        if table and "enum" in table:
            return table["enum"]
        return None

    def get_table_criteria_by_component(self, comp: Component) -> Optional[list[dict]]:
        table = self.get_table_by_component(comp)
        if table and "criteria" in table:
            return table["criteria"]
        return None

    def get_table_data_by_component(self, comp: Component) -> Optional[list[dict]]:
        table = self.get_table_by_component(comp)
        if table and "data" in table:
            return table["data"]
        return None

    def convert_enum_table_to_detail(
        self, comp: Component
    ) -> Optional[list[list[str]]]:
        enum_table = self.get_table_enum_by_component(comp)
        if enum_table is None or "description" not in enum_table[0]:
            return None

        detail_table = []
        for row, current_et in enumerate(enum_table):
            if row == 0:
                haeder = []
                for col, (key, value) in enumerate(current_et.items()):
                    if col == 0:
                        haeder.append(f"{comp['latex_symbol']}")
                    elif key == "description":
                        haeder.append("Description")
                    else:
                        haeder.append(str(key))
                detail_table.append(haeder)
            
            row_data = []
            for value in current_et.values():
                row_data.append(value)
            detail_table.append(row_data)

        return detail_table

    def get_figure_server_url(self) -> str:
        return SERVER_URL

    @property
    def binary_operators(self) -> list[str]:
        return binary_operators

    @property
    def relation_operators(self) -> list[str]:
        return relation_operators

    @property
    def function_operators(self) -> list[str]:
        return function_operators


def create_dict_content_component_manager(
    *,
    content_list: list[Content],
    component_list: list[Component],
    data_table: list[DataTable],
) -> DictContentComponentManager:
    manager = DictContentComponentManager()
    manager.add_content(content_list)
    manager.add_component(component_list)
    manager.add_data_table(data_table)
    return manager
