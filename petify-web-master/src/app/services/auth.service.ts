import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { mockedUser } from './user.mocked';
@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private loggedIn = false;
    public user = null;
    constructor(private http: HttpClient) {
    }

    public isLoggedIn() {
        return true;
    }

    public getDetails() {
        return new Promise((resolve, reject) => {
            if (this.user) {
                resolve(this.user);
            } else {
                this.http.get("https://petify-web.azurewebsites.net/.auth/me").subscribe(rsp => {
                    this.user = rsp[0];
                    resolve(this.user);
                }, (err) => {
                    this.user = mockedUser[0];
                    resolve(this.user);
                })
            }
        })
    }
}