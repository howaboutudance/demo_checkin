import React from 'react';
import './demo.css';
import { api_base_url } from "./api_url";

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
			cells[i] = (cells[i] === null) ? "✖️": null;
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

		return(
		<div className="list">
			<div className="list-content"> {rv}</div>
			<div className="bottom-toolbar">
				<button onClick={this.handleNext}>Next</button>
				<button onClick={this.handlePrev}>Prev</button>
			</div>
		</div>

		)
	}
}

function ListRow(props){
	return(
		<div className="row"> 
			<div className="checkbox" onClick = {props.clickFunc}>{props.cell}</div>
			<div className="cell" anum={props.rowData.anum} onClick = {() => props.onQuery(props.rowData.anum)}>
				{props.rowData.firstName} {props.rowData.lastName}
			</div>
		</div>
	)
}

export { List }
