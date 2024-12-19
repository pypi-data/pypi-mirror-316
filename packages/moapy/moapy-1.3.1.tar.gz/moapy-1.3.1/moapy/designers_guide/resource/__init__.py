from itertools import chain

from moapy.designers_guide.content_component_manager.content_component import (
    Component,
    Content,
    DataTable,
)
from moapy.designers_guide.resource.content_component import (
    component_list as origin_component_list,
    data_table as origin_table_data_list,
)
from moapy.designers_guide.resource.contents import (
    contents as origin_content_list,
)
import moapy.designers_guide.resource.component17 as component17
import moapy.designers_guide.resource.component18 as component18
import moapy.designers_guide.resource.component19 as component19
import moapy.designers_guide.resource.component20 as component20
import moapy.designers_guide.resource.component29 as component29
import moapy.designers_guide.resource.component30 as component30


def compose_component_list(*args: list[list[Component]]):
    return list(chain(*args))


def compose_table_data_list(*args: list[list[DataTable]]):
    return list(chain(*args))


def compose_content_list(*args: list[list[Content]]):
    return list(chain(*args))


components = compose_component_list(
    origin_component_list,
    component17.component_list,
    component18.component_list,
    component19.component_list,
    component20.component_list,
    component29.component_list,
    component30.component_list,
)
data_tables = compose_table_data_list(
    origin_table_data_list,
    component17.data_table,
    component18.data_table,
    component19.data_table,
    component20.data_table,
    component29.data_table,
    component30.data_table,
)
contents = compose_content_list(
    origin_content_list,
    component17.content,
    component18.content,
    component19.content,
    component20.content,
    component29.content,
    component30.content,
)
