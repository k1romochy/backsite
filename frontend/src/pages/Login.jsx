import React, { useState, useContext } from "react";
import { Input, Button, Card, message, Modal, Form } from "antd";
import { AuthContext } from "../components/AuthContext.jsx";
import { useNavigate } from "react-router-dom";
import axios from "axios";


const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const { login, register } = useContext(AuthContext);
    const navigate = useNavigate();


    const [isRegisterModalVisible, setRegisterModalVisible] = useState(false);
    const [registerLoading, setRegisterLoading] = useState(false);

    // Вход
    const handleLogin = async () => {
        try {
            const credentials = {
                username: username,
                password: password
            };

            await login(credentials); // Передаем JSON, а не FormData
            message.success("Вы успешно вошли!");
            navigate("/");
        } catch (error) {
            message.error(error.message || "Ошибка входа");
        }
    };


    // Регистрация
    const handleRegister = async (values) => {
        setRegisterLoading(true);
        try {
            await register({
                username: values.username,
                email: values.email,
                password: values.password
            });
            navigate("/");
        } catch (error) {
            message.error(error.response?.data?.message || "Ошибка при регистрации");
        }
        setRegisterLoading(false);
    };


    return (
        <Card title="Авторизация" style={{ width: 400, margin: "auto", marginTop: 100 }}>
            <Input placeholder="Логин" value={username} onChange={(e) => setUsername(e.target.value)} />
            <Input.Password placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} style={{ marginTop: 10 }} />
            <Button type="primary" onClick={handleLogin} style={{ marginTop: 10, width: "100%" }}>
                Войти
            </Button>
            <Button type="default" onClick={() => setRegisterModalVisible(true)} style={{ marginTop: 10, width: "100%" }}>
                Зарегистрироваться
            </Button>

            {/* Модальное окно регистрации */}
            <Modal
                title="Регистрация"
                open={isRegisterModalVisible}
                onCancel={() => setRegisterModalVisible(false)}
                footer={null}
            >
                <Form layout="vertical" onFinish={handleRegister}>
                    <Form.Item label="Логин" name="username" rules={[{ required: true, message: "Введите логин!" }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item label="Email" name="email" rules={[{ required: true, message: "Введите email!", type: "email" }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item label="Пароль" name="password" rules={[{ required: true, message: "Введите пароль!" }]}>
                        <Input.Password />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit" loading={registerLoading} style={{ width: "100%" }}>
                            Зарегистрироваться
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
        </Card>
    );
};

export default Login;
