from copy import deepcopy
from typing import Optional

from moapy.designers_guide.content_component_manager.content_component import (
    Component,
    DataTable,
    Content,
)
from moapy.designers_guide.resource.content_component import (
    SERVER_URL,
    binary_operators,
    relation_operators,
    function_operators,
)


class ListComponentManager:
    def __init__(self):
        self._component: list[Component] = []
        self._data_table: list[DataTable] = []
        self._content: list[Content] = []

    def _add_content(self, content: Content) -> None:
        if not content["id"]:
            raise ValueError("Content id is required")
        if content["id"] in self._content:
            raise ValueError(f"Content with id {content['id']} already exists")
        self._content.append(deepcopy(content))

    def add_content(self, content: Content | list[Content]) -> None:
        for cont in content:
            self._add_content(cont)

    def _add_component(self, component: Component) -> None:
        if not component["id"]:
            raise ValueError("Component id is required")
        if component["id"] in self._component:
            raise ValueError(f"Component with id {component['id']} already exists")
        self._component.append(deepcopy(component))

    def add_component(self, component: Component | list[Component]) -> None:
        for comp in component:
            self._add_component(comp)

    def _add_data_table(self, data_table: DataTable) -> None:
        if not data_table["id"]:
            raise ValueError("Data table id is required")
        if data_table["id"] in self._data_table:
            raise ValueError(f"Data table with id {data_table['id']} already exists")
        self._data_table.append(deepcopy(data_table))

    def add_data_table(self, data_table: DataTable | list[DataTable]) -> None:
        for dt in data_table:
            self._add_data_table(dt)

    @property
    def component_list(self) -> list[Component]:
        return deepcopy(self._component)

    @property
    def data_table(self) -> list[DataTable]:
        return deepcopy(self._data_table)

    @property
    def content_list(self) -> list[Content]:
        return deepcopy(self._content)

    def find_component_by_id(self, id: str) -> Optional[Component]:
        for comp in self._component:
            if comp["id"] == id:
                return comp
        return None

    def find_content_by_id(self, id: str) -> Optional[Content]:
        for cont in self._content:
            if cont["id"] == id:
                return cont
        return None

    def update_component(self, id: str, component: Component) -> None:
        for i, comp in enumerate(self._component):
            if comp["id"] == id:
                self._component[i] = component
                return
        raise ValueError(f"Component with id {id} not found")

    def find_by_latex_symbol(self, target_latex_symbol: str) -> Optional[Component]:
        for comp in self._component:
            if comp["latex_symbol"] == target_latex_symbol:
                return comp
        return None

    def find_comp(
        self, latex_symbol: str, standard: str, reference: str
    ) -> Optional[Component]:
        for comp in self._component:
            if (
                comp["latex_symbol"] == latex_symbol
                and comp["standard"] == standard
                and comp["reference"] == reference
            ):
                return comp
        return None

    def get_table_by_component(self, comp: Component) -> Optional[DataTable]:
        if "table" in comp:
            return next(dt for dt in self._data_table if dt["id"] == comp["id"])
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

        detail_table = [[f"{comp['latex_symbol']}", "Description"]]
        for et in enum_table:
            row = []
            row.append(f"{et['label']}")
            if "description" in et:
                row.append(f"{et['description']}")
            detail_table.append(row)
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


def create_list_content_component_manager(
    *,
    content_list: list[Content],
    component_list: list[Component],
    data_table: list[DataTable],
) -> ListComponentManager:
    manager = ListComponentManager()
    manager.add_content(content_list)
    manager.add_component(component_list)
    manager.add_data_table(data_table)
    return manager
