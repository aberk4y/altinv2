
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL || '/api',
});

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      if (window.location.pathname.startsWith('/admin') && window.location.pathname !== '/adminyonetim_log_tr') {
        window.location.href = '/adminyonetim_log_tr';
      }
    }
    return Promise.reject(error);
  }
);

export const login = async (username, password) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  const response = await api.post('/admin/login', formData);
  if (response.data.access_token) {
    localStorage.setItem('token', response.data.access_token);
  }
  return response.data;
};

export const getMargins = async () => {
  const response = await api.get('/margins');
  return response.data;
};

// Helper methods attached to api object for compatibility
api.getPrices = async (type = 'all') => {
  const response = await api.get(`/prices?type=${type}`);
  return response.data;
};

api.getPortfolio = async () => {
  const response = await api.get('/portfolio');
  return response.data;
};

api.createPortfolioItem = async (itemData) => {
  const response = await api.post('/portfolio', itemData);
  return response.data;
};

api.deletePortfolioItem = async (id) => {
  const response = await api.delete(`/portfolio/${id}`);
  return response.data;
};

export const updateMargin = async (marginData) => {
  const response = await api.post('/margins', marginData);
  return response.data;
};

export { api };
export default api;