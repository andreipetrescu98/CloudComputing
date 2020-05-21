import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from './auth.service';

@Injectable({
    providedIn: 'root'
})
export class AdvertService {

    constructor(private http: HttpClient, private authService: AuthService) {

    }

    addAdvert(data) {
        return this.http.post("https://petify-api.azurewebsites.net/advert", data).toPromise();
    }

    subscribeToAdvert(data){
        return this.http.post("https://petify-api.azurewebsites.net/subscribe", data).toPromise();
    }

    getAdverts() {
        return this.http.get("https://petify-api.azurewebsites.net/adverts").toPromise();
    }

    getMyAdverts(id) {
        return this.http.get(`https://petify-api.azurewebsites.net/adverts/${id}`).toPromise();
    }

    getSubscribedAdverts(id) {
        return this.http.get(`https://petify-api.azurewebsites.net/subscriptions/${id}`).toPromise();
    }

}