from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Optional

import sempy.fabric as fabric
import sempy.fabric._client._tom as tom_client
from sempy.fabric._client._utils import _init_analysis_services, generate_guid
from sempy._utils._log import log

if TYPE_CHECKING:
    _init_analysis_services()

    import Microsoft.AnalysisServices.Tabular as TOM


class TOMWrapper(
    tom_client.HasMixin,
    tom_client.IsMixin,
    tom_client.UsedInMixin,
    tom_client.ListAllMixin,
    tom_client.GetMixin,
    tom_client.InMixin,
    tom_client.ShowMixin,
):
    """
    Convenience wrapper around the TOM object model for a semantic model. Always use the connect_semantic_model function to make sure the TOM object is initialized correctly.

    `XMLA read/write endpoints <https://learn.microsoft.com/power-bi/enterprise/service-premium-connect-tools#to-enable-read-write-for-a-premium-capacity>`_ must
     be enabled if setting the readonly parameter to False.

    Parameters
    ----------
    dataset : str
        Name of the semantic model.
    workspace : str
        The Fabric workspace name.
    readonly : bool
        Whether the connection is read-only or read/write. Setting this to False enables read/write which saves the changes made back to the server.
    """

    _dataset: str
    _workspace: str
    _readonly: bool
    _tables_added: List[str]
    _table_map: Dict[str, Any]
    _column_map: Dict[str, Any]

    def __init__(self, dataset: str, workspace: str, readonly: bool):

        # initialize .NET to make sure System and Microsoft.AnalysisServices.Tabular is defined
        _init_analysis_services()

        from Microsoft.AnalysisServices import AmoException as AmoException

        self._dataset = dataset
        self._workspace = workspace
        self._readonly = readonly
        self._tables_added = []

        self._tom_server = fabric.create_tom_server(
            readonly=readonly, workspace=workspace
        )
        try:
            self._model = self._tom_server.Databases.GetByName(dataset).Model
        except AmoException:
            self._tom_server.Dispose()
            raise ValueError(f"Dataset {dataset} not found in workspace {workspace}")

        self._table_map = {}
        self._column_map = {}
        for t in self._model.Tables:
            if len(t.LineageTag) == 0:
                t.LineageTag = generate_guid()
            self._table_map[t.LineageTag] = t.Name

        for c in self.all_columns:
            if len(c.LineageTag) == 0:
                c.LineageTag = generate_guid()
            self._column_map[c.LineageTag] = [c.Name, c.DataType]

    @property
    def model(self) -> "TOM.Model":
        """
        The semantic model's Tabular Object Model.
        """
        return self._model

    @property
    def dataset(self) -> str:
        """
        The name of the semantic model.
        """
        return self._dataset

    @property
    def workspace(self) -> str:
        """
        The Fabric workspace name.
        """
        return self._workspace

    def close(self):
        """
        Close the connection to the semantic model.
        """
        self._tom_server.Dispose()


@log
@contextmanager
def connect_semantic_model(
    dataset: str, readonly: bool = True, workspace: Optional[str] = None
) -> Iterator[TOMWrapper]:
    """
    Connect to the Tabular Object Model (TOM) within a semantic model.

    Parameters
    ----------
    dataset : str
        Name of the semantic model.
    readonly : bool, default=True
        Whether the connection is read-only or read/write. Setting this to False enables read/write which saves the changes made back to the server.
    workspace : str, default=None
        The Fabric workspace name.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Yields
    ------
    TOMWrapper
        A connection to the semantic model's Tabular Object Model.
    """

    if workspace is None:
        workspace_id = fabric.get_workspace_id()
        workspace = fabric.resolve_workspace_name(workspace_id)

    tw = TOMWrapper(dataset=dataset, workspace=workspace, readonly=readonly)
    try:
        yield tw
    finally:
        tw.close()
