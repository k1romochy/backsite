import { createContext, useState, useEffect } from "react";
import axios from "axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchUser = async () => {
        try {
            const response = await axios.get("http://localhost:8000/users/show/me/", { withCredentials: true });
            setUser(response.data);
        } catch (error) {
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUser();
    }, []);

    const login = async (formData) => {
        try {
            await axios.post("http://localhost:8000/auth/login/", formData, {
                headers: { "Content-Type": "multipart/form-data" },
                withCredentials: true,
            });
            await fetchUser();  // ⚡ После входа сразу обновляем пользователя
        } catch (error) {
            throw new Error("Неверный логин или пароль");
        }
    };

    const register = async (userData) => {
        try {
            await axios.post("http://localhost:8000/users/registrate/", userData, { withCredentials: true });
        } catch (error) {;
        }
    };

    const logout = async () => {
        await axios.post("http://localhost:8000/auth/logout/", {}, { withCredentials: true });
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthProvider