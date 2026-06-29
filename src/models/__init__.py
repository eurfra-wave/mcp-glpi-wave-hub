"""Paquete models - Exporta todos los modelos."""

from src.models.ticket import (
    TicketBase,
    TicketFollowup,
    TicketTask,
    TicketSolution,
    TicketWithDetails,
    TicketCreateInput,
    TicketUpdateInput,
)
from src.models.asset import (
    ComputerBase,
    ComputerWithDetails,
    PrinterBase,
    MonitorBase,
    PhoneBase,
    NetworkEquipmentBase,
    NetworkEquipmentWithPorts,
    AssetCreateInput,
    ComputerCreateInput,
    PrinterCreateInput,
    NetworkEquipmentCreateInput,
    AssetUpdateInput,
)
from src.models.software import SoftwareBase, SoftwareCreateInput
from src.models.problem import ProblemBase, ProblemCreateInput, ProblemUpdateInput
from src.models.change import ChangeBase, ChangeCreateInput, ChangeUpdateInput
from src.models.user import UserBase, UserCreateInput, GroupBase, GroupCreateInput, GroupUserInput
from src.models.project import ProjectBase, ProjectCreateInput, ProjectUpdateInput
from src.models.kb import KnowbaseItemBase, KnowbaseItemCreateInput
from src.models.contract import ContractBase, ContractCreateInput, SupplierBase, SupplierCreateInput
from src.models.location import LocationBase, LocationCreateInput, EntityBase, CategoryBase
from src.models.document import DocumentBase

__all__ = [
    # Tickets
    "TicketBase",
    "TicketFollowup",
    "TicketTask",
    "TicketSolution",
    "TicketWithDetails",
    "TicketCreateInput",
    "TicketUpdateInput",
    # Assets
    "ComputerBase",
    "ComputerWithDetails",
    "PrinterBase",
    "MonitorBase",
    "PhoneBase",
    "NetworkEquipmentBase",
    "NetworkEquipmentWithPorts",
    "AssetCreateInput",
    "ComputerCreateInput",
    "PrinterCreateInput",
    "NetworkEquipmentCreateInput",
    "AssetUpdateInput",
    # Software
    "SoftwareBase",
    "SoftwareCreateInput",
    # Problems
    "ProblemBase",
    "ProblemCreateInput",
    "ProblemUpdateInput",
    # Changes
    "ChangeBase",
    "ChangeCreateInput",
    "ChangeUpdateInput",
    # Users/Groups
    "UserBase",
    "UserCreateInput",
    "GroupBase",
    "GroupCreateInput",
    "GroupUserInput",
    # Projects
    "ProjectBase",
    "ProjectCreateInput",
    "ProjectUpdateInput",
    # KB
    "KnowbaseItemBase",
    "KnowbaseItemCreateInput",
    # Contracts/Suppliers
    "ContractBase",
    "ContractCreateInput",
    "SupplierBase",
    "SupplierCreateInput",
    # Locations/Entities
    "LocationBase",
    "LocationCreateInput",
    "EntityBase",
    "CategoryBase",
    # Documents
    "DocumentBase",
]