import React from "react";


function App() {
    const [location, min_experience, max_experience] = React.useState({});
    
    React.useEffect(() => {
      fetch("/fwwcdb")
        .then((response) => response.json())
        .then((programmerData) => setResults(programmerData));
    }, []);
  
  
    return (
      <ReactRouterDOM.BrowserRouter>
        <Navbar brand="find_women_who_code()" />
        <div className="container-fluid">
          <ReactRouterDOM.Route exact path="/">
            <Homepage />
          </ReactRouterDOM.Route>
          <ReactRouterDOM.Route exact path="/search_results">
            <SearchInputs location={location} min_experience={min_experience} max_experience={max_experience}/>
          </ReactRouterDOM.Route>
        </div>
      </ReactRouterDOM.BrowserRouter>
    );
  }