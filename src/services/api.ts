import axios, { AxiosError } from 'axios';
import { 
  User, 
  Activity, 
  CreateActivityData, 
  LoginCredentials, 
  RegisterData, 
  AuthResponse,
  ApiError 
} from '../types';

const API_BASE_URL = 'https://fitness-tracker-api-soub.onrender.com/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token management
export const tokenManager = {
  getAccessToken: () => localStorage.getItem('access_token'),
  getRefreshToken: () => localStorage.getItem('refresh_token'),
  setTokens: (access: string, refresh: string) => {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  },
  clearTokens: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = tokenManager.getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = tokenManager.getRefreshToken();
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
            refresh: refreshToken,
          });
          
          const { access } = response.data;
          tokenManager.setTokens(access, refreshToken);
          
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access}`;
          }
          
          return api(originalRequest);
        }
      } catch (refreshError) {
        tokenManager.clearTokens();
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

// Error handler
const handleApiError = (error: AxiosError): ApiError => {
  if (error.response?.data) {
    const data = error.response.data as any;
    return {
      message: data.detail || data.message || 'An error occurred',
      details: data,
    };
  }
  return {
    message: error.message || 'Network error occurred',
  };
};

// Auth API
export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    try {
      const response = await api.post('/token/', credentials);
      const { access, refresh } = response.data;
      tokenManager.setTokens(access, refresh);
      
      // Get user profile
      const userResponse = await api.get('/auth/profile/');
      return {
        user: userResponse.data,
        access,
        refresh,
      };
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  register: async (userData: RegisterData): Promise<AuthResponse> => {
    try {
      const response = await api.post('/auth/register/', userData);
      const { user, access, refresh } = response.data;
      tokenManager.setTokens(access, refresh);
      return { user, access, refresh };
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  logout: () => {
    tokenManager.clearTokens();
  },

  getCurrentUser: async (): Promise<User> => {
    try {
      const response = await api.get('/auth/profile/');
      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },
};

// Activities API
export const activitiesApi = {
  getActivities: async (): Promise<Activity[]> => {
    try {
      const response = await api.get('/activities/');
      return response.data.results || response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  createActivity: async (activityData: CreateActivityData): Promise<Activity> => {
    try {
      const response = await api.post('/activities/', activityData);
      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  updateActivity: async (id: number, activityData: Partial<CreateActivityData>): Promise<Activity> => {
    try {
      const response = await api.put(`/activities/${id}/`, activityData);
      return response.data;
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },

  deleteActivity: async (id: number): Promise<void> => {
    try {
      await api.delete(`/activities/${id}/`);
    } catch (error) {
      throw handleApiError(error as AxiosError);
    }
  },
};