import React from 'react';
import ReactDOM from 'react-dom';
import './demo.css';
import { List } from './List';
import { AuthDialog } from './Auth';


const host = "localhost"
const port = "5000"
const api_version = "1.0"
const api_base_url = `http:////${host}:${port}//api//v${api_version}`
class Chrome extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			query: "",
			key: null
		}
	}
	render(){
		if (!this.state.key){
			return (
				<AuthDialog />
			)
		}

		function basicparse(val){
			const url = `api_base_url//students`+val;
			fetch(url)
			.then((resp) => {
				return resp.json();
			})
			.then((data) => {
				console.log(data.student)
			});
		}
		return (
			<div className="sheet">
				<List func={basicparse} />
				<Profile />
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
				<p> {this.props.query} </p>
			</div>)}
}

ReactDOM.render(
	<Chrome />,
	document.getElementById('root'),
);
