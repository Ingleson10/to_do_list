// services/api.js
import axios from 'axios';
import { refreshToken } from './auth';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

// Configuração centralizada da API
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 segundos
  headers: {
    'Content-Type': 'application/json',
    'X-App-Version': process.env.REACT_APP_VERSION || '1.0.0'
  }
});

// Interceptor para adicionar token antes das requisições
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token && !config.url.includes('/auth/')) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Interceptor para tratamento centralizado de erros e renew de token
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    
    // Tratamento para token expirado (status 401)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const newToken = await refreshToken();
        localStorage.setItem('access_token', newToken);
        
        // Atualiza header e repete a requisição original
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Redireciona para login se o refresh falhar
        if (refreshError.response?.status === 401) {
          localStorage.clear();
          window.location.href = '/login?session=expired';
        }
        return Promise.reject(refreshError);
      }
    }
    
    // Tratamento genérico de erros
    const errorMessage = error.response?.data?.detail || 
                         error.response?.data?.message || 
                         error.message || 
                         'Erro desconhecido';
    
    // Formatação especial para erros de validação
    if (error.response?.status === 400 && error.response.data?.errors) {
      error.formattedErrors = formatValidationErrors(error.response.data.errors);
    }
    
    return Promise.reject({ ...error, message: errorMessage });
  }
);

// Formata erros de validação do Django
const formatValidationErrors = (errors) => {
  return Object.entries(errors).map(([field, messages]) => ({
    field,
    messages: Array.isArray(messages) ? messages : [messages]
  }));
};

// --- Serviços de Autenticação ---
export const authService = {
  login: async (credentials) => {
    const response = await api.post('/auth/token/', credentials);
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete api.defaults.headers.common['Authorization'];
  },

  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    const response = await api.post('/auth/token/refresh/', { refresh: refreshToken });
    localStorage.setItem('access_token', response.data.access);
    return response.data.access;
  },

  register: async (userData) => {
    return await api.post('/auth/register/', userData);
  },

  getProfile: async () => {
    return await api.get('/auth/profile/');
  }
};

// --- Serviços de Notas (CRUD completo) ---
export const notesService = {
  getAll: async (params = {}) => {
    const response = await api.get('/notes/', { params });
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/notes/${id}/`);
    return response.data;
  },

  create: async (noteData) => {
    const response = await api.post('/notes/', noteData);
    return response.data;
  },

  update: async (id, noteData) => {
    const response = await api.patch(`/notes/${id}/`, noteData);
    return response.data;
  },

  delete: async (id) => {
    await api.delete(`/notes/${id}/`);
  },

  search: async (query) => {
    const response = await api.get('/notes/search/', { params: { q: query } });
    return response.data;
  },

  analyze: async (id) => {
    const response = await api.post(`/notes/${id}/analyze/`);
    return response.data;
  }
};

// --- Serviços de Tarefas ---
export const tasksService = {
  // ... (estrutura similar ao notesService)
};

// Exporta a instância base para casos específicos
export default api;