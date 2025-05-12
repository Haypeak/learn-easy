import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  headers: {
    'Content-Type': 'application/json',
  
  },
});
// const api = {
//   baseURL: process.env.REACT_APP_API_URL,
  
//   async request(endpoint, options = {}) {
//     const response = await fetch(`${this.baseURL}${endpoint}`, {
//       ...options,
//       headers: {
//         'Content-Type': 'application/json',
//         ...options.headers,
//       },
//     });

//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }

//     return response.json();
//   },

//   get(endpoint, options = {}) {
//     return this.request(endpoint, { method: 'GET', ...options });
//   },

//   post(endpoint, data, options = {}) {
//     return this.request(endpoint, { method: 'POST', body: JSON.stringify(data), ...options });
//   },

  // You can add more methods like put, delete, etc. as needed
// };

// Example usage:
// api.get('/some-endpoint').then(data => console.log(data)).catch(error => console.error(error));


api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add a response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

export default api;

