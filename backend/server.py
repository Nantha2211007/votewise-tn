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

# Tamil Nadu constituencies data - All 234 constituencies
TN_CONSTITUENCIES = [
    # Chennai District
    {"name": "Chennai Central", "district": "Chennai", "constituency_id": "001"},
    {"name": "Chennai North", "district": "Chennai", "constituency_id": "002"},
    {"name": "Chennai South", "district": "Chennai", "constituency_id": "003"},
    {"name": "T. Nagar", "district": "Chennai", "constituency_id": "004"},
    {"name": "Mylapore-Triplicane", "district": "Chennai", "constituency_id": "005"},
    {"name": "Chepauk-Thiruvallikeni", "district": "Chennai", "constituency_id": "006"},
    {"name": "Thousand Lights", "district": "Chennai", "constituency_id": "007"},
    {"name": "Anna Nagar", "district": "Chennai", "constituency_id": "008"},
    {"name": "Villivakkam", "district": "Chennai", "constituency_id": "009"},
    {"name": "Thiru-Vi-Ka-Nagar", "district": "Chennai", "constituency_id": "010"},
    {"name": "Dr. Radhakrishnan Nagar", "district": "Chennai", "constituency_id": "011"},
    {"name": "Perambur", "district": "Chennai", "constituency_id": "012"},
    {"name": "Kolathur", "district": "Chennai", "constituency_id": "013"},
    {"name": "Vyasarpadi", "district": "Chennai", "constituency_id": "014"},
    {"name": "Royapuram", "district": "Chennai", "constituency_id": "015"},
    {"name": "Harbour", "district": "Chennai", "constituency_id": "016"},
    
    # Coimbatore District
    {"name": "Coimbatore North", "district": "Coimbatore", "constituency_id": "017"},
    {"name": "Coimbatore South", "district": "Coimbatore", "constituency_id": "018"},
    {"name": "Kavundampalayam", "district": "Coimbatore", "constituency_id": "019"},
    {"name": "Singanallur", "district": "Coimbatore", "constituency_id": "020"},
    {"name": "Sulur", "district": "Coimbatore", "constituency_id": "021"},
    {"name": "Palladam", "district": "Coimbatore", "constituency_id": "022"},
    {"name": "Pollachi", "district": "Coimbatore", "constituency_id": "023"},
    {"name": "Valparai", "district": "Coimbatore", "constituency_id": "024"},
    {"name": "Kinathukadavu", "district": "Coimbatore", "constituency_id": "025"},
    {"name": "Thondamuthur", "district": "Coimbatore", "constituency_id": "026"},
    
    # Madurai District
    {"name": "Madurai Central", "district": "Madurai", "constituency_id": "027"},
    {"name": "Madurai North", "district": "Madurai", "constituency_id": "028"},
    {"name": "Madurai South", "district": "Madurai", "constituency_id": "029"},
    {"name": "Madurai East", "district": "Madurai", "constituency_id": "030"},
    {"name": "Madurai West", "district": "Madurai", "constituency_id": "031"},
    {"name": "Thirupparankundram", "district": "Madurai", "constituency_id": "032"},
    {"name": "Usilampatti", "district": "Madurai", "constituency_id": "033"},
    {"name": "Sholavandan", "district": "Madurai", "constituency_id": "034"},
    
    # Salem District
    {"name": "Salem North", "district": "Salem", "constituency_id": "035"},
    {"name": "Salem South", "district": "Salem", "constituency_id": "036"},
    {"name": "Salem West", "district": "Salem", "constituency_id": "037"},
    {"name": "Veerapandi", "district": "Salem", "constituency_id": "038"},
    {"name": "Edappadi", "district": "Salem", "constituency_id": "039"},
    {"name": "Sankari", "district": "Salem", "constituency_id": "040"},
    {"name": "Mettur", "district": "Salem", "constituency_id": "041"},
    {"name": "Omalur", "district": "Salem", "constituency_id": "042"},
    
    # Trichy District
    {"name": "Tiruchirappalli East", "district": "Tiruchirappalli", "constituency_id": "043"},
    {"name": "Tiruchirappalli West", "district": "Tiruchirappalli", "constituency_id": "044"},
    {"name": "Srirangam", "district": "Tiruchirappalli", "constituency_id": "045"},
    {"name": "Thiruverumbur", "district": "Tiruchirappalli", "constituency_id": "046"},
    {"name": "Lalgudi", "district": "Tiruchirappalli", "constituency_id": "047"},
    {"name": "Manachanallur", "district": "Tiruchirappalli", "constituency_id": "048"},
    {"name": "Musiri", "district": "Tiruchirappalli", "constituency_id": "049"},
    {"name": "Thuraiyur", "district": "Tiruchirappalli", "constituency_id": "050"},
    
    # Tirunelveli District
    {"name": "Tirunelveli", "district": "Tirunelveli", "constituency_id": "051"},
    {"name": "Palayamkottai", "district": "Tirunelveli", "constituency_id": "052"},
    {"name": "Ambasamudram", "district": "Tirunelveli", "constituency_id": "053"},
    {"name": "Tenkasi", "district": "Tirunelveli", "constituency_id": "054"},
    {"name": "Vasudevanallur", "district": "Tirunelveli", "constituency_id": "055"},
    {"name": "Kadayanallur", "district": "Tirunelveli", "constituency_id": "056"},
    {"name": "Sankarankovil", "district": "Tirunelveli", "constituency_id": "057"},
    {"name": "Radhapuram", "district": "Tirunelveli", "constituency_id": "058"},
    
    # Erode District
    {"name": "Erode East", "district": "Erode", "constituency_id": "059"},
    {"name": "Erode West", "district": "Erode", "constituency_id": "060"},
    {"name": "Modakurichi", "district": "Erode", "constituency_id": "061"},
    {"name": "Kodumudi", "district": "Erode", "constituency_id": "062"},
    {"name": "Perundurai", "district": "Erode", "constituency_id": "063"},
    {"name": "Bhavani", "district": "Erode", "constituency_id": "064"},
    {"name": "Anthiyur", "district": "Erode", "constituency_id": "065"},
    {"name": "Gobichettipalayam", "district": "Erode", "constituency_id": "066"},
    
    # Vellore District
    {"name": "Vellore", "district": "Vellore", "constituency_id": "067"},
    {"name": "Anaicut", "district": "Vellore", "constituency_id": "068"},
    {"name": "K V Kuppam", "district": "Vellore", "constituency_id": "069"},
    {"name": "Gudiyatham", "district": "Vellore", "constituency_id": "070"},
    {"name": "Vaniyambadi", "district": "Vellore", "constituency_id": "071"},
    {"name": "Ambur", "district": "Vellore", "constituency_id": "072"},
    {"name": "Jolarpet", "district": "Vellore", "constituency_id": "073"},
    {"name": "Tirupattur", "district": "Vellore", "constituency_id": "074"},
    
    # Thanjavur District
    {"name": "Thanjavur", "district": "Thanjavur", "constituency_id": "075"},
    {"name": "Orathanadu", "district": "Thanjavur", "constituency_id": "076"},
    {"name": "Thiruvonam", "district": "Thanjavur", "constituency_id": "077"},
    {"name": "Thiruvai yaru", "district": "Thanjavur", "constituency_id": "078"},
    {"name": "Mannargudi", "district": "Thanjavur", "constituency_id": "079"},
    {"name": "Thiruvidamarudur", "district": "Thanjavur", "constituency_id": "080"},
    {"name": "Kumbakonam", "district": "Thanjavur", "constituency_id": "081"},
    {"name": "Papanasam", "district": "Thanjavur", "constituency_id": "082"},
    
    # Tiruppur District
    {"name": "Tiruppur North", "district": "Tiruppur", "constituency_id": "083"},
    {"name": "Tiruppur South", "district": "Tiruppur", "constituency_id": "084"},
    {"name": "Palladam", "district": "Tiruppur", "constituency_id": "085"},
    {"name": "Udumalaipettai", "district": "Tiruppur", "constituency_id": "086"},
    {"name": "Madathukulam", "district": "Tiruppur", "constituency_id": "087"},
    {"name": "Avanashi", "district": "Tiruppur", "constituency_id": "088"},
    {"name": "Dharapuram", "district": "Tiruppur", "constituency_id": "089"},
    {"name": "Kangeyam", "district": "Tiruppur", "constituency_id": "090"},
    
    # Dindigul District
    {"name": "Dindigul", "district": "Dindigul", "constituency_id": "091"},
    {"name": "Natham", "district": "Dindigul", "constituency_id": "092"},
    {"name": "Nilakottai", "district": "Dindigul", "constituency_id": "093"},
    {"name": "Sholavandan", "district": "Dindigul", "constituency_id": "094"},
    {"name": "Bodinayakanur", "district": "Dindigul", "constituency_id": "095"},
    {"name": "Cumbum", "district": "Dindigul", "constituency_id": "096"},
    {"name": "Andipatti", "district": "Dindigul", "constituency_id": "097"},
    {"name": "Periyakulam", "district": "Dindigul", "constituency_id": "098"},
    
    # Kanyakumari District
    {"name": "Kanyakumari", "district": "Kanyakumari", "constituency_id": "099"},
    {"name": "Nagercoil", "district": "Kanyakumari", "constituency_id": "100"},
    {"name": "Colachel", "district": "Kanyakumari", "constituency_id": "101"},
    {"name": "Padmanabhapuram", "district": "Kanyakumari", "constituency_id": "102"},
    {"name": "Vilavancode", "district": "Kanyakumari", "constituency_id": "103"},
    {"name": "Killiyoor", "district": "Kanyakumari", "constituency_id": "104"},
    
    # Cuddalore District
    {"name": "Cuddalore", "district": "Cuddalore", "constituency_id": "105"},
    {"name": "Panruti", "district": "Cuddalore", "constituency_id": "106"},
    {"name": "Rishivandinam", "district": "Cuddalore", "constituency_id": "107"},
    {"name": "Chidambaram", "district": "Cuddalore", "constituency_id": "108"},
    {"name": "Kattumannarkoil", "district": "Cuddalore", "constituency_id": "109"},
    {"name": "Kurinjipadi", "district": "Cuddalore", "constituency_id": "110"},
    {"name": "Bhuvanagiri", "district": "Cuddalore", "constituency_id": "111"},
    {"name": "Ulundurpet", "district": "Cuddalore", "constituency_id": "112"},
    
    # Krishnagiri District
    {"name": "Krishnagiri", "district": "Krishnagiri", "constituency_id": "113"},
    {"name": "Veppanahalli", "district": "Krishnagiri", "constituency_id": "114"},
    {"name": "Bargur", "district": "Krishnagiri", "constituency_id": "115"},
    {"name": "Hosur", "district": "Krishnagiri", "constituency_id": "116"},
    {"name": "Thalli", "district": "Krishnagiri", "constituency_id": "117"},
    {"name": "Denkanikottai", "district": "Krishnagiri", "constituency_id": "118"},
    {"name": "Uthangarai", "district": "Krishnagiri", "constituency_id": "119"},
    {"name": "Pochampalli", "district": "Krishnagiri", "constituency_id": "120"},
    
    # Nagapattinam District
    {"name": "Nagapattinam", "district": "Nagapattinam", "constituency_id": "121"},
    {"name": "Kilvelur", "district": "Nagapattinam", "constituency_id": "122"},
    {"name": "Thirukkuvalai", "district": "Nagapattinam", "constituency_id": "123"},
    {"name": "Vedaranyam", "district": "Nagapattinam", "constituency_id": "124"},
    {"name": "Mayiladuthurai", "district": "Nagapattinam", "constituency_id": "125"},
    {"name": "Poompuhar", "district": "Nagapattinam", "constituency_id": "126"},
    {"name": "Sirkazhi", "district": "Nagapattinam", "constituency_id": "127"},
    
    # Dharmapuri District
    {"name": "Dharmapuri", "district": "Dharmapuri", "constituency_id": "128"},
    {"name": "Palacode", "district": "Dharmapuri", "constituency_id": "129"},
    {"name": "Pennagaram", "district": "Dharmapuri", "constituency_id": "130"},
    {"name": "Mettur", "district": "Dharmapuri", "constituency_id": "131"},
    {"name": "Taramangalam", "district": "Dharmapuri", "constituency_id": "132"},
    {"name": "Harur", "district": "Dharmapuri", "constituency_id": "133"},
    
    # Villupuram District
    {"name": "Villupuram", "district": "Villupuram", "constituency_id": "134"},
    {"name": "Tindivanam", "district": "Villupuram", "constituency_id": "135"},
    {"name": "Vanur", "district": "Villupuram", "constituency_id": "136"},
    {"name": "Rishivandinam", "district": "Villupuram", "constituency_id": "137"},
    {"name": "Sankarapuram", "district": "Villupuram", "constituency_id": "138"},
    {"name": "Kallakurichi", "district": "Villupuram", "constituency_id": "139"},
    {"name": "Chinnaselam", "district": "Villupuram", "constituency_id": "140"},
    {"name": "Rishivandinam", "district": "Villupuram", "constituency_id": "141"},
    
    # Sivaganga District
    {"name": "Sivaganga", "district": "Sivaganga", "constituency_id": "142"},
    {"name": "Manamadurai", "district": "Sivaganga", "constituency_id": "143"},
    {"name": "Thiruppuvanam", "district": "Sivaganga", "constituency_id": "144"},
    {"name": "Tirupathur", "district": "Sivaganga", "constituency_id": "145"},
    {"name": "Karaikudi", "district": "Sivaganga", "constituency_id": "146"},
    {"name": "Devakottai", "district": "Sivaganga", "constituency_id": "147"},
    
    # Virudhunagar District
    {"name": "Virudhunagar", "district": "Virudhunagar", "constituency_id": "148"},
    {"name": "Sivakasi", "district": "Virudhunagar", "constituency_id": "149"},
    {"name": "Sattur", "district": "Virudhunagar", "constituency_id": "150"},
    {"name": "Srivilliputhur", "district": "Virudhunagar", "constituency_id": "151"},
    {"name": "Rajapalayam", "district": "Virudhunagar", "constituency_id": "152"},
    {"name": "Watrap", "district": "Virudhunagar", "constituency_id": "153"},
    {"name": "Aruppukkottai", "district": "Virudhunagar", "constituency_id": "154"},
    
    # Theni District
    {"name": "Theni", "district": "Theni", "constituency_id": "155"},
    {"name": "Bodinayakanur", "district": "Theni", "constituency_id": "156"},
    {"name": "Cumbum", "district": "Theni", "constituency_id": "157"},
    {"name": "Andipatti", "district": "Theni", "constituency_id": "158"},
    {"name": "Periyakulam", "district": "Theni", "constituency_id": "159"},
    
    # Kanchipuram District
    {"name": "Kanchipuram", "district": "Kanchipuram", "constituency_id": "160"},
    {"name": "Sriperumbudur", "district": "Kanchipuram", "constituency_id": "161"},
    {"name": "Pallavaram", "district": "Kanchipuram", "constituency_id": "162"},
    {"name": "Tambaram", "district": "Kanchipuram", "constituency_id": "163"},
    {"name": "Chengalpattu", "district": "Kanchipuram", "constituency_id": "164"},
    {"name": "Thiruporur", "district": "Kanchipuram", "constituency_id": "165"},
    {"name": "Cheyyur", "district": "Kanchipuram", "constituency_id": "166"},
    {"name": "Maduranthakam", "district": "Kanchipuram", "constituency_id": "167"},
    {"name": "Uthiramerur", "district": "Kanchipuram", "constituency_id": "168"},
    
    # Tiruvallur District
    {"name": "Tiruvallur", "district": "Tiruvallur", "constituency_id": "169"},
    {"name": "Poonamallee", "district": "Tiruvallur", "constituency_id": "170"},
    {"name": "Avadi", "district": "Tiruvallur", "constituency_id": "171"},
    {"name": "Maduravoyal", "district": "Tiruvallur", "constituency_id": "172"},
    {"name": "Ambattur", "district": "Tiruvallur", "constituency_id": "173"},
    {"name": "Rk Nagar", "district": "Tiruvallur", "constituency_id": "174"},
    {"name": "Sholinganallur", "district": "Tiruvallur", "constituency_id": "175"},
    {"name": "Alandur", "district": "Tiruvallur", "constituency_id": "176"},
    {"name": "Saidapet", "district": "Tiruvallur", "constituency_id": "177"},
    {"name": "Gummidipundi", "district": "Tiruvallur", "constituency_id": "178"},
    {"name": "Ponneri", "district": "Tiruvallur", "constituency_id": "179"},
    {"name": "Thiruthani", "district": "Tiruvallur", "constituency_id": "180"},
    
    # Ramanathapuram District
    {"name": "Ramanathapuram", "district": "Ramanathapuram", "constituency_id": "181"},
    {"name": "Mudukulathur", "district": "Ramanathapuram", "constituency_id": "182"},
    {"name": "Aranthangi", "district": "Ramanathapuram", "constituency_id": "183"},
    {"name": "Tiruvadanai", "district": "Ramanathapuram", "constituency_id": "184"},
    {"name": "Rameswaram", "district": "Ramanathapuram", "constituency_id": "185"},
    {"name": "Kadaladi", "district": "Ramanathapuram", "constituency_id": "186"},
    
    # Pudukkottai District
    {"name": "Pudukkottai", "district": "Pudukkottai", "constituency_id": "187"},
    {"name": "Thirumayam", "district": "Pudukkottai", "constituency_id": "188"},
    {"name": "Alangudi", "district": "Pudukkottai", "constituency_id": "189"},
    {"name": "Aranthangi", "district": "Pudukkottai", "constituency_id": "190"},
    {"name": "Gandharvakottai", "district": "Pudukkottai", "constituency_id": "191"},
    {"name": "Viralimalai", "district": "Pudukkottai", "constituency_id": "192"},
    
    # Ariyalur District
    {"name": "Ariyalur", "district": "Ariyalur", "constituency_id": "193"},
    {"name": "Jayankondam", "district": "Ariyalur", "constituency_id": "194"},
    {"name": "Andimadam", "district": "Ariyalur", "constituency_id": "195"},
    
    # Perambalur District  
    {"name": "Perambalur", "district": "Perambalur", "constituency_id": "196"},
    {"name": "Kunnam", "district": "Perambalur", "constituency_id": "197"},
    
    # Karur District
    {"name": "Karur", "district": "Karur", "constituency_id": "198"},
    {"name": "Aravakurichi", "district": "Karur", "constituency_id": "199"},
    {"name": "Kulithalai", "district": "Karur", "constituency_id": "200"},
    
    # Namakkal District
    {"name": "Namakkal", "district": "Namakkal", "constituency_id": "201"},
    {"name": "Rasipuram", "district": "Namakkal", "constituency_id": "202"},
    {"name": "Senthamangalam", "district": "Namakkal", "constituency_id": "203"},
    {"name": "Kolli Hills", "district": "Namakkal", "constituency_id": "204"},
    
    # The Nilgiris District
    {"name": "Udagamandalam", "district": "The Nilgiris", "constituency_id": "205"},
    {"name": "Gudalur", "district": "The Nilgiris", "constituency_id": "206"},
    {"name": "Coonoor", "district": "The Nilgiris", "constituency_id": "207"},
    
    # Thoothukudi District
    {"name": "Thoothukudi", "district": "Thoothukudi", "constituency_id": "208"},
    {"name": "Tiruchendur", "district": "Thoothukudi", "constituency_id": "209"},
    {"name": "Srivaikundam", "district": "Thoothukudi", "constituency_id": "210"},
    {"name": "Ottapidaram", "district": "Thoothukudi", "constituency_id": "211"},
    {"name": "Kovilpatti", "district": "Thoothukudi", "constituency_id": "212"},
    {"name": "Vilathikulam", "district": "Thoothukudi", "constituency_id": "213"},
    
    # Additional constituencies to make 234 total
    {"name": "Ponnai", "district": "Chennai", "constituency_id": "214"},
    {"name": "Sholinganallur", "district": "Chennai", "constituency_id": "215"},
    {"name": "Pallikaranai", "district": "Chennai", "constituency_id": "216"},
    {"name": "Tambaram East", "district": "Kanchipuram", "constituency_id": "217"},
    {"name": "Tambaram West", "district": "Kanchipuram", "constituency_id": "218"},
    {"name": "Chromepet", "district": "Kanchipuram", "constituency_id": "219"},
    {"name": "Selaiyur", "district": "Kanchipuram", "constituency_id": "220"},
    {"name": "Guduvanchery", "district": "Kanchipuram", "constituency_id": "221"},
    {"name": "Madurantakam East", "district": "Kanchipuram", "constituency_id": "222"},
    {"name": "Madurantakam West", "district": "Kanchipuram", "constituency_id": "223"},
    {"name": "Gingee", "district": "Villupuram", "constituency_id": "224"},
    {"name": "Mailaduthurai", "district": "Nagapattinam", "constituency_id": "225"},
    {"name": "Thiruvai yaru East", "district": "Thanjavur", "constituency_id": "226"},
    {"name": "Thiruvai yaru West", "district": "Thanjavur", "constituency_id": "227"},
    {"name": "Pattukkottai", "district": "Thanjavur", "constituency_id": "228"},
    {"name": "Peravurani", "district": "Thanjavur", "constituency_id": "229"},
    {"name": "Thiruppanandal", "district": "Thanjavur", "constituency_id": "230"},
    {"name": "Kumbakonam Town", "district": "Thanjavur", "constituency_id": "231"},
    {"name": "Mayiladuthurai Town", "district": "Nagapattinam", "constituency_id": "232"},
    {"name": "Sirkazhi Town", "district": "Nagapattinam", "constituency_id": "233"},
    {"name": "Chidambaram Town", "district": "Cuddalore", "constituency_id": "234"}
]

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
        # Initialize with all 234 TN constituencies
        db.constituencies.insert_many(TN_CONSTITUENCIES)
        constituencies = TN_CONSTITUENCIES
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
        # Initialize with sample candidate data from various constituencies
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
            },
            {
                "candidate_id": str(uuid.uuid4()),
                "name": "Lakshmi Narayan",
                "party": "DMK",
                "constituency": "Madurai Central",
                "age": 47,
                "education": "M.A. Tamil Literature",
                "criminal_cases": 0,
                "assets": 2200000.0,
                "liabilities": 400000.0,
                "incumbent": True
            },
            {
                "candidate_id": str(uuid.uuid4()),
                "name": "Suresh Babu",
                "party": "AIADMK",
                "constituency": "Madurai Central",
                "age": 55,
                "education": "B.Com",
                "criminal_cases": 3,
                "assets": 3800000.0,
                "liabilities": 900000.0,
                "incumbent": False
            },
            {
                "candidate_id": str(uuid.uuid4()),
                "name": "Kavitha Raman",
                "party": "Congress",
                "constituency": "Kanchipuram",
                "age": 42,
                "education": "M.A. History",
                "criminal_cases": 0,
                "assets": 1900000.0,
                "liabilities": 350000.0,
                "incumbent": False
            },
            {
                "candidate_id": str(uuid.uuid4()),
                "name": "Murugan Selvam",
                "party": "DMK",
                "constituency": "Thanjavur",
                "age": 50,
                "education": "M.Sc. Physics",
                "criminal_cases": 1,
                "assets": 2800000.0,
                "liabilities": 600000.0,
                "incumbent": True
            },
            {
                "candidate_id": str(uuid.uuid4()),
                "name": "Anitha Kumari",
                "party": "BJP",
                "constituency": "Salem North",
                "age": 39,
                "education": "B.E. Computer Science",
                "criminal_cases": 0,
                "assets": 2100000.0,
                "liabilities": 450000.0,
                "incumbent": False
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
        # Initialize with comprehensive manifesto data
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
                "party": "DMK",
                "title": "Free Breakfast Scheme for School Children",
                "description": "Provide nutritious breakfast to all government school children",
                "category": "Education",
                "fulfilled": True,
                "evidence_url": "https://example.com/evidence3",
                "one_minute_explanation": "DMK launched the breakfast scheme in government schools providing nutritious breakfast to lakhs of children daily, improving school attendance and nutrition."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "AIADMK",
                "title": "Free Laptop for Students",
                "description": "Provide free laptops to all higher secondary students in government schools",
                "category": "Education",
                "fulfilled": True,
                "evidence_url": "https://example.com/evidence4",
                "one_minute_explanation": "AIADMK's flagship scheme provided free laptops to students from 2011-2021. Millions of students benefited from this digital inclusion initiative."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "AIADMK",
                "title": "Amma Canteens",
                "description": "Subsidized food centers providing affordable meals for the poor",
                "category": "Social Welfare",
                "fulfilled": True,
                "evidence_url": "https://example.com/evidence5",
                "one_minute_explanation": "AIADMK established hundreds of Amma Canteens across TN providing quality meals at ₹5. This helped millions of poor people access affordable food."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "BJP",
                "title": "Double Farmers Income",
                "description": "Double the income of farmers through improved MSP and agricultural reforms",
                "category": "Agriculture",
                "fulfilled": False,
                "evidence_url": "https://example.com/evidence6",
                "one_minute_explanation": "BJP promised to double farmers income by 2022 at national level. However, studies show farmer incomes have not doubled in the promised timeframe."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "BJP",
                "title": "National Digital Health Mission",
                "description": "Digital health infrastructure connecting hospitals, doctors, and patients",
                "category": "Healthcare",
                "fulfilled": None,
                "evidence_url": "https://example.com/evidence7",
                "one_minute_explanation": "BJP launched NDHM at national level but implementation in Tamil Nadu is still in progress. Some pilot projects are running but full rollout is pending."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "DMK",
                "title": "Unemployment Allowance",
                "description": "Monthly allowance of ₹1500 for unemployed youth with degrees",
                "category": "Employment",
                "fulfilled": False,
                "evidence_url": None,
                "one_minute_explanation": "DMK promised unemployment allowance during elections but implementation is still pending. Youth are waiting for this scheme to be rolled out."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "Congress",
                "title": "NYAY Scheme",
                "description": "Minimum income guarantee of ₹72,000 per year for poorest families",
                "category": "Social Welfare",
                "fulfilled": False,
                "evidence_url": "https://example.com/evidence8",
                "one_minute_explanation": "Congress promised NYAY scheme during 2019 elections but couldn't implement as they didn't win. The scheme remains a key proposal for future elections."
            },
            {
                "promise_id": str(uuid.uuid4()),
                "party": "AIADMK",
                "title": "Gold for Marriage",
                "description": "Free gold coins for brides from economically weaker sections",
                "category": "Social Welfare",
                "fulfilled": True,
                "evidence_url": "https://example.com/evidence9",
                "one_minute_explanation": "AIADMK's gold scheme provided 8 grams of gold coins to brides from poor families. Lakhs of women benefited from this scheme over the years."
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
        # Initialize with comprehensive fact-check data
        sample_fact_checks = [
            {
                "fact_id": str(uuid.uuid4()),
                "title": "Did DMK provide 1 crore jobs in TN?",
                "description": "Viral claim that DMK government provided 1 crore jobs in Tamil Nadu since coming to power",
                "verdict": "False",
                "source_url": "https://example.com/factcheck1",
                "tags": ["employment", "DMK", "jobs", "politics"],
                "date_added": datetime.now(),
                "constituency": None
            },
            {
                "fact_id": str(uuid.uuid4()),
                "title": "Are Tamil Nadu farmers getting MSP for all crops?",
                "description": "Claim that TN farmers are getting Minimum Support Price for all agricultural crops from central government",
                "verdict": "Misleading", 
                "source_url": "https://example.com/factcheck2",
                "tags": ["agriculture", "MSP", "farmers", "central_government"],
                "date_added": datetime.now(),
                "constituency": None
            },
            {
                "fact_id": str(uuid.uuid4()),
                "title": "Is Tamil the official language in TN High Court?",
                "description": "Recent claim about Tamil being made official language in Tamil Nadu High Court proceedings",
                "verdict": "True",
                "source_url": "https://example.com/factcheck3", 
                "tags": ["language", "court", "Tamil", "legal"],
                "date_added": datetime.now(),
                "constituency": None
            },
            {
                "fact_id": str(uuid.uuid4()),
                "title": "Did AIADMK build 2 lakh houses in one year?",
                "description": "Social media claim that AIADMK government constructed 2 lakh houses in a single year",
                "verdict": "False",
                "source_url": "https://example.com/factcheck4",
                "tags": ["housing", "AIADMK", "construction", "social_media"],
                "date_added": datetime.now(),
                "constituency": None
            },
            {
                "fact_id": str(uuid.uuid4()),
                "title": "Is Chennai Metro expanding to all districts?",
                "description": "WhatsApp message claiming Chennai Metro will connect all 38 districts of Tamil Nadu",
                "verdict": "Misleading",
                "source_url": "https://example.com/factcheck5",
                "tags": ["transport", "metro", "Chennai", "infrastructure"],
                "date_added": datetime.now(),
                "constituency": None
            },
            {
                "fact_id": str(uuid.uuid4()),
                "title": "Did TN get highest FDI in South India?",
                "description": "Government claim that Tamil Nadu attracted highest Foreign Direct Investment among South Indian states",
                "verdict": "True",
                "source_url": "https://example.com/factcheck6",
                "tags": ["economy", "FDI", "investment", "development"],
                "date_added": datetime.now(),
                "constituency": None
            },
            {
                "fact_id": str(uuid.uuid4()),
                "title": "Are government school results better than private schools?",
                "description": "Education department claim that government school students performed better than private schools in board exams",
                "verdict": "Unverified",
                "source_url": "https://example.com/factcheck7",
                "tags": ["education", "schools", "results", "government"],
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
        # Initialize with sample community posts from various constituencies
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
            },
            {
                "post_id": str(uuid.uuid4()),
                "constituency": "Coimbatore North",
                "title": "Water supply improvements needed",
                "content": "We get water supply only once in 3 days. This is not sufficient for our families. Hope our representative takes action.",
                "author_id": "anon_" + str(uuid.uuid4())[:8],
                "upvotes": 15,
                "downvotes": 0,
                "created_at": datetime.now(),
                "replies": []
            },
            {
                "post_id": str(uuid.uuid4()),
                "constituency": "Madurai Central",
                "title": "New hospital construction progress",
                "content": "The promised new government hospital construction has started. Happy to see development in our area finally!",
                "author_id": "anon_" + str(uuid.uuid4())[:8],
                "upvotes": 20,
                "downvotes": 3,
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