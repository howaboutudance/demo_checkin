import React from 'react';
import './demo.css';

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

export { Profile } 
