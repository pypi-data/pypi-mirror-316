# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING, Any, Dict, List, Union
from xml.etree import ElementTree

from .diaglayers.basevariant import BaseVariant
from .diaglayers.diaglayer import DiagLayer
from .diaglayers.ecushareddata import EcuSharedData
from .diaglayers.ecuvariant import EcuVariant
from .diaglayers.functionalgroup import FunctionalGroup
from .diaglayers.protocol import Protocol
from .nameditemlist import NamedItemList
from .odxcategory import OdxCategory
from .odxlink import OdxDocFragment, OdxLinkDatabase, OdxLinkId
from .snrefcontext import SnRefContext
from .utils import dataclass_fields_asdict

if TYPE_CHECKING:
    from .database import Database


@dataclass
class DiagLayerContainer(OdxCategory):
    ecu_shared_datas: NamedItemList[EcuSharedData]
    protocols: NamedItemList[Protocol]
    functional_groups: NamedItemList[FunctionalGroup]
    base_variants: NamedItemList[BaseVariant]
    ecu_variants: NamedItemList[EcuVariant]

    @property
    def ecus(self) -> NamedItemList[EcuVariant]:
        """ECU variants defined in the container

        This property is an alias for `.ecu_variants`"""
        return self.ecu_variants

    def __post_init__(self) -> None:
        self._diag_layers = NamedItemList[DiagLayer](chain(
            self.ecu_shared_datas,
            self.protocols,
            self.functional_groups,
            self.base_variants,
            self.ecu_variants,
        ),)

    @staticmethod
    def from_et(et_element: ElementTree.Element,
                doc_frags: List[OdxDocFragment]) -> "DiagLayerContainer":

        cat = OdxCategory.category_from_et(et_element, doc_frags, doc_type="CONTAINER")
        doc_frags = cat.odx_id.doc_fragments
        kwargs = dataclass_fields_asdict(cat)

        ecu_shared_datas = NamedItemList([
            EcuSharedData.from_et(dl_element, doc_frags)
            for dl_element in et_element.iterfind("ECU-SHARED-DATAS/ECU-SHARED-DATA")
        ])
        protocols = NamedItemList([
            Protocol.from_et(dl_element, doc_frags)
            for dl_element in et_element.iterfind("PROTOCOLS/PROTOCOL")
        ])
        functional_groups = NamedItemList([
            FunctionalGroup.from_et(dl_element, doc_frags)
            for dl_element in et_element.iterfind("FUNCTIONAL-GROUPS/FUNCTIONAL-GROUP")
        ])
        base_variants = NamedItemList([
            BaseVariant.from_et(dl_element, doc_frags)
            for dl_element in et_element.iterfind("BASE-VARIANTS/BASE-VARIANT")
        ])
        ecu_variants = NamedItemList([
            EcuVariant.from_et(dl_element, doc_frags)
            for dl_element in et_element.iterfind("ECU-VARIANTS/ECU-VARIANT")
        ])

        return DiagLayerContainer(
            ecu_shared_datas=ecu_shared_datas,
            protocols=protocols,
            functional_groups=functional_groups,
            base_variants=base_variants,
            ecu_variants=ecu_variants,
            **kwargs)

    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:
        result = super()._build_odxlinks()

        for ecu_shared_data in self.ecu_shared_datas:
            result.update(ecu_shared_data._build_odxlinks())
        for protocol in self.protocols:
            result.update(protocol._build_odxlinks())
        for functional_group in self.functional_groups:
            result.update(functional_group._build_odxlinks())
        for base_variant in self.base_variants:
            result.update(base_variant._build_odxlinks())
        for ecu_variant in self.ecu_variants:
            result.update(ecu_variant._build_odxlinks())

        return result

    def _resolve_odxlinks(self, odxlinks: OdxLinkDatabase) -> None:
        super()._resolve_odxlinks(odxlinks)

        for ecu_shared_data in self.ecu_shared_datas:
            ecu_shared_data._resolve_odxlinks(odxlinks)
        for protocol in self.protocols:
            protocol._resolve_odxlinks(odxlinks)
        for functional_group in self.functional_groups:
            functional_group._resolve_odxlinks(odxlinks)
        for base_variant in self.base_variants:
            base_variant._resolve_odxlinks(odxlinks)
        for ecu_variant in self.ecu_variants:
            ecu_variant._resolve_odxlinks(odxlinks)

    def _finalize_init(self, database: "Database", odxlinks: OdxLinkDatabase) -> None:
        super()._finalize_init(database, odxlinks)

        for ecu_shared_data in self.ecu_shared_datas:
            ecu_shared_data._finalize_init(database, odxlinks)
        for protocol in self.protocols:
            protocol._finalize_init(database, odxlinks)
        for functional_group in self.functional_groups:
            functional_group._finalize_init(database, odxlinks)
        for base_variant in self.base_variants:
            base_variant._finalize_init(database, odxlinks)
        for ecu_variant in self.ecu_variants:
            ecu_variant._finalize_init(database, odxlinks)

    def _resolve_snrefs(self, context: SnRefContext) -> None:
        super()._resolve_snrefs(context)

    @property
    def diag_layers(self) -> NamedItemList[DiagLayer]:
        return self._diag_layers

    def __getitem__(self, key: Union[int, str]) -> DiagLayer:
        return self.diag_layers[key]
