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

class ProjectItem extends React.Component {
  render() {
    const project = this.props.project;
    return (
      <div className='project'>
        <h3>{project.title}</h3>
        <ul className='task-list'>
          {project.tasks.map((task) => {
            return <TaskItem task={task} />
          })}
        </ul>
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
