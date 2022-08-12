import { Injectable } from '@angular/core';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  Router,
  CanActivateChild,
} from '@angular/router';
import { from, map, Observable, of, switchMap, timer } from 'rxjs';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthGuard implements CanActivate, CanActivateChild {
  constructor(
    private readonly authService: AuthService,
    private readonly router: Router
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (this.authService.authorized === undefined) {
      return this.authService.tokenChecked.pipe(
        map((authorized) => {
          if (authorized === false) {
            return this.router.createUrlTree(['auth']);
          }
          return authorized;
        })
      );
    } else {
      if (this.authService.authorized === false) {
        return this.router.createUrlTree(['auth']);
      }
      return this.authService.authorized;
    }
  }

  canActivateChild(
    childRoute: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ) {
    return this.canActivate(childRoute, state);
  }
}

