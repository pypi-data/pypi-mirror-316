from typing import Literal
import warnings

from moapy.designers_guide.content_component_manager.content_component import (
    Component,
    Content,
    DataTable,
    ContentComponentManager,
)
from moapy.designers_guide.content_component_manager.dict_content_component import (
    create_dict_content_component_manager,
)
from moapy.designers_guide.content_component_manager.list_content_component import (
    create_list_content_component_manager,
)


def create_content_component_manager(
    *,
    content_list: list[Content] | None = None,
    component_list: list[Component] | None = None,
    data_table: list[DataTable] | None = None,
    version: Literal["default", "list", "dict"] = "dict",
) -> ContentComponentManager:
    if content_list is None:
        content_list = []
    if component_list is None:
        component_list = []
    if data_table is None:
        data_table = []

    if version == "default":
        warnings.warn(
            "default version is deprecated. Use dict instead.",
            DeprecationWarning,
        )
        import moapy.designers_guide.resource.content_component as content_component
        from moapy.designers_guide.resource.contents import contents

        default_content_manager = content_component
        
        # polyfill for ComponentManager
        def update_component(id: str, component_list: Component):
            for content in contents:
                if content["id"] == id:
                    content["component"] = component_list

        setattr(default_content_manager, "update_component", update_component)

        # polyfill for ContentManager
        def find_content_by_id(id: str) -> Component | None:
            for content in contents:
                if content["id"] == id:
                    return content
            return None

        setattr(default_content_manager, "find_content_by_id", find_content_by_id)
        setattr(default_content_manager, "content_list", contents)

        return default_content_manager

    match version:
        case "list":
            warnings.warn(
                "list version is deprecated. Use dict instead.",
                DeprecationWarning,
            )
            return create_list_content_component_manager(
                content_list=content_list,
                component_list=component_list,
                data_table=data_table,
            )
        case "dict":
            return create_dict_content_component_manager(
                content_list=content_list,
                component_list=component_list,
                data_table=data_table,
            )
        case _:
            raise ValueError(f"Invalid version: {version}")


__all__ = ["create_content_component_manager", "ContentComponentManager"]
