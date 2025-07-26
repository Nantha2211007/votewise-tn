import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from typing import List, Optional
import uuid
from datetime import datetime
from pydantic import BaseModel

# Get MongoDB URL from environment
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = MongoClient(mongo_url)
db = client.votewise_tn

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class Candidate(BaseModel):
    candidate_id: str
    name: str
    party: str
    constituency: str
    age: int
    education: str
    criminal_cases: int
    assets: float
    liabilities: float
    incumbent: bool = False
    photo_url: Optional[str] = None

class ManifestoPromise(BaseModel):
    promise_id: str
    party: str
    title: str
    description: str
    category: str
    fulfilled: Optional[bool] = None
    evidence_url: Optional[str] = None
    one_minute_explanation: str

class FactCheck(BaseModel):
    fact_id: str
    title: str
    description: str
    verdict: str  # "True", "False", "Misleading", "Unverified"
    source_url: Optional[str] = None
    tags: List[str] = []
    date_added: datetime
    constituency: Optional[str] = None

class CommunityPost(BaseModel):
    post_id: str
    constituency: str
    title: str
    content: str
    author_id: str  # Anonymous ID
    upvotes: int = 0
    downvotes: int = 0
    created_at: datetime
    replies: List[dict] = []

# API Endpoints

@app.get("/")
async def root():
    return {"message": "VoteWise TN API is running"}

# Constituencies
@app.get("/api/constituencies")
async def get_constituencies():
    """Get all 234 constituencies in Tamil Nadu"""
    constituencies = list(db.constituencies.find({}, {"_id": 0}))
    if not constituencies:
        # Initialize with sample data for now
        sample_constituencies = [
            {"name": "Chennai Central", "district": "Chennai", "constituency_id": "001"},
            {"name": "Chennai North", "district": "Chennai", "constituency_id": "002"},
            {"name": "Chennai South", "district": "Chennai", "constituency_id": "003"},
            {"name": "T. Nagar", "district": "Chennai", "constituency_id": "004"},
            {"name": "Mylapore", "district": "Chennai", "constituency_id": "005"},
            {"name": "Coimbatore North", "district": "Coimbatore", "constituency_id": "006"},
            {"name": "Coimbatore South", "district": "Coimbatore", "constituency_id": "007"},
            {"name": "Madurai Central", "district": "Madurai", "constituency_id": "008"},
            {"name": "Madurai North", "district": "Madurai", "constituency_id": "009"},
            {"name": "Madurai South", "district": "Madurai", "constituency_id": "010"}
        ]
        db.constituencies.insert_many(sample_constituencies)
        constituencies = sample_constituencies
    return constituencies

# Candidates
@app.get("/api/candidates")
async def get_candidates(constituency: Optional[str] = None):
    """Get candidates, optionally filtered by constituency"""
    query = {}
    if constituency:
        query["constituency"] = constituency
    
    candidates = list(db.candidates.find(query, {"_id": 0}))
    if not candidates:
        # Initialize with sample candidate data
        sample_candidates = [
            {
                "candidate_id": str(uuid.uuid4()),
                "name": "Arjun Kumar",
                "party": "DMK",
                "constituency": "Chennai Central",
                "age": 45,
                "education": "M.A. Political Science",
                "criminal_cases": 0,
                "assets": 2500000.0,
                "liabilities": 500000.0,
                "incumbent": True
            },
            {
                "candidate_id": str(uuid.uuid4()),
                "name": "Priya Sharma",
                "party": "AIADMK",
                "constituency": "Chennai Central", 
                "age": 52,
                "education": "B.A. Economics",
                "criminal_cases": 1,
                "assets": 1800000.0,
                "liabilities": 300000.0,
                "incumbent": False
            },
            {
                "candidate_id": str(uuid.uuid4()),
                "name": "Rajesh Natarajan",
                "party": "BJP",
                "constituency": "Chennai Central",
                "age": 38,
                "education": "MBA",
                "criminal_cases": 0,
                "assets": 3200000.0,
                "liabilities": 800000.0,
                "incumbent": False
            },
            {
                "candidate_id": str(uuid.uuid4()),
                "name": "Meera Devi",
                "party": "DMK",
                "constituency": "Coimbatore North",
                "age": 41,
                "education": "M.Sc. Agriculture",
                "criminal_cases": 0,
                "assets": 1500000.0,
                "liabilities": 200000.0,
                "incumbent": False
            },
            {
                "candidate_id": str(uuid.uuid4()),
                "name": "Karthik Subramanian",
                "party": "AIADMK",
                "constituency": "Coimbatore North",
                "age": 49,
                "education": "B.E. Civil Engineering",
                "criminal_cases": 2,
                "assets": 4500000.0,
                "liabilities": 1200000.0,
                "incumbent": True
            }
        ]
        db.candidates.insert_many(sample_candidates)
        candidates = sample_candidates
        
    return candidates

# Manifestos
@app.get("/api/manifestos")
async def get_manifestos(party: Optional[str] = None, category: Optional[str] = None):
    """Get manifesto promises, optionally filtered by party and category"""
    query = {}
    if party:
        query["party"] = party
    if category:
        query["category"] = category
        
    manifestos = list(db.manifestos.find(query, {"_id": 0}))
    if not manifestos:
        # Initialize with sample manifesto data
        sample_manifestos = [
            {
                "promise_id": str(uuid.uuid4()),
                "party": "DMK",
                "title": "Free Bus Travel for Women",
                "description": "Provide free bus travel for all women across Tamil Nadu in government buses",
                "category": "Transport",
                "fulfilled": True,
                "evidence_url": "https://example.com/evidence1",
                "one_minute_explanation": "DMK promised free bus travel for women during elections and implemented it successfully in 2021. All women can now travel free in government buses across TN."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "DMK",
                "title": "₹1000 Monthly Allowance for Women",
                "description": "Monthly financial assistance of ₹1000 for women heads of families",
                "category": "Social Welfare",
                "fulfilled": True,
                "evidence_url": "https://example.com/evidence2", 
                "one_minute_explanation": "Under 'Kalaignar Magalir Urimai Thogai' scheme, eligible women receive ₹1000 monthly. This was a key election promise that has been implemented."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "AIADMK",
                "title": "Free Laptop for Students",
                "description": "Provide free laptops to all higher secondary students in government schools",
                "category": "Education",
                "fulfilled": True,
                "evidence_url": "https://example.com/evidence3",
                "one_minute_explanation": "AIADMK's flagship scheme provided free laptops to students from 2011-2021. Millions of students benefited from this digital inclusion initiative."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "BJP",
                "title": "Double Farmers Income",
                "description": "Double the income of farmers through improved MSP and agricultural reforms",
                "category": "Agriculture",
                "fulfilled": False,
                "evidence_url": "https://example.com/evidence4",
                "one_minute_explanation": "BJP promised to double farmers income by 2022 at national level. However, studies show farmer incomes have not doubled in the promised timeframe."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "DMK",
                "title": "Unemployment Allowance",
                "description": "Monthly allowance of ₹1500 for unemployed youth with degrees",
                "category": "Employment",
                "fulfilled": False,
                "evidence_url": null,
                "one_minute_explanation": "DMK promised unemployment allowance during elections but implementation is still pending. Youth are waiting for this scheme to be rolled out."
            }
        ]
        db.manifestos.insert_many(sample_manifestos)
        manifestos = sample_manifestos
        
    return manifestos

# Fact Checks (Kisu Kisu)
@app.get("/api/fact-checks")
async def get_fact_checks(verdict: Optional[str] = None, constituency: Optional[str] = None):
    """Get fact-checks, optionally filtered by verdict and constituency"""
    query = {}
    if verdict:
        query["verdict"] = verdict
    if constituency:
        query["constituency"] = constituency
        
    fact_checks = list(db.fact_checks.find(query, {"_id": 0}))
    if not fact_checks:
        # Initialize with sample fact-check data
        sample_fact_checks = [
            {
                "fact_id": str(uuid.uuid4()),
                "title": "Did DMK provide 1 crore jobs in TN?",
                "description": "Viral claim that DMK government provided 1 crore jobs in Tamil Nadu",
                "verdict": "False",
                "source_url": "https://example.com/factcheck1",
                "tags": ["employment", "DMK", "jobs"],
                "date_added": datetime.now(),
                "constituency": None
            },
            {
                "fact_id": str(uuid.uuid4()),
                "title": "Are Tamil Nadu farmers getting MSP for all crops?",
                "description": "Claim that TN farmers are getting Minimum Support Price for all agricultural crops",
                "verdict": "Misleading", 
                "source_url": "https://example.com/factcheck2",
                "tags": ["agriculture", "MSP", "farmers"],
                "date_added": datetime.now(),
                "constituency": None
            },
            {
                "fact_id": str(uuid.uuid4()),
                "title": "Is Tamil the official language in TN High Court?",
                "description": "Recent claim about Tamil being made official language in Tamil Nadu High Court proceedings",
                "verdict": "True",
                "source_url": "https://example.com/factcheck3", 
                "tags": ["language", "court", "Tamil"],
                "date_added": datetime.now(),
                "constituency": None
            }
        ]
        db.fact_checks.insert_many(sample_fact_checks)
        fact_checks = sample_fact_checks
        
    return fact_checks

# Community Posts
@app.get("/api/community-posts")
async def get_community_posts(constituency: Optional[str] = None):
    """Get community posts, optionally filtered by constituency"""
    query = {}
    if constituency:
        query["constituency"] = constituency
        
    posts = list(db.community_posts.find(query, {"_id": 0}).sort("created_at", -1))
    if not posts:
        # Initialize with sample community posts
        sample_posts = [
            {
                "post_id": str(uuid.uuid4()),
                "constituency": "Chennai Central",
                "title": "What do you think about the new bus route?",
                "content": "The new MTC bus route connecting our area is really helpful. But frequency could be better during peak hours.",
                "author_id": "anon_" + str(uuid.uuid4())[:8],
                "upvotes": 12,
                "downvotes": 2,
                "created_at": datetime.now(),
                "replies": []
            },
            {
                "post_id": str(uuid.uuid4()),
                "constituency": "Chennai Central", 
                "title": "Road conditions in our area",
                "content": "The roads near the market have been in poor condition for months. When will our MLA address this issue?",
                "author_id": "anon_" + str(uuid.uuid4())[:8],
                "upvotes": 8,
                "downvotes": 1,
                "created_at": datetime.now(),
                "replies": []
            }
        ]
        db.community_posts.insert_many(sample_posts)
        posts = sample_posts
        
    return posts

@app.post("/api/community-posts")
async def create_community_post(
    constituency: str,
    title: str,
    content: str
):
    """Create a new community post"""
    post = {
        "post_id": str(uuid.uuid4()),
        "constituency": constituency,
        "title": title,
        "content": content,
        "author_id": "anon_" + str(uuid.uuid4())[:8],
        "upvotes": 0,
        "downvotes": 0,
        "created_at": datetime.now(),
        "replies": []
    }
    
    db.community_posts.insert_one(post)
    return {"message": "Post created successfully", "post_id": post["post_id"]}

# Vote on community posts
@app.post("/api/community-posts/{post_id}/vote")
async def vote_on_post(post_id: str, vote_type: str):
    """Vote on a community post (upvote/downvote)"""
    if vote_type not in ["upvote", "downvote"]:
        raise HTTPException(status_code=400, detail="Invalid vote type")
    
    update_field = "upvotes" if vote_type == "upvote" else "downvotes"
    result = db.community_posts.update_one(
        {"post_id": post_id},
        {"$inc": {update_field: 1}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {"message": f"Post {vote_type}d successfully"}

# Search endpoints
@app.get("/api/search/candidates")
async def search_candidates(q: str = Query(..., description="Search query")):
    """Search candidates by name or party"""
    query = {
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"party": {"$regex": q, "$options": "i"}},
            {"constituency": {"$regex": q, "$options": "i"}}
        ]
    }
    candidates = list(db.candidates.find(query, {"_id": 0}))
    return candidates

@app.get("/api/search/manifestos")
async def search_manifestos(q: str = Query(..., description="Search query")):
    """Search manifesto promises by title or description"""
    query = {
        "$or": [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"category": {"$regex": q, "$options": "i"}}
        ]
    }
    manifestos = list(db.manifestos.find(query, {"_id": 0}))
    return manifestos

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)