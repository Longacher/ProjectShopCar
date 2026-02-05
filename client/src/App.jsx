// app.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Базовый URL для API
const API_BASE_URL = 'http://localhost:8000/api'; // Замените на ваш URL

// Axios instance с базовой конфигурацией
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Клиентская модель для работы с автомобилями
class CarModel {
  // Получить список автомобилей с публичными данными
  static async getCars() {
    try {
      const response = await axios.get('/api/cars/masked/')
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // Получить список автомобилей с замаскированными данными
  static async getMaskedCars() {
    try {
      const response = await apiClient.get('/cars/masked/');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // Получить конкретный автомобиль по ID
  static async getCarById(id) {
    try {
      const response = await apiClient.get(`/cars/${id}/`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // Создать новый автомобиль
  static async createCar(carData) {
    try {
      const response = await apiClient.post('/cars/', carData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // Обновить автомобиль
  static async updateCar(id, carData) {
    try {
      const response = await apiClient.put(`/cars/${id}/`, carData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // Удалить автомобиль
  static async deleteCar(id) {
    try {
      const response = await apiClient.delete(`/cars/${id}/`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // Обработка ошибок
  static handleError(error) {
    if (error.response) {
      // Ошибка сервера
      console.error('Server Error:', error.response.data);
      console.error('Status:', error.response.status);
      return new Error(`Server Error: ${error.response.status}`);
    } else if (error.request) {
      // Ошибка сети
      console.error('Network Error:', error.request);
      return new Error('Network Error');
    } else {
      // Другая ошибка
      console.error('Error:', error.message);
      return new Error(error.message);
    }
  }
}

// Пример компонента, использующего модель
function App() {
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Загрузка автомобилей при монтировании компонента
  useEffect(() => {
    loadCars();
  }, []);

  const loadCars = async () => {
    setLoading(true);
    setError(null);
    try {
      // Можно использовать разные методы в зависимости от нужд:
      // const data = await CarModel.getCars(); // полные данные
      const data = await CarModel.getMaskedCars(); // замаскированные данные
      setCars(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCar = async (carData) => {
    try {
      const newCar = await CarModel.createCar(carData);
      setCars(prev => [...prev, newCar]);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdateCar = async (id, carData) => {
    try {
      const updatedCar = await CarModel.updateCar(id, carData);
      setCars(prev => prev.map(car => car.id === id ? updatedCar : car));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteCar = async (id) => {
    try {
      await CarModel.deleteCar(id);
      setCars(prev => prev.filter(car => car.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div>Ошибка: {error}</div>;

  return (
    <div className="App">
      <h1>Автомобили</h1>
      
      {/* Отображение списка автомобилей */}
      <div className="cars-list">
        {cars.map(car => (
          <CarCard 
            key={car.id}
            car={car}
            onUpdate={handleUpdateCar}
            onDelete={handleDeleteCar}
          />
        ))}
      </div>

      {/* Форма для создания нового автомобиля */}
      <AddCarForm onCreate={handleCreateCar} />
    </div>
  );
}

// Компонент карточки автомобиля
function CarCard({ car, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({});

  useEffect(() => {
    setEditData(car);
  }, [car]);

  const handleSave = async () => {
    await onUpdate(car.id, editData);
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="car-card editing">
        <input
          value={editData.brand || ''}
          onChange={(e) => setEditData({...editData, brand: e.target.value})}
          placeholder="Марка"
        />
        <input
          value={editData.model || ''}
          onChange={(e) => setEditData({...editData, model: e.target.value})}
          placeholder="Модель"
        />
        <input
          type="number"
          value={editData.year || ''}
          onChange={(e) => setEditData({...editData, year: parseInt(e.target.value)})}
          placeholder="Год"
        />
        {/* Добавьте остальные поля для редактирования */}
        <button onClick={handleSave}>Сохранить</button>
        <button onClick={() => setIsEditing(false)}>Отмена</button>
      </div>
    );
  }

  return (
    <div className="car-card">
      <h3>{car.brand} {car.model} ({car.year})</h3>
      
      {/* Отображение данных в зависимости от типа сериализатора */}
      {car.mileage_masked ? (
        // Маскированные данные
        <>
          <p>Пробег: {car.mileage_masked}</p>
          <p>Цена: {car.price_masked}</p>
          <p>Описание: {car.description_masked}</p>
        </>
      ) : (
        // Полные данные
        <>
          <p>Пробег: {car.mileage}</p>
          <p>Цена: {car.price}</p>
          <p>Описание: {car.description}</p>
        </>
      )}
      
      <p>Двигатель: {car.engine_type}</p>
      <p>Коробка: {car.transmission}</p>
      <p>Привод: {car.drive_type}</p>
      <p>Мощность: {car.horsepower} л.с.</p>
      <p>Владельцев: {car.owners_count}</p>
      <p>ДТП: {car.has_accidents ? 'Да' : 'Нет'}</p>
      <p>Такси: {car.was_taxi ? 'Да' : 'Нет'}</p>
      <p>Продан: {car.is_sold ? 'Да' : 'Нет'}</p>
      <p>Обслуживание в год: {car.yearly_maintenance}</p>

      <button onClick={() => setIsEditing(true)}>Редактировать</button>
      <button onClick={() => onDelete(car.id)}>Удалить</button>
    </div>
  );
}

// Компонент формы добавления автомобиля
function AddCarForm({ onCreate }) {
  const [formData, setFormData] = useState({
    brand: '',
    model: '',
    year: '',
    engine_type: 'petrol',
    transmission: 'manual',
    drive_type: 'front',
    horsepower: '',
    mileage: '',
    price: '',
    owners_count: '1',
    has_accidents: false,
    was_taxi: false,
    description: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await onCreate({
        ...formData,
        year: parseInt(formData.year),
        horsepower: parseInt(formData.horsepower),
        mileage: parseInt(formData.mileage),
        price: parseFloat(formData.price),
        owners_count: parseInt(formData.owners_count)
      });
      // Очистка формы после успешного создания
      setFormData({
        brand: '',
        model: '',
        year: '',
        engine_type: 'petrol',
        transmission: 'manual',
        drive_type: 'front',
        horsepower: '',
        mileage: '',
        price: '',
        owners_count: '1',
        has_accidents: false,
        was_taxi: false,
        description: ''
      });
    } catch (err) {
      console.error('Ошибка при создании автомобиля:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="add-car-form">
      <h2>Добавить автомобиль</h2>
      
      <input
        name="brand"
        value={formData.brand}
        onChange={handleChange}
        placeholder="Марка"
        required
      />
      
      <input
        name="model"
        value={formData.model}
        onChange={handleChange}
        placeholder="Модель"
        required
      />
      
      <input
        name="year"
        type="number"
        value={formData.year}
        onChange={handleChange}
        placeholder="Год выпуска"
        min="1990"
        max="2024"
        required
      />

      {/* Добавьте остальные поля формы */}
      
      <select
        name="engine_type"
        value={formData.engine_type}
        onChange={handleChange}
      >
        <option value="petrol">Бензин</option>
        <option value="diesel">Дизель</option>
        <option value="hybrid">Гибрид</option>
        <option value="electric">Электро</option>
        <option value="gas">Газ/Бензин</option>
      </select>

      <select
        name="transmission"
        value={formData.transmission}
        onChange={handleChange}
      >
        <option value="manual">Механическая</option>
        <option value="automatic">Автоматическая</option>
        <option value="robot">Роботизированная</option>
        <option value="variator">Вариатор</option>
      </select>

      <button type="submit">Добавить автомобиль</button>
    </form>
  );
}

export default App;
