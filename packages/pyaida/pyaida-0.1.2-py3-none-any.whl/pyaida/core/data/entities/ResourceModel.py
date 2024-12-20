from pyaida.core.data.AbstractModel import (
    AbstractEntityModel,
    AbstractModel,
    Field,
    model_validator,
)
import typing
from datetime import datetime
import uuid
from pyaida.core.utils import sha_hash


class UserResources(AbstractModel):

    class Config:
        namespace: str = "public"

    id: uuid.UUID
    user_id: uuid.UUID
    resource_id: uuid.UUID

    @model_validator(mode="before")
    @classmethod
    def _val(cls, values):
        """id from the hash"""
        values["id"] = sha_hash(
            {
                "user_id": str(values["user_id"]),
                "resource_id": str(values["resource_id"]),
            }
        )

        return values


class NoteResources(AbstractModel):

    class Config:
        namespace: str = "public"

    id: uuid.UUID
    note_id: uuid.UUID
    resource_id: uuid.UUID

    @model_validator(mode="before")
    @classmethod
    def _val(cls, values):
        """id from the hash"""
        values["id"] = sha_hash(
            {
                "note_id": str(values["note_id"]),
                "resource_id": str(values["resource_id"]),
            }
        )

        return values


class DraftResources(AbstractModel):

    class Config:
        namespace: str = "public"

    id: uuid.UUID
    draft_id: uuid.UUID
    resource_id: uuid.UUID

    @model_validator(mode="before")
    @classmethod
    def _val(cls, values):
        """id from the hash"""
        values["id"] = sha_hash(
            {
                "draft_id": str(values["draft_id"]),
                "resource_id": str(values["resource_id"]),
            }
        )

        return values


class ResourceModel(AbstractModel):
    """The Resource Model is a general model for adding references to material such as books, websites etc.
    It serves as a generic way to refer to things and follows a bib reference entity model.
    You can use external linked functions to resolve details from a uri
    """

    class Config:
        namespace: str = "public"
        name: str = "Resources"
        functions: dict = {
            "pyaida.resources_parse_page_metadata": "Use this api function to parse attributes from the uri and return a fleshed out ResourceModel"
        }

    id: uuid.UUID = Field(
        description="The unique key normally a hash of a uri or similar"
    )
    description: str = Field(
        description="The summary or abstract of the resource",
        embedding_provider="openai.text-embedding-ada-002",
    )
    uri: str = Field(
        description="A required unique resource identifier such as a web url"
    )
    image: typing.Optional[str] = Field(
        None, description="A required unique resource identifier such as a web url"
    )
    title: str = Field(description="The title of the resources")
    authors: typing.Optional[typing.List[str]] = Field(
        default=None, description="One or more authors"
    )
    """description is inherited"""
    resource_type: typing.Optional[str] = Field(
        default=None, description="The type of the resource e.g. web|book|article|etc."
    )
    reference_date: typing.Optional[datetime] = Field(
        default=None, description="Access or publication date"
    )
    publisher: typing.Optional[str] = Field(
        default=None, description="The publisher if relevant"
    )
    published_city: typing.Optional[str] = Field(
        default=None, description="The publisher city if relevant"
    )
    metadata: typing.Optional[dict] = Field(default={}, description="Extra metadata")

    @model_validator(mode="before")
    @classmethod
    def _val(cls, values):

        values["id"] = sha_hash(values["uri"])

        return values
