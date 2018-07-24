import React from 'react';
import './demo.css';

const api_version = "1.0"
const host = "localhost"
const port = "5000"

const api_base_url = `http:////${host}:${port}/api/v${api_version}`

class List extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			rows: [], 
		}
	}
	componentDidMount() {
		let url = `${api_base_url}/students`
		fetch(url)
			.then( response => {
				return response.json();
			}).then( data => {
				this.setState({rows: data.students});
			});
	}
	render(){
		var rv = [];

		for(var i = 0; i < this.state.rows.length; i++){
			rv.push(<ListRow func={this.props.func} key={i} rowData={this.state.rows[i]} />);
		}

		return <div className="list">{rv}</div>
	}
}
class Checkbox extends React.Component {
	render(){
		function handleClick(e) {
			console.log('checkbox was clicked');

		}
		return <div className="checkbox" onClick={handleClick}></div>;
	}
}

function ListRow(props){
	return(
		<div className="row">
			<span>
				<Checkbox />
				<div onClick={() => props.func(props.rowData.anum)} className="cell">
					{props.rowData.firstName} {props.rowData.lastName}
				</div>
			</span>
		</div>
	)
}

export { List }
