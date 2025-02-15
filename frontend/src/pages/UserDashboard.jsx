import React, { useEffect, useState } from "react";
import { Table, Button, message } from "antd";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const UserDashboard = () => {
    const [items, setItems] = useState([]);
    const navigate = useNavigate();

    // Загружаем доступный инвентарь
    const fetchItems = async () => {
        try {
            const response = await axios.get("http://localhost:8000/items/", { withCredentials: true });
            setItems(response.data);
        } catch (error) {
            message.error("Ошибка загрузки инвентаря");
        }
    };

    useEffect(() => {
        fetchItems();
    }, []);

    // Отправка заявки на использование
    const requestItem = async (itemId) => {
        try {
            await axios.post(
                "http://localhost:8000/message/create/",
                { item_id: itemId },
                { withCredentials: true }
            );
            message.success("Заявка отправлена!");
        } catch (error) {
            message.error("Ошибка при отправке заявки");
        }
    };

    const columns = [
        {
            title: "Название",
            dataIndex: "name",
            key: "name",
        },
        {
            title: "Состояние",
            dataIndex: "condition",
            key: "condition",
        },
        {
            title: "Доступно",
            dataIndex: "quantity",
            key: "quantity",
        },
        {
            title: "Действия",
            key: "actions",
            render: (_, record) => (
                <Button type="primary" onClick={() => requestItem(record.id)}>
                    Отправить заявку
                </Button>
            ),
        },
    ];

    return (
        <div style={{ padding: 20 }}>
            <h2>Доступный инвентарь</h2>
            <Table dataSource={items} columns={columns} rowKey="id" />
        </div>
    );
};

export default UserDashboard;
