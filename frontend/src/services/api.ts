import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export interface TodoItem {
  id?: string;  // MongoDB使用字符串ID
  title: string;
  description?: string;
  completed: boolean;
  created_at?: string;
}

export const api = {
  getTodos: async (): Promise<TodoItem[]> => {
    const response = await axios.get(`${API_BASE_URL}/todos`);
    // 转换 _id 为 id
    return response.data.map((item: any) => ({
      ...item,
      id: item._id,
    }));
  },

  createTodo: async (todo: Omit<TodoItem, 'id'>): Promise<TodoItem> => {
    const response = await axios.post(`${API_BASE_URL}/todos`, todo);
    const item = response.data;
    return { ...item, id: item._id };
  },

  updateTodo: async (id: string, todo: TodoItem): Promise<TodoItem> => {
    const response = await axios.put(`${API_BASE_URL}/todos/${id}`, todo);
    const item = response.data;
    return { ...item, id: item._id };
  },

  deleteTodo: async (id: string): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/todos/${id}`);
  },
}; 