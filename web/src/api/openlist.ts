import request from './request'

interface Response<T> {
  content: T
}

interface ListParams {
  path: string
  password?: string
  page?: number
  per_page?: number
  refresh?: boolean
}

export type OpenListType = {
  id: string
  path: string
  name: string
  size: number
  is_dir: boolean
  modified: string
  created: string
  sign: string
  thumb: string
  type: number
  hashinfo: string
  hash_info: null
}

async function list(params: ListParams): Promise<OpenListType[]> {
  const requestParams = {
    path: params.path,
    password: params.password || '',
    page: params.page || 1,
    per_page: params.per_page || 0,
    refresh: params.refresh || false,
  }

  const response = await request<Response<OpenListType[]>>('/openlist/list', {
    method: 'POST',
    body: JSON.stringify(requestParams),
  })
  return response.content
}

export const OpenList = {
  list,
}

