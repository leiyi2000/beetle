import { useState, useEffect } from 'react'

// 定义一个通用的本地存储钩子，支持任意类型的数据
function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((val: T) => T)) => void] {
  // 获取初始值的状态函数
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      // 尝试从localStorage获取值
      const item = window.localStorage.getItem(key)
      // 如果存在则解析并返回，否则返回初始值
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      // 如果出错则返回初始值
      console.error(`Error reading localStorage key "${key}":`, error)
      return initialValue
    }
  })

  // 当键或值变化时更新localStorage
  useEffect(() => {
    try {
      // 将值序列化并存储到localStorage
      window.localStorage.setItem(key, JSON.stringify(storedValue))
    } catch (error) {
      // 记录错误
      console.error(`Error setting localStorage key "${key}":`, error)
    }
  }, [key, storedValue])

  // 返回存储的值和更新函数
  return [storedValue, setStoredValue]
}

export default useLocalStorage
