import axios from 'axios';

const api = {
  baseURL: process.env.REACT_APP_API_URL,

  async request(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': 'https://learneasyapp.netlify.app',
      ...options.headers,
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/signin';
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  get(endpoint, options = {}) {
    return this.request(endpoint, { method: 'GET', ...options });
  },

  post(endpoint, data, options = {}) {
    return this.request(endpoint, { method: 'POST', body: JSON.stringify(data), ...options });
  },

  put(endpoint, data, options = {}) {
    return this.request(endpoint, { method: 'PUT', body: JSON.stringify(data), ...options });
  },

  delete(endpoint, options = {}) {
    return this.request(endpoint, { method: 'DELETE', ...options });
  },
};
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

