"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Campaign schema for Facebook ads creator
class Campaign(BaseModel):
    """
    Campaigns collection schema for generated Facebook ad campaigns
    Collection name: "campaign"
    """
    title: str = Field(..., description="Campaign title")
    objective: str = Field(..., description="Marketing objective (Awareness, Traffic, Leads, Sales)")
    product_name: str = Field(..., description="Product or service name")
    audience: str = Field(..., description="Target audience description")
    pain_points: Optional[str] = Field(None, description="Key pain points")
    benefits: Optional[str] = Field(None, description="Key benefits/value props")
    offer: Optional[str] = Field(None, description="Offer or incentive")
    call_to_action: Optional[str] = Field(None, description="Primary CTA")
    brand_voice: Optional[str] = Field(None, description="Brand voice/tone")
    visual_style: Optional[str] = Field(None, description="Desired creative style (e.g., comic, playful)")
    platforms: Optional[List[str]] = Field(default_factory=lambda: ["Facebook"], description="Platforms")
    budget: Optional[float] = Field(None, ge=0, description="Estimated budget")

    # Generated creative fields
    primary_text: str = Field(..., description="Primary ad text")
    headline: str = Field(..., description="Ad headline")
    description: Optional[str] = Field(None, description="Ad description")
    hooks: Optional[List[str]] = Field(default_factory=list, description="Hook variations")
    emojis: Optional[List[str]] = Field(default_factory=list, description="Emojis used")
    color_palette: Optional[List[str]] = Field(default_factory=list, description="Suggested colors")
    hashtags: Optional[List[str]] = Field(default_factory=list, description="Suggested hashtags")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
