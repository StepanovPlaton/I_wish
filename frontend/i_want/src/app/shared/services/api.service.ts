import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { retry, map, switchMap, catchError } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import { IUser, IUserAuthorizationData, IUserAuthorizationResponse } from '../models/user.models';
import { IAuthorizationResponse, IWish } from '../models/http.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

    constructor(
        private http: HttpClient,
    ) {

    }

    checkToken(Login: string, Token: string) {
        return this.http.post(`/api/check_token?Login=${Login}`, {Token})
        .pipe(
            switchMap(()=> of(true)),
            catchError(()=> of(false))
        )
    }

    registrationUser(userRegistrationData: IUserAuthorizationData): Observable<IUserAuthorizationResponse | null> {
        return this.http.post<IAuthorizationResponse>(`/api/registration?Login=${userRegistrationData.login}&Password=${userRegistrationData.password}`, {})
        .pipe(
            switchMap((response) => {
                return of({ token: response.Token, id: response.ID })
            }),
            catchError((error) => {
                return of(null)
            })
        )
    }

    authorizationUser(userAuthorizationData: IUserAuthorizationData): Observable<IUserAuthorizationResponse | null> {
        return this.http.post<IAuthorizationResponse>(`/api/authorization?Login=${userAuthorizationData.login}&Password=${userAuthorizationData.password}`, {})
        .pipe(
            switchMap((response) => {
                return of({ token: response.Token, id: response.ID })
            }),
            catchError((error) => {
                return of(null)
            })
        )
    }

    getUserInfo(Login: string) {
        return this.http.get<IUser>(`/api/${Login}`)
    }

    updateUserInfo(
        authData: IUserAuthorizationData & IUserAuthorizationResponse,
        userInfo: IUser
    ) {
        return this.http.put(`/api/${authData.login}`, {
            "Token": authData.token,
            ...userInfo
        })
    }


    getWishes(Login?: string): Observable<IWish[]> {
        if(Login) {
            return this.http.get<IWish[]>(`/api/${Login}/wishes`)
        } else {
            return this.http.get<IWish[]>(`/api/wishes`)
        }
    }

    getWish(WishID: number): Observable<IWish> {
        return this.http.get<IWish>(`/api/wishes/${WishID}`)
    }

    updateWish(
        authData: IUserAuthorizationData & IUserAuthorizationResponse,
        wish: IWish
    ) {
        return this.http.put(`/api/${authData.login}/wishes/${wish.ID}`, {
            "Token": authData.token,
            ...wish
        })
    }

    createWish(
        authData: IUserAuthorizationData & IUserAuthorizationResponse,
        wish: IWish
    ) {
        return this.http.post(`/api/${authData.login}/wishes`, {
            "Token": authData.token,
            ...wish
        })
    }

    deleteWish(
        authData: IUserAuthorizationData & IUserAuthorizationResponse,
        wishID: number
    ) {
        return this.http.delete(`/api/${authData.login}/wishes/${wishID}`, {
            body: {
                "Token": authData.token
            }
        })
    }
    
}
