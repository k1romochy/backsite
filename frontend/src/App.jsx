import React, { useContext } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, AuthContext } from "./components/AuthContext";
import AppContent from "./AppContent";
import Login from "./pages/Login";
import AdminDashboard from "./pages/AdminDashboard.jsx";
import AdminRequests from "./pages/AdminRequests.jsx";
import CreateReport from "./pages/CreateReport.jsx";
import ReportForm from "./pages/ReportForm.jsx";


const App = () => {
    return (
        <AuthProvider>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/admin" element={<AdminRoute />} />
                <Route path="/requests" element={<AdminRequests />} />
                <Route path="/create-report" element={<CreateReport />} />
                <Route path="/report" element={<ReportForm />} />
                <Route path="/*" element={<ProtectedRoute />} />
            </Routes>
        </AuthProvider>
    );
};

// Защищенный маршрут для авторизованных пользователей
const ProtectedRoute = () => {
    const { user, loading } = useContext(AuthContext);

    if (loading) return <div>Загрузка...</div>;
    return user ? <AppContent /> : <Navigate to="/login" />;
};

// Маршрут только для админов
const AdminRoute = () => {
    const { user, loading } = useContext(AuthContext);

    if (loading) return <div>Загрузка...</div>;
    return user && user.role === "Admin" ? <AdminDashboard /> : <Navigate to="/" />;
};

export default App;
