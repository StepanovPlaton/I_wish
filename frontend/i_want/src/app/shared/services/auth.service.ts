import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie';
import { map, Observable, of, Subject, switchMap } from 'rxjs';
import { IUserAuthorizationData, IUserAuthorizationResponse } from '../models/user.models';
import { ApiService } from './api.service';

@Injectable({
    providedIn: "root"
})
export class AuthService {

    authorized: boolean | undefined = undefined;
    tokenChecked: Subject<boolean> = new Subject<boolean>()

    public userAuthorizationData: 
        IUserAuthorizationData & IUserAuthorizationResponse | null = null

    constructor(
        private readonly cookieService: CookieService,
        private readonly apiService: ApiService,
        private readonly router: Router,
    ) { 
        if(this.cookieService.hasKey("authData")) {
            this.userAuthorizationData = this.cookieService.getObject("authData") as IUserAuthorizationData & IUserAuthorizationResponse
            if(this.userAuthorizationData.login && this.userAuthorizationData.token) {
                this.apiService.checkToken(
                    this.userAuthorizationData.login,
                    this.userAuthorizationData.token
                ).subscribe((checkResult) => {
                    console.log(checkResult)
                    if(!checkResult) {
                        this.cookieService.remove("authData")
                        this.userAuthorizationData = null;
                        this.authorized = false;
                        this.tokenChecked.next(this.authorized);
                    } else { 
                        this.authorized = true;
                        this.tokenChecked.next(this.authorized);
                    }
                })
            } else {
                this.userAuthorizationData = null;
                this.authorized = false;
                this.tokenChecked.next(this.authorized);
            }
        } else {
            this.authorized = false;
            this.tokenChecked.next(this.authorized);
        }
    }

    registrationUser(userRegistrationData: IUserAuthorizationData): Observable<boolean> {
        return this.apiService.registrationUser(userRegistrationData).pipe(
            switchMap((response) => {
                if(response) {
                    this.userAuthorizationData = {
                        ...userRegistrationData,
                        ...response
                    }
                    this.cookieService.putObject("authData", this.userAuthorizationData)
                    this.authorized = true;
                    return of(true)
                } else {
                    return of(false)
                }
            })
        )
    }

    authorizationUser(userAuthorizationData: IUserAuthorizationData): Observable<boolean> {
        return this.apiService.authorizationUser(userAuthorizationData).pipe(
            switchMap((response) => {
                if(response) {
                    this.userAuthorizationData = {
                        ...userAuthorizationData,
                        ...response
                    }
                    this.cookieService.putObject("authData", this.userAuthorizationData)
                    this.authorized = true
                    return of(true)
                } else {
                    return of(false)
                }
            })
        )
    }


    logout() {
        this.cookieService.remove("authData")
        this.userAuthorizationData = null
        this.authorized = false
        this.router.navigate([""])
    }
}