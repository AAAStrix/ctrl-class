class TaskItem extends React.Component {
  constructor(props) {
    super(props);
    const { task } = props;
    let { completed } = task;
    if (typeof completed === 'undefined') {
      completed = false;
    }
    this.state = { completed };
  }

  handleChange(event) {
    const checked = event.target.checked;
    // TODO: Add some sort of AJAX request here to toggle the task in the DB
    this.setState({
      completed: checked
    });
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
    const tasks = this.props.tasks;
    return (
      <ul className='task-list'>
        {tasks.map((task) => {
          return <TaskItem task={task} />
        })}
      </ul>
    );
  }
}

class ProjectItem extends React.Component {
  render() {
    const project = this.props.project;
    return (
      <div className='project'>
        <h3>{project.title}</h3>
        <TaskList tasks={project.tasks} />
      </div>
    );
  }
}

class ProjectList extends React.Component {
  render() {
    return (
      <div className='projects'>
        {this.props.projects.map((project) => {
          return <ProjectItem project={project} />
        })}
      </div>
    );
  }
}

document.registerReact('project-list', ProjectList);
document.registerReact('task-list', TaskList);
