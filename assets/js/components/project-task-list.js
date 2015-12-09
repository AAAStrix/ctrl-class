function parseStringArray(array) {
  return array.map(function(item) {
    if (typeof item === 'string') {
      return JSON.parse(item);
    }
    return item;
  });
}

let dispatchInstance = null;
class ActionDispatch {

  constructor() {
    this.store = Store.getInstance();
  }

  /**
   * Get the singleton instance of the ActionDispatch object
   */
  static getInstance() {
    if (!dispatchInstance) {
      dispatchInstance = new ActionDispatch();
    }
    return dispatchInstance;
  }

  /**
   * Send the update to the server for the tasks with some ID number, setting
   * the value of all of them in the UI to the same value
   */
  updateCompletedState(id, completed) {
    this.store.update(id, { completed });

    // Make the AJAX request and verify that it set the new status correctly
    $.post(`/task/toggle?key=${id}`)
      .done((data) => {
        if (typeof data === 'string') {
          data = JSON.parse(data);
        }
        if (data.completed != completed) {
          this.store.update(id, { completed });
        }
      });
  }

  /**
   * Send the request to the server to remove a task, then update the store
   */
  removeTask(id) {
    const task = this.store.tasks[id];
    const taskKey = task.key;
    const projectKey = task.project.key;
    $.get(`/task/remove?task_key=${taskKey}&project_key=${projectKey}`)
      .done(() => {
        this.store.update(taskKey, { removed: true });
      });
  }
}

let storeInstance = null;
class Store {
  constructor() {
    this.tasks = {};
    this.listeners = { tasks: {} };
  }

  static getInstance() {
    if (storeInstance === null) {
      storeInstance = new Store();
    }
    return storeInstance;
  }

  registerForChanges(id, callback) {
    if (!this.listeners.tasks[id]) {
      this.listeners.tasks[id] = [];
    }
    this.listeners.tasks[id].push(callback);
  }

  update(id, state) {
    if (!this.tasks[id]) {
      this.tasks[id] = {};
    }
    if (!this.listeners.tasks[id]) {
      this.listeners.tasks[id] = [];
    }
    for (let key in state) {
      const value = state[key];
      this.tasks[id][key] = value;
    }
    if (!this.tasks[id].completed) {
      this.tasks[id].completed = false;
    }
    this.listeners.tasks[id].forEach((cb) => cb(this.tasks[id]));
    return this.tasks[id];
  }
}

class EmptyPlaceholder extends React.Component {
  render() {
    const label = this.props.children;
    const containerStyle = {
      width: '100%'
    };
    const headerStyle = {
      color: 'grey',
      fontWeight: 'bold',
      textAlign: 'center',
      width: '100%'
    };
    return (
      <div className='well' style={containerStyle}>
        <h2 style={headerStyle}>{label}</h2>
      </div>
    );
  }
}

class TaskItem extends React.Component {
  constructor(props) {
    super(props);
    const { task, project } = props;
    if (project) {
      task.project = project;
    }
    this.dispatch = ActionDispatch.getInstance();
    this.store = Store.getInstance();
    this.state = { task: this.store.update(task.key, task) };
    this.store.registerForChanges(task.key, (state) => {
      this.setState({ task: state });
    });
  }

  completeTask(event) {
    const checked = event.target.checked;
    this.dispatch.updateCompletedState(this.state.task.key, checked);
  }

  removeTask() {
    if (confirm('Are you sue you want to move this task?')) {
      this.dispatch.removeTask(this.state.task.key);
    }
  }

  render() {
    const { task } = this.state;
    const { completed } = task;
    const completeHandler = this.completeTask.bind(this);
    const removeHandler = this.removeTask.bind(this);
    const style = {};
    if (completed) {
      style['text-decoration'] = 'line-through';
    } else {
      style['text-decoration'] = 'none';
    }
    return (
      <li className='task'>
        <input type='checkbox' onChange={completeHandler} checked={completed} />
        <span style={style}>{task.title}</span>
        &nbsp;
        <a href='#' onClick={removeHandler}>Remove</a>
      </li>
    );
  }
}

class TaskList extends React.Component {
  constructor(props) {
    super(props);
    this.store = Store.getInstance();
    let { tasks, project } = props;
    tasks = parseStringArray(tasks);
    tasks.forEach((task) => {
      const { removed } = task;
      this.store.registerForChanges(task.key, (state) => {
        if (removed !== state.removed) {
          this.updateStateFor(state);
        }
      });
    });
    this.state = { tasks, project };
  }

  updateStateFor(updatedTask) {
    const tasks = this.state.tasks.map(function(task) {
      if (task.key === updatedTask.key) {
        task.removed = updatedTask.removed;
      }
      return task;
    });
    this.setState({ tasks });
  }

  render() {
    const project = this.state.project;
    let tasks = this.state.tasks
      .filter((task) => !task.removed)
      .map((task) => {
        return <TaskItem task={task} project={project}/>;
      });
    if (tasks.length === 0) {
      tasks = <EmptyPlaceholder>No Tasks</EmptyPlaceholder>;
    }
    return (
      <ul className='task-list'>
        {tasks}
      </ul>
    );
  }
}

class ProjectItem extends React.Component {
  render() {
    const project = this.props.project;
    const url = `/project?key=${project.key}`;
    return (
      <div className='project'>
        <h3><a href={url}>{project.title}</a></h3>
        <TaskList tasks={project.tasks} project={project}/>
      </div>
    );
  }
}

class ProjectList extends React.Component {
  render() {
    let projects = this.props.projects.map((project) => {
      return <ProjectItem project={project} />;
    });
    if (projects.length === 0) {
      projects = <EmptyPlaceholder>No Projects</EmptyPlaceholder>;
    }
    return (
      <div className='projects'>
        {projects}
      </div>
    );
  }
}

document.registerReact('project-list', ProjectList);
document.registerReact('task-list', TaskList);
