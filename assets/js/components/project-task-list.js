class TaskItem extends React.Component {
  render() {
    const task = this.props.task;
    return (
      <li class='task'>
        <input type='checkbox' /> {task.title}
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
