from typing import Optional

from pydantic import BaseModel, Field
from .constants import INCLUDED_FIELDS


class ImageInfo(BaseModel):
    url: str
    width: int
    height: int


class Link(BaseModel):
    href: str
    title: str


class Links(BaseModel):
    self: Optional[Link] | None = None
    next: Optional[Link] | None = None


class Ingredient(BaseModel):
    text: str
    quantity: float
    measure: Optional[str]
    food: str
    weight: float
    foodCategory: Optional[str] | None = None
    foodId: str
    image: Optional[str] | None = None


class Nutrient(BaseModel):
    label: str
    quantity: float
    unit: str


class SubDigest(BaseModel):
    label: str
    tag: str
    schemaOrgTag: Optional[str] | None = None
    total: float
    hasRDI: bool
    daily: float
    unit: str


class Digest(BaseModel):
    label: str
    tag: str
    sschemaOrgTag: Optional[str] | None = None
    total: float
    hasRDI: bool
    daily: float
    unit: str
    sub: list[SubDigest] | None = None


class Recipe(BaseModel):
    uri: str
    label: str
    image: str
    images: dict[str, ImageInfo]
    source: str
    url: str
    shareAs: str
    yield_field: float = Field(..., alias="yield")
    dietLabels: list[str]
    healthLabels: list[str]
    cautions: list[str]
    ingredientLines: list[str]
    ingredients: list[Ingredient]
    calories: float
    glycemicIndex: Optional[float] | None = None
    inflammatoryIndex: Optional[float] | None = None
    totalC02Emissions: Optional[float] | None = None
    co2EmissionsClass: Optional[str] | None = None
    totalWeight: float
    totalTime: float
    cuisineType: Optional[list[str]] | None = None
    mealType: Optional[list[str]] | None = None
    dishType: Optional[list[str]] | None = None
    instructions: Optional[list[str]] | None = None
    externalId: Optional[str] | None = None
    totalNutrients: dict[str, Nutrient]
    totalDaily: dict[str, Nutrient]
    digest: list[Digest]
    tags: Optional[list[str]] | None = None


class Hit(BaseModel):
    recipe: Recipe
    links: Links = Field(..., alias="_links")


class EdamamResponse(BaseModel):
    from_field: int = Field(..., alias="from")
    to: int
    count: int
    links: Links = Field(..., alias="_links")
    hits: list[Hit]


class ApiSettings(BaseModel):
    api_key: str
    app_id: str
    edamam_base_url: str
    included_fields: tuple = INCLUDED_FIELDS
    custom_validator_mapping: dict | None = None
    custom_validator_class: object | None = None
    db_type: str = "public"
    random: bool = False
    enable_beta: bool = False
    enable_account_user_tracking: bool = False
