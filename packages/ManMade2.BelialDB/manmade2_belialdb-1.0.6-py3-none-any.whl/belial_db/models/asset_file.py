from typing import Any
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .relationships import Base, MapAssetFileAssociation
from .map import Map


class AssetFile(Base):
    """
    Represents an asset file in the database.

    Attributes:
        Id (int): The primary key for the asset file.
        Path (str): The file path of the asset.
        Type (str): The type of the asset.
        DoodadSetIndex (int): The index of the doodad set.
        DoodadSetNames (str): The names of the doodad sets.
        MapId (int): The foreign key referencing the associated map.
        Map (Mapped[MapModel]): The relationship to the MapModel.
    """

    __tablename__ = "asset_files"

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Path: Mapped[str] = mapped_column(String, nullable=False)
    Type: Mapped[str] = mapped_column(String, nullable=False)
    DoodadSetIndex: Mapped[int] = mapped_column(Integer, nullable=False)
    DoodadSetNames: Mapped[str] = mapped_column(String, nullable=True)

    Maps: Mapped[list[Map]] = relationship(
        "Map", secondary=MapAssetFileAssociation, back_populates="AssetFiles"
    )

    def __eq__(self, other: Any):
        if not isinstance(other, AssetFile):
            return NotImplemented
        return self.Id == other.Id

    def __hash__(self):
        return hash(self.Id)

    def __repr__(self):
        return f"<AssetFile(Id={self.Id}, Path='{self.Path}', Type='{self.Type}', DoodadSetIndex={self.DoodadSetIndex})>"
