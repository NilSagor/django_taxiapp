import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { AuthService, User } from './auth.service';
import { UserFactory } from '../testing/factories';

describe('AuthService', () => {
	let authService: AuthService;
  	
  	beforeEach(() => { TestBed.configureTestingModule({
	  	imports: [HttpClientTestingModule],
	  	declarations: [],
	  	providers: [AuthService]
  	})
  });


  it('should be created', () => {
    const service: AuthService = TestBed.get(AuthService);
    expect(service).toBeTruthy();
  });
});


describe('Authentication using a service', () => {
	let authService: AuthService;
 	let httpMock: HttpTestingController;

  	beforeEach(() => { TestBed.configureTestingModule({
	  	imports: [HttpClientTestingModule],
	  	declarations: [],
	  	providers: [AuthService]
 	});
	 authService = TestBed.get(AuthService);
	 httpMock = TestBed.get(HttpTestingController);
	});

	afterEach(() =>{
		httpMock.verify();
	});

	it('should allow a user to sign up for a new account', () =>{
		// set up the data
		const userData = UserFactory.create();
		const photo = new File(['photo'], userData.photo, {type: 'image/jpeg'});
		// Execute the function under test
		authService.signUp(
			userData.username,
			userData.first_name,
			userData.last_name,
			'pAssw0rd!',
			userData.group,
			photo
		).subscribe(user => {
			expect(user).toBe(userData);
		});
		const request = httpMock.expectOne('http://localhost:8000/api/sign_up/')
	});

	it('should allow a new user to log in to an existing account', ()=> {
		// set up the data
		const userData = UserFactory.create();
		// A successful login should write data to local storage
		localStorage.clear();
		// Execute the function under test
		authService.logIn(
			userData.username, 'pAssw0rd!'
		).subscribe( user => {
			expect(user).toBe(userData);
		});
		const request = httpMock.expectOne('http://localhost:8000/api/log_in/');
		request.flush(userData);
		// confirm that the expected  data was written to local storage
		expect(localStorage.getItem('taxi.user')).toBe(JSON.stringify(userData));
	});

	it('should allow a user to log out', () => {
		// set up the data
		const userData = {};
		// a successful logout should delete storage data
		localStorage.setItem('taxi.user', JSON.stringify({}));
		// execute the function under test
		authService.logOut().subscribe(user => {
			expect(user).toEqual(userData);
		});
		const request = httpMock.expectOne('http://localhost:8000/api/log_out/');
		request.flush(userData);
		// confirm that local storage data was deleted
		expect(localStorage.getItem('taxi.user')).toBeNull();
	});

	it('should detemine whether a user is logged in', () => {
		localStorage.clear();
		expect(User.getUser()).toBeFalsy();
		localStorage.setItem('taxi.user', JSON.stringify(
			UserFactory.create()
			));
		expect(User.getUser()).toBeTruthy();
		
	});


});
