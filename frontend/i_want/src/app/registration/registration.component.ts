import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.less']
})
export class RegistrationComponent implements OnInit {
  Login: string = "";
  Password: string = "";
  failedRegistration: boolean = false;

  constructor(
    private http: HttpClient,
    private router: Router,
    private ref: ChangeDetectorRef,
  ) { }

  ngOnInit() {
  }



  loginChanged(event: KeyboardEvent) { 
    this.Login = (<HTMLInputElement>event.target)?.value; 
    this.failedRegistration = false;
  }
  passwordChanged(event: KeyboardEvent) { 
    this.Password = (<HTMLInputElement>event.target)?.value; 
    this.failedRegistration = false;
  }

  registration(event: Event) {
    this.http.post<{Token: string} | null>(`/api/registration?Login=${this.Login}&Password=${this.Password}`, {})
    .subscribe(Response => {
      if(Response) {
        this.failedRegistration = false;
        localStorage.setItem("token", Response.Token)
        localStorage.setItem("login", this.Login)
        this.router.navigate(["/"])
      } else { this.failedRegistration = true; this.ref.markForCheck(); }
    }, error => { this.failedRegistration = true; this.ref.markForCheck(); })
  }

}
