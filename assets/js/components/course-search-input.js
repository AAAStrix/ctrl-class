class CourseSearchResult extends React.Component {
  render() {
    return (
      <li>{this.props.name}</li>
    )
  }
}

class CourseSearchResultList extends React.Component {
  render() {
    return (
      <ul>
        {this.props.courses.map((result) => {
          return <CourseSearchResult name={result.title} />;
        })}
      </ul>
    );
  }
}

class CourseSearchInput extends React.Component {
  constructor(props) {
    super(props);
    this.state = { results: [], searchValue: '' };
    this.handleInputChange = this.handleInputChange.bind(this);
  }

  getResultsFromServer(search) {
    $.ajax({
      url: `/courses/search?query=${encodeURI(search)}`,
      dataType: 'json',
      success: ({ courses }) => {
        this.setState({ results: courses });
      }
    })
  }

  handleInputChange(event) {
    const searchValue = event.target.value
    this.setState({ searchValue });
    this.getResultsFromServer(searchValue);
  }

  render() {
    return (
      <div>
        <input type='text'
          placeholder='Search for a Class'
          value={this.state.searchValue}
          onChange={this.handleInputChange} />
        <CourseSearchResultList courses={this.state.results} />
      </div>
    )
  }
}

ReactDOM.render(
  <CourseSearchInput />,
  document.getElementById('course-search-input')
);
