import React from 'react';
import './demo.css';
import Form from "react-jsonschema-form"

const schema = {
  title: "Student Details",
  type: "object",
  required: ["title"],
  properties: {
    firstName: {type: "string", title: "First Name", default: "First"},
    lastName: {type: "string", title: "Last Name", default: "Last"},
	preferredFirstName: {type:"string", title:"Preferred Name", default:"Preferred"},
	pronoun: {type: "string", title: "Pronoun", default:"Pronoun"}
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
				<ProfileForm query={this.props.query} />
			</div>
		)}
}

class ProfileForm extends React.Component {
	render () {
		return (
			<Form schema = {schema}
				formData = {this.props.query}
				onchange={console.log("changed")}
				onSubmit={console.log("submitted")}
				onError = {console.error("errors")}>
				<div><button type="submit">Update</button></div>
			</Form>
		)
	}
}


export { Profile } 
