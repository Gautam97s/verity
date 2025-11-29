import axios from "axios";

export const API = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "1"
    }
});
