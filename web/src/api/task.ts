import request from './request'

export type TaskType = {
  id: number
  src: string
  dst: string
  interval: number
  cleanup: boolean
  status: string
  created_at: string
  updated_at: string
}

export async function reads() {
  return request<TaskType[]>('/task/reads', {
    method: 'POST',
  })  
}

export const Task = {
  reads: reads
}