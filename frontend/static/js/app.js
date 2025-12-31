// Social Media Automation Bot - Frontend JavaScript

const API_BASE_URL = window.location.origin;
let authToken = localStorage.getItem('authToken');
let currentUser = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    
    if (authToken) {
        loadUserProfile();
    } else {
        showLogin();
    }
});

// Setup event listeners
function setupEventListeners() {
    // Login form
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    
    // Register form
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    
    // Post form
    document.getElementById('post-form').addEventListener('submit', handleSchedulePost);
    
    // Account form
    document.getElementById('account-form').addEventListener('submit', handleAddAccount);
}

// Authentication functions
async function handleLogin(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            authToken = result.data.token;
            currentUser = result.data.user;
            localStorage.setItem('authToken', authToken);
            
            showSection('dashboard');
            loadDashboard();
            alert('Login successful!');
        } else {
            alert(result.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        username: formData.get('username'),
        email: formData.get('email'),
        password: formData.get('password'),
        subscription_plan: formData.get('subscription_plan')
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            authToken = result.data.token;
            currentUser = result.data.user;
            localStorage.setItem('authToken', authToken);
            
            showSection('dashboard');
            loadDashboard();
            alert('Registration successful!');
        } else {
            alert(result.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
    }
}

async function loadUserProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/user/profile`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentUser = result.data;
            showSection('dashboard');
            loadDashboard();
        } else {
            logout();
        }
    } catch (error) {
        console.error('Profile load error:', error);
        logout();
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    showLogin();
}

// Navigation functions
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    const section = document.getElementById(`${sectionName}-section`);
    if (section) {
        section.classList.add('active');
    }
    
    // Load data for the section
    if (authToken) {
        switch(sectionName) {
            case 'dashboard':
                loadDashboard();
                break;
            case 'analytics':
                loadAnalytics();
                break;
            case 'accounts':
                loadAccounts();
                break;
        }
    }
}

function showLogin() {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById('login-section').classList.add('active');
}

function showRegister() {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById('register-section').classList.add('active');
}

// Dashboard functions
async function loadDashboard() {
    try {
        // Load posts
        const postsResponse = await fetch(`${API_BASE_URL}/api/posts`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const postsResult = await postsResponse.json();
        
        if (postsResult.success) {
            const posts = postsResult.data;
            const pendingPosts = posts.filter(p => p.status === 'pending');
            
            // Update stats
            document.getElementById('total-posts').textContent = posts.length;
            document.getElementById('pending-posts').textContent = pendingPosts.length;
            
            // Display upcoming posts
            displayUpcomingPosts(pendingPosts);
        }
        
        // Load basic analytics
        const analyticsResponse = await fetch(`${API_BASE_URL}/api/analytics/summary?days=30`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const analyticsResult = await analyticsResponse.json();
        
        if (analyticsResult.success) {
            const analytics = analyticsResult.data;
            document.getElementById('total-reach').textContent = analytics.total_reach.toLocaleString();
            document.getElementById('engagement-rate').textContent = analytics.avg_engagement_rate + '%';
        }
        
    } catch (error) {
        console.error('Dashboard load error:', error);
    }
}

function displayUpcomingPosts(posts) {
    const container = document.getElementById('upcoming-posts');
    
    if (posts.length === 0) {
        container.innerHTML = '<p class="text-muted">No upcoming posts scheduled</p>';
        return;
    }
    
    container.innerHTML = posts.slice(0, 5).map(post => `
        <div class="post-item">
            <h4>${post.content.substring(0, 50)}${post.content.length > 50 ? '...' : ''}</h4>
            <p>Scheduled: ${new Date(post.scheduled_time).toLocaleString()}</p>
            <div class="post-platforms">
                ${post.platforms.map(p => `<span class="platform-badge">${p}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

// Post scheduling functions
async function handleSchedulePost(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const platforms = Array.from(formData.getAll('platforms'));
    
    if (platforms.length === 0) {
        alert('Please select at least one platform');
        return;
    }
    
    const data = {
        content: formData.get('content'),
        platforms: platforms,
        scheduled_time: new Date(formData.get('scheduled_time')).toISOString(),
        media_url: formData.get('media_url') || null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/posts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Post scheduled successfully!');
            e.target.reset();
            showSection('dashboard');
        } else {
            alert(result.error || 'Failed to schedule post');
        }
    } catch (error) {
        console.error('Schedule post error:', error);
        alert('Failed to schedule post. Please try again.');
    }
}

// Analytics functions
async function loadAnalytics() {
    try {
        // Load analytics summary
        const summaryResponse = await fetch(`${API_BASE_URL}/api/analytics/summary?days=30`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const summaryResult = await summaryResponse.json();
        
        if (summaryResult.success) {
            const analytics = summaryResult.data;
            
            document.getElementById('analytics-likes').textContent = analytics.total_likes.toLocaleString();
            document.getElementById('analytics-shares').textContent = analytics.total_shares.toLocaleString();
            document.getElementById('analytics-comments').textContent = analytics.total_comments.toLocaleString();
            document.getElementById('analytics-engagement').textContent = analytics.avg_engagement_rate + '%';
            
            // Display platform breakdown
            displayPlatformBreakdown(analytics.platform_breakdown);
        }
        
        // Load best posting times
        const timesResponse = await fetch(`${API_BASE_URL}/api/analytics/best-times`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const timesResult = await timesResponse.json();
        
        if (timesResult.success) {
            displayBestTimes(timesResult.data);
        }
        
    } catch (error) {
        console.error('Analytics load error:', error);
    }
}

function displayPlatformBreakdown(breakdown) {
    const container = document.getElementById('platform-breakdown');
    
    if (!breakdown || Object.keys(breakdown).length === 0) {
        container.innerHTML = '<p class="text-muted">No data available</p>';
        return;
    }
    
    container.innerHTML = Object.entries(breakdown).map(([platform, stats]) => `
        <div class="analytics-item">
            <span class="label">${platform.charAt(0).toUpperCase() + platform.slice(1)}:</span>
            <span class="value">${stats.posts} posts, ${stats.reach.toLocaleString()} reach</span>
        </div>
    `).join('');
}

function displayBestTimes(times) {
    const container = document.getElementById('best-times');
    
    if (times.length === 0) {
        container.innerHTML = '<p class="text-muted">No recommendations available</p>';
        return;
    }
    
    container.innerHTML = times.map(time => `
        <div class="time-recommendation">
            <strong>${time.hour}:00 on ${time.day}</strong> - ${time.reason}
        </div>
    `).join('');
}

// Accounts functions
async function loadAccounts() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/accounts`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayAccounts(result.data);
        }
    } catch (error) {
        console.error('Accounts load error:', error);
    }
}

function displayAccounts(accounts) {
    const container = document.getElementById('connected-accounts');
    
    if (accounts.length === 0) {
        container.innerHTML = '<p class="text-muted">No accounts connected</p>';
        return;
    }
    
    container.innerHTML = accounts.map(account => `
        <div class="account-item">
            <div class="account-info">
                <h4>${account.platform.charAt(0).toUpperCase() + account.platform.slice(1)}</h4>
                <p>${account.account_name}</p>
            </div>
            <span class="account-status ${account.is_active ? '' : 'inactive'}">
                ${account.is_active ? 'Active' : 'Inactive'}
            </span>
        </div>
    `).join('');
}

function showAddAccount() {
    document.getElementById('add-account-form').style.display = 'block';
}

function hideAddAccount() {
    document.getElementById('add-account-form').style.display = 'none';
    document.getElementById('account-form').reset();
}

async function handleAddAccount(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        platform: formData.get('platform'),
        account_name: formData.get('account_name'),
        credentials: formData.get('credentials')
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/accounts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Account connected successfully!');
            hideAddAccount();
            loadAccounts();
        } else {
            alert(result.error || 'Failed to connect account');
        }
    } catch (error) {
        console.error('Add account error:', error);
        alert('Failed to connect account. Please try again.');
    }
}
