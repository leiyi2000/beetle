import request from './request'

export type TaskType = {
  id: number
  src: string
  dst: string
  interval: number
  cleanup: boolean
  status: 'running' | 'stopped'
  created_at: string
  updated_at: string
  _create?: boolean
}

export async function reads() {
  return request<TaskType[]>('/task/reads', {
    method: 'POST',
  })
}

export async function remove(id: number) {
  return request('/task/delete', {
    method: 'POST',
    body: JSON.stringify({ id: id }),
  })
}

export async function create(payload: {
  src: string
  dst: string
  cleanup: boolean
  interval: number
  status: string
}) {
  return request<TaskType>('/task/create', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function update(payload: {
  id: number
  src: string
  dst: string
  cleanup: boolean
  interval: number
  status: string
}) {
  return request<number>('/task/update', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export const Task = {
  reads: reads,
  remove: remove,
  create: create,
  update: update,
}
