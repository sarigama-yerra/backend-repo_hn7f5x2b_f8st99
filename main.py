import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from database import create_document, get_documents, db
from schemas import Campaign

app = FastAPI(title="AdGen API", description="Generate comic-style Facebook ad campaigns")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CampaignInput(BaseModel):
    title: str = Field(..., description="Campaign title")
    objective: str = Field(..., description="Objective: Awareness, Traffic, Leads, Sales")
    product_name: str
    audience: str
    pain_points: Optional[str] = None
    benefits: Optional[str] = None
    offer: Optional[str] = None
    call_to_action: Optional[str] = None
    brand_voice: Optional[str] = None
    budget: Optional[float] = Field(None, ge=0)

@app.get("/")
def read_root():
    return {"message": "AdGen Backend Running"}

@app.get("/schema")
def get_schema():
    # Simplified schema exposure for the viewer
    return {
        "collections": [
            {
                "name": "campaign",
                "fields": [
                    "title", "objective", "product_name", "audience", "pain_points", "benefits",
                    "offer", "call_to_action", "brand_voice", "visual_style", "platforms", "budget",
                    "primary_text", "headline", "description", "hooks", "emojis", "color_palette", "hashtags"
                ]
            }
        ]
    }

@app.post("/api/generate", response_model=Campaign)
def generate_campaign(payload: CampaignInput):
    try:
        visual_style = "comic, playful, vibrant"
        # Simple deterministic generation rules
        emojis = ["💥", "🎯", "😂", "📣", "🚀"]
        hooks = [
            f"What if {payload.product_name} made {payload.audience.split(' ')[0]} easier?",
            f"Stop struggling with {payload.pain_points or 'the usual hassles'}!",
            f"Level up your {payload.objective.lower()} with a comic twist!",
        ]
        headline = f"{payload.product_name} — {payload.objective} with a Smile"
        primary_text = (
            f"{emojis[0]} POW! Meet {payload.product_name} — your sidekick for {payload.objective.lower()}.\n"
            f"{emojis[2]} No more {payload.pain_points or 'boring moments'} — {payload.benefits or 'get results fast'}.\n"
            f"{emojis[4]} {payload.call_to_action or 'Try it today'} and turn scrollers into fans!"
        )
        description = f"A comic-style, thumb-stopping creative made for {payload.audience}."
        color_palette = ["#111827", "#0EA5E9", "#22C55E", "#F59E0B", "#F43F5E"]
        hashtags = ["#FacebookAds", "#ComicStyle", "#Marketing", "#Creativity", "#AdTech"]

        doc = Campaign(
            title=payload.title,
            objective=payload.objective,
            product_name=payload.product_name,
            audience=payload.audience,
            pain_points=payload.pain_points,
            benefits=payload.benefits,
            offer=payload.offer,
            call_to_action=payload.call_to_action,
            brand_voice=payload.brand_voice,
            visual_style=visual_style,
            platforms=["Facebook"],
            budget=payload.budget,
            primary_text=primary_text,
            headline=headline,
            description=description,
            hooks=hooks,
            emojis=emojis,
            color_palette=color_palette,
            hashtags=hashtags,
        )

        # Persist to Mongo if configured
        try:
            if db is not None:
                create_document("campaign", doc)
        except Exception:
            pass

        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/campaigns")
def list_campaigns(limit: int = 20):
    try:
        if db is None:
            return []
        items = get_documents("campaign", {}, limit)
        for it in items:
            it["_id"] = str(it.get("_id"))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
