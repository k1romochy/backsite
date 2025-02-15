import React, { useState, useContext } from "react";
import { Input, Button, Card, message } from "antd";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const { login } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            await login(username, password);
            message.success("Вы успешно вошли!");
            navigate("/");
        } catch (error) {
            message.error("Ошибка: " + error.message);
        }
    };

    return (
        <Card title="Авторизация" style={{ width: 400, margin: "auto", marginTop: 100 }}>
            <Input placeholder="Логин" value={username} onChange={(e) => setUsername(e.target.value)} />
            <Input.Password placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} style={{ marginTop: 10 }} />
            <Button type="primary" onClick={handleLogin} style={{ marginTop: 10, width: "100%" }}>
                Войти
            </Button>
        </Card>
    );
};

export default Login;
