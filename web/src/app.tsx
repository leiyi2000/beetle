import { useState } from 'react'
import { useEffect } from 'react'
import '@ant-design/v5-patch-for-react-19'
import { message, type TreeSelectProps } from 'antd'
import { DoubleRightOutlined } from '@ant-design/icons'
import { TreeSelect, Button, Radio, InputNumber, Modal } from 'antd'

import { OpenList } from './api/openlist'
import { Task, type TaskType } from './api/task'

type TreeNode = {
  id: string
  pId: string
  value: string
  title: string
  isLeaf?: boolean
  disabled?: boolean
}
function Tree(props: { dir: string; updateDir: (value: string) => void }) {
  const { dir, updateDir } = props
  const [treeData, setTreeData] = useState<TreeNode[]>([])

  useEffect(() => {
    OpenList.list({ path: '/' }).then((response) => {
      setTreeData(
        response.map((item) => ({
          id: '/' + item.name,
          pId: '/',
          value: '/' + item.name,
          title: item.name,
          isLeaf: !item.is_dir,
          disabled: !item.is_dir,
        }))
      )
    })
  }, [])

  const onLoadData: TreeSelectProps['loadData'] = async (node) => {
    const { id } = node
    const response = await OpenList.list({ path: id })
    setTreeData(
      treeData.concat(
        response.map((item) => ({
          id: id + '/' + item.name,
          pId: id,
          value: id + '/' + item.name,
          title: item.name,
          isLeaf: !item.is_dir,
          disabled: !item.is_dir,
        }))
      )
    )
  }

  return (
    <div className="h-8 w-100">
      <TreeSelect
        value={dir}
        onChange={(value) => {
          let dir = value;
          if (dir && !dir.endsWith("/")) {
            dir += "/";
          }
          updateDir(dir)
        }}
        treeData={treeData}
        loadData={onLoadData}
        treeDataSimpleMode={true}
        treeNodeLabelProp="value"
        style={{ width: '100%', height: '100%', fontSize: 18 }}
      />
    </div>
  )
}

function TaskCard(props: {
  task: TaskType
  onCleanupChange: (cleanup: boolean) => void
  onIntervalChange: (interval: number) => void
  onRunningChange: (isRunning: boolean) => void
  setTasks: React.Dispatch<React.SetStateAction<TaskType[]>>
}) {
  const { task, setTasks, onRunningChange, onCleanupChange, onIntervalChange } =
    props
  const [loading, setLoading] = useState<boolean>(false)

  const handleRemove = async () => {
    setLoading(true)
    await Task.remove(task.id)
    setTasks((prev) => prev.filter((t) => t.id !== task.id))
    setLoading(false)
  }

  const handleUpdateSrc = (src: string) => {
    setTasks((prev) => prev.map((t) => (t.id === task.id ? { ...t, src } : t)))
  }

  const handleUpdateDst = (dst: string) => {
    setTasks((prev) => prev.map((t) => (t.id === task.id ? { ...t, dst } : t)))
  }

  return (
    <div className="flex flex-col space-y-3 rounded-xl border border-gray-200 bg-white px-8 py-3 shadow-sm transition-shadow duration-200 hover:shadow-md">
      <div className="flex min-h-10 flex-row items-center justify-between gap-5">
        <Tree {...{ dir: task.src, updateDir: handleUpdateSrc }} />
        <div className="flex items-center">
          <DoubleRightOutlined
            className="text-blue-600"
            style={{ fontSize: 16 }}
          />
        </div>
        <Tree {...{ dir: task.dst, updateDir: handleUpdateDst }} />
      </div>

      <hr className="my-2 w-full border-t border-gray-200" />

      <div className="flex flex-row justify-between gap-5">
        <div className="flex flex-col gap-2">
          <div className="flex text-sm font-medium text-gray-700">
            <div className="min-w-20">
              <p>开启任务</p>
            </div>
            <div className="min-w-15">
              <Radio
                checked={task.status === 'running'}
                onChange={() => onRunningChange?.(true)}
              >
                是
              </Radio>
            </div>
            <div className="min-w-15">
              <Radio
                checked={task.status != 'running'}
                onChange={() => onRunningChange?.(false)}
              >
                否
              </Radio>
            </div>
          </div>
          <div className="flex items-center text-sm font-medium text-gray-700">
            <div className="max-w-20 min-w-20">
              <p>删除源文件</p>
            </div>
            <div className="min-w-15">
              <Radio
                checked={task.cleanup === true}
                onChange={() => onCleanupChange?.(true)}
                value="true"
              >
                是
              </Radio>
            </div>
            <div className="min-w-15">
              <Radio
                checked={task.cleanup === false}
                onChange={() => onCleanupChange?.(false)}
                value="false"
              >
                否
              </Radio>
            </div>
          </div>
        </div>
        <div className="flex flex-row items-center justify-center">
          <div className="min-w-20">
            <p>同步频率</p>
          </div>
          <div className="flex w-28 items-center gap-2">
            <InputNumber
              value={Math.round(task.interval / 60)}
              min={5}
              step={1}
              onChange={(value) => onIntervalChange((value || 0) * 60)}
              style={{ width: '100%' }}
            />
            <span className="text-sm whitespace-nowrap text-gray-500">
              分钟
            </span>
          </div>
        </div>
      </div>
      <div className="flex h-12 flex-row items-end justify-end gap-8">
        <Button
          type="primary"
          loading={loading}
          onClick={() => {
            Modal.confirm({
              title: '确认删除吗？',
              okText: '确认',
              cancelText: '取消',
              okType: 'danger',
              onOk: () => {
                handleRemove()
              },
            })
          }}
        >
          删除
        </Button>
        <Button
          type="primary"
          onClick={async () => {
            if (!task.src || !task.dst) {
              message.error('路径不允许为空')
              return
            }
            if (task._create == true) {
              const response = await Task.create({
                src: task.src,
                dst: task.dst,
                cleanup: task.cleanup,
                interval: task.interval,
                status: task.status,
              })
              if ('error' in response) {
                message.error('任务已存在')
                return
              }
              setTasks((prev) =>
                prev.map((t) => (t.id === task.id ? response : t))
              )
              message.success('创建成功')
              return
            }
            const rows = await Task.update({
              id: task.id,
              src: task.src,
              dst: task.dst,
              cleanup: task.cleanup,
              interval: task.interval,
              status: task.status,
            })
            if (rows == 1) {
              message.success('成功保存')
            } else {
              message.error('保存失败')
            }
          }}
        >
          保存
        </Button>
      </div>
    </div>
  )
}

function TopNav(props: {
  setTasks: React.Dispatch<React.SetStateAction<TaskType[]>>
}) {
  const { setTasks } = props

  return (
    <div className="border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-gray-900">Beetle</h1>
          </div>
          <Button
            type="primary"
            size="large"
            className="border-blue-600 bg-blue-600 shadow-sm hover:border-blue-700 hover:bg-blue-700"
            onClick={() => {
              setTasks((prv) => {
                return [
                  ...prv,
                  {
                    id: Date.now(),
                    src: '',
                    dst: '',
                    cleanup: false,
                    interval: 60 * 60 * 8,
                    status: 'running',
                    created_at: '',
                    updated_at: '',
                    _create: true,
                  },
                ]
              })
            }}
          >
            新增任务
          </Button>
        </div>
      </div>
    </div>
  )
}

function App() {
  const [tasks, setTasks] = useState<TaskType[]>([])

  useEffect(() => {
    Task.reads().then((tasks) => {
      setTasks(tasks)
    })
  }, [])

  const handleTaskRunningChange = (taskId: number, isRunning: boolean) => {
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId
          ? { ...task, status: isRunning ? 'running' : 'stopped' }
          : task
      )
    )
  }

  const handleCleanupChange = (taskId: number, cleanup: boolean) => {
    setTasks((prev) =>
      prev.map((task) => (task.id === taskId ? { ...task, cleanup } : task))
    )
  }

  const handleIntervalChange = (taskId: number, interval: number) => {
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId
          ? { ...task, interval: Math.max(300, interval) }
          : task
      )
    )
  }
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <TopNav setTasks={setTasks} />
      <div className="mx-auto flex max-w-7xl justify-center px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex w-200 min-w-100 flex-col gap-4">
          {tasks.map((task) => (
            <TaskCard
              setTasks={setTasks}
              key={task.id}
              task={task}
              onRunningChange={(isRunning) =>
                handleTaskRunningChange(task.id, isRunning)
              }
              onCleanupChange={(cleanup) =>
                handleCleanupChange(task.id, cleanup)
              }
              onIntervalChange={(interval) =>
                handleIntervalChange(task.id, interval)
              }
            />
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
