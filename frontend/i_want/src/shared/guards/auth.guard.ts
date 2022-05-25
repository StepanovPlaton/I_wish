import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private router: Router,) {}

  canActivate(): boolean {
    const Login = localStorage.getItem('login');
    const Token = localStorage.getItem('token');
    if(Login && Token) { return true }
    this.router.navigate(['auth']);
    return false
  }
}