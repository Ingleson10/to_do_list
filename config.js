// Configuração base
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Adicionar token JWT automaticamente
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Exemplo: Buscar notas
const fetchNotes = async () => {
  try {
    const response = await api.get('/notes/');
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar notas:', error);
  }
};

// Exemplo: Login
const login = async (credentials) => {
  try {
    const response = await api.post('/auth/token/', credentials);
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
  } catch (error) {
    console.error('Erro no login:', error);
  }
};