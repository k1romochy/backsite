import React, { useEffect, useState } from "react";
import { Button, Layout, Table, message } from "antd";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const { Header, Content } = Layout;

const AdminDashboard = () => {
    const navigate = useNavigate();
    const [reports, setReports] = useState([]);

    // Загружаем отчеты с сервера
    const fetchReports = async () => {
        try {
            const response = await axios.get("http://localhost:8000/message/", { withCredentials: true });
            setReports(response.data);
        } catch (error) {
            message.error("Ошибка при загрузке отчетов");
        }
    };

    useEffect(() => {
        fetchReports();
    }, []);

    // Определяем колонки таблицы
    const columns = [
        {
            title: "ID",
            dataIndex: "id",
            key: "id",
        },
        {
            title: "Пользователь",
            dataIndex: "username",
            key: "username",
        },
        {
            title: "Предмет",
            dataIndex: "item_name",
            key: "item_name",
        },
        {
            title: "Сообщение",
            dataIndex: "message",
            key: "message",
        },
        {
            title: "Дата создания",
            dataIndex: "created_at",
            key: "created_at",
        },
    ];

    return (
        <Layout>
            {/* Шапка */}
            <Header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h2 style={{ color: "white" }}>Админ-панель</h2>
                <div>
                    <Button type="default" onClick={() => navigate("/")}>
                        🏠 На главный экран
                    </Button>
                    <Button type="primary" style={{ marginLeft: 10 }} onClick={() => navigate("/create-report")}>
                        📊 Создать отчет
                    </Button>
                </div>
            </Header>

            {/* Контент с таблицей отчетов */}
            <Content style={{ padding: 20 }}>
                <h2>Список отчетов</h2>
                <Table dataSource={reports} columns={columns} rowKey="id" />
            </Content>
        </Layout>
    );
};

export default AdminDashboard;
