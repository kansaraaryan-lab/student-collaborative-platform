import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const storedUser = localStorage.getItem("campus_user");

  if (storedUser) {
    const user = JSON.parse(storedUser);

    if (user?.id) {
      config.headers["X-User-ID"] = user.id;
    }
  }

  return config;
});

export default api;