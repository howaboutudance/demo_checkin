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
			cells: Array(5).fill(null),
		}
		this.handleCheck = this.handleCheck.bind(this);
	}
	handleCheck(i){
		const cells = this.state.cells.slice();
		return () => {
			cells[i] = (cells[i] === null) ? "X": null;
			this.setState({cells: cells})
		}
	}
	componentDidMount(){
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
			rv.push(<ListRow onQuery={this.props.onQuery} clickFunc={this.handleCheck(i)} key={i} rowData={this.state.rows[i]} cell={this.state.cells[i]}/>);
		}

		return <div className="list">{rv}</div>
	}
}

function ListRow(props){
	return(
		<div className="row"> 
			<span>
				<div className="checkbox" onClick = {props.clickFunc}>{props.cell}</div>
				<div className="cell" anum={props.rowData.anum} onClick = {() => props.onQuery(props.rowData.anum)}>
					{props.rowData.firstName} {props.rowData.lastName}
				</div>
			</span>
		</div>
	)
}

export { List }
