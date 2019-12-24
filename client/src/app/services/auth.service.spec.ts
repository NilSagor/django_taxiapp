import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { AuthService } from './auth.service';

describe('AuthService', () => {
	let authService: AuthService;
  beforeEach(() => TestBed.configureTestingModule({
  	imports: [HttpClientTestingModule],
  	declarations: [],
  	providers: [AuthService]
  }));

  it('should be created', () => {
    const service: AuthService = TestBed.get(AuthService);
    expect(service).toBeTruthy();
  });
});
