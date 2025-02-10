import React, { useState, useEffect } from "react";
import { Card, Select, Input, Button, message } from "antd";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const { TextArea } = Input;

const CreateReport = () => {
    const [report, setReport] = useState("");
    const [items, setItems] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);
    const navigate = useNavigate();

    // Загружаем предметы
    const fetchItems = async () => {
        try {
            const response = await axios.get("http://localhost:8000/items/", { withCredentials: true });
            setItems(response.data);
        } catch (error) {
            message.error("Ошибка загрузки предметов");
        }
    };

    useEffect(() => {
        fetchItems();
    }, []);

    const handleSubmit = async () => {
        if (!selectedItem || !report.trim()) {
            message.warning("Выберите предмет и введите текст отчета!");
            return;
        }

        try {
            console.log("Отправляем данные:", { message: report, item_id: selectedItem }); // ✅ Логируем перед отправкой

            await axios.post(
                "http://localhost:8000/message/create/",
                { message: report, item_id: selectedItem }, // ✅ item_id передается
                { withCredentials: true }
            );

            message.success("Отчет создан!");
            navigate("/admin");
        } catch (error) {
            console.error("Ошибка при создании отчета:", error); // ✅ Логируем ошибку
            message.error("Ошибка при создании отчета");
        }
    };


    return (
        <Card title="Создать отчет" style={{ width: 500, margin: "auto", marginTop: 100 }}>
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

            <TextArea
                placeholder="Введите текст отчета"
                value={report}
                onChange={(e) => setReport(e.target.value)}
                rows={4}
            />

            <Button type="primary" onClick={handleSubmit} style={{ marginTop: 10, width: "100%" }}>
                Создать отчет
            </Button>
        </Card>
    );
};

export default CreateReport;
