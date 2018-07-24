import React from 'react';
import ReactDOM from 'react-dom';
import './demo.css';
import { List } from './List';
import { AuthDialog } from './Auth';


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
			const url = "http://localhost:5000/api/v1.0/students/"+val;
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
