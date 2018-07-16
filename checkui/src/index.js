import React from 'react';
import ReactDOM from 'react-dom';
import './demo.css';

class Chrome extends React.Component {
	render(){
		return (
			<div className="sheet">
				<List />
			</div>
		);
	}
}
class List extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			rows: Array(20).fill(null),
		}

	}
	render(){
		return (
			<div className="row">
				<span>
				<Checkbox />
				<Cell />
				</span>
			</div>
		);
	}
}
class Checkbox extends React.Component {
	render(){
		return <div className="checkbox"></div>;
	}
}

class Cell extends React.Component {
	render(){
		return <div className="cell">cell name</div>;
	}
}

ReactDOM.render(
	<Chrome />,
	document.getElementById('root'),
);
