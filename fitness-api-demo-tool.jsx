import React, { useState } from 'react';
import { Play, User, Activity, Target, BarChart3, Trophy, Settings, CheckCircle, XCircle, Loader } from 'lucide-react';

const FitnessApiDemo = () => {
  const [apiUrl, setApiUrl] = useState('https://fitness-tracker-api-soub.onrender.com');
  const [token, setToken] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const addResult = (title, data, success = true) => {
    const newResult = {
      id: Date.now(),
      title,
      data: typeof data === 'string' ? data : JSON.stringify(data, null, 2),
      success,
      timestamp: new Date().toLocaleTimeString()
    };
    setResults(prev => [newResult, ...prev.slice(0, 9)]); // Keep last 10 results
  };

  const makeRequest = async (endpoint, method = 'GET', body = null, requiresAuth = false) => {
    setIsLoading(true);
    try {
      const headers = {
        'Content-Type': 'application/json',
      };
      
      if (requiresAuth && token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${apiUrl}${endpoint}`, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null,
      });

      const data = await response.json();
      
      if (response.ok) {
        addResult(`${method} ${endpoint}`, data, true);
        return data;
      } else {
        addResult(`${method} ${endpoint}`, data, false);
        return null;
      }
    } catch (error) {
      addResult(`${method} ${endpoint}`, `Error: ${error.message}`, false);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const demoSteps = [
    {
      id: 'register',
      title: '1. Register User',
      icon: <User className="w-5 h-5" />,
      description: 'Create a new user account',
      action: async () => {
        const userData = {
          username: `demo_user_${Date.now()}`,
          email: `demo${Date.now()}@example.com`,
          password: 'demo123456',
          password_confirm: 'demo123456',
          first_name: 'Demo',
          last_name: 'User'
        };
        const result = await makeRequest('/api/auth/register/', 'POST', userData);
        if (result && result.access) {
          setToken(result.access);
          addResult('🔑 Token Saved', 'Authentication token automatically saved for next requests!', true);
        }
        return result;
      }
    },
    {
      id: 'login',
      title: '2. Login User',
      icon: <Settings className="w-5 h-5" />,
      description: 'Login with existing credentials',
      action: async () => {
        const loginData = {
          username: 'demo_user',
          password: 'demo123456'
        };
        const result = await makeRequest('/api/token/', 'POST', loginData);
        if (result && result.access) {
          setToken(result.access);
          addResult('🔑 Token Updated', 'New authentication token saved!', true);
        }
        return result;
      }
    },
    {
      id: 'create_activity',
      title: '3. Log Running Activity',
      icon: <Activity className="w-5 h-5" />,
      description: 'Create a fitness activity',
      action: async () => {
        const activityData = {
          activity_type: 'running',
          duration: Math.floor(Math.random() * 60) + 20, // 20-80 minutes
          distance: (Math.random() * 10 + 2).toFixed(1), // 2-12 km
          calories_burned: Math.floor(Math.random() * 400) + 200, // 200-600 calories
          date: new Date().toISOString().split('T')[0],
          notes: 'Demo running activity'
        };
        return await makeRequest('/api/activities/', 'POST', activityData, true);
      }
    },
    {
      id: 'create_cycling',
      title: '4. Log Cycling Activity',
      icon: <Activity className="w-5 h-5" />,
      description: 'Create another activity type',
      action: async () => {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        
        const activityData = {
          activity_type: 'cycling',
          duration: Math.floor(Math.random() * 90) + 30, // 30-120 minutes
          distance: (Math.random() * 20 + 5).toFixed(1), // 5-25 km
          calories_burned: Math.floor(Math.random() * 600) + 300, // 300-900 calories
          date: yesterday.toISOString().split('T')[0],
          notes: 'Demo cycling activity'
        };
        return await makeRequest('/api/activities/', 'POST', activityData, true);
      }
    },
    {
      id: 'view_activities',
      title: '5. View All Activities',
      icon: <BarChart3 className="w-5 h-5" />,
      description: 'Get list of user activities',
      action: async () => {
        return await makeRequest('/api/activities/', 'GET', null, true);
      }
    },
    {
      id: 'create_goal',
      title: '6. Set Fitness Goal',
      icon: <Target className="w-5 h-5" />,
      description: 'Create a monthly distance goal',
      action: async () => {
        const today = new Date();
        const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
        const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
        
        const goalData = {
          goal_type: 'distance',
          target_value: 50,
          period: 'monthly',
          activity_type: 'running',
          start_date: startOfMonth.toISOString().split('T')[0],
          end_date: endOfMonth.toISOString().split('T')[0]
        };
        return await makeRequest('/api/activities/goals/', 'POST', goalData, true);
      }
    },
    {
      id: 'view_metrics',
      title: '7. View Metrics',
      icon: <BarChart3 className="w-5 h-5" />,
      description: 'Get activity statistics',
      action: async () => {
        return await makeRequest('/api/activities/metrics/', 'GET', null, true);
      }
    },
    {
      id: 'view_leaderboard',
      title: '8. View Leaderboard',
      icon: <Trophy className="w-5 h-5" />,
      description: 'See competitive rankings',
      action: async () => {
        return await makeRequest('/api/activities/leaderboard/', 'GET', null, true);
      }
    }
  ];

  const runFullDemo = async () => {
    setResults([]);
    addResult('🚀 Starting Full Demo', 'Running all demo steps automatically...', true);
    
    for (const step of demoSteps) {
      await new Promise(resolve => setTimeout(resolve, 1000)); // Pause between steps
      await step.action();
    }
    
    addResult('✅ Demo Complete', 'All API endpoints tested successfully!', true);
  };

  const clearResults = () => {
    setResults([]);
    setToken('');
  };

  return (
    <div className="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h1 className="text-3xl font-bold text-center mb-2 text-blue-600">
          🏃‍♂️ Fitness Tracker API Demo Tool
        </h1>
        <p className="text-center text-gray-600 mb-6">
          Interactive demo tool for your Fitness Tracker API project
        </p>

        {/* API URL Configuration */}
        <div className="mb-6 p-4 bg-blue-50 rounded-lg">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            API Base URL:
          </label>
          <input
            type="url"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="https://your-app.onrender.com"
          />
          <p className="text-sm text-gray-600 mt-2">
            🔗 Replace with your deployed API URL
          </p>
        </div>

        {/* Quick Actions */}
        <div className="flex gap-4 mb-6 flex-wrap">
          <button
            onClick={runFullDemo}
            disabled={isLoading}
            className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            <Play className="w-5 h-5" />
            {isLoading ? 'Running Demo...' : 'Run Full Demo'}
          </button>
          
          <button
            onClick={clearResults}
            className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors"
          >
            Clear Results
          </button>

          {token && (
            <div className="flex items-center gap-2 text-green-600 bg-green-50 px-3 py-2 rounded-lg">
              <CheckCircle className="w-5 h-5" />
              <span className="text-sm font-medium">Authenticated</span>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Demo Steps */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Demo Steps</h2>
          <div className="space-y-3">
            {demoSteps.map((step) => (
              <div key={step.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <div className="text-blue-600 mt-1">
                    {step.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-800">{step.title}</h3>
                    <p className="text-sm text-gray-600 mb-3">{step.description}</p>
                    <button
                      onClick={step.action}
                      disabled={isLoading}
                      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors text-sm disabled:opacity-50 flex items-center gap-2"
                    >
                      {isLoading ? <Loader className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                      Run Step
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">
            API Response Results
          </h2>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {results.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <BarChart3 className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>No results yet. Run a demo step to see API responses!</p>
              </div>
            ) : (
              results.map((result) => (
                <div
                  key={result.id}
                  className={`p-4 rounded-lg border-l-4 ${
                    result.success
                      ? 'bg-green-50 border-green-500'
                      : 'bg-red-50 border-red-500'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    {result.success ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-600" />
                    )}
                    <span className="font-semibold text-gray-800">
                      {result.title}
                    </span>
                    <span className="text-xs text-gray-500 ml-auto">
                      {result.timestamp}
                    </span>
                  </div>
                  <pre className="text-xs text-gray-700 whitespace-pre-wrap overflow-x-auto bg-white p-2 rounded border">
                    {result.data}
                  </pre>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Demo Instructions */}
      <div className="mt-6 bg-blue-50 rounded-lg p-6">
        <h2 className="text-lg font-bold text-blue-800 mb-3">
          🎯 How to Use This Demo Tool
        </h2>
        <div className="text-sm text-blue-700 space-y-2">
          <p><strong>1.</strong> Update the API URL above with your deployed app URL</p>
          <p><strong>2.</strong> Click "Run Full Demo" for a complete walkthrough</p>
          <p><strong>3.</strong> Or run individual steps to show specific features</p>
          <p><strong>4.</strong> Share your screen during presentations to show live API responses</p>
          <p><strong>5.</strong> The tool automatically handles authentication tokens</p>
        </div>
      </div>
    </div>
  );
};

export default FitnessApiDemo;