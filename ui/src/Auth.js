import React from 'react';
import './demo.css';

const base_auth_url = "http://localhost:5000/api/v1.0/auth"

class AuthDialog extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			username: "",
			password: ""
		}
		this.handleUsername = this.handleUsername.bind(this);
		this.handlePassword = this.handlePassword.bind(this);
		this.loginPost = this.loginPost.bind(this);

	}
	loginPost (event) {
		let loginJson = {
			password: this.state.password,
			username: atob(this.state.username)
		}
		let url = `${base_auth_url}\\login`

		fetch(url, {method:"POST"})
		.then((resp) => {
			return resp.json();
		}).then((data) => {
			console.log(data)
			this.setState({key: data.apikey}) // TODO: look up OnError or equivalant for fetch api 
		})
		event.preventDefault();
	}
	handleUsername(event){
		this.setState({username: event.target.value})
	}
	handlePassword(event){
		this.setState({password: btoa(event.target.value)})
	}
	render() {
		return (
			<div className="auth-dialog">
				<form onSubmit={this.loginPost} >
					<label>Username</label>
					<input id="username" value={this.state.username} type="text" onChange={this.handleUsername}/>
					<label>Password</label>
					<input id="password" value={atob(this.state.password)} type="password" onChange={this.handlePassword}/>
					<input type="submit"/>
				</form>
			</div>
		)
	}
}

export {AuthDialog};
