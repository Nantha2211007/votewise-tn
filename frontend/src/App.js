import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [currentLanguage, setCurrentLanguage] = useState(null); // null initially for language selection
  const [activeTab, setActiveTab] = useState('candidates');
  const [loading, setLoading] = useState(false);
  
  // Data states
  const [constituencies, setConstituencies] = useState([]);
  const [selectedConstituency, setSelectedConstituency] = useState('');
  const [candidates, setCandidates] = useState([]);
  const [manifestos, setManifestos] = useState([]);
  const [factChecks, setFactChecks] = useState([]);
  const [communityPosts, setCommunityPosts] = useState([]);
  
  // Filter states
  const [selectedParty, setSelectedParty] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedVerdict, setSelectedVerdict] = useState('');
  const [showOnlyFactChecked, setShowOnlyFactChecked] = useState(false);
  
  // Search states
  const [searchQuery, setSearchQuery] = useState('');
  
  // Community post form
  const [newPost, setNewPost] = useState({ title: '', content: '' });

  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Translations
  const translations = {
    english: {
      appTitle: 'VoteWise TN',
      tagline: 'Make Informed Decisions. Empower Your Vote.',
      languageSelection: {
        title: 'Welcome to VoteWise TN',
        subtitle: 'Choose your preferred language',
        selectEnglish: 'Continue in English',
        selectTamil: 'தமிழில் தொடரவும்'
      },
      tabs: {
        candidates: 'Candidates',
        manifestos: 'Manifestos', 
        factcheck: 'Kisu Kisu',
        community: 'Community'
      },
      candidatesTab: {
        title: 'Compare Candidates',
        selectConstituency: 'Select Constituency',
        allConstituencies: 'All Constituencies',
        name: 'Name',
        party: 'Party',
        age: 'Age',
        education: 'Education',
        criminal: 'Criminal Cases',
        assets: 'Assets',
        liabilities: 'Liabilities',
        incumbent: 'Incumbent',
        search: 'Search candidates...'
      },
      manifestosTab: {
        title: 'Party Manifestos',
        allParties: 'All Parties',
        allCategories: 'All Categories',
        fulfilled: 'Fulfilled',
        notFulfilled: 'Not Fulfilled',
        pending: 'Pending',
        readMore: 'Read More',
        readLess: 'Read Less',
        evidence: 'Evidence',
        search: 'Search promises...'
      },
      factCheckTab: {
        title: 'Fact Checks (Kisu Kisu)',
        onlyFactChecked: 'Show only fact-checked news',
        allVerdicts: 'All Verdicts',
        true: 'True',
        false: 'False', 
        misleading: 'Misleading',
        unverified: 'Unverified',
        source: 'Source',
        tags: 'Tags'
      },
      communityTab: {
        title: 'Community Discussion',
        newPost: 'New Post',
        postTitle: 'Post Title',
        postContent: 'What would you like to discuss?',
        submit: 'Submit Post',
        upvote: 'Upvote',
        downvote: 'Downvote',
        replies: 'replies'
      },
      common: {
        loading: 'Loading...',
        error: 'Error loading data',
        noData: 'No data available',
        anonymous: 'Anonymous'
      }
    },
    tamil: {
      appTitle: 'வோட்வைஸ் TN',
      tagline: 'தகவலறிந்த முடிவுகள் எடுங்கள். உங்கள் வாக்கை வலுப்படுத்துங்கள்.',
      languageSelection: {
        title: 'வோட்வைஸ் TN க்கு வரவேற்கிறோம்',
        subtitle: 'உங்கள் விருப்பமான மொழியைத் தேர்ந்தெடுக்கவும்',
        selectEnglish: 'Continue in English',
        selectTamil: 'தமிழில் தொடரவும்'
      },
      tabs: {
        candidates: 'வேட்பாளர்கள்',
        manifestos: 'தேர்தல் அறிக்கைகள்',
        factcheck: 'கிசு கிசு',
        community: 'சமூகம்'
      },
      candidatesTab: {
        title: 'வேட்பாளர்களை ஒப்பிடுங்கள்',
        selectConstituency: 'தொகுதியைத் தேர்ந்தெடுக்கவும்',
        allConstituencies: 'அனைத்து தொகுதிகள்',
        name: 'பெயர்',
        party: 'கட்சி',
        age: 'வயது',
        education: 'கல்வி',
        criminal: 'குற்றவியல் வழக்குகள்',
        assets: 'சொத்துக்கள்',
        liabilities: 'கடன்கள்',
        incumbent: 'தற்போதைய',
        search: 'வேட்பாளர்களைத் தேடுங்கள்...'
      },
      manifestosTab: {
        title: 'கட்சி அறிக்கைகள்',
        allParties: 'அனைத்து கட்சிகள்',
        allCategories: 'அனைத்து பிரிவுகள்',
        fulfilled: 'நிறைவேற்றப்பட்டது',
        notFulfilled: 'நிறைவேற்றப்படவில்லை',
        pending: 'நிலுவையில்',
        readMore: 'மேலும் படிக்க',
        readLess: 'குறைவாக படிக்க',
        evidence: 'ஆதாரம்',
        search: 'வாக்குறுதிகளைத் தேடுங்கள்...'
      },
      factCheckTab: {
        title: 'உண்மை சரிபார்ப்பு (கிசு கிசு)',
        onlyFactChecked: 'சரிபார்க்கப்பட்ட செய்திகளை மட்டும் காட்டு',
        allVerdicts: 'அனைத்து தீர்ப்புகள்',
        true: 'உண்மை',
        false: 'பொய்',
        misleading: 'தவறான வழிகாட்டுதல்',
        unverified: 'சரிபார்க்கப்படவில்லை',
        source: 'ஆதாரம்',
        tags: 'குறிச்சொற்கள்'
      },
      communityTab: {
        title: 'சமூக விவாதம்',
        newPost: 'புதிய இடுகை',
        postTitle: 'இடுகை தலைப்பு',
        postContent: 'என்ன பற்றி விவாதிக்க விரும்புகிறீர்கள்?',
        submit: 'இடுகை போடுக',
        upvote: 'ஆதரவு',
        downvote: 'எதிர்ப்பு',
        replies: 'பதில்கள்'
      },
      common: {
        loading: 'ஏற்றுகிறது...',
        error: 'தரவு ஏற்றுவதில் பிழை',
        noData: 'தரவு இல்லை',
        anonymous: 'அநாமதேய'
      }
    }
  };

  const t = currentLanguage ? translations[currentLanguage] : translations.english;

  // Language Selection Component
  const renderLanguageSelection = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-700 to-red-600 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 md:p-12 max-w-md w-full text-center">
        <div className="mb-8">
          <img 
            src="https://images.unsplash.com/photo-1708346561250-ea0f8b54bc1c" 
            alt="Tamil Nadu Culture"
            className="w-32 h-32 mx-auto rounded-full object-cover mb-6 shadow-lg"
          />
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome to VoteWise TN
          </h1>
          <h2 className="text-xl font-semibold text-gray-700 mb-1">
            வோட்வைஸ் TN க்கு வரவேற்கிறோம்
          </h2>
          <p className="text-gray-600 mb-8">
            Choose your preferred language<br/>
            உங்கள் விருப்பமான மொழியைத் தேர்ந்தெடுக்கவும்
          </p>
        </div>
        
        <div className="space-y-4">
          <button
            onClick={() => setCurrentLanguage('english')}
            className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:bg-blue-700 transition-colors duration-200 shadow-md"
          >
            Continue in English
          </button>
          <button
            onClick={() => setCurrentLanguage('tamil')}
            className="w-full bg-red-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:bg-red-700 transition-colors duration-200 shadow-md"
          >
            தமிழில் தொடரவும்
          </button>
        </div>
      </div>
    </div>
  );

  // API calls
  const fetchConstituencies = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/constituencies`);
      setConstituencies(response.data);
    } catch (error) {
      console.error('Error fetching constituencies:', error);
    }
  };

  const fetchCandidates = async (constituency = '') => {
    try {
      setLoading(true);
      const params = constituency ? `?constituency=${encodeURIComponent(constituency)}` : '';
      const response = await axios.get(`${API_BASE_URL}/api/candidates${params}`);
      setCandidates(response.data);
    } catch (error) {
      console.error('Error fetching candidates:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchManifestos = async (party = '', category = '') => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (party) params.append('party', party);
      if (category) params.append('category', category);
      const response = await axios.get(`${API_BASE_URL}/api/manifestos?${params}`);
      setManifestos(response.data);
    } catch (error) {
      console.error('Error fetching manifestos:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFactChecks = async (verdict = '') => {
    try {
      setLoading(true);
      const params = verdict ? `?verdict=${encodeURIComponent(verdict)}` : '';
      const response = await axios.get(`${API_BASE_URL}/api/fact-checks${params}`);
      setFactChecks(response.data);
    } catch (error) {
      console.error('Error fetching fact checks:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCommunityPosts = async (constituency = '') => {
    try {
      setLoading(true);
      const params = constituency ? `?constituency=${encodeURIComponent(constituency)}` : '';
      const response = await axios.get(`${API_BASE_URL}/api/community-posts${params}`);
      setCommunityPosts(response.data);
    } catch (error) {
      console.error('Error fetching community posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const submitCommunityPost = async () => {
    if (!newPost.title.trim() || !newPost.content.trim() || !selectedConstituency) {
      alert('Please fill all fields and select a constituency');
      return;
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/api/community-posts`, {
        constituency: selectedConstituency,
        title: newPost.title,
        content: newPost.content
      });
      
      if (response.data.message) {
        setNewPost({ title: '', content: '' });
        fetchCommunityPosts(selectedConstituency);
      }
    } catch (error) {
      console.error('Error submitting post:', error);
      alert('Error submitting post. Please try again.');
    }
  };

  const voteOnPost = async (postId, voteType) => {
    try {
      await axios.post(`${API_BASE_URL}/api/community-posts/${postId}/vote`, {
        vote_type: voteType
      });
      fetchCommunityPosts(selectedConstituency);
    } catch (error) {
      console.error('Error voting on post:', error);
    }
  };

  // Initialize data on mount
  useEffect(() => {
    if (currentLanguage) {
      fetchConstituencies();
      fetchCandidates();
      fetchManifestos();
      fetchFactChecks();
      fetchCommunityPosts();
    }
  }, [currentLanguage]);

  // Update data when filters change
  useEffect(() => {
    if (activeTab === 'candidates' && currentLanguage) {
      fetchCandidates(selectedConstituency);
    }
  }, [selectedConstituency, activeTab, currentLanguage]);

  useEffect(() => {
    if (activeTab === 'manifestos' && currentLanguage) {
      fetchManifestos(selectedParty, selectedCategory);
    }
  }, [selectedParty, selectedCategory, activeTab, currentLanguage]);

  useEffect(() => {
    if (activeTab === 'factcheck' && currentLanguage) {
      fetchFactChecks(selectedVerdict);
    }
  }, [selectedVerdict, activeTab, currentLanguage]);

  useEffect(() => {
    if (activeTab === 'community' && currentLanguage) {
      fetchCommunityPosts(selectedConstituency);
    }
  }, [selectedConstituency, activeTab, currentLanguage]);

  // Show language selection if no language is chosen
  if (!currentLanguage) {
    return renderLanguageSelection();
  }

  // Filter data based on search
  const filteredCandidates = candidates.filter(candidate =>
    candidate.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    candidate.party.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredManifestos = manifestos.filter(manifesto =>
    manifesto.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    manifesto.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredFactChecks = showOnlyFactChecked 
    ? factChecks.filter(fc => fc.verdict !== 'Unverified')
    : factChecks;

  // Get unique values for filters
  const parties = [...new Set(candidates.map(c => c.party))];
  const categories = [...new Set(manifestos.map(m => m.category))];
  const verdicts = ['True', 'False', 'Misleading', 'Unverified'];

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  const getVerdictColor = (verdict) => {
    switch (verdict) {
      case 'True': return 'bg-green-100 text-green-800';
      case 'False': return 'bg-red-100 text-red-800';
      case 'Misleading': return 'bg-yellow-100 text-yellow-800';
      case 'Unverified': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getFulfilledColor = (fulfilled) => {
    if (fulfilled === true) return 'bg-green-100 text-green-800';
    if (fulfilled === false) return 'bg-red-100 text-red-800';
    return 'bg-yellow-100 text-yellow-800';
  };

  const getFulfilledText = (fulfilled) => {
    if (fulfilled === true) return t.manifestosTab.fulfilled;
    if (fulfilled === false) return t.manifestosTab.notFulfilled;
    return t.manifestosTab.pending;
  };

  const renderCandidatesTab = () => (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row gap-4">
        <select 
          value={selectedConstituency}
          onChange={(e) => setSelectedConstituency(e.target.value)}
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">{t.candidatesTab.allConstituencies}</option>
          {constituencies.map(constituency => (
            <option key={constituency.constituency_id} value={constituency.name}>
              {constituency.name} ({constituency.district})
            </option>
          ))}
        </select>
        <input
          type="text"
          placeholder={t.candidatesTab.search}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {loading ? (
        <div className="text-center py-8">{t.common.loading}</div>
      ) : (
        <div className="grid gap-6">
          {filteredCandidates.map(candidate => (
            <div key={candidate.candidate_id} className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-1">{candidate.name}</h3>
                  <p className="text-gray-600">{candidate.constituency} • {candidate.party}</p>
                </div>
                {candidate.incumbent && (
                  <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium mt-2 md:mt-0 self-start">
                    {t.candidatesTab.incumbent}
                  </span>
                )}
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-700">{t.candidatesTab.age}:</span>
                  <p className="text-gray-900">{candidate.age} years</p>
                </div>
                <div>
                  <span className="font-medium text-gray-700">{t.candidatesTab.education}:</span>
                  <p className="text-gray-900">{candidate.education}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-700">{t.candidatesTab.criminal}:</span>
                  <p className={`font-bold ${candidate.criminal_cases > 0 ? 'text-red-600' : 'text-green-600'}`}>
                    {candidate.criminal_cases}
                  </p>
                </div>
                <div>
                  <span className="font-medium text-gray-700">{t.candidatesTab.assets}:</span>
                  <p className="text-gray-900">{formatCurrency(candidate.assets)}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderManifestosTab = () => (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row gap-4">
        <select 
          value={selectedParty}
          onChange={(e) => setSelectedParty(e.target.value)}
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">{t.manifestosTab.allParties}</option>
          {parties.map(party => (
            <option key={party} value={party}>{party}</option>
          ))}
        </select>
        
        <select 
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">{t.manifestosTab.allCategories}</option>
          {categories.map(category => (
            <option key={category} value={category}>{category}</option>
          ))}
        </select>
        
        <input
          type="text"
          placeholder={t.manifestosTab.search}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {loading ? (
        <div className="text-center py-8">{t.common.loading}</div>
      ) : (
        <div className="grid gap-6">
          {filteredManifestos.map(manifesto => (
            <ManifestoCard key={manifesto.promise_id} manifesto={manifesto} t={t} />
          ))}
        </div>
      )}
    </div>
  );

  const renderFactCheckTab = () => (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex items-center">
          <input
            type="checkbox"
            id="factCheckedOnly"
            checked={showOnlyFactChecked}
            onChange={(e) => setShowOnlyFactChecked(e.target.checked)}
            className="mr-2"
          />
          <label htmlFor="factCheckedOnly" className="text-sm text-gray-700">
            {t.factCheckTab.onlyFactChecked}
          </label>
        </div>
        
        <select 
          value={selectedVerdict}
          onChange={(e) => setSelectedVerdict(e.target.value)}
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">{t.factCheckTab.allVerdicts}</option>
          {verdicts.map(verdict => (
            <option key={verdict} value={verdict}>
              {t.factCheckTab[verdict.toLowerCase()] || verdict}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="text-center py-8">{t.common.loading}</div>
      ) : (
        <div className="grid gap-6">
          {filteredFactChecks.map(factCheck => (
            <div key={factCheck.fact_id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex flex-col md:flex-row md:items-start md:justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{factCheck.title}</h3>
                  <p className="text-gray-700 mb-3">{factCheck.description}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getVerdictColor(factCheck.verdict)} ml-0 md:ml-4 mb-3 md:mb-0 self-start`}>
                  {t.factCheckTab[factCheck.verdict.toLowerCase()] || factCheck.verdict}
                </span>
              </div>
              
              {factCheck.tags.length > 0 && (
                <div className="mb-3">
                  <span className="text-sm font-medium text-gray-700 mr-2">{t.factCheckTab.tags}:</span>
                  {factCheck.tags.map(tag => (
                    <span key={tag} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs mr-2">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
              
              {factCheck.source_url && (
                <div>
                  <span className="text-sm font-medium text-gray-700 mr-2">{t.factCheckTab.source}:</span>
                  <a href={factCheck.source_url} target="_blank" rel="noopener noreferrer" 
                     className="text-blue-600 hover:text-blue-800 text-sm underline">
                    View Source
                  </a>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderCommunityTab = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4">{t.communityTab.newPost}</h3>
        
        <div className="space-y-4">
          <select 
            value={selectedConstituency}
            onChange={(e) => setSelectedConstituency(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">{t.candidatesTab.selectConstituency}</option>
            {constituencies.map(constituency => (
              <option key={constituency.constituency_id} value={constituency.name}>
                {constituency.name} ({constituency.district})
              </option>
            ))}
          </select>
          
          <input
            type="text"
            placeholder={t.communityTab.postTitle}
            value={newPost.title}
            onChange={(e) => setNewPost({...newPost, title: e.target.value})}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          
          <textarea
            placeholder={t.communityTab.postContent}
            value={newPost.content}
            onChange={(e) => setNewPost({...newPost, content: e.target.value})}
            rows={4}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          
          <button
            onClick={submitCommunityPost}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            {t.communityTab.submit}
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-8">{t.common.loading}</div>
      ) : (
        <div className="grid gap-6">
          {communityPosts.map(post => (
            <div key={post.post_id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex flex-col md:flex-row md:items-start md:justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-gray-900 mb-1">{post.title}</h3>
                  <p className="text-sm text-gray-500 mb-2">
                    {post.constituency} • {t.common.anonymous} • {new Date(post.created_at).toLocaleDateString()}
                  </p>
                  <p className="text-gray-700">{post.content}</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4 pt-4 border-t border-gray-200">
                <button
                  onClick={() => voteOnPost(post.post_id, 'upvote')}
                  className="flex items-center space-x-1 text-green-600 hover:text-green-800"
                >
                  <span>👍</span>
                  <span>{post.upvotes}</span>
                </button>
                
                <button
                  onClick={() => voteOnPost(post.post_id, 'downvote')}
                  className="flex items-center space-x-1 text-red-600 hover:text-red-800"
                >
                  <span>👎</span>
                  <span>{post.downvotes}</span>
                </button>
                
                <span className="text-gray-500 text-sm">
                  {post.replies.length} {t.communityTab.replies}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'candidates': return renderCandidatesTab();
      case 'manifestos': return renderManifestosTab();
      case 'factcheck': return renderFactCheckTab();
      case 'community': return renderCommunityTab();
      default: return renderCandidatesTab();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-red-600 via-orange-500 to-yellow-500 text-white">
        <div className="container mx-auto px-4 py-16">
          <div className="flex flex-col lg:flex-row items-center">
            <div className="lg:w-1/2 lg:pr-8 mb-8 lg:mb-0">
              <h1 className="text-4xl lg:text-6xl font-bold mb-4">{t.appTitle}</h1>
              <p className="text-xl lg:text-2xl mb-8">{t.tagline}</p>
              
              {/* Language change option */}
              <button
                onClick={() => setCurrentLanguage(null)}
                className="bg-white bg-opacity-20 text-white px-6 py-3 rounded-lg font-medium hover:bg-opacity-30 transition-colors"
              >
                {currentLanguage === 'english' ? 'தமிழில் மாற்று' : 'Change to English'}
              </button>
            </div>
            
            <div className="lg:w-1/2">
              <img 
                src="https://images.unsplash.com/photo-1708346561250-ea0f8b54bc1c" 
                alt="Tamil Nadu Temple Architecture"
                className="w-full h-80 object-cover rounded-lg shadow-2xl"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="container mx-auto px-4">
          <nav className="flex space-x-8 overflow-x-auto py-4">
            {Object.entries(t.tabs).map(([key, label]) => (
              <button
                key={key}
                onClick={() => {
                  setActiveTab(key);
                  setSearchQuery('');
                }}
                className={`whitespace-nowrap px-4 py-2 font-medium border-b-2 transition-colors ${
                  activeTab === key
                    ? 'border-red-500 text-red-600'
                    : 'border-transparent text-gray-700 hover:text-red-600 hover:border-red-300'
                }`}
              >
                {label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        {renderContent()}
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <p className="mb-4">&copy; 2025 {t.appTitle}. Made for the people of Tamil Nadu.</p>
          <p className="text-gray-400">
            Data sourced from public records and official websites. 
            Help us improve by reporting any inaccuracies.
          </p>
        </div>
      </footer>
    </div>
  );
}

// Component for manifesto cards with expand/collapse functionality
function ManifestoCard({ manifesto, t }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getFulfilledColor = (fulfilled) => {
    if (fulfilled === true) return 'bg-green-100 text-green-800';
    if (fulfilled === false) return 'bg-red-100 text-red-800';
    return 'bg-yellow-100 text-yellow-800';
  };

  const getFulfilledText = (fulfilled) => {
    if (fulfilled === true) return t.manifestosTab.fulfilled;
    if (fulfilled === false) return t.manifestosTab.notFulfilled;
    return t.manifestosTab.pending;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
      <div className="flex flex-col md:flex-row md:items-start md:justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-bold text-gray-900 mb-2">{manifesto.title}</h3>
          <p className="text-gray-600 mb-2">{manifesto.party} • {manifesto.category}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getFulfilledColor(manifesto.fulfilled)} ml-0 md:ml-4 mb-3 md:mb-0 self-start`}>
          {getFulfilledText(manifesto.fulfilled)}
        </span>
      </div>
      
      <div className="mb-4">
        <p className="text-gray-700 mb-3">{manifesto.one_minute_explanation}</p>
        
        {isExpanded && (
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-gray-700 mb-3">{manifesto.description}</p>
            {manifesto.evidence_url && (
              <div>
                <span className="text-sm font-medium text-gray-700 mr-2">{t.manifestosTab.evidence}:</span>
                <a href={manifesto.evidence_url} target="_blank" rel="noopener noreferrer" 
                   className="text-blue-600 hover:text-blue-800 text-sm underline">
                  View Evidence
                </a>
              </div>
            )}
          </div>
        )}
      </div>
      
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
      >
        {isExpanded ? t.manifestosTab.readLess : t.manifestosTab.readMore}
      </button>
    </div>
  );
}

export default App;