import React, { useEffect, useState, useContext } from "react";
import { Table, Button, message, Tag } from "antd";
import axios from "axios";
import { AuthContext } from "../components/AuthContext.jsx";

const AdminRequests = () => {
    const { user } = useContext(AuthContext);
    const [requests, setRequests] = useState([]);

    // Загружаем заявки
    const fetchRequests = async () => {
        try {
            const response = await axios.get("http://localhost:8000/request/", { withCredentials: true });
            setRequests(response.data);
        } catch (error) {
            message.error("Ошибка при загрузке заявок");
        }
    };

    useEffect(() => {
        fetchRequests();
    }, []);

    // Обновление статуса заявки
    const updateRequestCondition = async (requestId, newCondition) => {
        try {
            await axios.patch(
                `http://localhost:8000/request/${requestId}/`,
                { condition: newCondition }, // ✅ Передаем только `condition`
                { withCredentials: true }
            );
            message.success("Статус заявки обновлен!");
            fetchRequests(); // Перезагружаем список
        } catch (error) {
            message.error("Ошибка при обновлении статуса");
        }
    };

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
            title: "ID предмета",
            dataIndex: "item_id",
            key: "item_id",
        },
        {
            title: "Название предмета",
            dataIndex: "item_name",
            key: "item_name",
        },
        {
            title: "Статус",
            dataIndex: "condition",
            key: "condition",
            render: (condition) => (
                <Tag color={condition === "Одобрено" ? "green" : condition === "Отклонено" ? "red" : "blue"}>
                    {condition}
                </Tag>
            ),
        },
        {
            title: "Действия",
            key: "actions",
            render: (_, record) => (
                <>
                    <Button
                        type="primary"
                        onClick={() => updateRequestCondition(record.id, "Одобрено")}
                        style={{ marginRight: 8 }}
                    >
                        ✅ Одобрить
                    </Button>
                    <Button type="default" danger onClick={() => updateRequestCondition(record.id, "Отклонено")}>
                        ❌ Отклонить
                    </Button>
                </>
            ),
        },
    ];

    if (!user || user.role !== "Admin") {
        return <div>Доступ запрещен</div>;
    }

    return (
        <div style={{ padding: 20 }}>
            <h2>Управление заявками</h2>
            <Table dataSource={requests} columns={columns} rowKey="id" />
        </div>
    );
};

export default AdminRequests;
