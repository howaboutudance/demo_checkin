import React from 'react';
import ReactDOM from 'react-dom';
import './demo.css';
import { List } from './List';

const host = "localhost"
const port = "5000"
const api_version = "1.0"
const api_base_url = `http:////${host}:${port}/api/v${api_version}`
class Chrome extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			query: ""
		}
		this.handleQuery = this.handleQuery.bind(this)
	}
	handleQuery(e){
			const url = `${api_base_url}/students/${e}`;
			fetch(url)
			.then((resp) => {
				return resp.json();
			})
			.then((data) => {
				this.setState({query: JSON.stringify(data.student)})
			});
		}
	handleQueryClick(e){
	}
	render(){

		
		return (
			<div className="sheet">
				<List onQuery={this.handleQuery} />
				<Profile query={this.state.query}/>
			</div>
		);
	}
}

class Profile extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			profile: ""
		}
	}
	componentDidMount() {
	}
	render() { 
		return(
			<div className="profile">
				<textarea value={this.props.query}>
				</textarea>
			</div>)}
}

ReactDOM.render(
	<Chrome />,
	document.getElementById('root'),
);
