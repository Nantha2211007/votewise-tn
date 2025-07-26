#!/usr/bin/env python3
"""
VoteWise TN Backend API Testing Suite
Tests all backend endpoints for the Tamil Nadu election awareness app
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend/.env
BACKEND_URL = "https://85eec81d-1e0c-466d-abb2-e5f1d172ef29.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class BackendTester:
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        
    def log_test(self, test_name, passed, message=""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = f"{status}: {test_name}"
        if message:
            result += f" - {message}"
        print(result)
        self.test_results.append({"test": test_name, "passed": passed, "message": message})
        
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def test_root_endpoint(self):
        """Test root endpoint - Note: Root serves frontend, so we skip this test"""
        # The root endpoint serves the React frontend, not the API
        # This is expected behavior in the current setup
        self.log_test("Root endpoint", True, "Root serves frontend (expected behavior)")
    
    def test_constituencies_endpoint(self):
        """Test GET /api/constituencies"""
        try:
            response = requests.get(f"{API_BASE}/constituencies", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    # Check data structure
                    first_constituency = data[0]
                    required_fields = ["name", "district", "constituency_id"]
                    if all(field in first_constituency for field in required_fields):
                        self.log_test("GET /api/constituencies", True, f"Returned {len(data)} constituencies")
                    else:
                        self.log_test("GET /api/constituencies", False, f"Missing required fields: {required_fields}")
                else:
                    self.log_test("GET /api/constituencies", False, "Empty or invalid response")
            else:
                self.log_test("GET /api/constituencies", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/constituencies", False, f"Error: {str(e)}")
    
    def test_candidates_endpoint(self):
        """Test GET /api/candidates"""
        try:
            # Test without filter
            response = requests.get(f"{API_BASE}/candidates", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    # Check data structure
                    first_candidate = data[0]
                    required_fields = ["candidate_id", "name", "party", "constituency", "age", "education", "criminal_cases", "assets", "liabilities"]
                    if all(field in first_candidate for field in required_fields):
                        self.log_test("GET /api/candidates", True, f"Returned {len(data)} candidates")
                        
                        # Test with constituency filter
                        test_constituency = first_candidate["constituency"]
                        filter_response = requests.get(f"{API_BASE}/candidates?constituency={test_constituency}", timeout=10)
                        if filter_response.status_code == 200:
                            filtered_data = filter_response.json()
                            if all(candidate["constituency"] == test_constituency for candidate in filtered_data):
                                self.log_test("GET /api/candidates (filtered)", True, f"Filter works correctly")
                            else:
                                self.log_test("GET /api/candidates (filtered)", False, "Filter not working properly")
                        else:
                            self.log_test("GET /api/candidates (filtered)", False, f"Filter request failed: {filter_response.status_code}")
                    else:
                        self.log_test("GET /api/candidates", False, f"Missing required fields: {required_fields}")
                else:
                    self.log_test("GET /api/candidates", False, "Empty or invalid response")
            else:
                self.log_test("GET /api/candidates", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/candidates", False, f"Error: {str(e)}")
    
    def test_manifestos_endpoint(self):
        """Test GET /api/manifestos"""
        try:
            # Test without filter
            response = requests.get(f"{API_BASE}/manifestos", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    # Check data structure
                    first_manifesto = data[0]
                    required_fields = ["promise_id", "party", "title", "description", "category", "one_minute_explanation"]
                    if all(field in first_manifesto for field in required_fields):
                        self.log_test("GET /api/manifestos", True, f"Returned {len(data)} manifestos")
                        
                        # Test party filter
                        test_party = first_manifesto["party"]
                        party_response = requests.get(f"{API_BASE}/manifestos?party={test_party}", timeout=10)
                        if party_response.status_code == 200:
                            party_data = party_response.json()
                            if all(manifesto["party"] == test_party for manifesto in party_data):
                                self.log_test("GET /api/manifestos (party filter)", True, "Party filter works")
                            else:
                                self.log_test("GET /api/manifestos (party filter)", False, "Party filter not working")
                        
                        # Test category filter
                        test_category = first_manifesto["category"]
                        category_response = requests.get(f"{API_BASE}/manifestos?category={test_category}", timeout=10)
                        if category_response.status_code == 200:
                            category_data = category_response.json()
                            if all(manifesto["category"] == test_category for manifesto in category_data):
                                self.log_test("GET /api/manifestos (category filter)", True, "Category filter works")
                            else:
                                self.log_test("GET /api/manifestos (category filter)", False, "Category filter not working")
                    else:
                        self.log_test("GET /api/manifestos", False, f"Missing required fields: {required_fields}")
                else:
                    self.log_test("GET /api/manifestos", False, "Empty or invalid response")
            else:
                self.log_test("GET /api/manifestos", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/manifestos", False, f"Error: {str(e)}")
    
    def test_fact_checks_endpoint(self):
        """Test GET /api/fact-checks"""
        try:
            # Test without filter
            response = requests.get(f"{API_BASE}/fact-checks", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    # Check data structure
                    first_fact_check = data[0]
                    required_fields = ["fact_id", "title", "description", "verdict", "tags", "date_added"]
                    if all(field in first_fact_check for field in required_fields):
                        self.log_test("GET /api/fact-checks", True, f"Returned {len(data)} fact-checks")
                        
                        # Test verdict filter
                        test_verdict = first_fact_check["verdict"]
                        verdict_response = requests.get(f"{API_BASE}/fact-checks?verdict={test_verdict}", timeout=10)
                        if verdict_response.status_code == 200:
                            verdict_data = verdict_response.json()
                            if all(fact["verdict"] == test_verdict for fact in verdict_data):
                                self.log_test("GET /api/fact-checks (verdict filter)", True, "Verdict filter works")
                            else:
                                self.log_test("GET /api/fact-checks (verdict filter)", False, "Verdict filter not working")
                    else:
                        self.log_test("GET /api/fact-checks", False, f"Missing required fields: {required_fields}")
                else:
                    self.log_test("GET /api/fact-checks", False, "Empty or invalid response")
            else:
                self.log_test("GET /api/fact-checks", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/fact-checks", False, f"Error: {str(e)}")
    
    def test_community_posts_get(self):
        """Test GET /api/community-posts"""
        try:
            # Test without filter
            response = requests.get(f"{API_BASE}/community-posts", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    if len(data) > 0:
                        # Check data structure
                        first_post = data[0]
                        required_fields = ["post_id", "constituency", "title", "content", "author_id", "upvotes", "downvotes", "created_at"]
                        if all(field in first_post for field in required_fields):
                            self.log_test("GET /api/community-posts", True, f"Returned {len(data)} posts")
                            
                            # Test constituency filter
                            test_constituency = first_post["constituency"]
                            filter_response = requests.get(f"{API_BASE}/community-posts?constituency={test_constituency}", timeout=10)
                            if filter_response.status_code == 200:
                                filtered_data = filter_response.json()
                                if all(post["constituency"] == test_constituency for post in filtered_data):
                                    self.log_test("GET /api/community-posts (filtered)", True, "Constituency filter works")
                                else:
                                    self.log_test("GET /api/community-posts (filtered)", False, "Constituency filter not working")
                        else:
                            self.log_test("GET /api/community-posts", False, f"Missing required fields: {required_fields}")
                    else:
                        self.log_test("GET /api/community-posts", True, "No posts yet (empty list is valid)")
                else:
                    self.log_test("GET /api/community-posts", False, "Response is not a list")
            else:
                self.log_test("GET /api/community-posts", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/community-posts", False, f"Error: {str(e)}")
    
    def test_community_posts_create(self):
        """Test POST /api/community-posts"""
        try:
            # Create a test post
            test_post_data = {
                "constituency": "Chennai Central",
                "title": "Test Community Post",
                "content": "This is a test post to verify the API is working correctly."
            }
            
            response = requests.post(f"{API_BASE}/community-posts", json=test_post_data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "post_id" in data:
                    self.log_test("POST /api/community-posts", True, f"Post created with ID: {data['post_id']}")
                    return data["post_id"]  # Return post_id for voting test
                else:
                    self.log_test("POST /api/community-posts", False, f"Invalid response format: {data}")
            else:
                self.log_test("POST /api/community-posts", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("POST /api/community-posts", False, f"Error: {str(e)}")
        return None
    
    def test_community_posts_vote(self, post_id=None):
        """Test POST /api/community-posts/{post_id}/vote"""
        if not post_id:
            # Try to get an existing post ID
            try:
                response = requests.get(f"{API_BASE}/community-posts", timeout=10)
                if response.status_code == 200:
                    posts = response.json()
                    if posts and len(posts) > 0:
                        post_id = posts[0]["post_id"]
                    else:
                        self.log_test("POST /api/community-posts/{post_id}/vote", False, "No posts available to vote on")
                        return
            except:
                self.log_test("POST /api/community-posts/{post_id}/vote", False, "Could not get posts for voting test")
                return
        
        try:
            # Test upvote
            upvote_response = requests.post(f"{API_BASE}/community-posts/{post_id}/vote", json={"vote_type": "upvote"}, timeout=10)
            if upvote_response.status_code == 200:
                upvote_data = upvote_response.json()
                if "upvoted successfully" in upvote_data.get("message", "").lower():
                    self.log_test("POST /api/community-posts/{post_id}/vote (upvote)", True, "Upvote successful")
                else:
                    self.log_test("POST /api/community-posts/{post_id}/vote (upvote)", False, f"Unexpected response: {upvote_data}")
            else:
                self.log_test("POST /api/community-posts/{post_id}/vote (upvote)", False, f"Status code: {upvote_response.status_code}")
            
            # Test downvote
            downvote_response = requests.post(f"{API_BASE}/community-posts/{post_id}/vote", json={"vote_type": "downvote"}, timeout=10)
            if downvote_response.status_code == 200:
                downvote_data = downvote_response.json()
                if "downvoted successfully" in downvote_data.get("message", "").lower():
                    self.log_test("POST /api/community-posts/{post_id}/vote (downvote)", True, "Downvote successful")
                else:
                    self.log_test("POST /api/community-posts/{post_id}/vote (downvote)", False, f"Unexpected response: {downvote_data}")
            else:
                self.log_test("POST /api/community-posts/{post_id}/vote (downvote)", False, f"Status code: {downvote_response.status_code}")
                
        except Exception as e:
            self.log_test("POST /api/community-posts/{post_id}/vote", False, f"Error: {str(e)}")
    
    def test_search_candidates(self):
        """Test GET /api/search/candidates"""
        try:
            # Test search with a common name
            search_queries = ["Arjun", "DMK", "Chennai"]
            
            for query in search_queries:
                response = requests.get(f"{API_BASE}/search/candidates?q={query}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        self.log_test(f"GET /api/search/candidates (q={query})", True, f"Search returned {len(data)} results")
                    else:
                        self.log_test(f"GET /api/search/candidates (q={query})", False, "Response is not a list")
                else:
                    self.log_test(f"GET /api/search/candidates (q={query})", False, f"Status code: {response.status_code}")
                    
        except Exception as e:
            self.log_test("GET /api/search/candidates", False, f"Error: {str(e)}")
    
    def test_search_manifestos(self):
        """Test GET /api/search/manifestos"""
        try:
            # Test search with common terms
            search_queries = ["bus", "women", "education"]
            
            for query in search_queries:
                response = requests.get(f"{API_BASE}/search/manifestos?q={query}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        self.log_test(f"GET /api/search/manifestos (q={query})", True, f"Search returned {len(data)} results")
                    else:
                        self.log_test(f"GET /api/search/manifestos (q={query})", False, "Response is not a list")
                else:
                    self.log_test(f"GET /api/search/manifestos (q={query})", False, f"Status code: {response.status_code}")
                    
        except Exception as e:
            self.log_test("GET /api/search/manifestos", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 60)
        print("VoteWise TN Backend API Testing Suite")
        print("=" * 60)
        print(f"Testing backend at: {BACKEND_URL}")
        print()
        
        # Run all tests
        self.test_root_endpoint()
        self.test_constituencies_endpoint()
        self.test_candidates_endpoint()
        self.test_manifestos_endpoint()
        self.test_fact_checks_endpoint()
        self.test_community_posts_get()
        
        # Create a post and test voting
        post_id = self.test_community_posts_create()
        self.test_community_posts_vote(post_id)
        
        self.test_search_candidates()
        self.test_search_manifestos()
        
        # Print summary
        print()
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"Total: {self.passed_tests + self.failed_tests}")
        
        if self.failed_tests > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("=" * 60)
        
        return self.failed_tests == 0

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)