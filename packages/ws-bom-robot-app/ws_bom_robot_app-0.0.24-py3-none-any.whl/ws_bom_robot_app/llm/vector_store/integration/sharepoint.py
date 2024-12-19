import asyncio
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.v2.processes.connectors.sharepoint  import SharepointIndexerConfig, SharepointDownloaderConfig, SharepointConnectionConfig, SharepointAccessConfig
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Union, Optional
from pydantic import BaseModel, Field, AliasChoices

class SharepointParams(BaseModel):
  client_id : str = Field(validation_alias=AliasChoices("clientId","client_id"))
  client_secret : str = Field(validation_alias=AliasChoices("clientSecret","client_secret"))
  site_url: str = Field(validation_alias=AliasChoices("siteUrl","site_url"))
  site_path: str = Field(default=None,validation_alias=AliasChoices("sitePath","site_path"))
  recursive: bool = Field(default=False)
  omit_files: bool = Field(default=False, validation_alias=AliasChoices("omitFiles","omit_files")),
  omit_pages: bool = Field(default=False, validation_alias=AliasChoices("omitPages","omit_pages")),
  omit_lists: bool = Field(default=False, validation_alias=AliasChoices("omitLists","omit_lists")),
  extension: list[str] = Field(default=None)
class Sharepoint(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = SharepointParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'sharepoint'
  def run(self) -> None:
    indexer_config = SharepointIndexerConfig(
      path=self.__data.site_path,
      recursive=self.__data.recursive,
      omit_files=self.__data.omit_files,
      omit_pages=self.__data.omit_pages,
      omit_lists=self.__data.omit_lists
    )
    downloader_config = SharepointDownloaderConfig(
      download_dir=self.working_directory
    )
    connection_config = SharepointConnectionConfig(
      access_config=SharepointAccessConfig(client_cred=self.__data.client_secret),
      client_id=self.__data.client_id,
      site=self.__data.site_url,
      permissions_config=None
    )
    self.__unstructured_ingest.pipeline(
      indexer_config,
      downloader_config,
      connection_config,
      extension=self.__data.extension).run()
  async def load(self) -> list[Document]:
      await asyncio.to_thread(self.run)
      await asyncio.sleep(1)
      return await Loader(self.working_directory).load()
