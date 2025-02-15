import React from "react";
import { Card, Button, Input, Flex } from "antd";
import { useNavigate } from "react-router-dom";

const CurrencyCardItem = ({
                              currency,
                              isAdmin,
                              deleteItem,
                              newQuantity,
                              setNewQuantity,
                              newCondition,
                              setNewCondition,
                              updateItem,
                              userId,
                              setUserId,
                              assignUser,
                              unassignUser,
                          }) => {
    const navigate = useNavigate();

    return (
        <Card title={currency.name} style={{ width: 550 }}>
            <p>Название: {currency.name}</p>
            <p>Количество: {currency.quantity}</p>
            <p>Состояние: {currency.condition}</p>

            <p>
                Закреплённые пользователи:{" "}
                {currency.users?.length > 0
                    ? currency.users.map((user) => `${user.username} - ${user.id}`).join(", ")
                    : "Нет пользователей"}
            </p>

            {!isAdmin && (
                <Button type="primary" onClick={() => navigate("/report")}>
                    Оставить отчет
                </Button>
            )}

            {isAdmin && (
                <Flex justify="space-around" gap="large" className="mb-4">
                    <Flex vertical align="center">
                        <Button type="primary" danger onClick={deleteItem}>
                            Удалить предмет
                        </Button>
                    </Flex>

                    <Flex vertical align="center">
                        <Button type="primary" onClick={updateItem}>
                            Обновить предмет
                        </Button>
                        <Flex vertical gap="small" className="mt-2">
                            <Input
                                placeholder="Количество"
                                value={newQuantity}
                                onChange={(e) => setNewQuantity(e.target.value)}
                            />
                            <Input
                                placeholder="Состояние"
                                value={newCondition}
                                onChange={(e) => setNewCondition(e.target.value)}
                            />
                        </Flex>
                    </Flex>

                    <Flex vertical align="center">
                        <Button type="default" danger onClick={unassignUser}>
                            Привязать/Отвязать
                        </Button>
                        <Flex vertical gap="small" className="mt-2">
                            <Input
                                placeholder="ID пользователя"
                                value={userId}
                                onChange={(e) => setUserId(e.target.value)}
                            />
                            <Button type="default" onClick={assignUser}>
                                Привязать
                            </Button>
                        </Flex>
                    </Flex>
                </Flex>
            )}
        </Card>
    );
};

export default CurrencyCardItem;
