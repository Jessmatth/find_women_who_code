
class SearchInputs extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
      location: 'San Francisco',
      min_experience: '1',
      max_experience: '2'
      };
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleInputChange(event) {
      const target = event.target;
      const value = target.type === 'text' ? target.submitted : target.value;
      const name = target.name;
  
      this.setState({
        [name]: value
      });
    }
  
    handleSubmit(event) {
      alert('A search was submitted: ' + this.state.value);
      event.preventDefault();
    }
  
    render() {
      return (
        <form>
          <label>
            Location:
            <input type="text" value={this.state.location} onChange={this.handleChange} />
          </label>
        
          <br />
        
            <label>
             Minimum Years of experience:
            <select value={this.state.min_experience} onChange={this.handleChange}>
              <option value="1">One</option>
              <option value="2">Two</option>
              <option value="3">Three</option>
              <option value="4">Four</option>
              <option value="5">Five</option>
              <option value="6">Six</option>
              <option value="7">Seven</option>
              <option value="8">Eight</option>
              <option value="9">Nine</option>
              <option value="10">Ten</option>
              <option value="11">Eleven</option>
              <option value="12">Twelve</option>
              <option value="13">Thirteen</option>
              <option value="14">Fourteen</option>
            </select>
            </label>
        
            <label>
             Max Years of experience:
            <select value={this.state.max_experience} onChange={this.handleChange}>
              <option value="1">One</option>
              <option value="2">Two</option>
              <option value="3">Three</option>
              <option value="4">Four</option>
              <option value="5">Five</option>
              <option value="6">Six</option>
              <option value="7">Seven</option>
              <option value="8">Eight</option>
              <option value="9">Nine</option>
              <option value="10">Ten</option>
              <option value="11">Eleven</option>
              <option value="12">Twelve</option>
              <option value="13">Thirteen</option>
              <option value="14">Fourteen</option>
            </select>
            </label>
          <input type="submit" value="Submit" />
        </form>
      )};
      }
 
class SearchOutputs  {

    constructor(programmer) {
        this.name = programmer.name;
        this.company = programmer.company;
        this.location = programmer.location;
        this.created_at = programmer.created_at;
        this.email = programmer.email;
        this.twitter_username = programmer.twitter_username;

    }

    display() {
  return(

    <div className="tc bg-light-green dib br3 pa3 ma2 grow bw2 shadow-5">
      <h1>{this.name}</h1>
      <ul>
        <li>{this.company}</li>
        <li>{this.location}</li>
        <li>{this.created_at}</li>
        <li>{this.email}</li>
        <li>{this.twitter_username}</li>
     </ul>
    </div>
    )
}};
