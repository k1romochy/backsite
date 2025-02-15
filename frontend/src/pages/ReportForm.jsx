import React, { useState, useEffect } from "react";
import { Card, Select, Button, message } from "antd";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const ReportForm = () => {
    const [items, setItems] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);
    const navigate = useNavigate();

    // Загружаем предметы пользователя
    const fetchUserItems = async () => {
        try {
            const response = await axios.get("http://localhost:8000/items/", { withCredentials: true });
            setItems(response.data);
        } catch (error) {
            message.error("Ошибка загрузки предметов");
        }
    };

    useEffect(() => {
        fetchUserItems();
    }, []);

    const handleSubmit = async () => {
        if (!selectedItem) {
            message.warning("Выберите предмет!");
            return;
        }

        try {
            await axios.post(
                "http://localhost:8000/request/create/",
                { item_id: selectedItem, condition: "На рассмотрении" }, // ✅ Теперь отправляем `condition`
                { withCredentials: true }
            );
            message.success("Заявка отправлена!");
            navigate("/");
        } catch (error) {
            message.error("Ошибка при отправке заявки");
        }
    };

    return (
        <Card title="Отправить заявку" style={{ width: 500, margin: "auto", marginTop: 100 }}>
            <Select
                placeholder="Выберите предмет"
                style={{ width: "100%", marginBottom: 10 }}
                onChange={(value) => setSelectedItem(value)}
            >
                {items.map((item) => (
                    <Select.Option key={item.id} value={item.id}>
                        {item.name}
                    </Select.Option>
                ))}
            </Select>

            <Button type="primary" onClick={handleSubmit} style={{ marginTop: 10, width: "100%" }}>
                Отправить заявку
            </Button>
        </Card>
    );
};

export default ReportForm;
