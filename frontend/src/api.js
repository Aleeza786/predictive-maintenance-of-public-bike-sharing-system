import axios from "axios";

// Base URL of your FastAPI backend
const API = axios.create({
  baseURL: "http://127.0.0.1:8000", // You can change port if backend runs elsewhere
});

// Example API endpoints (you can add more later)
export const getDashboardData = () => API.get("/dashboard");
export const getBikeStatus = () => API.get("/bikes/status");
export const predictFailure = (data) => API.post("/predict", data);

export default API;
