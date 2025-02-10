import React, { useContext, useEffect, useState } from "react";
import { Menu, message, Flex } from "antd";
import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import axios from "axios";
import CurrencyCardItem from "./components/CurrencyCardItem.jsx";
import AddItem from "./components/AddItem.jsx";
import ReportForm from "./pages/ReportForm.jsx";
import AdminRequests from "./pages/AdminRequests.jsx";
import CreateReport from "./pages/CreateReport.jsx";
import { AuthContext } from "./components/AuthContext.jsx";


const AppContent = () => {
    const [current, setCurrent] = useState([]);
    const [currencyId, setCurrencyId] = useState(1);
    const [currencyData, setCurrencyData] = useState(null);
    const [newQuantity, setNewQuantity] = useState("");
    const [newCondition, setNewCondition] = useState("");
    const [userId, setUserId] = useState("");
    const navigate = useNavigate();
    const {user, logout} = useContext(AuthContext);

    const fetchCurrentItems = () => {
        axios.get("http://localhost:8000/items/", { withCredentials: true })
            .then(response => {
                const currencyResponse = response.data;

                // Формируем список элементов меню
                const menuItems = currencyResponse.map(c => (
                    <Menu.Item key={c.id}>{c.name}</Menu.Item>
                ));

                setCurrent(menuItems);
            })
            .catch(error => {
                message.error("Ошибка при загрузке списка предметов");
            });
    };
    // Получение данных конкретного предмета
    const fetchCurrency = () => {
        axios.get(`http://localhost:8000/items/${currencyId}/`, {withCredentials: true}).then(response => {
            console.log(response.data);
            setCurrencyData(response.data);
        });
    };

    // Удаление предмета
    const deleteItem = async () => {
        try {
            await axios.delete(`http://localhost:8000/items/${currencyId}/`, {withCredentials: true});
            message.success("Предмет удален!");
            fetchCurrentItems();
            setCurrencyData(null);
        } catch (error) {
            message.error("Ошибка при удалении предмета");
        }
    };

    // Обновление предмета
    const updateItem = async () => {
        try {
            await axios.patch(`http://localhost:8000/items/${currencyId}/`, {
                quantity: parseInt(newQuantity),
                condition: newCondition,
                withCredentials: true
            });
            message.success("Предмет обновлен!");
            fetchCurrency();
        } catch (error) {
            message.error("Ошибка при обновлении предмета");
        }
    };

    // Привязка пользователя
    const assignUser = async () => {
        try {
            await axios.post(`http://localhost:8000/items/${currencyId}/assign/${userId}/`, {withCredentials: true});
            message.success("Пользователь привязан!");
            fetchCurrency();
        } catch (error) {
            message.error("Ошибка при привязке пользователя");
        }
    };

    // Отвязка пользователя
    const unassignUser = async () => {
        try {
            await axios.post(`http://localhost:8000/items/${currencyId}/unassign/${userId}/`, { withCredentials: true, user_id: parseInt(userId) });
            message.success("Пользователь отвязан!");
            fetchCurrency();
        } catch (error) {
            message.error("Ошибка при отвязке пользователя");
        }
    };

    useEffect(() => {
        fetchCurrency();
    }, [currencyId]);

    useEffect(() => {
        fetchCurrentItems();
    }, []);

    const onClick = (e) => {
        const id = Number(e.key);
        if (!isNaN(id)) {
            setCurrencyId(id);
        }
    };

    return (
        <Flex className="h-screen" gap="middle">
            <Menu
                style={{ width: 256, position: "fixed", left: 0, top: 0, height: "100vh", overflowY: "auto" }}
                onClick={onClick}
                selectedKeys={[currencyId.toString()]}
            >
                {/* Заголовок списка предметов */}
                <Menu.ItemGroup title="Список предметов">
                    {current} {/* Здесь будут загруженные предметы */}
                </Menu.ItemGroup>

                {user?.role === "Admin" && (
                    <>
                        <Menu.Divider />
                        <Menu.ItemGroup title="Админ-панель">
                            <Menu.Item key="add-item" onClick={() => navigate("/add-item")} style={{ color: "red" }}>
                                ➕ Добавить предмет
                            </Menu.Item>
                            <Menu.Item key="admin-requests" onClick={() => navigate("/requests")} style={{ color: "red" }}>
                                📌 Управление заявками
                            </Menu.Item>
                            <Menu.Item key="admin-panel" onClick={() => navigate("/admin")} style={{ color: "red" }}>
                                ⚙️ Админ-панель
                            </Menu.Item>
                            <Menu.Item key="create-report" onClick={() => navigate("/create-report")} style={{ color: "red" }}>
                                📊 Создать отчет
                            </Menu.Item>
                        </Menu.ItemGroup>
                    </>
                )}

                <Menu.Divider />
                <Menu.Item key="logout" onClick={logout}>
                    🚪 Выйти
                </Menu.Item>
            </Menu>

            <Flex justify="center" align="center" style={{ flex: 1, height: "100vh", marginLeft: 256 }}>
                <Routes>
                    <Route path="/add-item" element={<AddItem />} />
                    <Route path="/report" element={<ReportForm />} /> {/* ✅ Заявка пользователя */}
                    <Route path="/requests" element={user?.role === "Admin" ? <AdminRequests /> : <Navigate to="/" />} />
                    <Route path="/create-report" element={user?.role === "Admin" ? <CreateReport /> : <Navigate to="/" />} />
                    <Route
                        path="/"
                        element={
                            currencyData ? (
                                <CurrencyCardItem
                                    currency={currencyData}
                                    deleteItem={deleteItem}
                                    isAdmin={user?.role === "Admin"}
                                    newQuantity={newQuantity}
                                    setNewQuantity={setNewQuantity}
                                    newCondition={newCondition}
                                    setNewCondition={setNewCondition}
                                    updateItem={updateItem}
                                    userId={userId}
                                    setUserId={setUserId}
                                    assignUser={assignUser}
                                    unassignUser={unassignUser}
                                />
                            ) : (
                                <div>Выберите предмет</div>
                            )
                        }
                    />
                </Routes>
            </Flex>
        </Flex>
    );
};

export default AppContent



