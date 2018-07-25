import React from 'react';
import ReactDOM from 'react-dom';
import './demo.css';
import { List } from './List';
import { Profile } from './Profile';
import { api_base_url } from "./api_url";

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
				this.setState({query: JSON.stringify(data.student,null, 2)})
			});
		}
	handleQueryClick(e){
	}
	render(){

		
		return (
			<article className="sheet">
				<List onQuery={this.handleQuery} />
				<Profile query={this.state.query}/>
			</article>
		);
	}
}

class Bottom extends React.Component {
	render() {
		return <footer className="toolbar"><div>Admin</div></footer>
	}
}


ReactDOM.render(
	<React.Fragment>	
		<Bottom />
		<Chrome />
	</React.Fragment>,
	document.getElementById('root'),
);

