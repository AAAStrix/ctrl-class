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
    this.tasks = {};
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
   * Resgister a task item to a particular ID
   */
  registerTaskItem(id, instance) {
    if (!this.tasks[id]) {
      this.tasks[id] = [];
    }
    this.tasks[id].push(instance);
  }

  /**
   * Set the value of all task items with the same ID number
   */
  updateCompletionFor(id, completed) {
    this.tasks[id].forEach(function(instance) {
      instance.setState({ completed });
    });
  }

  /**
   * Send the update to the server for the tasks with some ID number, setting
   * the value of all of them in the UI to the same value
   */
  sendUpdateFor(id, value) {
    this.updateCompletionFor(id, value);

    // Make the AJAX request and verify that it set the new status correctly
    $.post(`/task/toggle?key=${id}`)
      .done((data) => {
        if (typeof data === 'string') {
          data = JSON.parse(data);
        }
        if (data.completed != value) {
          this.updateCompletionFor(id, data.completed);
        }
      });
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
    const { task } = props;
    const { key } = task;
    let { completed } = task;
    if (typeof completed === 'undefined') {
      completed = false;
    }
    this.state = { completed };
    this.dispatch = ActionDispatch.getInstance();
    this.dispatch.registerTaskItem(key, this);
  }

  setChecked(complete) {
    this.setState({
      completed: complete
    });
  }

  handleChange(event) {
    const checked = event.target.checked;
    this.dispatch.sendUpdateFor(this.props.task.key, checked);
  }

  render() {
    const task = this.props.task;
    const checked = this.state.completed;
    const clickHandler = this.handleChange.bind(this);
    const style = {};
    if (checked) {
      style['text-decoration'] = 'line-through';
    } else {
      style['text-decoration'] = 'none';
    }
    return (
      <li className='task'>
        <input type='checkbox' onChange={clickHandler} checked={checked} />
        <span style={style}>{task.title}</span>
      </li>
    );
  }
}

class TaskList extends React.Component {
  render() {
    const project = this.props.project;
    this.props.tasks = parseStringArray(this.props.tasks);
    let tasks = this.props.tasks.map((task) => {
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
