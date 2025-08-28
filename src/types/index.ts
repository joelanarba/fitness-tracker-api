export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_joined: string;
  created_at: string;
  updated_at: string;
}

export interface Activity {
  id: number;
  user: string;
  activity_type: string;
  duration: number;
  distance?: number;
  calories_burned?: number;
  date: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface CreateActivityData {
  activity_type: string;
  duration: number;
  distance?: number;
  calories_burned?: number;
  date: string;
  notes?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
}

export interface ApiError {
  message: string;
  details?: Record<string, string[]>;
}