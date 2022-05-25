import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-authorization',
  templateUrl: './authorization.component.html',
  styleUrls: ['./authorization.component.scss']
})

export class AuthorizationComponent implements OnInit {
  Login: string = "";
  Password: string = "";
  failedAuth: boolean = false;

  constructor(private http: HttpClient, 
              private ref: ChangeDetectorRef,
              private router: Router,
  ) { 
    
  }

  ngOnInit() {
  }

  loginChanged(event: KeyboardEvent) { 
    this.Login = (<HTMLInputElement>event.target)?.value; 
    this.failedAuth = false;
  }
  passwordChanged(event: KeyboardEvent) { 
    this.Password = (<HTMLInputElement>event.target)?.value; 
    this.failedAuth = false;
  }

  login(event: Event) {
    this.http.post<{Token: string} | null>(`/api/authorization?Login=${this.Login}&Password=${this.Password}`, {})
    .subscribe(Response => {
      if(Response) {
        this.failedAuth = false;
        localStorage.setItem("token", Response.Token)
        localStorage.setItem("login", this.Login)
        this.router.navigate(["/"])
      } else { this.failedAuth = true; this.ref.markForCheck(); }
    }, error => { this.failedAuth = true; this.ref.markForCheck(); })
  }
}
