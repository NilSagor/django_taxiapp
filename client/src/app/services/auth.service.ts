
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';


export class User {
	constructor(
		public id?: number,
		public username?: string,
		public first_name?: string,
		public last_name?: string,
		public group?: string,
		public photo?: any		
	){}

	static create(data:any):User {
		return new User(
			data.id,
			data.username,
			data.first_name,
			data.last_name,
			data.group,
			data.photo
		);
	}
}

@Injectable({
  providedIn: 'root'
})

export class AuthService {

  constructor(private http: HttpClient) { }

  signUp(
  	username: string,
  	firstName: string,
  	lastName: string,
  	password: string,
  	group: string,
  	photo: any
  ): Observable<User> {
  	const url = 'http://localhost:8000/api/sign_up/';
  	const formData = new FormData();
  	formData.append('username', username);
  	formData.append('first_name', firstName);
  	formData.append('last_name', lastName);
  	formData.append('password1', password);
  	formData.append('password2', password);
  	formData.append('group', group);
  	formData.append('photo', photo);
  	return this.http.request<User>('POST', url, {body:formData});
  }

  logIn(
  	username:	string,
  	password:	string
  ): Observable<User>{
  	const url = 'http://localhost:8000/api/log_in';
  	return this.http.post<User>(url, {usrname, password}).pipe(
  		tap(user =>	localStorage.setItem('taxi.user', JSON.stringify(user))));
  }


}
