import React, { useState } from "react";
import { Form, Input, Button, message } from "antd";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const AddItem = () => {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const onFinish = async (values) => {
        setLoading(true);
        try {
            await axios.post("http://localhost:8000/items/create_item/", values, {withCredentials: true});
            message.success("Предмет успешно добавлен!");
            navigate("/");
        } catch (error) {
            message.error("Ошибка при добавлении предмета");
        }
        setLoading(false);
    };

    return (
        <Form layout="vertical" onFinish={onFinish} style={{ maxWidth: 400, margin: "auto", marginTop: 50 }}>
            <Form.Item label="Название предмета" name="name" rules={[{ required: true, message: "Введите название!" }]}>
                <Input />
            </Form.Item>
            <Form.Item label="Количество" name="quantity" rules={[{ required: true, message: "Введите количество!" }]}>
                <Input type="number" />
            </Form.Item>
            <Form.Item label="Состояние" name="condition" rules={[{ required: true, message: "Введите состояние!" }]}>
                <Input />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                    Добавить предмет
                </Button>
            </Form.Item>
        </Form>
    );
};

export default AddItem;
