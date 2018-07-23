import React from 'react';
import ReactDOM from 'react-dom';
import './demo.css';

class Chrome extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			query: ""
		}
	}
	render(){

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
class List extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			rows: [], 
		}
	}
	componentDidMount() {
		fetch("http://localhost:5000/api/v1.0/students")
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
