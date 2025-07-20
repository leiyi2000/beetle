/**
 * API服务层 - 集中管理所有API请求
 */

// 基础API URL从环境变量获取
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api'

// 通用请求选项
const defaultOptions: RequestInit = {
  headers: {
    'Content-Type': 'application/json',
  },
}

// 通用请求处理函数
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const url = `${API_BASE_URL}${endpoint}`
    const response = await fetch(url, {
      ...defaultOptions,
      ...options,
    })

    // 检查响应状态
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`)
    }

    // 解析JSON响应
    return (await response.json()) as T
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}

// 用户相关API
export const userAPI = {
  // 获取用户信息
  getProfile: () => fetchAPI<UserProfile>('/user/profile'),

  // 更新用户信息
  updateProfile: (data: Partial<UserProfile>) =>
    fetchAPI<UserProfile>('/user/profile', {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
}

// 数据相关API
export const dataAPI = {
  // 获取数据列表
  getItems: () => fetchAPI<Item[]>('/items'),

  // 获取单个数据项
  getItem: (id: string) => fetchAPI<Item>(`/items/${id}`),

  // 创建数据项
  createItem: (data: Omit<Item, 'id'>) =>
    fetchAPI<Item>('/items', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // 更新数据项
  updateItem: (id: string, data: Partial<Item>) =>
    fetchAPI<Item>(`/items/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  // 删除数据项
  deleteItem: (id: string) =>
    fetchAPI<void>(`/items/${id}`, {
      method: 'DELETE',
    }),
}

// 类型定义
export interface UserProfile {
  id: string
  name: string
  email: string
  avatar?: string
}

export interface Item {
  id: string
  title: string
  description: string
  createdAt: string
  updatedAt: string
}
